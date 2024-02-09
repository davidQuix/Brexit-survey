import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import JSONDeserializer, JSONSerializer, QuixTimeseriesSerializer
import functions

app = Application.Quix("transformation-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=QuixTimeseriesSerializer())

sdf = app.dataframe(input_topic)

# counters for the status messages
row_counter = 0

# Transformer to chart data
def transform_data(row: dict, state: State):
    global row_counter
    row_data = {}

    # If no data (end) return row and reset row counter
    if row == {}:        
        # Reset store
        for key in state.get("Keys", []):
            state.delete(key)
        row_counter = 0
        return row

    print()

    # Increate row counter
    row_counter +=1 
    
    # Add valid on the row to check duplicities
    functions.count_data([row["Vote"]], state)
    functions.count_data([row["UK_country"]], state)
    functions.count_data([row["Vote"], row["Gender"]], state)
    functions.count_data([row["Vote"], row["Age_range"]], state)
    functions.count_data([row["Vote"], row["UK_country"]], state)

    # The chart data that we want to set on the row
    values = [ 
        { "key": "Support", "total": row_counter }, 
        { "key": "Oppose", "total": row_counter },
        { "key": "Neutral", "total": row_counter },
        { "key": "Support_Female", "total": state.get("Support", 0) }, 
        { "key": "Support_Male", "total": state.get("Support", 0) },   
        { "key": "Oppose_Female", "total": state.get("Oppose", 0) },  
        { "key": "Oppose_Male", "total": state.get("Oppose", 0) },
        { "key": "Support_Young Adult", "total": state.get("Support", 0) },
        { "key": "Support_Adult", "total": state.get("Support", 0) }, 
        { "key": "Support_Elderly", "total": state.get("Support", 0) }, 
        { "key": "Oppose_Young Adult", "total": state.get("Oppose", 0) },
        { "key": "Oppose_Adult", "total": state.get("Oppose", 0) }, 
        { "key": "Oppose_Elderly", "total": state.get("Oppose", 0) }, 
        { "key": "Support_England", "total": state.get("England", 0) },  
        { "key": "Oppose_England", "total": state.get("England", 0) }, 
        { "key": "Neutral_England", "total": state.get("England", 0) }, 
    ]

    # Update row with the chart data defined above
    for val in values:
        row_data[val["key"]] = functions.calc_percentage(state.get(val["key"], 0), val["total"])   

    # Store the tola of votes
    row_data["Total_votes"] = row_counter
    row_data["Timestamp"] = row["Timestamp"]

    return row_data

def filter_data(row: dict, state: State):
    return row == {} or row["Valid"]
    return True

# Filter invalid votes
# sdf = sdf.filter(filter_data, stateful=True)

# Trasform data to char values
sdf = sdf.apply(transform_data, stateful=True)

# print the row with this inline function
sdf = sdf.update(lambda row: print(row))

# publish the updated row to the output topic
sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)
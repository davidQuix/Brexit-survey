import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import JSONDeserializer, JSONSerializer
import functions

app = Application.Quix("transformation-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=JSONSerializer())

sdf = app.dataframe(input_topic)

# counters for the status messages
row_counter = 0
def count_names(row: dict, state: State):
    global row_counter
    row_data = {}

    if row == {}:
        row_counter = 0
        return row

    row_counter +=1 
    
    # Add valid on the row to check duplicities
    functions.count_data([row["Vote"]], state)
    functions.count_data([row["Vote"], row["Gender"]], state)
    
    values = [ 
        { "key": "Support", "total": row_counter }, 
        { "key": "Oppose", "total": row_counter },
        { "key": "Neutral", "total": row_counter },
        { "key": "Support_Female", "total": state.get("Support", 0) }, 
        { "key": "Support_Male", "total": state.get("Support", 0) },   
        # { "key": "Oppose_Female", "total": state.get("Oppose", 0) },  
        # { "key": "Oppose_Male", "total": state.get("Oppose", 0) }
    ]

    for val in values:
        row_data[val["key"]] = functions.calc_percentage(state.get(val["key"], 0), val["total"])   

    row_data["Total_votes"] = row_counter

    # return the updated row so more processing can be done on it
    return row_data

def filter_invalids(row: dict):
    return row["Valid"] == True

# Filter invalid votes
sdf = sdf.filter(filter_invalids)

# apply the result of the count_names function to the row
sdf = sdf.apply(count_names, stateful=True)

# print the row with this inline function
sdf = sdf.update(lambda row: print(row))

# publish the updated row to the output topic
sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)
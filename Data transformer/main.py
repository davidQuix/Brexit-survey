import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import JSONDeserializer, JSONSerializer
import functions

app = Application.Quix("transformation-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=JSONSerializer())

sdf = app.dataframe(input_topic)

def count_names(row: dict, state: State):
    row_data = {}

    # Add valid on the row to check duplicities
    row_data["valid"] = functions.check_duplicities(row["ID"], state)
   
    # Add Age_range on the row
    row_data["Age_range"] = functions.get_age_range(row["Age"])

    # Add UK_country on the row
    row_data["UK_country"] = functions.get_uk_country(row["Location"])

    # return the updated row so more processing can be done on it
    return row_data

def filter_invalids(row: dict):
    return row['Valid'] == True

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
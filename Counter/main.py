import os
from quixstreams import Application, State
from quixstreams.models.serializers.quix import JSONDeserializer, JSONSerializer
from functions import Functions


app = Application.Quix("transformation-v1", auto_offset_reset="latest")

input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())
output_topic = app.topic(os.environ["output"], value_serializer=JSONSerializer())

sdf = app.dataframe(input_topic)

def get_age_range(number):
    if 0 <= number <= 12:
        return "Children"
    elif 13 <= number <= 17:
         return "Teenager"
    elif 18 <= number <= 34:
        return "Young Adult"
    else:
        return "Elderly"

def check_duplicities(id, state: State):
    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    id_count = state.get(id, 0)

    # add one to the name count
    id_count += 1

    # store the new count in state
    state.set(id, id_count)

    if id_count > 1:
        return False
    else:
        return True

def count_names(row: dict, state: State):

    # get the value from the name column for this row
    # so we can see if it's in state
    # add the name count to the row data
    row["valid"] = check_duplicities(row["ID"], state)


    row["Age range"] = get_age_range(row["Age"])

    # return the updated row so more processing can be done on it
    return row

# apply the result of the count_names function to the row
sdf = sdf.apply(count_names, stateful=True)

# print the row with this inline function
sdf = sdf.update(lambda row: print(row))

# publish the updated row to the output topic
sdf = sdf.to_topic(output_topic)

if __name__ == "__main__":
    app.run(sdf)
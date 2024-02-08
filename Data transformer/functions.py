from quixstreams import State

def get_key(values):
    key = ""
    for val in values:
        if key != "": 
            key += "_"
        key += val
    return key

def count_data2(values):
    key = get_key(values)
    
    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    value_count = State.get(key, 0)

    # add one to the name count
    value_count += 1

    # store the new count in state
    State.set(key, value_count)

    return State

def calc_percentage(value, total_count):
    return value / total_count * 100
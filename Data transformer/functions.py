from quixstreams import State

def count_data2(values, state: State):
    key = ""
    for val in values:
        if key != "": 
            key += "_"
        key += val

    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    value_count = state.get(key, 0)

    # add one to the name count
    value_count += 1

    # store the new count in state
    state.set(key, value_count)

    return state

def calc_percentage(value, total_count):
    return value / total_count * 100
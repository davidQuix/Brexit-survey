from quixstreams import State

def get_key(values):
    key = ""
    for val in values:
        if key != "": 
            key += "_"
        key += val
    return key

def add_if_not_exists(arr, string_to_add):
    if string_to_add not in arr:
        arr.append(string_to_add)

def count_data(values, state: State):
    key = get_key(values)
    
    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    value_count = state.get(key, 0)

    # add one to the name count
    value_count += 1

    # store the new count in state
    state.set(key, key)

    return state

def calc_percentage(value, total_count):
    return value / total_count * 100
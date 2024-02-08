from quixstreams import State

def get_key(values):
    key = ""
    for val in values:
        if key != "": 
            key += "_"
        key += val
    return key

def add_if_not_exists(arr, key):
    if key not in arr:
        arr.append(key)

def set_key(key, state: State):
    arr = state.get(key, 0)
    print(arr)

def count_data(values, state: State):
    key = get_key(values)
    
    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    value_count = state.get(key, 0)

    # add one to the name count
    value_count += 1

    # store the new count in state
    state.set(key, value_count)

    set_key(key, State)

def calc_percentage(value, total_count):
    return value / total_count * 100
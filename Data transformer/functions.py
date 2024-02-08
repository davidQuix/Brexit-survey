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

def store_key(key, state: State):
    arr = state.get("keys", [])
    add_if_not_exists(arr, key)
    state.set("keys", arr)

def count_data(values, state: State):
    # get key from the current values
    key = get_key(values)

    # store the new key on the state
    store_key(key, state)

    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    value_count = state.get(key, 0)

    # add one to the name count
    value_count += 1

    # store the new count in state
    state.set(key, value_count)


def calc_percentage(value, total_count):
    if total_count == 0:
        return 0
    return value / total_count * 100
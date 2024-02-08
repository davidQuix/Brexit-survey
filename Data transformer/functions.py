from quixstreams import State

def count_percentage(value, total_count, state: State):
    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    value_count = state.get(value, 0)

    # add one to the name count
    value_count += 1

    # store the new count in state
    state.set(value, value_count)

    return state
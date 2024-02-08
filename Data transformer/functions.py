from quixstreams import State
from uk_cities import england_cities, scotland_cities, wales_cities, ni_cities

def count_duplicities(id, state: State):
    # check state, if the name is already there then retrieve the count
    # default to 0 if the name wasn't in state
    id_count = state.get(id, 0)

    # add one to the name count
    id_count += 1

    # store the new count in state
    state.set(id, id_count)

    return id_count
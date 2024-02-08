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
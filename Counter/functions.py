from quixstreams import State
from uk_cities import england_cities, scotland_cities, wales_cities, ni_cities

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

def get_uk_country(city):
    if city in england_cities:
        return "England"
    elif city in scotland_cities:
        return "Scotland"
    elif city in wales_cities:
        return "Wales"
    elif city in ni_cities:
        return "North Ireland"
    else:
        return None

def get_age_range(number):
    if 0 <= number <= 12:
        return "Children"
    elif 13 <= number <= 17:
        return "Teenager"
    elif 18 <= number <= 34:
        return "Young Adult"
    elif 35 <= number <= 65:
        return "Adult"
    else:
        return "Elderly"
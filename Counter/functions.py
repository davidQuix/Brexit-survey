from quixstreams import State
from uk_cities import england_cities, scotland_cities, wales_cities, ni_cities

# Function that check if there are duplicities 
def check_duplicities(id, state: State):
    # default to 0 if the name wasn't in state
    id_count = state.get(id, 0)

    # add one to the count
    id_count += 1

    # store the new count in state
    state.set(id, id_count)

    if id_count > 1:
        return False
    else:
        return True

# Function that gets the UK contry based on the city
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

# Function that gets the Age range based on the age
def get_age_range(age):
    if 0 <= age <= 12:
        return "Children"
    elif 13 <= age <= 17:
        return "Teenager"
    elif 18 <= age <= 34:
        return "Young Adult"
    elif 35 <= age <= 65:
        return "Adult"
    else:
        return "Elderly"
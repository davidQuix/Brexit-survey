class functions:

    def get_age_range(number):
        if 0 <= number <= 12:
            return "Children"
        elif 13 <= number <= 17:
            return "Teenager"
        elif 18 <= number <= 34:
            return "Young Adult"
        else:
            return "Elderly"

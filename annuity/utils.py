def get_duration(pol_year):
    if pol_year >= 25:
        return 25

    durations = [0, 10, 15, 20, 25]
    for i in range(len(durations)-1):
        if durations[i] <= pol_year < durations[i+1]:
            return durations[i]

    return durations[-1]


def get_month(x):
    if x % 12 == 0:
        return 12
    else:
        return x % 12


def freq_to_int(freq):
    if freq == "M":
        return 12
    elif freq == "Q":
        return 4
    elif freq == "H":
        return 2
    elif freq == "Y":
        return 1
    else:
        raise ValueError("Incorrect PREM_FREQ.")

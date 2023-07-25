def get_duration(x):
    if x >= 25:
        return 25
    durations = [0, 10, 15, 20, 25]
    for i in range(len(durations)-1):
        if durations[i] <= x < durations[i + 1]:
            return durations[i]
    return durations[-1]

d = {'1': 50, '2': 600, '3': 70}

def maxDict(dict):
    return max(dict.items(), key = lambda t: t[1])

print(maxDict(d))
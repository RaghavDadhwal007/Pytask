newarr = [0,0,0,1,1,1,0,0,0,1,1,0,1,1,1,1,0,0,1,1,1,1,1]

def maxOne(n):
    res = 0
    a = 0

    for i in n:
        if i == 0:
            if a < res:
                a = res 
            res = 0
        else:
            res += 1

    if a < res:
        return res

    return a

print(maxOne(newarr))

def q1(l):
    i = 0
    maxi = 0
    while i < len(l) - 1:
        maxi = l[i] if l[i] > l[i + 1] else l[i + 1]
        i += 1
    return maxi

def q2(l):
    # s = 0
    # for i in l: s += int(i)
    # return s

    return [(s:=0 + int(i)) for i in l]

l = [1,2,3, 2, 4]
print(q2(l))
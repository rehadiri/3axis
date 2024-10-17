# Python function to print permutations of a given list


def permutasyon(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]

    l = []

    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1:]
        for p in permutasyon(remLst):
            l.append([m] + p)
    return l


data = []
output = []
for i in range(10):
    data.append(i)

for p in permutasyon(data):
    output.append(p)
print('ok')

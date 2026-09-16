L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
    li = []
    for i in t:
        li.append(t[0])
    return li


L2 = sorted(L, key=by_name)
print(L2)

def by_score(t):
    score = []
    for i in t:
        score.append(t[1])
    return score


L2 = sorted(L, key=by_score,reverse = True)
print(L2)
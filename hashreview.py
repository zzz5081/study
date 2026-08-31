def count_chars(str):
    seen = {}
    for i in str:
        if i not in seen:
            seen[i] = 1
        else:
            seen[i] = seen[i] + 1
    return seen

from collections import defaultdict
def count_chars(str):
    s = defaultdict(int)
    for i in str:
        s[i] = s[i] + 1
    return s
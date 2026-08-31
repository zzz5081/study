# def count_chars(s: str) -> dict:
#     result = {}
#     for i in s:
#         if not i in result:
#             result[i] = 1
#         elif i in result:
#             result[i] = result[i] + 1
#     return result
#
# print(count_chars("hello"))    # {"h": 1, "e": 1, "l": 2, "o": 1}

# from collections import Counter
#
# c = Counter("Banana")
# print(c)
# print(c["a"])

from collections import defaultdict

c = defaultdict(int)

for i in "apple":
    c[i] = c[i] + 1
print(c)
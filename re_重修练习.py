import re

m = re.search(r"(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})","2026-09-16 10:23:45 ERROR 数据提取失败")
#print() 不会打印，我记得好像是group(0)还是group(1)
print(m.group(1)) #突然想起来了

#['1','22','333']
n = re.findall(r"\d+","a1b22c333")
print(n)

#不会去重
print(re.findall(r"\d+","a1b1"))

#不知道这个模式"a.c"什么意思
print(re.match(r"\w+","abc"))
print(re.search(r"\w+","abc"))
print(re.findall(r"\w+","abc"))
print(re.match("\w","xxabcxx"))

# 不会

import re
pat = r"a.c"
strings = ["abc", "xxabcxx", "abcxx"]

# 我的预测：
print(f"实际:{re.match(pat,strings[0])}")#   match("abc")      → abc
print(f"实际:{re.match(pat,strings[1])}")#   match("xxabcxx")  → None
print(f"实际:{re.match(pat,strings[0])}")#   match("abcxx")    → abc
print(f"实际:{re.search(pat,strings[0])}")#   search("abc")     → abc
print(f"实际:{re.search(pat,strings[1])}")#   search("xxabcxx") → abc
print(f"实际:{re.search(pat,strings[2])}")#   search("abcxx")   → abc
print(f"实际:{re.fullmatch(pat,strings[0])}")#   fullmatch("abc")     → abc
print(f"实际:{re.fullmatch(pat,strings[1])}")#   fullmatch("xxabcxx") → None
print(f"实际:{re.fullmatch(pat,strings[2])}")#   fullmatch("abcxx")   → None

# 然后跑一遍，把实际结果打在旁边对比
#不知道fullmatch怎么用，之前是findall吗

n = re.search("(?P<phone>1[3-9]\d{9})","我的电话是13812345678")
n.group("phone")
print(n.groupdict())
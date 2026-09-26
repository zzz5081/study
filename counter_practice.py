from collections import Counter
from collections import defaultdict

# ① 用 Counter 统计一句话里每个字符出现的次数
c = Counter("abracadabra")
print(c)
# ② 打印前 3 名（用 most_common）
print(c.most_common(3))
# ③ 打印所有计数之和
print(sum(c.values()))
# ④ 造第二个 Counter，和第一个做 & 和 + 运算，看结果
d = Counter("abracad")
print(c)
print(d)
print(c & d) #取交集，两者都有的取最小的
print(c + d) #相加，都有的值相加，没有的变成有的
# ⑤ （配合你刚学的 defaultdict）造一个 defaultdict(int) 累加计数，
#    和 Counter 对比一下，感受两者的关系
group = defaultdict(int)
for i in ("abracadabra"):
    group[i] += 1
print(group)
print(c)
print(dict(group))
print(dict(c))


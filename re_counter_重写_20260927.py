target = "张三 13812345678 入职 2024-03-15"
import re
m = re.search('r(?P<name>\w+)\s(?P<telephone>\d{11})\s\w{2}\s(?P<time>\d{4}-\d{2}-\d{2})',target)
print(m.group('telephone'),m.group('time'))
#match锁开头不锁结尾
#search不锁
#fullmatch锁开头和结尾


from collections import Counter,defaultdict
cc = Counter(split("我是谁,我在哪,我做了什么,我不知道"))
print(cc.most_common(3),sum())
dd = defaultdict(list)
l = [('张三','北京'),('李四','上海'),('王五','北京')]
for name,city in l:
    dd[city].append(name)
print(dd)
#Counter可以用各种方法并且读一下没有的会返回0但是不会创建一个新键录入脏数据
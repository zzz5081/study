from pathlib import Path
from collections import defaultdict

# ① 用 rglob 找出当前目录下所有 .py 文件
#    打印：文件名 / 后缀 / 大小（字节）
p = Path('.').rglob('*.py')
for obj in p:
    print(f"{obj.name}/{obj.suffix}/{obj.stat().st_size}")
# ② 挑出所有 .log 文件，单独打印文件名
n = Path('.').rglob('*.log')
for f in n:
    print(f.name)
# ③ 统计：.py 文件一共几个、总大小多少字节 + 换算成 KB（保留 1 位小数）
#我发现生成器好像一旦遍历到底就用不了了
m = Path('.').rglob('*.py')
num = 0
sum_size = 0
for i in m:
    num += 1
    sum_size += i.stat().st_size
print(f'带.py的文件一共{num}个,总大小{sum_size}字节,换算成kb为{sum_size/1024:.1f}')
# ④ 进阶：按后缀分组（用 defaultdict(list)），打印每种后缀有几个文件
group = defaultdict(list)
for s in Path('.').rglob('*'):
    if s.is_file():
        group[s.suffix].append(s.name)
for sx,nm in group.items():
    print(f'{sx or "无后缀"}:{len(nm)}')
# help(defaultdict)
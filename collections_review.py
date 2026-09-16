import re
from collections import Counter, defaultdict
from pathlib import Path
# 一行日志的完整结构：日期 时间 级别 消息
lines = Path("test.log").read_text(encoding = 'utf-8').splitlines()
partten = r"^(\d{4}-\d{2}-\d{2})\s(\d{2}):(\d{2}):(\d{2})\s(INFO|ERROR|WARNING)\s(.+)$"

levels = defaultdict(int)
hours = Counter()
skipped = []
errors = []

for line in lines:
    m = re.match(partten,line)       # 匹配不到 = 脏行
    if not m:
        skipped.append(line)                 # 记录下来，不参与统计
        continue    # 直接跳过
    if m.group(5) == "ERROR":
        errors.append(line)
    date, hh, mm, ss, level, msg = m.groups()
    levels[level] += 1
    hours[hh] += 1

print("级别:", dict(levels))
print("按小时:", dict(hours))
print("有效行数:",sum(levels.values()))
print("跳过的脏行:", skipped)
for s in skipped:
    print("   -",s)
total = sum(levels.values())
for level,count in levels.items():
    print(f"{level}:{count}条({count/total* 100:.1f}%)")

print("错误 Top3:",Counter(errors).most_common(3))
# =========================================================================
# ⑤ pathlib               目标：遍历 + 统计                      约 15 分钟
# -------------------------------------------------------------------------
# 要求：对【当前脚本所在目录】做这几件事：
#   1. 找出所有 .py 文件（递归）
#   2. 打印每个文件的 文件名 + 大小（字节）
#   3. 统计 .py 文件一共有几个、总大小多少 KB
# ⚠️ 提示：目录要用【脚本自己的位置】，不要用当前工作目录
# =========================================================================
from pathlib import Path
p = Path(__file__).parent.rglob('*.py')
for i in p:
    print(i)

pp = Path(__file__).parent.rglob('*')
for m in pp:
    if m.is_file():
        print(m.name,m.stat().st_size)

num = 0
size = 0
ppp = Path(__file__).parent.rglob('*.py')
for l in ppp:
    num += 1
    size += l.stat().st_size
print(f".py文件一共{num}个,总大小{size/1024:.1f}KB")

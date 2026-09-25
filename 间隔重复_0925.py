# 任务1：默写 logging 的 6 步配置（屏幕 INFO / 文件 DEBUG / 带时间戳格式）
#  口诀：拿 logger → 设总闸 → 造两个 handler → 各自设闸 → 设格式 → 接上去
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
file_handler = logging.FileHandler("test1.log")
file_handler.setLevel(logging.DEBUG)

fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(fmt)
file_handler.setFormatter(fmt)

logger.addHandler(console)
logger.addHandler(file_handler)
# 任务2：默写 re 的 4 个点（各写一行代码或注释）
#  ① 4 位数字的量词怎么写              → ?
#\d{4}
#  ② findall 返回什么（类型 + 内容）    → ?
#返回列表 其中一个元素就是一个分隔的匹配的内容
#  ③ match/search/fullmatch 分别锁哪两端 → ?
#match锁开头不锁结尾
#search都不锁
#fullmatch锁开头又锁结尾
#  ④ 命名分组的语法                    → ?
#(?P<组名>内容)
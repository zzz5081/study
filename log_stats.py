"""9/6 W0 收官任务: 日志统计工具 (re + logging + pathlib)
预期输出: {"INFO": 6, "ERROR": 3, "WARNING": 3}
"""
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def count_levels(log_file: str) -> dict:
    """统计日志里每种级别 (INFO/ERROR/WARNING) 出现的次数"""
    counts = {"INFO": 0, "ERROR": 0, "WARNING": 0}
    p = Path(log_file)
    lines = p.read_text(encoding="utf-8").splitlines()

    for line in lines:
        # TODO 1: 用 re 找每行的级别，找到就 counts +1
        m = re.search(r"\b(INFO|ERROR|WARNING)\b",line)
        if m:
            counts[m.group(1)] += 1

    # TODO 2: 用 logging.info 记录"共读取 N 行日志"
    logging.info(f"共读取{len(lines)}行日志")
    return counts

if __name__ == "__main__":
    result = count_levels("test.log")
    print(result)

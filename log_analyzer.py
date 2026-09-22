from pathlib import Path
import re
import json
from collections import Counter,defaultdict
import argparse

class LogAnalyzer:
    def __init__(self,path):
        self.path = path
        self.levels = defaultdict(int)
        self.hours = Counter()
        self.skipped = []
        self.errors = []
    def parse(self):
        try:
            lines = Path(self.path).read_text(encoding = 'utf-8').splitlines()
        except FileNotFoundError:
            print("没有找到该项目")
            return
        pattern = r"^(\d{4}-\d{2}-\d{2})\s(\d{2}):(\d{2}):(\d{2})\s(INFO|ERROR|WARNING)\s(.+)$"
        for line in lines:
            m = re.match(pattern,line)
            if m is None:
                self.skipped.append(line)
                continue
            date,hh,mm,ss,level,msg = m.groups()
            self.levels[level] += 1
            self.hours[hh] += 1
            if level == "ERROR":
                self.errors.append(msg)
    def report(self):
        print("级别:",dict(self.levels))
        print("按小时:",dict(self.hours))
        print("按有效行数:",sum(self.levels.values()))
        print("跳过的脏行:",self.skipped)
        total = sum(self.levels.values())
        for level,count in self.levels.items():
            print(f"{level}:{count}条({count/total*100:.1f}%)")

    def summary(self):
        return dict(self.levels)

    def __str__(self):
        return f"LogAnalyzer({self.path},有效{sum(self.levels.values())}行)"

    def top_errors(self, n=3):
        x = Counter(self.errors)
        return x.most_common(n)

    @property
    def error_count(self):
        return len(self.errors)

class JsonLogAnalyzer(LogAnalyzer):
    def report(self):
        print(json.dumps(self.summary(),ensure_ascii=False,indent=2))

if __name__ == "__main__":
    # a = LogAnalyzer("test.log")
    # a.parse()
    # a.report()
    # print(a.summary())
    # print(a.top_errors())
    # print(a)
    # print("errors的行数为:",a.error_count)
    # j = JsonLogAnalyzer("test.log")
    # j.parse()
    # j.report()
    # print("summary:",j.summary())
    parser = argparse.ArgumentParser(description = "日志分析工具")
    parser.add_argument("path",help = "日志文件路径")
    parser.add_argument("--level",choices = ["INFO","ERROR","WARNING"],default = "INFO",help = "只统计某个级别(默认 INFO)")
    parser.add_argument("-n",type = int,default = 3,help = "显示错误 TOP N(默认3)")
    args = parser.parse_args()

    a1 = LogAnalyzer(args.path)
    a1.parse()
    a1.report()
    print(f"错误 Top {args.n}:",a1.top_errors(args.n))
    print(f"{args.level} 级别:{a1.summary()[args.level]}条")
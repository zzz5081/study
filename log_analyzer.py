from pathlib import Path
import re
from collections import Counter,defaultdict

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

    def top_errors(self,n = 3):
        x = Counter(self.errors)
        return x.most_common(n)

if __name__ == "__main__":
    a = LogAnalyzer("test.log")
    a.parse()
    a.report()
    print(a.summary())
    print(a.top_errors())
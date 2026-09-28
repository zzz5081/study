import argparse

parser = argparse.ArgumentParser(description = "日志分析工具")
parser.add_argument("path",help="日志文件路径")
#位置参数
parser.add_argument("--level",choices=["INFO","ERROR","WARNING"],default="INFO")#可选值
# 整数
parser.add_argument("-n",type=int,default=3,help="显示 TOP N")
# 开关
parser.add_argument("--verbose",action="store_true")
args = parser.parse_args()
print(args.path,args.level,args.n,args.verbose)
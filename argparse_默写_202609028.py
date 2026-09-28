import argparse

parser = argparse.ArgumentParser(description="文档日志工具")

parser.add_argument('path',help='文档路径')
parser.add_argument('--level',choices=["ERROR","INFO","WARNING"],default="INFO")
parser.add_argument('-n',type=int,default=3)
parser.add_argument('--verbose',action='store_True')

args = parser.parse_args()
print(args.path,args.level,args.n,args.verbose)
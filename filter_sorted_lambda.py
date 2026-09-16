students = [
    {"name": "小明", "score": 85},
    {"name": "小红", "score": 92},
    {"name": "小刚", "score": 78},
    {"name": "小美", "score": 92},
]
# 任务1：按成绩降序排序
def by_score(student):
    return student["score"]
print(sorted(students,key = by_score,reverse = True))
# 任务2：filter 筛出 score >= 80 的
l = list(filter(lambda x: x['score'] >= 80,students))
print(l)
# 任务3：及格学生按成绩降序（组合）
print(sorted(filter(lambda x: x['score'] >= 60,students),key = lambda x: x['score'],reverse = True))
# 挑战：成绩降序，成绩相同按名字升序
#      → key=lambda s: (-s["score"], s["name"])
sorted(sorted(students,key=lambda x:x['name']),key=lambda x:x['score'],reverse = True)
sorted(students,key=lambda s: (-s["score"],s["name"]))
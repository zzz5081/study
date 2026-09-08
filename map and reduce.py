# dict0 = {"A":"a","B":"b","C":"c","D":"d","E":"e","F":"f","G":"g","H":"h","I":"i","J":"j","K":"k","L":"l","M":"m","N":"n","O":"o","P":"p","Q":"q","R":"r","S":"s","T":"t","U":"u","V":"v","W":"w","X":"x","Y":"y","Z":"z"}
# dict1 = {"a":"A","b":"B","c":"C","d":"D","e":"E","f":"F","h":"H","g":"G","i":"I","j":"J","k":"K","l":"L","m":"M","n":"N","o":"O","p":"P","q":"Q","r":"R","s":"S","t":"T","u":"U","v":"V","w":"W","x":"X","y":"Y","z":"Z"}
# def normalize(name):
#     name = list(name)
#     if name[0] not in dict0:
#         name[0] = dict1[name[0]]
#     for i in range(1,len(name)):
#         if name[i] not in dict1:
#             name[i] = dict0[name[i]]
#     return ''.join(name)
# # 测试:
# L1 = ['adam', 'LISA', 'barT']
# L2 = list(map(normalize, L1))
# print(L2)


from functools import reduce

def prod(L):
    def add(a,b):
        return a*b
    return reduce(add,L)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')

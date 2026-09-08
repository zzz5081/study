def trim(s):
    left = 0
    while left < len(s) and s[left] == ' ':
        left += 1
    right = len(s) - 1
    while right >= 0 and s[right] == ' ':
        right -= 1
    if right == left:
        return ''
    return s[left:right + 1]

# 测试:
if trim('hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello') != 'hello':
    print('测试失败!')
elif trim('  hello  ') != 'hello':
    print('测试失败!')
elif trim('  hello  world  ') != 'hello  world':
    print('测试失败!')
elif trim('') != '':
    print('测试失败!')
elif trim('    ') != '':
    print('测试失败!')
else:
    print('测试成功!')

# 实验：密码为什么要"加盐哈希"
# 关键点：
#   1. 哈希是单向的 → 从哈希推不回密码
#   2. 盐【不需要保密】，它就在库里公开放着
#   3. 盐的作用 = 让每个用户的哈希【不同】→ 彩虹表【整体作废】
#   4. 盐防"横向"（破解一个不能复用到别人）；慢哈希防"纵向"（单个也试不了太多）
#      两者必须都有 → 真实项目用 bcrypt / argon2，不用 sha256
#
# 我踩的坑：
#   · b"salt+password.encode()" —— 把【表达式】写进引号，引号里永远是死文本
#   · 盐生成了却没用进 sha256（hash 部分和不加盐一模一样）
#   · stored.split('$') 返回【列表】，不能直接和字符串比
#   · 变量名 hash 覆盖了 Python 内建函数 hash()
#
# 验收（7 条）：见文件末尾 assert

import secrets,hashlib
def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16).hex()
    h = hashlib.sha256( (salt+password).encode() ).hexdigest()
    return salt+'$'+h
def verify_password(password: str, stored: str) -> bool:
    salt, h = stored.split('$')
    check = hashlib.sha256((salt+password).encode()).hexdigest()
    return h == check

if __name__ == '__main__':
    import hashlib as _hl
    h1 = hash_password('123456')
    h2 = hash_password('123456')

    assert h1 != h2                                                        # 1 整串不同
    assert h1.split('$')[1] != h2.split('$')[1]                            # 2 ★ hash 部分也不同
    assert h1.split('$')[1] != _hl.sha256('123456'.encode()).hexdigest()   # 3 ★ 不等于裸 sha256
    assert verify_password('123456', h1) is True                           # 4
    assert verify_password('123456', h2) is True                           # 5 不同盐也能过
    assert verify_password('654321', h1) is False                          # 6
    bad = h1[:-1] + ('0' if h1[-1] != '0' else '1')
    assert verify_password('123456', bad) is False                         # 7 改一个字符
    print('通过')

    # 每次结果不同 -> 破解了一个人也撞不到别人（每个人的盐不同，库里存的值都不同）
    # 慢哈希让暴力破解成本更高；而验证只需要算 1 次，所以很快（这是必须的）
    # ⭐ 第 2、3 条才是关键：整串不同只是表象，hash 部分不同才是盐真的生效

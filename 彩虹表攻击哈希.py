import hashlib

rainbow = {hashlib.sha256(p.encode()).hexdigest(): p for p in ['123456','password','qwerty','88888888','admin']}

print("攻击者的表建好了:")
for h,p in rainbow.items():
    print(f"{p:10} -> {h[:20]}...")

stolen_nosalt = [hashlib.sha256(p.encode()).hexdigest()
                 for p in ['123456','qwerty','password','abcdefg']]
print("\n偷不加盐的数据库,查表试试:")
for h in stolen_nosalt:
    print(f"  {h[:20]}...-> {rainbow.get(h)}")

from password_hash_实验 import hash_password

stolen_salt = [hash_password(p)
               for p in ['123456','qwerty','password','abcdefg']]
print("\n偷加盐的数据库，查表试试:")
for s in stolen_salt:
    salt, hh = s.split("$")
    print(f"  {hh[:20]}...-> {rainbow.get(hh)}   （★ 拿 hash 部分去查，也一样查不到）")

# 有耐心的破解者：知道盐之后，必须【针对这一个盐】重新算一遍表
#   TODO(10/13)：任选一个盐，用同一个密码字典重建一张小表，看能不能破出来
#   要体会到的点：别人算好的表【完全用不上】，每多一个用户就得多算一遍
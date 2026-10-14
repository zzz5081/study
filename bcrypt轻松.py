import time,hashlib,bcrypt

t = time.time()
for _ in range(10000):
    hashlib.sha256(b"salt" + b"123456").hexdigest()
sha = time.time() - t
print(f"sha256 * 10000 : {sha:.4f}秒")

t = time.time()
for _ in range(5):
    bcrypt.hashpw(b"123456",bcrypt.gensalt())
bc = time.time() - t
print(f"bcrypt * 5     : {bc:.4f} 秒")

print(f"\n单次之比: bcrypt 是 sha256 的 {bc/5/(sha/10000):,.0f} 倍")
print(f"攻击者试 10 亿个代码:")
print(f"   sha256: {sha/10000*1e9/3600:.1f} 小时")
print(f"   bcrypt    : {bc/5*1e9/3600/24/365:.0f} 年")

h1 = bcrypt.hashpw(b"123456",bcrypt.gensalt())
h2 = bcrypt.hashpw(b'123456',bcrypt.gensalt())
print(h1)
print(h2)
print("一样吗：",h1 == h2)
print("都能过吗:",bcrypt.checkpw(b"123456",h1),bcrypt.checkpw(b'123456',h2))
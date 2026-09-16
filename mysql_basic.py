"""用 Python 直接操作 MySQL（pymysql）—— 比 SQLAlchemy 简单直观

═══════════════════════════════════════════════════════════
为什么先学这个？
═══════════════════════════════════════════════════════════
你已经会写 SQL 了（SELECT / INSERT / UPDATE / DELETE）。
这个文件做的事就是：**把 SQL 字符串交给 MySQL 执行，再把结果取回来**。
没有 ORM 那一层抽象，你现在学它最顺。

只有三个新东西：
    1. pymysql.connect(...)  →  连上数据库（相当于 DBeaver 里点"连接"）
    2. conn.cursor()         →  拿到一个"执行器"，用它 execute(SQL)
    3. cursor.fetchall()     →  把查询结果取出来（元组的列表）

═══════════════════════════════════════════════════════════
运行方式
═══════════════════════════════════════════════════════════
    在 PyCharm 或终端运行均可（密码已设为系统环境变量，无需额外设置）
        python mysql_basic.py

学习顺序：先看 ① ② ③ 理解流程 → 然后自己填 TODO-1 ~ TODO-7
"""
import os
import pymysql

# ============================================================
# ① 连接配置（每个函数里都用它来连数据库）
# ============================================================
CONFIG = dict(
    host="localhost",
    port=3306,
    user="root",
    password=os.environ.get("MYSQL_PWD"),
    database="practice_db",
    charset="utf8mb4",
)

if not CONFIG["password"]:
    raise SystemExit("❌ 没读到密码，请先设置环境变量 MYSQL_PWD")


# ============================================================
# ② 建表（已写好，看一遍理解流程）
# ============================================================
def create_table():
    conn = pymysql.connect(**CONFIG)      # 连数据库
    cursor = conn.cursor()                # 拿执行器
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id    INT PRIMARY KEY AUTO_INCREMENT,
            name  VARCHAR(20),
            score INT
        )
    """)                                  # 执行一条 SQL（和你在 DBeaver 里敲的一样）
    conn.commit()                         # ⚠️ 建表/增删改 都要 commit 才生效
    cursor.close()
    conn.close()                          # 用完关掉
    print("✅ 建表完成：students")


# ============================================================
# ③ 插入（TODO-1 ~ TODO-3）
# ============================================================
def insert_data():
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()

    # TODO-1：插入一个学生（小明，85 分）
    #   提示：cursor.execute(
    #            "INSERT INTO students (name, score) VALUES (%s, %s)",
    #            ("小明", 85)          # ← 值单独传，千万别用 f-string 拼字符串！
    #         )

    # TODO-2：再批量插入两个（小红 92、小刚 78）
    #   提示：cursor.executemany("INSERT INTO students (name, score) VALUES (%s, %s)",
    #                            [("小红", 92), ("小刚", 78)])

    # TODO-3：提交 + 关闭
    #   提示：conn.commit()  然后 cursor.close() / conn.close()

    cursor.execute(
        "INSERT INTO students (name,score) VALUES (%s,%s)",
        ("小明",85)
    )
    cursor.executemany(
        "INSERT INTO students (name,score) VALUES (%s,%s)",
        [("小红",92),("小刚",78)]
    )
    conn.commit()
    cursor.close()
    conn.close()


# ============================================================
# ④ 查询（TODO-4 ~ TODO-5）
# ============================================================
def query_data():
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()

    # TODO-4：查出所有学生并打印
    #   提示：cursor.execute("SELECT id, name, score FROM students")
    #        rows = cursor.fetchall()          # [(1,'小明',85), (2,'小红',92), ...]
    #        for row in rows: print(row)

    # TODO-5：只查 score >= 80 的学生，打印姓名和分数
    #   提示：SELECT
    #     cursor.close()name, score FROM students WHERE score >= %s  并传参 (80,)
    cursor.execute("SELECT id,name,score from students")
    rows = cursor.fetchall()
    for row in rows:print(row)
    cursor.execute("SELECT name,score FROM students WHERE score >= 80")
    rows = cursor.fetchall()
    for row in rows:print(row)
    cursor.close()
    conn.close()


# ============================================================
# ⑤ 更新（TODO-6）
# ============================================================
def update_data():
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()

    # TODO-6：把小明的成绩改成 90，并 commit
    #   提示：cursor.execute("UPDATE students SET score = %s WHERE name = %s", (90, "小明"))
    cursor.execute("UPDATE students set score = 90 WHERE name = %s",("小明",))
    conn.commit()
    cursor.close()
    conn.close()



# ============================================================
# ⑥ 删除（TODO-7）
# ============================================================
def delete_data():
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()

    # TODO-7：删掉小刚，并 commit
    #   提示：cursor.execute("DELETE FROM students WHERE name = %s", ("小刚",))
    cursor.execute("DELETE FROM students WHERE name = %s",("小刚",))
    conn.commit()
    cursor.close()
    conn.close()


# ============================================================
# ⑦ 事务演示（已写好，直接跑，观察输出）
# ============================================================
def transaction_demo():
    conn = pymysql.connect(**CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM students WHERE name = '小明'")
    row = cursor.fetchone()
    if not row:
        print("⚠️ 没有小明这条数据，先完成 TODO-1")
        cursor.close()
        conn.close()
        return
    print(f"【事务演示】小明原始分数 = {row[0]}")

    cursor.execute("UPDATE students SET score = 0 WHERE name = '小明'")
    cursor.execute("SELECT score FROM students WHERE name = '小明'")
    print(f"  改成 0 之后（还没 commit） = {cursor.fetchone()[0]}")

    conn.rollback()                       # 撤销！
    cursor.execute("SELECT score FROM students WHERE name = '小明'")
    print(f"  rollback 之后 = {cursor.fetchone()[0]}   ← 回到原值 ✅")

    cursor.close()
    conn.close()
    print("  → 和你学的 SQL 事务一模一样：不 commit 就不算数")


# ============================================================
# 主流程
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    create_table()
    print("=" * 55)
    insert_data()
    insert_data.__doc__  # noqa
    print("=" * 55)
    query_data()
    print("=" * 55)
    update_data()
    print("=" * 55)
    delete_data()
    print("=" * 55)
    transaction_demo()


# ═══════════════════════════════════════════════════════════
# 参考答案（卡住 15 分钟以上再看）
# ═══════════════════════════════════════════════════════════
#
# TODO-1/2/3  insert_data：
#     cursor.execute("INSERT INTO students (name, score) VALUES (%s, %s)", ("小明", 85))
#     cursor.executemany("INSERT INTO students (name, score) VALUES (%s, %s)",
#                        [("小红", 92), ("小刚", 78)])
#     conn.commit()
#     cursor.close(); conn.close()
#
# TODO-4/5  query_data：
#     cursor.execute("SELECT id, name, score FROM students")
#     for row in cursor.fetchall():
#         print(row)
#     cursor.execute("SELECT name, score FROM students WHERE score >= %s", (80,))
#     for name, score in cursor.fetchall():
#         print(name, score)
#
# TODO-6  update_data：
#     cursor.execute("UPDATE students SET score = %s WHERE name = %s", (90, "小明"))
#     conn.commit()
#
# TODO-7  delete_data：
#     cursor.execute("DELETE FROM students WHERE name = %s", ("小刚",))
#     conn.commit()

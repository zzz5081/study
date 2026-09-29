# SQL 速查表

> 来源：2026-09-29（W4 Day 2）窗口函数/索引/事务实操 + 实测报错
> 用法：写 SQL 前扫一眼（1 分钟）；面试前重点看「执行顺序」和「窗口函数」

---

## 零、最重要的一条：**子句顺序 + 执行顺序**

### 书写顺序（必须按这个写，写错就是 `ERROR 1064`）

```
SELECT      要哪些列
FROM        从哪张表        ← 永远紧跟 SELECT
WHERE       筛【行】
GROUP BY    分组
HAVING      筛【组】
ORDER BY    排序
LIMIT       取几条
```
**记忆：选 → 表 → 行 → 组 → 组 → 排 → 限**

> ⚠️ **实操建议：先把 `SELECT ... FROM 表名` 两行写下来，再往上加别的。**

### 执行顺序（决定了"什么能写在哪儿"）

```
① FROM      确定数据从哪来
② WHERE     筛行              ← 别名、聚合、窗口函数都还不存在
③ GROUP BY  分组              ← 分组后"行"变成"组"
④ HAVING    筛组
⑤ SELECT    算要显示的列        ← 别名、窗口函数在这里诞生 ⭐
⑥ ORDER BY  排序
⑦ LIMIT     取前几条
```

### 🔑 由执行顺序推出的所有"能不能写"

| 想写在 | 用 | 行不行 | 为什么 |
|---|---|---|---|
| `WHERE` | 聚合函数 `AVG()` | ❌ | `GROUP BY`(③) 之后才有 |
| `WHERE` | 列别名 `AS x` | ❌ | `SELECT`(⑤) 之后才有 |
| `WHERE` | **窗口函数** | ❌ | `SELECT`(⑤) 之后才有 |
| `HAVING` | 聚合函数 | ✅ | `HAVING`(④) 在 `GROUP BY`(③) 之后 |
| `ORDER BY` | 列别名 | ✅ | `ORDER BY`(⑥) 在 `SELECT`(⑤) 之后 |

> **一句话：`WHERE` 执行得很早，看不到任何后面才算出来的东西。**

### 实测证据（两个实验）

```sql
-- 实验 1：WHERE 用 SELECT 的别名 → 报错
SELECT salary * 2 AS double_salary FROM employees WHERE double_salary > 30000;
-- ERROR 1054 (42S22): Unknown column 'double_salary' in 'where clause'

-- 实验 2：ORDER BY 用同一个别名 → 成功
SELECT name, salary * 2 AS double_salary FROM employees ORDER BY double_salary DESC LIMIT 3;
-- ✅ 张三 50000 / 李四 40000 / 王五 40000
```

---

## 一、窗口函数

### 为什么需要它？—— `GROUP BY` 会**丢掉"是谁"**

```sql
-- 需求：每个部门工资最高的员工，要显示名字
SELECT dept, MAX(salary) FROM employees GROUP BY dept;
-- → 只有 3 行，部门和最高工资都在，但"是谁"没了
```

**因为 `GROUP BY` 的本质是"把多行压成 1 行"—— 一旦压成 1 行，这一行就失去了"身份"。**

### 窗口函数不减少行数

```sql
SELECT name, dept, salary,
       MAX(salary) OVER (PARTITION BY dept) AS 本部门最高
FROM employees;
-- → 8 行全在，每行都带上"我这个部门的最高工资"
```

### 语法拆解

```sql
ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)
                  └─ 分组 ─┘  └── 组内排序 ──┘
```
- `PARTITION BY dept` → **分组**。**不写 = 全表当一组**
- `ORDER BY salary DESC` → **组内排序**。**排名函数必须写**（没顺序就没有"第几"）
- **⚠️ 方向（`ASC`/`DESC`）必须显式想清楚** —— 它决定"第 1 名是谁"

### 三个排名函数（并列时的区别）

以全公司 8 行为例（薪水降序）：

| 函数 | 并列时 | 结果 |
|---|---|---|
| `ROW_NUMBER()` | **不并列**，硬发号 | `1,2,3,4,5,6,7,8` |
| `RANK()` | 并列同名次，**跳号** | `1,2,2,`**`4`**`,5,6,6,`**`8`** |
| `DENSE_RANK()` | 并列同名次，**不跳号** | `1,2,2,`**`3`**`,4,5,5,`**`6`** |

> **奥运记忆法**：
> - `ROW_NUMBER` = 发**号码牌**（一人一号）
> - `RANK` = 奥运**名次**（两人并列第 2 → **没有第 3 名**，直接第 4）
> - `DENSE_RANK` = **密集**名次（并列第 2 → 下一个还是第 3，名次不空）

### 🔑 怎么选？（从需求推，别背题型）

| 你的需求 | 用 | 保证 |
|---|---|---|
| 给我排第 N~M 的**记录**（要固定条数） | `ROW_NUMBER` | **一定** N~M 条 |
| 给我**名次**落在 N~M 的人（并列都算） | `RANK` / `DENSE_RANK` | 可能不是固定条数 |

**实例（本表数据）**：
- 全公司排名第 3~5 → `ROW_NUMBER` 给 **3 行**，`RANK` 给 **2 行**（因为并列 20000 占了 2、2，没有第 3 名）
- 每部门最低工资 → 用 **`RANK`**（研发部两人并列 20000，两个都要显示；用 `ROW_NUMBER` 只会留下一个）

### 窗口函数不能写在 `WHERE` 里

```sql
WHERE rn = 1     ❌ 报错
```
**原因**：`WHERE`(②) 比 `SELECT`(⑤) 早，那时 `rn` 还不存在。

**解法：套一层子查询**
```sql
SELECT * FROM (
    SELECT name, dept, salary,
           ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
    FROM employees
) t
WHERE rn = 1;
```

> **判断法：有没有要在窗口函数结果上做筛选？**
> - 有（`WHERE rn = 1`）→ **必须套子查询**
> - 没有（只是加一列）→ **不用套，直接写**

---

## 二、`GROUP BY` 的硬性规矩（`ONLY_FULL_GROUP_BY`）

MySQL 8 默认开启。规矩：

> **`GROUP BY dept` 之后，`SELECT` 里只允许出现：**
> **① 分组列本身（`dept`）　② 聚合函数（`MAX()`/`AVG()`/`SUM()`/`COUNT()`）**

```sql
SELECT name FROM employees GROUP BY dept;
-- ERROR 1055 (42000): ... nonaggregated column 'employees.name'
--   which is not functionally dependent on columns in GROUP BY clause
```

**为什么**：每个部门有好几个人，压成 1 行后 `name` 该显示谁？**数据库不猜，直接拒绝。**

**想看某组的明细又想要组的统计量 → 用窗口函数，不要用 `GROUP BY`。**

---

## 三、排序 `ORDER BY` 的细节

| # | 规则 |
|---|---|
| 1 | **`ORDER BY a, b` = 先按 a 排；a 相同的再按 b 排**（像查字典） |
| 2 | **方向写在每列各自后面，不写 = `ASC`**。`ORDER BY dept, salary DESC` = dept 升序 + salary 降序 |
| 3 | **中文默认按 Unicode 码点排，不是拼音！** |

### ⚠️ 中文排序的坑

`dept` 的排序规则是 `utf8mb4_0900_ai_ci`（`ai`=不区分重音，`ci`=不区分大小写）。

实测：
```
ORDER BY 城市         实际：上海 → 北京 → 广州    （按 Unicode 码点 4E0A < 5317 < 5E7F）
                      拼音：北京 → 广州 → 上海    （完全不同！）
```

> **`ORDER BY 中文列` 的结果，对"人"来说是随机顺序。**

**想要有意义的顺序 → 显式指定：**
```sql
ORDER BY FIELD(dept, '研发', '产品', '运营'), salary DESC
-- FIELD(列, 值1, 值2, ...) 返回该值在列表中的位置 → 按位置排
```
`FIELD()` 是 MySQL 特有；PostgreSQL 要用 `CASE WHEN`。

---

## 四、改数据的安全习惯

```sql
-- ❌ 危险：name 可能重名 + 没索引
UPDATE accounts SET balance = balance - 500 WHERE name = '小明';

-- ✅ 安全：主键唯一 + 有索引
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
```

**实测（表里加了一个同名的小明）：**

| 条件 | 结果 |
|---|---|
| `WHERE name = '小明'` | **两个小明都被扣 500** —— 转一笔，扣两笔 |
| `WHERE id = 1` | 只有 id=1 被扣 ✅ |

**`EXPLAIN` 对比：**

| 条件 | `type` | `key` | `rows` |
|---|---|---|---|
| `WHERE id = 1` | `const` | `PRIMARY` | 1 |
| `WHERE name = '小明'` | **`ALL`** | **`NULL`** | 3 |

> `type`：`const`（唯一命中，最快）> `ref` > `range` > `index` > **`ALL` = 全表扫描（最慢）**
> **`rows` 现在 1 vs 3 看不出差距（表只 3 行）—— 表大了就是 1 次 vs 100 万次。**

### 📌 三条保命规则

1. **能用主键就用主键**（唯一 + 有索引）
2. **`WHERE` 用业务字段时先问：它唯一吗？** 不唯一就会改到多行
3. **改数据前先 `SELECT` 一遍同样的 `WHERE`**，看命中哪几行

---

## 五、事务

```sql
START TRANSACTION;     -- 开启：之后的修改进入"待定"状态
UPDATE ...;
UPDATE ...;
SELECT ...;            -- 事务内能看到自己的修改（"我"的视角）
ROLLBACK;              -- 撤销：全部回到 START 之前
-- 或
COMMIT;                -- 永久生效：别人也能看到了
```

### 为什么需要事务？

转账要**两条 UPDATE**。若第一条成功、第二条失败（断电/崩溃/约束报错）→
**钱凭空消失。事务保证"要么全成功，要么全不做"** = ACID 的 **A（原子性）**。

### ⚠️ 脚本要幂等（能重复跑）

**`COMMIT` 是永久的** —— 跑第二遍脚本会**累积效果**（余额 1000→500→0→-500）。

> **生产环境的脚本（数据库迁移、部署、数据修复）必须幂等**，
> 否则失败重试就会**重复施加效果**（重复扣钱、重复插入）。
>
> **做法：开头先把状态重置成已知值。**
> ```sql
> UPDATE accounts SET balance = 1000;    -- 重置，保证可反复演练
> ```

### 查看隔离级别

```sql
SELECT @@transaction_isolation;                          -- 默认 REPEATABLE-READ
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- 改成读已提交
```

---

## 六、本表踩过的坑（血泪）

| 坑 | 正确 |
|---|---|
| `GROUP BY` 写在 `FROM` 前面 | **`FROM` 永远紧跟 `SELECT`** |
| `ORDER BY salary` 没写方向，结果排反了 | **方向要显式写出来，并想清楚"第 1 名是谁"** |
| `ROW_NUMBER`/`RANK` 别名不一致（`AS rw` 却 `WHERE rk`） | **别名和外层 `WHERE` 必须同名** |
| 想"保留 8 行"却只 `SELECT dept, AVG(...)` | **明细列一个都不能少**（否则等于 `GROUP BY` 的结果复制多遍） |
| 没有 `WHERE` 也套了子查询 | **不筛就不用套** |
| `WHERE` 里用别名/聚合/窗口函数 | **`WHERE` 执行早，看不到它们** |
| `UPDATE ... WHERE name = ...` | **能用主键就用主键** |
| 文件名用中文，`mysql -e "source 中文名.sql"` | **命令行要打开的文件用英文名** |

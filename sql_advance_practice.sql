-- ============================================================
-- SQL 进阶练习：窗口函数 / 索引 / 事务
-- 用法（二选一）：
--   1. 命令行: mysql -u root -p < sql_advance_practice.sql
--   2. 或者打开 Navicat / MySQL Workbench，把内容复制进去逐段执行
-- 注意: 开头会 DROP DATABASE，别在正式库上跑！
-- ============================================================

DROP DATABASE IF EXISTS practice_db;
CREATE DATABASE practice_db DEFAULT CHARACTER SET utf8mb4;
USE practice_db;

-- ============================================================
-- 一、窗口函数
-- ============================================================
CREATE TABLE employees (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(20),
  dept VARCHAR(20),
  salary INT
);

INSERT INTO employees (name, dept, salary) VALUES
('张三','研发',25000),('李四','研发',20000),('王五','研发',20000),
('赵六','产品',18000),('钱七','产品',15000),
('孙八','运营',12000),('周九','运营',12000),('吴十','运营',9000);

-- 练习 1：三种排名函数对比（重点看并列时怎么处理）
SELECT name, dept, salary,
       ROW_NUMBER() OVER (partition by dept order by salary desc) as rn,
       RANK() over(partition by dept order by salary DESC) as rk,
		DENSE_RANK() over (partition by dept order by salary desc) as drk
FROM employees
ORDER BY dept,salary DESC;
-- 观察点：研发部两人并列 20000 →
--   ROW_NUMBER: 2, 3（不并列，按出现顺序）
--   RANK:       2, 2（并列但跳过 3）
--   DENSE_RANK: 2, 2（并列且不跳号，下一个是 3）

-- 练习 2（经典面试题）：每个部门工资最高的前 2 名
SELECT * FROM (
  SELECT name, dept, salary,
         ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t
WHERE rn <= 2;
-- 关键：窗口函数不能直接写在 WHERE 里，必须套一层子查询

-- 练习 3：每个部门总工资 + 占公司比例
SELECT name, dept, salary,
       SUM(salary) OVER (PARTITION BY dept) AS dept_sum,
       SUM(salary) OVER ()                 AS all_sum,
       ROUND(salary / SUM(salary) OVER () * 100, 2) AS pct
FROM employees;

-- 练习 4：和"上一名"员工比工资（LAG / LEAD）
SELECT name, salary,
	lag(salary,1,0) over (order by salary DESC) as prev_or_zero,
	LAG(salary,2) over (order by salary DESC) as two_row_back,
	lead(salary,1,0) over(order by salary DESC) as next_salary 
FROM employees
order by salary desc;

-- 【对比理解】GROUP BY vs 窗口函数
SELECT dept, SUM(salary) FROM employees GROUP BY dept;          -- 3 行（把多行压成 1 行）
SELECT dept, salary, SUM(salary) OVER (PARTITION BY dept) FROM employees;  -- 8 行（保留每行）

-- ============================================================
-- 二、索引
-- ============================================================
CREATE INDEX idx_dept ON employees(dept);
CREATE INDEX idx_dept_salary ON employees(dept, salary);   -- 联合索引

-- 用 EXPLAIN 看执行计划：type=ALL 是全表扫描，ref/range 是走索引
EXPLAIN SELECT * FROM employees WHERE dept = '研发';          -- ✅ 走索引
EXPLAIN SELECT * FROM employees WHERE salary = 20000;          -- ❌ salary 没单独索引

-- 失效场景 1：对索引列做函数运算
EXPLAIN SELECT * FROM employees WHERE YEAR(name) = 2026;       -- ❌ 列被函数包住 → 失效

-- 失效场景 2：联合索引的"最左前缀"原则
EXPLAIN SELECT * FROM employees WHERE dept = '研发' AND salary > 10000;  -- ✅ 用上 (dept,salary)
EXPLAIN SELECT * FROM employees WHERE salary > 10000;                    -- ❌ 跳过最左列 dept

-- 失效场景 3：前置模糊匹配
EXPLAIN SELECT * FROM employees WHERE dept LIKE '研%';          -- ✅ 前缀匹配可走索引
EXPLAIN SELECT * FROM employees WHERE dept LIKE '%发';          -- ❌ 前置 % 失效

-- ============================================================
-- 三、事务
-- ============================================================
CREATE TABLE accounts (
  id INT PRIMARY KEY,
  name VARCHAR(20),
  balance INT
);
INSERT INTO accounts VALUES (1,'小明',1000),(2,'小红',1000);

-- 演练 A：回滚（转账中途撤销）
START TRANSACTION;
UPDATE accounts SET balance = balance - 300 WHERE id = 1;
UPDATE accounts SET balance = balance + 300 WHERE id = 2;
SELECT * FROM accounts;          -- 事务内看到：小明 700 / 小红 1300
ROLLBACK;                        -- 撤销！全部回到 1000/1000
SELECT * FROM accounts;          -- 又是 1000/1000

-- 演练 B：提交（转账成功）
START TRANSACTION;
UPDATE accounts SET balance = balance - 300 WHERE id = 1;
UPDATE accounts SET balance = balance + 300 WHERE id = 2;
COMMIT;                          -- 永久生效
SELECT * FROM accounts;          -- 700 / 1300
w
-- 查看当前隔离级别（MySQL 8 默认 REPEATABLE-READ）
SELECT @@transaction_isolation;
set SESSION transaction ISOLATION level read committed;
select @@TRANSACTION_ISOLATION;

-- ============================================================
-- 四、动手任务（自己写，别抄上面的）
-- ============================================================
-- 1. 查出每个部门工资最低的员工（用窗口函数）
-- 2. 查出全公司工资排名第 3 到第 5 的员工
-- 3. 给 employees 表加一个"部门平均工资"的列（不改变行数）
-- 4. 用事务演练：小明转 500 给小红，然后回滚，再提交一次

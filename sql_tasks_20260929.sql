-- USE practice_db;

-- SELECT * FROM (
--     -- 这里：把 name, dept, salary + RANK() 那一列 都查出来
--     SELECT name,dept,salary,
--         RANK() OVER(PARTITION BY dept ORDER BY salary ASC) as rk
--     -- RANK() OVER (PARTITION BY ... ORDER BY ...) AS ...
--     -- FROM employees
--     FROM employees
-- ) t
-- -- 这里：外层筛
-- -- WHERE ...
-- WHERE rk <= 1
-- ;

-- 2a. 用 ROW_NUMBER
-- SELECT * FROM (
--     SELECT name,dept,salary,
--         ROW_NUMBER() OVER(ORDER BY salary DESC) as rw
--     FROM employees
-- ) t
-- -- WHERE 3<=rw and rw<=5
-- WHERE rw BETWEEN 3 AND 5
-- ;
-- -- 2b. 用 RANK
-- SELECT * FROM(
--     SELECT name,dept,salary,
--         RANK() OVER(ORDER BY salary DESC) as rk
--     FROM employees
-- ) t
-- -- WHERE 3<=rk and rk <= 5
-- WHERE rk BETWEEN 3 AND 5
-- ;
-- -- 3a. 用 GROUP BY 试试（看看会出几行）
-- SELECT dept,AVG(salary)
-- FROM employees
-- GROUP BY dept
-- ;

-- -- 3b. 用窗口函数（看看会出几行）
-- SELECT name,dept,salary,
--     AVG(salary) OVER(PARTITION BY dept) as 部门平均工资
-- FROM employees
-- ORDER BY dept,salary DESC;

USE practice_db;
UPDATE accounts SET balance = 1000;    -- 重置（幂等性）
SELECT *
FROM accounts;
START TRANSACTION;
-- 4a. 转账 → SELECT → ROLLBACK → SELECT
UPDATE accounts SET balance = balance - 500 WHERE id = '1';
UPDATE accounts SET balance = balance + 500 WHERE id = '2';
SELECT *
FROM accounts;
ROLLBACK;
SELECT *
FROM accounts;

-- 4b. 转账 → COMMIT → SELECT
START TRANSACTION;
UPDATE accounts SET balance = balance - 500 WHERE id = '1';
UPDATE accounts SET balance = balance + 500 WHERE id = '2';
COMMIT;
SELECT * FROM accounts;

-- ==============================
-- Preview the Data:
-- ==============================

-- Get the First 10 Rows:
SELECT * FROM raw_bank_statement LIMIT 10;
SELECT * FROM raw_internal_ledger LIMIT 10;


-- ==============================
-- Understand the Data:
-- ==============================

-- SEE DATA TYPES:
\d raw_bank_statement;
\d raw_internal_ledger;

-- ROW COUNT FASTER BUT LESS ACCURATE:
SELECT relname AS table_name, reltuples::BIGINT AS approx_row_count FROM pg_class WHERE relname = 'raw_bank_statement';
SELECT relname AS table_name, reltuples::BIGINT AS approx_row_count FROM pg_class WHERE relname = 'raw_internal_ledger';

-- ROW COUNT MORE ACCURATE BUT SLOWER:
SELECT COUNT(*) AS row_count FROM raw_bank_statement;
SELECT COUNT(*) AS row_count FROM raw_internal_ledger;

-- 
-- COUNT MISSING VALUES:
--
-- FOR Larger Tables, Use TABLESAMPLE SYSTEM (1) to Get a Sample % of the Data, 1 means 1% of the Data, 10 means 10% of the Data, etc.
-- This is a good way to get a quick overview of the data without loading the entire table into memory.
-- But if dataset is small, you can use the entire dataset, then you don't have to use TABLESAMPLE SYSTEM (1).
SELECT COUNT(*) - COUNT(date) AS null_date, COUNT(*) - COUNT(description) AS null_description, COUNT(*) - COUNT(amount) AS null_amount, COUNT(*) - COUNT(transaction_id) AS null_transaction_id, COUNT(*) - COUNT(transaction_type) AS null_transaction_type, COUNT(*) - COUNT(account_number) AS null_account_number, COUNT(*) - COUNT(currency) AS null_currency, COUNT(*) - COUNT(status) AS null_status FROM raw_bank_statement TABLESAMPLE SYSTEM (1); 

SELECT COUNT(*) - COUNT(date) AS null_date, COUNT(*) - COUNT(description) AS null_description, COUNT(*) - COUNT(amount) AS null_amount, COUNT(*) - COUNT(transaction_id) AS null_transaction_id, COUNT(*) - COUNT(transaction_type) AS null_transaction_type, COUNT(*) - COUNT(account_number) AS null_account_number, COUNT(*) - COUNT(currency) AS null_currency, COUNT(*) - COUNT(status) AS null_status FROM raw_internal_ledger TABLESAMPLE SYSTEM (1);

-- 
-- COUNT DUPLICATE VALUES:
-- 
SELECT COUNT(*) AS groups_with_duplicates FROM (SELECT amount, transaction_id, transaction_type, account_number, currency FROM raw_bank_statement GROUP BY amount, transaction_id, transaction_type, account_number, currency HAVING COUNT(*) > 1) AS DuplicateGroups;

-- CREATE A TEMP TABLE FOR DUPLICATES FOR 1 MONTH (IT'S USEFUL IF THE ORIGINAL TABLE IS HUGE AND CAN'T BE LOADED INTO MEMORY OR COPIED INTO A NEW TABLE):
-- This is a good way to get a quick overview of the data without loading the entire table into memory.
-- Temp tables are automatically dropped at the end of the session.

-- If date is already in date type:
CREATE TEMP TABLE tmp_exploring_jan AS SELECT * FROM raw_bank_statement WHERE date >= DATE '2025-03-01' AND date < DATE '2025-04-01';
-- If date is in string(TEXT) type:
CREATE TEMP TABLE tmp_exploring_jan AS SELECT * FROM raw_bank_statement WHERE TO_DATE(date, 'YYYY/MM/DD') >= DATE '2025-03-01' AND TO_DATE(date, 'YYYY/MM/DD') < DATE '2025-04-01';
-- If date is in string(TEXT) format and has a specific format (YYYY/MM/DD):
CREATE TEMP TABLE tmp_exploring_jan AS SELECT * FROM raw_bank_statement WHERE date ~ '^\d{4}/\d{2}/\d{2}$' AND TO_DATE(date, 'YYYY/MM/DD') >= DATE '2025-03-01' AND TO_DATE(date, 'YYYY/MM/DD') < DATE '2025-04-01';

SELECT amount, transaction_id, transaction_type, currency, status, COUNT(*) FROM tmp_exploring_jan GROUP BY amount, transaction_id, transaction_type, currency, status HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC;

-- 
-- COUNT DISTINCT VALUES (UNIQUE VALUES):
-- fast if the column is already indexed.
SELECT COUNT(DISTINCT account_number) FROM raw_bank_statement;
SELECT COUNT(DISTINCT account_number) FROM raw_internal_ledger;

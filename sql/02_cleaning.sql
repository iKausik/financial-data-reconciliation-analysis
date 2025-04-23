-- Description: This SQL script cleans and transforms a raw bank statement dataset. It removes duplicates, standardizes data types, and formats the data for consistency. The cleaned data is then stored in a new table called cleaned_bank_statement.


CREATE TABLE cleaned_bank_statement AS
SELECT 
    ROW_NUMBER() OVER () AS id,
    CAST(date AS DATE) AS txn_date,
    TRIM(description) AS txn_description,
    CAST(amount AS FLOAT) AS txn_amount,
    TRIM(LOWER(CAST(transaction_id AS TEXT))) AS txn_id,
    UPPER(COALESCE(transaction_type, 'UNKNOWN')) AS txn_type,
    CAST(account_number AS TEXT) AS account_no,
    UPPER(COALESCE(currency, 'UNKNOWN')) AS currency,
    UPPER(COALESCE(status, 'UNKNOWN')) AS txn_status,
    CURRENT_TIMESTAMP AS created_at
FROM (
    SELECT *, 
        ROW_NUMBER() OVER (
            PARTITION BY transaction_id 
            ORDER BY date DESC
        ) AS row_num
    FROM raw_bank_statement
) deduped
WHERE row_num = 1;


CREATE TABLE cleaned_internal_ledger AS
SELECT 
    ROW_NUMBER() OVER () AS id,
    CAST(date AS DATE) AS txn_date,
    -- TO_DATE(date, 'MM/DD/YYYY') AS txn_date,
    TRIM(description) AS txn_description,
    CAST(amount AS FLOAT) AS txn_amount,
    TRIM(LOWER(CAST(transaction_id AS TEXT))) AS txn_id,
    UPPER(COALESCE(transaction_type, 'UNKNOWN')) AS txn_type,
    CAST(account_number AS TEXT) AS account_no,
    UPPER(COALESCE(currency, 'UNKNOWN')) AS currency,
    UPPER(COALESCE(status, 'UNKNOWN')) AS txn_status,
    CURRENT_TIMESTAMP AS created_at
FROM (
    SELECT *, 
        ROW_NUMBER() OVER (
            PARTITION BY transaction_id 
            ORDER BY date DESC
        ) AS row_num
    FROM raw_internal_ledger
) deduped
WHERE row_num = 1;

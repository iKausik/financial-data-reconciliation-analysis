-- Unmatched records from the bank statement
-- This query creates a new table called unmatched_from_bank that contains records from the bank statement that do not have a corresponding record in the internal ledger.
CREATE TABLE unmatched_from_bank AS
SELECT 
    b.*, 
    CURRENT_TIMESTAMP AS detected_at,
    CURRENT_DATE AS reconciliation_date,
    'recon_bot_v1' AS detected_by
FROM cleaned_bank_statement b
WHERE NOT EXISTS (
    SELECT 1 
    FROM cleaned_internal_ledger i
    WHERE b.txn_id = i.txn_id
);


-- Unmatched records from the internal ledger
-- This query creates a new table called unmatched_from_ledger that contains records from the internal ledger that do not have a corresponding record in the bank statement.
CREATE TABLE unmatched_from_ledger AS
SELECT 
    i.*, 
    CURRENT_TIMESTAMP AS detected_at,
    CURRENT_DATE AS reconciliation_date,
    'recon_bot_v1' AS detected_by
FROM cleaned_internal_ledger i
WHERE NOT EXISTS (
    SELECT 1 
    FROM cleaned_bank_statement b
    WHERE i.txn_id = b.txn_id
);

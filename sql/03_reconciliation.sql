-- Match records present in BOTH the bank statement and internal ledger
-- This query creates a new table called reconciled_txns that contains the results of the reconciliation process.
-- It joins the cleaned bank statement and internal ledger tables on the txn_id field, which is assumed to be a unique identifier for transactions in both tables. 

CREATE TABLE reconciled_txns AS
SELECT
    b.txn_id,
    b.txn_date AS bank_txn_date,
    i.txn_date AS internal_txn_date,
    b.txn_amount AS bank_txn_amount,
    i.txn_amount AS internal_txn_amount,
    b.account_no,
    b.currency,
    b.txn_status AS bank_status,
    i.txn_status AS internal_status,
    
    -- High-confidence flag
    CASE
        WHEN b.txn_amount = i.txn_amount AND b.txn_date = i.txn_date THEN 'MATCHED'
        ELSE 'MISMATCHED'
    END AS reconciliation_status,

    -- Human-readable reason
    CASE
        WHEN b.txn_amount <> i.txn_amount AND b.txn_date <> i.txn_date THEN 'AMOUNT & DATE MISMATCH'
        WHEN b.txn_amount <> i.txn_amount THEN 'AMOUNT MISMATCH'
        WHEN b.txn_date <> i.txn_date THEN 'DATE MISMATCH'
        ELSE NULL
    END AS notes,

    CURRENT_TIMESTAMP AS reconciled_at,
    CURRENT_DATE AS reconciliation_date,
    'recon_bot_v1' AS reconciled_by

FROM cleaned_bank_statement b
INNER JOIN cleaned_internal_ledger i 
    ON b.txn_id = i.txn_id;


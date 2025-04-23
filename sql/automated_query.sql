-- This SQL script is designed to automate the reconciliation process between a bank statement and an internal ledger.
-- It identifies matched and unmatched transactions, providing a clear overview of the reconciliation status. The script assumes that the bank statement and internal ledger have been cleaned and are ready for reconciliation.
INSERT INTO reconciled_txns (
    txn_id,
    bank_txn_date,
    internal_txn_date,
    bank_txn_amount,
    internal_txn_amount,
    account_no,
    currency,
    bank_status,
    internal_status,
    reconciliation_status,
    notes,
    reconciled_at,
    reconciliation_date,
    reconciled_by
)
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
    
    CASE
        WHEN b.txn_amount = i.txn_amount AND b.txn_date = i.txn_date THEN 'MATCHED'
        ELSE 'MISMATCHED'
    END AS reconciliation_status,

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
    ON b.txn_id = i.txn_id

-- Only reconcile if not already done
WHERE NOT EXISTS (
    SELECT 1 
    FROM reconciled_txns r
    WHERE r.txn_id = b.txn_id
);


-- Unmatched records from the bank statement
-- This query creates a new table called unmatched_from_bank that contains records from the bank statement that do not have a corresponding record in the internal ledger.
INSERT INTO unmatched_from_bank (
    txn_id,
    txn_date,
    txn_description,
    txn_amount,
    account_no,
    currency,
    txn_type,
    txn_status,
    created_at,
    detected_at,
    reconciliation_date,
    detected_by
)
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
)
AND NOT EXISTS (
    SELECT 1 
    FROM unmatched_from_bank ub
    WHERE ub.txn_id = b.txn_id
);


-- -- Unmatched records from the internal ledger
-- This query creates a new table called unmatched_from_ledger that contains records from the internal ledger that do not have a corresponding record in the bank statement.
INSERT INTO unmatched_from_ledger (
    txn_id,
    txn_date,
    txn_description,
    txn_amount,
    account_no,
    currency,
    txn_type,
    txn_status,
    created_at,
    detected_at,
    reconciliation_date,
    detected_by
)
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
)
AND NOT EXISTS (
    SELECT 1 
    FROM unmatched_from_ledger ul
    WHERE ul.txn_id = i.txn_id
);

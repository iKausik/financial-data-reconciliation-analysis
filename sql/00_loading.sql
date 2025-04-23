-- 
-- Load the Raw Data to PostgreSQL:
-- 
CREATE TABLE raw_bank_statement (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    amount NUMERIC(12, 2),
    transaction_id TEXT,
    transaction_type TEXT,
    account_number TEXT,
    currency TEXT,
    status TEXT
)

COPY raw_bank_statement (date, description, amount, transaction_id, transaction_type, account_number, currency, status) FROM 'D:/00001-DATA-WORK/vscode-workspaces/practice/AAA__portfolio__AAA/Finance/data-reconciliation-and-integrity-analysis/data/raw/bank_statement.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE raw_internal_ledger (
    id SERIAL PRIMARY KEY,
    date TEXT,
    description TEXT,
    amount NUMERIC(12, 2),
    transaction_id TEXT,
    transaction_type TEXT,
    account_number TEXT,
    currency TEXT,
    status TEXT
)

COPY raw_internal_ledger (date, description, amount, transaction_id, transaction_type, account_number, currency, status) FROM 'D:/00001-DATA-WORK/vscode-workspaces/practice/AAA__portfolio__AAA/Finance/data-reconciliation-and-integrity-analysis/data/raw/internal_ledger.csv' DELIMITER ',' CSV HEADER;

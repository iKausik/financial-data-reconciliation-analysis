from config import get_db_connection, get_db_cursor
import pandas as pd

def get_reconciled_txns():
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            # Your database operations here
            try:
                # Execute the query
                cur.execute("SELECT * FROM reconciled_txns TABLESAMPLE SYSTEM (10)")
                
                # Get column names
                columns = [desc[0] for desc in cur.description]
                
                # Fetch all results
                results = cur.fetchall()
                
                # Convert results to pandas DataFrame
                df = pd.DataFrame(results, columns=columns)

                return df
                                            
            except Exception as e:
                print(f"Error executing query: {e}")
                conn.rollback()
            else:
                conn.commit()

def get_unmatched_from_bank_txns():
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            try:
                # Execute the query
                cur.execute("SELECT * FROM unmatched_from_bank TABLESAMPLE SYSTEM (10)")
                
                # Get column names
                columns = [desc[0] for desc in cur.description]
                
                # Fetch all results
                results = cur.fetchall()
                
                # Convert results to pandas DataFrame
                df = pd.DataFrame(results, columns=columns)

                return df
                                
            except Exception as e:
                print(f"Error executing query: {e}")
                conn.rollback()
            else:
                conn.commit()

def get_unmatched_from_ledger_txns():
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            try:
                # Execute the query
                cur.execute("SELECT * FROM unmatched_from_ledger TABLESAMPLE SYSTEM (10)")
                
                # Get column names
                columns = [desc[0] for desc in cur.description]
                
                # Fetch all results
                results = cur.fetchall()
                
                # Convert results to pandas DataFrame
                df = pd.DataFrame(results, columns=columns)

                return df
                                
            except Exception as e:
                print(f"Error executing query: {e}")
                conn.rollback()
            else:
                conn.commit()

def get_total_by_currency():
    with get_db_connection() as conn:
        with get_db_cursor(conn) as cur:
            try:
                query = """
                    SELECT currency, SUM(bank_txn_amount) as total_bank_amount, SUM(internal_txn_amount) as total_internal_amount 
                    FROM reconciled_txns 
                    GROUP BY currency
                """

                # Execute the query
                cur.execute(query)

                # Get column names
                columns = [desc[0] for desc in cur.description]
                
                # Fetch all results
                results = cur.fetchall()
                
                # Convert results to pandas DataFrame
                df = pd.DataFrame(results, columns=columns)

                return df
                                
            except Exception as e:
                print(f"Error executing query: {e}")
                conn.rollback()
            else:
                conn.commit()

# result = get_total_by_currency()
# print(result)

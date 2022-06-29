import sqlite3
import os.path

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    db_path = os.path.join(BASE_DIR, "FastAPI/rates.db")
    conn = sqlite3.connect(db_path)

except sqlite3.Error as error:
    print("Failed to read data from sqlite db", error)

# Execute query on the sqlite DB
cur = conn.cursor()
drop_monthly_rates_table = """ 
        drop table monthly_rates
"""
cur.execute(drop_monthly_rates_table)
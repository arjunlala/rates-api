
from bs4 import BeautifulSoup
import requests
import sqlite3
from sqlite3 import Error
import os.path
from datetime import datetime


try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
    db_path = os.path.join(BASE_DIR, "FastAPI/rates.db")
    conn = sqlite3.connect(db_path)

except sqlite3.Error as error:
    print("Failed to read data from sqlite db", error)

# Execute query on the sqlite DB
cur = conn.cursor()
create_monthly_rates_table = """ 
        CREATE TABLE IF NOT EXISTS monthly_rates (
            maturity_date TEXT PRIMARY KEY,
            sofr real NOT NULL,
            libor real NOT NULL
        ); 
"""
cur.execute(create_monthly_rates_table)

url = "https://www.pensford.com/resources/forward-curve"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

data = []
table = soup.find('table')
table_body = table.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip('%') for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values

#prevent multiple runs on same day
first_element = data[0]
check_date = datetime.strptime(first_element[0], '%m/%d/%Y')

if check_date < datetime.now():
    for row in data:
        del row[2]
        row[0] = row[0].replace("/", "")
        sql = """
            INSERT OR REPLACE INTO monthly_rates (maturity_date, sofr, libor) VALUES ('{date}', {so}, {li});
        """.format(date = row[0], so = row[1], li = row[2])
        cur.execute(sql)
        conn.commit()

# Execute query on the sqlite DB
cur = conn.cursor()
cur.execute("SELECT * FROM monthly_rates")

# Print everything from a table
rows = cur.fetchall()
for row in rows:
    print(row)

conn.close()

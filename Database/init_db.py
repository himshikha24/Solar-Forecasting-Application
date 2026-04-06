import sqlite3
from src.data_loader import load_data

df = load_data()
conn = sqlite3.connect("Database/solar.db")
df.to_sql("solar_data", conn, if_exists="replace", index=False)
conn.close()

print("Database created successfully")


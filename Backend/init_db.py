import sqlite3

# connect to the database file
conn = sqlite3.connect("../DataBase/databites.db")

# open the schema file and run all the sql commands in it
with open("../DataBase/databites_schema.sql", "r") as file:
    sql_script = file.read()

conn.executescript(sql_script)

conn.commit()
conn.close()

print("database initialized")
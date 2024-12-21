import os
import sqlite3

database = os.environ.get("VERSIONS_DB")
database_src = os.environ.get("VERSIONS_DB_SRC") or ''

print("Updating database...")
with open(database_src, 'r') as fi:
    lines = fi.read().split(';')
    with sqlite3.Connection(database) as db:
        for line in lines: 
            if len(line) > 0:
                print(line)
                db.execute(line)
print("Database updated...")

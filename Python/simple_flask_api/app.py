#!/usr/bin/env python3
import sqlite3
from flask import Flask, jsonify
from pathlib import Path

# Initialise Flask app
app = Flask(__name__)

CWD = Path(__file__).resolve().parent
DB_PATH = CWD / "items.sqlite"

# Initialise database and create table if it does not exist
conn = sqlite3.connect(DB_PATH)
cursor =  conn.cursor()

cursor.executescript("""
    PRAGMA foreign_keys=ON;
    PRAGMA journal_mode=WAL;
    PRAGMA synchronous=NORMAL;
    PRAGMA mmap_size=134217728; -- 128 * 1024 * 1024
    PRAGMA journal_size_limit=67108864; -- 64 * 1024 * 1024
    PRAGMA cache_size=2000;
""")

cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")

# Insert some sample data if the table is empty
cursor.execute("SELECT COUNT(*) FROM items")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute("INSERT INTO items (name) VALUES ('Sample Item 1')")
    cursor.execute("INSERT INTO items (name) VALUES ('Sample Item 2')")
    conn.commit()
conn.close()

# Define the GET /items endpoint
@app.route("/items", methods = ["GET"])
def get_items():
    # Connect to the database and fetch all items
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM items")
    rows = cursor.fetchall()
    conn.close()
    # Convert the query result into a list of dictionaries
    items = []
    if rows:
        for row in rows:
            items.append({"id": row[0], "name": row[1]})
    # Return the list of items as JSON
    return jsonify(items)

# Run the app on local development server
if __name__ == "__main__":
    app.run(debug=True)

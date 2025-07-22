import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "db/portfolios.db"

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            ticker TEXT,
            weight REAL,
            esg_score INTEGER,
            carbon_footprint REAL,
            sector TEXT,
            expected_return REAL,
            carbon_impact REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_portfolio(user, df, performance):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    timestamp = datetime.now().isoformat()
    
    rows = []
    for _, row in df.iterrows():
        rows.append((
            user,
            row['Ticker'],
            row['Weight'],
            row['ESG Score'],
            row['Carbon Footprint'],
            row['Sector'],
            performance['return'],
            performance['carbon'],
            timestamp
        ))
    
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO portfolios
        (user, ticker, weight, esg_score, carbon_footprint, sector, expected_return, carbon_impact, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', rows)
    conn.commit()
    conn.close()

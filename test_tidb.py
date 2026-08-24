#!/usr/bin/env python
"""Quick TiDB connection test for Vercel deployment."""
import os
import re
import pymysql
import certifi

DATABASE_URL = os.environ.get('DATABASE_URL', '')
if not DATABASE_URL:
    print("❌ Set DATABASE_URL first")
    exit(1)

match = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/([^?]+)', DATABASE_URL)
if not match:
    print("❌ Invalid DATABASE_URL format")
    exit(1)

user, password, host, port, dbname = match.groups()
print(f"Connecting to: {host}:{port}/{dbname}...")

conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    port=int(port),
    database=dbname,
    ssl={'ca': certifi.where()} if host not in ('localhost', '127.0.0.1') else None,
    charset='utf8mb4',
)

cursor = conn.cursor()
cursor.execute("SELECT 1")
result = cursor.fetchone()
print(f"✅ Connection successful! Result: {result[0]}")

cursor.close()
conn.close()

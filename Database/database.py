import sqlite3
import os

DB_NAME = "Database/spamchecker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabel akun pengguna
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Tabel untuk menyimpan user yang dicentang "Ingat Saya"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            remember INTEGER DEFAULT 0
        )
    """)

    # Tabel untuk menyimpan email yang diklasifikasi
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            title TEXT,
            body TEXT,
            date TEXT,
            category TEXT,
            probability REAL
        )
    """)

    conn.commit()
    conn.close()

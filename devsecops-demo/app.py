"""
DevSecOps demo app — intentionally contains common vulnerability patterns
so that a SAST (static application security testing) scanner has
something real to catch. This code is NOT meant to be run as a real
service; it exists purely to demonstrate a CI security gate.

Do not deploy this. Do not remove the vulnerabilities without
understanding what each one is and why a scanner flags it — that's
the point of this exercise.
"""

import sqlite3
import subprocess

# --- Vulnerability 1: Hardcoded secret ---
# A SAST scanner should flag this immediately. Secrets belong in
# environment variables or a secrets manager, never in source code.
API_SECRET_KEY = "sk_live_51Hg3jKLm9pQxT2vN8bRzYw"


def get_user(username):
    """
    --- Vulnerability 2: SQL Injection ---
    User input is concatenated directly into a SQL query rather than
    using parameterized queries. A scanner should flag string
    formatting/concatenation feeding directly into a database cursor.
    """
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


def run_diagnostic(hostname):
    """
    --- Vulnerability 3: Command Injection ---
    User-controlled input passed to a shell command with shell=True.
    A scanner should flag this as OS command injection risk.
    """
    result = subprocess.run(["ping", "-c", "1", hostname], capture_output=True)
    return result.stdout


if __name__ == "__main__":
    print("This is a demo app for SAST scanning — not meant to be run.")

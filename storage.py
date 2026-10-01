import sqlite3
from datetime import date

DB_PATH ="jobs.db"

def init_db():
    conn=sqlite3.connect(DB_PATH)
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS seen_jobs(
                    dedup_key TEXT PRIMARY KEY,
                    title TEXT,
                    company TEXT,
                    url TEXT,
                    source TEXT,
                    first_seen_date TEXT
                )
             """)
    conn.commit()
    conn.close()
    
def filter_unseen(jobs):
    """Return only the jobs not already recorded as seen in the previous run."""
    conn=sqlite3.connect(DB_PATH)
    seen_keys={row[0] for row in conn.execute("SELECT dedup_key FROM seen_jobs")}
    conn.close()
    return [job for job in jobs if job.dedup_key not in seen_keys]
def record_seen(jobs):
    """Mark these jobs as seen so future runs won't show or re-score them again."""
    conn=sqlite3.connect(DB_PATH)
    today=date.today().isoformat()
    conn.executemany(
        "INSERT OR IGNORE INTO seen_jobs (dedup_key, title, company, url, source, first_seen_date) VALUES (?, ?, ?, ?, ?, ?)",
        [(job.dedup_key, job.title, job.company, job.url, job.source, today) for job in jobs],
    )
    conn.commit()
    conn.close()

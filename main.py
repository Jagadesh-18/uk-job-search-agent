import os
from datetime import date 

from aggregate import aggregate_jobs
from ranker import score_jobs
from storage import init_db, filter_unseen, record_seen
from emailer import send_digest_email

SEARCH_TERMS = ["machine learning engineer", "AI engineer", "data scientist", "MLOps engineer"]
DIGEST_DIR= "digests"

def get_ranked_jobs(search_terms, location="", top_n=15):
    init_db()
    jobs = aggregate_jobs(search_terms, location)
    new_jobs = filter_unseen(jobs)
    if not new_jobs:
        return[]
    scores = score_jobs(jobs)

    scored_jobs = [
        (s["score"], s["reason"], jobs[s["index"]])
        for s in scores
        if s["relevant"]
    ]
    scored_jobs.sort(key=lambda x: x[0], reverse=True)
    top_jobs = scored_jobs[:top_n]
    
    record_seen(new_jobs)
    return top_jobs

def write_digest(top_jobs):
    os.makedirs(DIGEST_DIR, exist_ok=True)
    today= date.today().isoformat()
    filepath=os.path.join(DIGEST_DIR, f"job_digest_{today}.md")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Job Digest for {today}\n\n")
        if not top_jobs:
            f.write("no new jobs found since last run.\n")
        else:
            f.write(f"{len(top_jobs)} new jobs found:\n\n")
            for score, reason, job in top_jobs:
                f.write(f"## [{job.title}]({job.url}) at {job.company} ({job.location})\n")
                f.write(f"- Source: {job.source}\n")
                f.write(f"- **Location:** {job.location}\n")
                if job.salary:
                    f.write(f"- **Salary:** {job.salary}\n")
                f.write(f"- Score: {score}\n")
                f.write(f"- Why: {reason}\n\n")
                f.write(f"- **Link:** {job.url}\n\n")
    return filepath

if __name__ == "__main__":
    top_jobs = get_ranked_jobs(SEARCH_TERMS)
    filepath=write_digest(top_jobs)
    if not top_jobs:
        print("No new jobs found since last run.")
    else:
        print(f"Top {len(top_jobs)} ranked jobs:\n")
        for score, reason, job in top_jobs:
            print(f"[{score}] [{job.source}] {job.title} at {job.company} ({job.location})")
            print(f"  Why: {reason}")
            print(f"  {job.url}\n")
    print(f"\nDigest Saved to {filepath}")
    
    with open(filepath, 'r', encoding="utf-8") as f:
        body=f.read()
    if send_digest_email(f"Job Digest --{date.today().isoformat()}",body):
        print("Digest email sent successfully.")
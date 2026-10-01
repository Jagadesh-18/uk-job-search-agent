from aggregate import aggregate_jobs
from ranker import score_jobs
from storage import init_db, filter_unseen, record_seen

SEARCH_TERMS = ["machine learning engineer", "AI engineer", "data scientist", "MLOps engineer"]

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


if __name__ == "__main__":
    top_jobs = get_ranked_jobs(SEARCH_TERMS)
    if not top_jobs:
        print("No new jobs found since last run.")
    else:
        print(f"Top {len(top_jobs)} ranked jobs:\n")
        for score, reason, job in top_jobs:
            print(f"[{score}] [{job.source}] {job.title} at {job.company} ({job.location})")
            print(f"  Why: {reason}")
            print(f"  {job.url}\n")
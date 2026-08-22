from aggregate import aggregate_jobs
from ranker import score_jobs


def get_ranked_jobs(keywords, location="", top_n=15):
    jobs = aggregate_jobs(keywords, location)
    scores = score_jobs(jobs)

    scored_jobs = [
        (s["score"], s["reason"], jobs[s["index"]])
        for s in scores
        if s["relevant"]
    ]
    scored_jobs.sort(key=lambda x: x[0], reverse=True)
    return scored_jobs[:top_n]


if __name__ == "__main__":
    top_jobs = get_ranked_jobs("machine learning engineer", location="London")
    print(f"Top {len(top_jobs)} ranked jobs:\n")
    for score, reason, job in top_jobs:
        print(f"[{score}] [{job.source}] {job.title} at {job.company} ({job.location})")
        print(f"  Why: {reason}")
        print(f"  {job.url}\n")
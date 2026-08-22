from reed_client import search_reed_jobs, normalize_reed_job
from adzuna_client import search_adzuna_jobs, normalize_adzuna_job

SENIORITY_EXCLUDE=["senior", "sr","sr.", "lead", "principal", "staff", "head of", "director", "vp ", "chief", "mid-snr", "mid/senior"]

def is_entry_level(title):
    title_lower=title.lower()
    return not any(term in title_lower for term in SENIORITY_EXCLUDE)
def aggregate_jobs(keywords, location="", results_per_source=20):
    reed_jobs = [normalize_reed_job(j) for j in search_reed_jobs(keywords, location)]
    adzuna_jobs = [normalize_adzuna_job(j) for j in search_adzuna_jobs(keywords, location)]
    all_jobs = reed_jobs + adzuna_jobs

    seen, deduped = set(), []
    for job in all_jobs:
        if job.dedup_key not in seen:
            seen.add(job.dedup_key)
            deduped.append(job)
    return [j for j in deduped if is_entry_level(j.title)]

if __name__=="__main__":
    jobs = aggregate_jobs("machine learning engineer", location="London")
    print(f"{len(jobs)} entry-level jobs after merging, dedup, and filtering\n")
    for job in jobs:
        print(f"[{job.source}] {job.title} at {job.company} ({job.location})")
        print(f"  {job.url}\n")
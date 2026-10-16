from reed_client import search_reed_jobs, normalize_reed_job
from adzuna_client import search_adzuna_jobs, normalize_adzuna_job
import re 
import re

SENIORITY_PATTERN = re.compile(
    r"\b(senior|sr|lead|principal|staff|head of|director|vp|chief|mid-snr|ii|iii|iv)\b",
    re.IGNORECASE,
)

def is_entry_level(title):
    return not SENIORITY_PATTERN.search(title)

def aggregate_jobs(search_terms, location=""):
    all_jobs = []
    for term in search_terms:
        all_jobs += [normalize_reed_job(j) for j in search_reed_jobs(term, location)]
        all_jobs += [normalize_adzuna_job(j) for j in search_adzuna_jobs(term, location)]
    

    seen, deduped = set(), []
    for job in all_jobs:
        if job.dedup_key not in seen:
            seen.add(job.dedup_key)
            deduped.append(job)
    return [j for j in deduped if is_entry_level(j.title)]

if __name__=="__main__":
    jobs = aggregate_jobs("machine learning engineer","AI engineer", "data scientist")
    print(f"{len(jobs)} entry-level jobs after merging, dedup, and filtering\n")
   
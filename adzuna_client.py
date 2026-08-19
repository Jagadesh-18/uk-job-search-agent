import os
import requests
from dotenv import load_dotenv

load_dotenv()

adzuna_app_id = os.getenv("ADZUNA_APP_ID")
adzuna_app_key = os.getenv("ADZUNA_APP_KEY")
adzuna_base_url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

def search_adzuna_jobs(keywords, location="", results_per_page=20):
    """Search for jobs on Adzuna using the provided keywords and location."""
    params = {
        "app_id": adzuna_app_id,
        "app_key": adzuna_app_key,
        "what": keywords,
        "where": location,
        "results_per_page": results_per_page
    }
    response = requests.get(adzuna_base_url, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()['results']  # Return the JSON response
if __name__ == "__main__":
    jobs = search_adzuna_jobs("machine learning engineer", location="london")
    print(f"Found {len(jobs)} jobs\n")
    for job in jobs[:5]:
        print(f"- {job['title']} at {job.get('company', {}).get('display_name', 'Unknown')} ({job.get('location', {}).get('display_name', '')})")
        print(f"   URL: {job['redirect_url']}\n")
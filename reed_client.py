import os
import requests 
from dotenv import load_dotenv
from models import Job

load_dotenv()

reed_api_key = os.getenv("REED_API_KEY")
reed_base_url = "https://www.reed.co.uk/api/1.0/search"

def normalize_reed_job(raw):
    salary = f"£{raw['minimumSalary']:,.0f}+" if raw.get("minimumSalary") else None
    return Job(
        title=raw["jobTitle"],
        company=raw["employerName"],
        location=raw["locationName"],
        url=raw["jobUrl"],
        source="reed",
        salary=salary,
        description=raw.get("jobDescription"),
    )

def search_reed_jobs(keywords, location="", results_to_take=20):
    """Search for jobs on Reed.co.uk using the provided keywords and location."""
    params = {
        "keywords": keywords,
        "location": location,
        "resultsToTake": results_to_take
    }
        # Reed uses HTTP Basic Auth: your API key as the username, blank password
    response = requests.get(reed_base_url, params=params, auth=(reed_api_key, ''))
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()['results']  # Return the JSON response
if __name__=="__main__":
    jobs=search_reed_jobs("machine learning engineer",location="london")
    print(f"Found {len(jobs)} jobs\n")
    for jobs in jobs[:5]:
        print(f" - {jobs['jobTitle']} at {jobs['employerName']}, Location: {jobs['locationName']}, Salary: {jobs.get('salary', 'Not specified')}")
        print(f"   URL: {jobs['jobUrl']}\n")
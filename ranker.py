import os
from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client =genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CV_SUMMARY = """
MSc Artificial Intelligence student at the University of Southampton (2025-2026).
Skills: Python, SQL, Java, Flask, Scikit-learn, Pandas, NumPy, Matplotlib, Power BI, MySQL.
Projects: reinforcement-learning trading agent for maritime auctions, student performance
prediction (96% accuracy classifier), heart disease prediction (Random Forest, Flask deployment),
healthcare chatbot Android app.
Looking for: entry-level/graduate AI Engineer, Machine Learning Engineer, or Data Scientist roles in the UK.
"""

class JobScore(BaseModel):
    index: int
    relevant: bool  # True only if genuinely an AI/ML/Data Science role
    score: int       # fit score 0-100
    reason: str       # one short sentence


class ScoreResults(BaseModel):
    results: List[JobScore]


def score_jobs(jobs):
    """Send a batch of jobs to Gemini in one call and get back a relevance/fit score for each."""
    job_list_text = "\n".join(
        f'{i}. "{job.title}" at {job.company} ({job.location})' + (f" - {job.salary}" if job.salary else "")
        for i, job in enumerate(jobs)
    )

    prompt = f"""Candidate background:
{CV_SUMMARY}

Score every job below for fit. Mark relevant=false for anything that isn't genuinely an
AI/ML/Data Science role — e.g. Machine Operator, Maintenance Engineer, or a generic
Systems/Infrastructure Engineer role that only matched on the word "machine" or "engineer".

Jobs:
{job_list_text}"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ScoreResults,
        ),
    )

    parsed = ScoreResults.model_validate_json(response.text)
    return [r.model_dump() for r in parsed.results]
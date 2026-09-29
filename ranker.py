import os
import time
from typing import List
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from pydantic import BaseModel
from dotenv import load_dotenv
from pydantic import BaseModel, Field
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
    index: int = Field(description="The job's index in the input list")
    relevant: bool = Field(description="True only if genuinely an AI/ML/Data Science role, not an unrelated job that matched on keywords")
    score: int = Field(description="Fit score against the candidate's background", ge=0, le=100)
    reason: str = Field(description="One short sentence explaining the score")


class ScoreResults(BaseModel):
    results: List[JobScore] = Field(description="One score per job, in the same order as the input list")

MODELS_TO_TRY = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest", "gemini-3.8-flash"]
def score_jobs(jobs, max_retries_per_model=5):
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
    for model_name in MODELS_TO_TRY:
        for attempt in range(max_retries_per_model):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ScoreResults,
                    ),
                )

                parsed = ScoreResults.model_validate_json(response.text)
                return [r.model_dump() for r in parsed.results]
            except ServerError:
                if attempt ==max_retries_per_model -1:
                    print(f"{model_name} still unavailable after {max_retries_per_model} attempts — trying next model...")
                    break
                wait=5*(2**attempt)
                print(f"Gemini overloaded, retrying in {wait}s (attempt {attempt + 1}/{max_retries_per_model})...")
                time.sleep(wait)
    raise RuntimeError("All Gemini models unavailable after retries — try again later.")
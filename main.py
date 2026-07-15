from fastapi import FastAPI
from pydantic import BaseModel

from services.matcher import calculate_match
from services.feedback import generate_feedback

app = FastAPI()

class AnalyzeRequest(BaseModel):

    job: dict

    candidate: dict

@app.get("/")
def home():

    return {
        "message":
        "AI Recruitment Service Running"
    }


@app.post("/analyze")
def analyze(
    data: AnalyzeRequest
):


    resume_text = (
        data
        .candidate
        .get(
            "resume_text",
            ""
        )
    )


    job_text = (
        data
        .job
        .get(
            "description",
            ""
        )
    )

    score = calculate_match(
        resume_text,
        job_text
    )


    feedback = generate_feedback(
        score
    )

    return {

        "score": score,

        "feedback": feedback

    }
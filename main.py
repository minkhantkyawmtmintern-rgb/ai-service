from fastapi import FastAPI
from pydantic import BaseModel

from services.matcher import calculate_match
from services.feedback import generate_feedback
from services.skill_matcher import compare_skills

app = FastAPI(title="AI Recruitment Service")

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
        ) or ""
    )


    job_text = (
        data
        .job
        .get(
            "description",
        ) or ""
    )

    semantic_score = calculate_match(
        resume_text,
        job_text
    )

    skill_result = compare_skills(
        data.candidate.get("skills",[]),
        data.job.get("required_skills",[])
    )

    final_score = (
        semantic_score * 0.7 + skill_result["skill_score"]*0.3

    )

    feedback = generate_feedback(
        final_score
    )

    return {

        "score": round(final_score,2),

        "semantic_score":semantic_score,

        "skill_score":skill_result["skill_score"],

        "feedback": {
            "summary":feedback["summary"],
            "level":feedback["level"],
            "matched_skills":skill_result["matched_skills"],
            "missing_skills":skill_result["missing_skills"]
        }

    }
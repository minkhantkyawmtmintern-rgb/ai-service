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
def analyze( data: AnalyzeRequest):

    resume_text = (data.candidate.get("resume_text",) or "" )


    job_text = ( data.job.get("description",  ) or "" )

    semantic_score = calculate_match(resume_text, job_text )

    skill_result = compare_skills(
        data.candidate.get("skills",[]),
        data.job.get("required_skills",[])
    )

    final_score = (
        semantic_score * 0.7 + skill_result["skill_score"]*0.3

    )

    feedback = generate_feedback(
        final_score,
        skill_result["matched_skills"],
        skill_result["missing_skills"]
    )

    return {

        "score": round(final_score, 2),

        "semantic_score": round(semantic_score, 2),

        "skill_score": round(skill_result["skill_score"], 2),

        "feedback": {

            "summary": feedback["summary"],

            "level": feedback["level"],

            "strengths": feedback["strengths"],

            "weaknesses": feedback["weaknesses"],

            "recommendation": feedback["recommendation"],

            "confidence": feedback["confidence"],

            "hiring_risk": feedback["hiring_risk"],

            "interview_suggestion": feedback["interview_suggestion"],

            "explanation": feedback["explanation"],

            "matched_skills": skill_result["matched_skills"],

            "missing_skills": skill_result["missing_skills"]

        }

    }
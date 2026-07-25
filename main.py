from fastapi import FastAPI
from pydantic import BaseModel

from services.matcher import calculate_match
from services.feedback import generate_feedback
from services.skill_matcher import compare_skills
from services.resume_parser import (
    extract_resume_information
)


app = FastAPI(
    title="AI Recruitment Service"
)


class AnalyzeRequest(BaseModel):

    job: dict

    candidate: dict


class ResumeRequest(BaseModel):

    resume_text: str


@app.get("/")
def home():

    return {
        "message":
            "AI Recruitment Service Running"
    }


@app.post("/resume-analysis")
def resume_analysis(
    data: ResumeRequest
):

    return extract_resume_information(
        data.resume_text
    )


@app.post("/analyze")
def analyze(
    data: AnalyzeRequest
):

    # ==================================================
    # 1. Extract Candidate Data
    # ==================================================

    candidate = data.candidate
    job = data.job

    resume_text = (
        candidate.get(
            "resume_text"
        ) or ""
    )

    candidate_skills = (
        candidate.get(
            "skills",
            []
        ) or []
    )

    candidate_profile = (
        candidate.get(
            "profile",
            {}
        ) or {}
    )

    candidate_experience = (
        candidate_profile.get(
            "experience"
        )
    )

    candidate_education = (
        candidate_profile.get(
            "education"
        )
    )

    # ==================================================
    # 2. Job Data
    # ==================================================

    job_description = (
        job.get(
            "description"
        ) or ""
    )

    required_skills = (
        job.get(
            "required_skills",
            []
        ) or []
    )

    required_experience = (
        job.get(
            "minimum_experience"
        ) or 0
    )

    required_education = (
        job.get(
            "education"
        ) or ""
    )

    # ==================================================
    # 3. Semantic Matching
    # ==================================================

    semantic_score = calculate_match(
        resume_text,
        job_description
    )

    # ==================================================
    # 4. Skill Matching
    # ==================================================

    skill_result = compare_skills(
        candidate_skills,
        required_skills
    )

    skill_score = skill_result[
        "skill_score"
    ]

    # ==================================================
    # 5. Experience Matching
    # ==================================================

    experience_score = calculate_experience_score(
        candidate_experience,
        required_experience
    )

    # ==================================================
    # 6. Education Matching
    # ==================================================

    education_score = calculate_education_score(
        candidate_education,
        required_education
    )

    # ==================================================
    # 7. Profile Completeness
    # ==================================================

    profile_score = calculate_profile_score(
        resume_text=resume_text,
        skills=candidate_skills,
        experience=candidate_experience,
        education=candidate_education
    )

    # ==================================================
    # 8. Final AI Score
    # ==================================================

    final_score = (

        semantic_score * 0.40

        +

        skill_score * 0.30

        +

        experience_score * 0.15

        +

        education_score * 0.10

        +

        profile_score * 0.05
    )

    final_score = round(
        final_score,
        2
    )

    # ==================================================
    # 9. AI Feedback
    # ==================================================

    feedback = generate_feedback(

        score=final_score,

        matched_skills=
            skill_result[
                "matched_skills"
            ],

        missing_skills=
            skill_result[
                "missing_skills"
            ],

        additional_skills=
            skill_result[
                "additional_skills"
            ],

        semantic_score=
            semantic_score,

        skill_score=
            skill_score,

        experience_score=
            experience_score,

        education_score=
            education_score,

        profile_score=
            profile_score
    )

    # ==================================================
    # 10. Response
    # ==================================================

    return {

        "score":
            final_score,

        "semantic_score":
            round(
                semantic_score,
                2
            ),

        "skill_score":
            round(
                skill_score,
                2
            ),

        "experience_score":
            round(
                experience_score,
                2
            ),

        "education_score":
            round(
                education_score,
                2
            ),

        "profile_score":
            round(
                profile_score,
                2
            ),

        "feedback": {

            "summary":
                feedback[
                    "summary"
                ],

            "level":
                feedback[
                    "level"
                ],

            "strengths":
                feedback[
                    "strengths"
                ],

            "weaknesses":
                feedback[
                    "weaknesses"
                ],

            "recommendation":
                feedback[
                    "recommendation"
                ],

            "confidence":
                feedback[
                    "confidence"
                ],

            "hiring_risk":
                feedback[
                    "hiring_risk"
                ],

            "interview_suggestion":
                feedback[
                    "interview_suggestion"
                ],

            "explanation":
                feedback[
                    "explanation"
                ],

            "matched_skills":
                skill_result[
                    "matched_skills"
                ],

            "missing_skills":
                skill_result[
                    "missing_skills"
                ],

            "additional_skills":
                skill_result[
                    "additional_skills"
                ],

            "score_breakdown":
                feedback[
                    "score_breakdown"
                ]
        }
    }


# ======================================================
# Helper Functions
# ======================================================

def calculate_experience_score(
    candidate_experience,
    required_experience
):

    if required_experience <= 0:

        return 100.0

    if candidate_experience is None:

        return 0.0

    try:

        candidate_experience = float(
            candidate_experience
        )

        required_experience = float(
            required_experience
        )

    except (
        TypeError,
        ValueError
    ):

        return 0.0

    if candidate_experience >= required_experience:

        return 100.0

    score = (
        candidate_experience
        / required_experience
    ) * 100

    return round(
        min(score, 100),
        2
    )


def calculate_education_score(
    candidate_education,
    required_education
):

    if not required_education:

        return 100.0

    if not candidate_education:

        return 0.0

    candidate = str(
        candidate_education
    ).lower()

    required = str(
        required_education
    ).lower()

    # Direct match
    if required in candidate:

        return 100.0

    # Related education terms
    related_groups = [

        {
            "computer science",
            "software engineering",
            "information technology",
            "information systems"
        },

        {
            "bachelor",
            "bachelor's",
            "bsc"
        },

        {
            "master",
            "master's",
            "msc"
        }
    ]

    for group in related_groups:

        candidate_match = any(
            term in candidate
            for term in group
        )

        required_match = any(
            term in required
            for term in group
        )

        if (
            candidate_match
            and required_match
        ):

            return 80.0

    return 30.0


def calculate_profile_score(
    resume_text,
    skills,
    experience,
    education
):

    score = 0

    # Resume text
    if resume_text:
        score += 40

    # Skills
    if skills:
        score += 25

    # Experience
    if experience is not None:
        score += 20

    # Education
    if education:
        score += 15

    return float(
        min(score, 100)
    )
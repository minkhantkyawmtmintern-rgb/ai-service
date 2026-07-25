def generate_feedback(
    score,
    matched_skills,
    missing_skills,
    additional_skills=None,
    experience_score=0,
    education_score=0,
    semantic_score=0,
    skill_score=0,
    profile_score=0,
):

    additional_skills = additional_skills or []

    # -----------------------------------------
    # Recommendation Level
    # -----------------------------------------

    if score >= 85:

        summary = "Excellent candidate match."
        level = "High"
        recommendation = "Highly Recommended"
        interview = "Proceed to Technical Interview"
        risk = "Low"

    elif score >= 70:

        summary = "Strong candidate match."
        level = "High"
        recommendation = "Recommended"
        interview = "Proceed to HR Interview"
        risk = "Low"

    elif score >= 50:

        summary = "Moderate candidate match."
        level = "Medium"
        recommendation = "Consider for Further Review"
        interview = "Keep in Talent Pool"
        risk = "Medium"

    else:

        summary = "Low candidate match."
        level = "Low"
        recommendation = "Not Recommended"
        interview = "Do Not Proceed"
        risk = "High"

    # -----------------------------------------
    # Strengths
    # -----------------------------------------

    strengths = []

    if matched_skills:

        strengths.append(
            f"Matched {len(matched_skills)} "
            "required skill(s)."
        )

    if skill_score >= 80:

        strengths.append(
            "Strong technical skill alignment."
        )

    if semantic_score >= 70:

        strengths.append(
            "Resume content is highly relevant "
            "to the job description."
        )

    if experience_score >= 80:

        strengths.append(
            "Candidate experience aligns well "
            "with the job requirement."
        )

    if education_score >= 80:

        strengths.append(
            "Educational background aligns "
            "with the position."
        )

    if additional_skills:

        strengths.append(
            f"Candidate also has "
            f"{len(additional_skills)} additional "
            "skill(s)."
        )

    # -----------------------------------------
    # Weaknesses
    # -----------------------------------------

    weaknesses = []

    if missing_skills:

        weaknesses.append(
            "Missing skills: "
            + ", ".join(missing_skills)
        )

    if semantic_score < 50:

        weaknesses.append(
            "Resume content has relatively "
            "low semantic alignment with "
            "the job description."
        )

    if experience_score < 50:

        weaknesses.append(
            "Experience level may not fully "
            "meet the job requirement."
        )

    if education_score < 50:

        weaknesses.append(
            "Educational background has limited "
            "alignment with the position."
        )

    # -----------------------------------------
    # Explanation
    # -----------------------------------------

    explanation = (
        f"AI evaluated the candidate using "
        f"multiple factors. Semantic relevance "
        f"contributed {semantic_score:.2f}%, "
        f"technical skill alignment contributed "
        f"{skill_score:.2f}%, experience alignment "
        f"contributed {experience_score:.2f}%, "
        f"education alignment contributed "
        f"{education_score:.2f}%, and profile "
        f"completeness contributed "
        f"{profile_score:.2f}%."
    )

    # -----------------------------------------
    # Confidence
    # -----------------------------------------

    confidence = calculate_confidence(
        score=score,
        semantic_score=semantic_score,
        skill_score=skill_score,
        profile_score=profile_score
    )

    return {

        "summary": summary,

        "level": level,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendation": recommendation,

        "confidence": confidence,

        "hiring_risk": risk,

        "interview_suggestion": interview,

        "explanation": explanation,

        "score_breakdown": {

            "semantic": round(
                semantic_score,
                2
            ),

            "skills": round(
                skill_score,
                2
            ),

            "experience": round(
                experience_score,
                2
            ),

            "education": round(
                education_score,
                2
            ),

            "profile": round(
                profile_score,
                2
            )
        }
    }


def calculate_confidence(
    score,
    semantic_score,
    skill_score,
    profile_score
):

    confidence = 50

    # Strong semantic signal
    if semantic_score >= 70:
        confidence += 15
    elif semantic_score >= 50:
        confidence += 8

    # Strong skill signal
    if skill_score >= 80:
        confidence += 15
    elif skill_score >= 50:
        confidence += 8

    # Profile completeness
    if profile_score >= 80:
        confidence += 10
    elif profile_score >= 50:
        confidence += 5

    # Extreme scores are easier to classify
    if score >= 85 or score <= 30:
        confidence += 5

    return round(
        min(confidence, 99),
        2
    )
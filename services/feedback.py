def generate_feedback(score, matched_skills, missing_skills):

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
        risk = "Medium"

    elif score >= 50:
        summary = "Moderate candidate match."
        level = "Medium"
        recommendation = "Consider for Future Opportunities"
        interview = "Keep in Talent Pool"
        risk = "Medium"

    else:
        summary = "Low candidate match."
        level = "Low"
        recommendation = "Not Recommended"
        interview = "Do Not Proceed"
        risk = "High"

    strengths = []

    if len(matched_skills) > 0:
        strengths.append(
            f"Matched {len(matched_skills)} required skill(s)."
        )

    if score >= 80:
        strengths.append(
            "Resume is highly relevant to the job description."
        )

    if len(matched_skills) >= 3:
        strengths.append(
            "Strong technical skill alignment."
        )

    weaknesses = []

    if len(missing_skills) > 0:
        weaknesses.append(
            "Missing skills: " + ", ".join(missing_skills)
        )

    if score < 70:
        weaknesses.append(
            "Overall profile could better align with job requirements."
        )

    explanation = (
        f"The candidate matches {len(matched_skills)} required skill(s) "
        f"and is missing {len(missing_skills)} skill(s). "
        "The recommendation is based on both semantic resume analysis "
        "and technical skill matching."
    )

    confidence = round(
        min(99, score + 8),
        2
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

        "explanation": explanation

    }
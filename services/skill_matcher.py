def compare_skills(candidate_skills, required_skills):

    candidate_skills = [
        skill.lower().strip()
        for skill in candidate_skills
    ]

    required_skills = [
        skill.lower().strip()
        for skill in required_skills
    ]

    matched = []
    missing = []

    for skill in required_skills:
        if skill in candidate_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(required_skills) > 0:
        skill_score = len(matched)/len(required_skills)*100
    else:
        skill_score = 0

    return {
        "matched_skills":matched,
        "missing_skills":missing,
        "skill_score": round(skill_score,2)
    }
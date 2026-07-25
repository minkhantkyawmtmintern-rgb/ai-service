from services.matcher import calculate_match


def calculate_experience_match(
    candidate_experience,
    required_experience
):

    try:
        candidate_experience = float(
            candidate_experience or 0
        )

        required_experience = float(
            required_experience or 0
        )

    except (TypeError, ValueError):

        return 0.0

    if required_experience <= 0:
        return 100.0

    if candidate_experience >= required_experience:
        return 100.0

    return round(
        (candidate_experience / required_experience) * 100,
        2
    )


def calculate_education_match(
    candidate_education,
    required_education
):

    if not required_education:
        return 100.0

    if not candidate_education:
        return 0.0

    candidate = candidate_education.lower().strip()
    required = required_education.lower().strip()

    if required in candidate:
        return 100.0

    if candidate in required:
        return 80.0

    education_levels = {
        "high school": 1,
        "diploma": 2,
        "associate": 3,
        "bachelor": 4,
        "master": 5,
        "phd": 6
    }

    candidate_level = 0
    required_level = 0

    for name, level in education_levels.items():

        if name in candidate:
            candidate_level = level

        if name in required:
            required_level = level

    if candidate_level >= required_level > 0:
        return 100.0

    if candidate_level > 0 and required_level > 0:

        return round(
            (candidate_level / required_level) * 100,
            2
        )

    return 0.0

def calculate_additional_skill_score(
    candidate_skills,
    required_skills
):

    candidate = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    required = {
        skill.lower().strip()
        for skill in required_skills
    }

    if not candidate:
        return 0.0

    additional = candidate - required

    if not additional:
        return 0.0

    return round(
        min(
            len(additional) / max(len(required), 1) * 100,
            100
        ),
        2
    )

def calculate_final_score(
    semantic_score,
    skill_score,
    experience_score,
    education_score,
    additional_skill_score
):

    final_score = (

        semantic_score * 0.30

        + skill_score * 0.40

        + experience_score * 0.15

        + education_score * 0.10

        + additional_skill_score * 0.05

    )

    return round(
        max(0, min(final_score, 100)),
        2
    )
def normalize_skill(skill: str) -> str:

    return (
        skill
        .lower()
        .strip()
    )


def compare_skills(
    candidate_skills,
    required_skills
):

    candidate_set = {
        normalize_skill(skill)
        for skill in candidate_skills
        if skill
    }

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
        if skill
    }

    matched = sorted(
        candidate_set
        .intersection(required_set)
    )

    missing = sorted(
        required_set
        - candidate_set
    )

    additional = sorted(
        candidate_set
        - required_set
    )

    if required_set:

        skill_score = (
            len(matched)
            / len(required_set)
        ) * 100

    else:

        skill_score = 0

    return {

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "additional_skills":
            additional,

        "skill_score":
            round(
                skill_score,
                2
            )

    }
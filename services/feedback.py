def generate_feedback(score):
    if score >= 80:
        return {
            "summary":"Strong candidate match.",
            "level":"high",
        }
    elif score > 60:
        return {
            "summary":"Moderate candidate match.",
            "level":"medium",
        }
    else:
        return {
            "summary":"Low candidate match.",
            "level":"low",
        }
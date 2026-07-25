import re

KNOWN_SKILLS = [
    "PHP",
    "Laravel",
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "Vue",
    "Angular",
    "Node.js",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Docker",
    "Git",
    "HTML",
    "CSS",
    "REST API",
    "API Development",
]

def extract_resume_information(text: str):

    skills = []

    for skill in KNOWN_SKILLS:

        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):

            skills.append(skill)

    experience = 0

    match = re.search(r'(\d+)\+?\s*years?', text, re.IGNORECASE)

    if match:

        experience = int(match.group(1))

    education = ""

    education_keywords = [

        "Bachelor",

        "Master",

        "B.Sc",

        "M.Sc",

        "Computer Science",

    ]

    for edu in education_keywords:

        if edu.lower() in text.lower():

            education = edu

            break

    summary = text[:250]

    return {

        "summary": summary,

        "skills": skills,

        "experience_years": experience,

        "education": education,

    }
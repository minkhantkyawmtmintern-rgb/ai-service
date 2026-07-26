import re
from datetime import datetime


# Common section headings found in resumes.
SECTION_HEADINGS = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "about me",
        "objective",
        "career objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "technical expertise",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "career history",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
    ],
}


# Education level detection.
EDUCATION_LEVELS = [
    ("phd", "PhD"),
    ("doctorate", "Doctorate"),
    ("master", "Master's Degree"),
    ("m.sc", "Master's Degree"),
    ("msc", "Master's Degree"),
    ("bachelor", "Bachelor's Degree"),
    ("b.sc", "Bachelor's Degree"),
    ("bsc", "Bachelor's Degree"),
    ("associate", "Associate Degree"),
    ("diploma", "Diploma"),
]


# Technology / skill patterns.
#
# This is NOT used as the only source of skills.
# It is used to improve recognition of common multi-word
# technologies and technical phrases.
TECHNOLOGY_PATTERNS = [
    r"\bC\+\+\b",
    r"\bC#\b",
    r"\bF#\b",
    r"\bASP\.NET\b",
    r"\.NET\b",
    r"\bNode\.js\b",
    r"\bNext\.js\b",
    r"\bNuxt\.js\b",
    r"\bVue\.js\b",
    r"\bReact\.js\b",
    r"\bReact Native\b",
    r"\bTailwind CSS\b",
    r"\bBootstrap\b",
    r"\bREST API\b",
    r"\bRESTful API\b",
    r"\bGraphQL\b",
    r"\bMachine Learning\b",
    r"\bDeep Learning\b",
    r"\bNatural Language Processing\b",
    r"\bComputer Vision\b",
    r"\bData Analysis\b",
    r"\bData Science\b",
    r"\bDatabase Management\b",
    r"\bAPI Development\b",
    r"\bUnit Testing\b",
    r"\bSoftware Testing\b",
    r"\bGit\b",
    r"\bGitHub\b",
    r"\bGitLab\b",
    r"\bCI/CD\b",
    r"\bAWS\b",
    r"\bMicrosoft Azure\b",
    r"\bAzure\b",
    r"\bGoogle Cloud\b",
    r"\bFirebase\b",
    r"\bMySQL\b",
    r"\bPostgreSQL\b",
    r"\bMongoDB\b",
    r"\bSQLite\b",
    r"\bRedis\b",
    r"\bDocker\b",
    r"\bKubernetes\b",
    r"\bLaravel\b",
    r"\bDjango\b",
    r"\bFlask\b",
    r"\bFastAPI\b",
    r"\bSpring Boot\b",
    r"\bJava\b",
    r"\bPython\b",
    r"\bPHP\b",
    r"\bRuby\b",
    r"\bGo\b",
    r"\bRust\b",
    r"\bJavaScript\b",
    r"\bTypeScript\b",
    r"\bHTML\b",
    r"\bCSS\b",
    r"\bSQL\b",
]


def clean_text(text: str) -> str:
    """
    Normalize extracted PDF text.
    """

    if not text:
        return ""

    text = text.replace("\r", "\n")

    # Normalize repeated spaces.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """

    skill = skill.lower().strip()

    skill = re.sub(
        r"[^\w+#./ -]",
        "",
        skill
    )

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill.strip()


def unique_preserve_order(items):
    """
    Remove duplicate values while preserving order.
    """

    seen = set()
    result = []

    for item in items:

        normalized = normalize_skill(item)

        if not normalized:
            continue

        if normalized not in seen:

            seen.add(normalized)
            result.append(item.strip())

    return result


def extract_section(
    text: str,
    section_names: list[str]
) -> str:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    start_index = None

    for index, line in enumerate(lines):

        normalized = re.sub(
            r"[^a-zA-Z ]",
            "",
            line
        ).strip().lower()

        if normalized in section_names:

            start_index = index + 1
            break

    if start_index is None:
        return ""

    collected = []

    all_headings = []

    for values in SECTION_HEADINGS.values():
        all_headings.extend(values)

    for line in lines[start_index:]:

        normalized = re.sub(
            r"[^a-zA-Z ]",
            "",
            line
        ).strip().lower()

        if normalized in all_headings:
            break

        collected.append(line)

    return "\n".join(collected).strip()


def extract_skills(text: str):

    skills = []

    # Search the ENTIRE resume
    for pattern in TECHNOLOGY_PATTERNS:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for match in matches:
            skills.append(match)

    # If a dedicated Skills section exists,
    # also parse comma/bullet separated items.
    skills_section = extract_section(
        text,
        SECTION_HEADINGS["skills"]
    )

    if skills_section:

        parts = re.split(
            r"[,|•;\n]",
            skills_section
        )

        for part in parts:

            part = part.strip()

            if 1 < len(part) <= 60:

                skills.append(part)

    return unique_preserve_order(skills)


def extract_experience_years(text: str):

    # --------------------------------------------------
    # 1. Explicit experience statement
    # --------------------------------------------------

    explicit_patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+experience",
        r"(\d+(?:\.\d+)?)\+?\s*years?\s+in\s+",
    ]

    for pattern in explicit_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return float(match.group(1))

    # --------------------------------------------------
    # 2. Calculate from date ranges
    # --------------------------------------------------

    current_year = datetime.now().year

    year_ranges = re.findall(
        r"\b(19\d{2}|20\d{2})\b"
        r"\s*[-–—]\s*"
        r"\b(19\d{2}|20\d{2}|present|current)\b",
        text,
        re.IGNORECASE
    )

    periods = []

    for start, end in year_ranges:

        start_year = int(start)

        if end.lower() in {
            "present",
            "current"
        }:
            end_year = current_year
        else:
            end_year = int(end)

        if (
            end_year >= start_year
            and end_year - start_year <= 50
        ):
            periods.append(
                (start_year, end_year)
            )

    if periods:

        earliest = min(
            start
            for start, _ in periods
        )

        latest = max(
            end
            for _, end in periods
        )

        experience = latest - earliest

        if experience > 0:
            return float(experience)

    # Unknown is NOT the same as zero experience.
    return None


def extract_education(text: str):

    education_section = extract_section(
        text,
        SECTION_HEADINGS["education"]
    )

    source = education_section or text

    detected_level = None

    for keyword, label in EDUCATION_LEVELS:

        if keyword.lower() in source.lower():

            detected_level = label
            break

    # Try to capture degree + field.
    degree_patterns = [
        r"(Bachelor(?:'s)?(?:\s+degree)?"
        r"(?:\s+in|\s+of)?\s+[A-Za-z][A-Za-z &]+)",

        r"(Master(?:'s)?(?:\s+degree)?"
        r"(?:\s+in|\s+of)?\s+[A-Za-z][A-Za-z &]+)",

        r"(B\.?Sc\.?(?:\s+in)?\s+[A-Za-z][A-Za-z &]+)",

        r"(M\.?Sc\.?(?:\s+in)?\s+[A-Za-z][A-Za-z &]+)",
    ]

    degree = None

    for pattern in degree_patterns:

        match = re.search(
            pattern,
            source,
            re.IGNORECASE
        )

        if match:

            degree = match.group(1).strip()
            break

    if degree:
        return degree

    if detected_level:
        return detected_level

    return None


def extract_summary(text: str):

    summary_section = extract_section(
        text,
        SECTION_HEADINGS["summary"]
    )

    if summary_section:

        # Limit extremely large sections.
        return summary_section[:500].strip()

    # Fallback:
    # use first meaningful lines rather than blindly
    # taking the first 250 characters.
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored = {
        "resume",
        "curriculum vitae",
        "cv",
    }

    meaningful = []

    for line in lines:

        if line.lower() in ignored:
            continue

        if len(line) >= 30:
            meaningful.append(line)

        if len(" ".join(meaningful)) >= 500:
            break

    return " ".join(
        meaningful
    )[:500].strip()


def extract_experience_section(text: str):

    return extract_section(
        text,
        SECTION_HEADINGS["experience"]
    )


def extract_resume_information(
    text: str
):

    text = clean_text(text)

    if not text:
        return {
            "summary": None,
            "skills": [],
            "experience_years": None,
            "experience": None,
            "education": None,
        }

    skills = extract_skills(text)

    experience_years = (
        extract_experience_years(text)
    )

    education = extract_education(text)

    experience = (
        extract_experience_section(text)
    )

    summary = extract_summary(text)

    return {
        "summary": summary,

        "skills": skills,

        "experience_years":
            experience_years,

        "experience":
            experience or None,

        "education":
            education,

    }
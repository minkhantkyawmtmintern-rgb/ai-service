# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def calculate_match(resume_text:str, job_text:str):
#     documents = [resume_text,job_text]

#     vectorizer = TfidfVectorizer()

#     vectors = vectorizer.fit_transform(documents)

#     score = cosine_similarity(
#         vectors[0],
#         vectors[1]
#     )[0][0]

#     return round(score * 100, 2)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def calculate_match(
    resume_text: str,
    job_text: str
):

    resume_text = (
        resume_text or ""
    ).strip()

    job_text = (
        job_text or ""
    ).strip()

    if not resume_text or not job_text:

        return 0.0

    embeddings = model.encode(
        [
            resume_text,
            job_text
        ]
    )

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )

    score = float(
        similarity[0][0]
    )

    # Keep score within 0-100.
    score = max(
        0,
        min(score, 1)
    )

    return round(
        score * 100,
        2
    )
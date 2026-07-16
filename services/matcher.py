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

model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match(resume_text:str, job_text:str):
    embeddings = model.encode([resume_text, job_text])

    similarity = cosine_similarity(
        [
            embeddings[0]
        ],
        [
            embeddings[1]
        ]
    )
    score = similarity[0][0]
    
    return round(float(score * 100), 2)
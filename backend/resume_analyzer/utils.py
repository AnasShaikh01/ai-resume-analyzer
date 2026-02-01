import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def load_bert_model():
    """Load and cache the sentence transformer model."""
    return SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def calculate_similarity_bert(model: SentenceTransformer, text1: str, text2: str) -> float:
    """Return cosine similarity (0..1) between two texts using the provided model."""
    if not text1 or not text2:
        return 0.0
    try:
        emb1 = model.encode([text1])
        emb2 = model.encode([text2])
        sim = cosine_similarity(emb1, emb2)[0][0]
        return float(np.clip(sim, -1.0, 1.0))
    except Exception:
        return 0.0

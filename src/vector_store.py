import faiss
import numpy as np


def create_faiss_index(embeddings):
    """
    Create a FAISS index using cosine similarity.
    """

    embeddings = np.asarray(embeddings).astype("float32")

    if embeddings.size == 0 or embeddings.ndim < 2:
        embeddings = np.zeros((1, 384), dtype="float32")

    # Normalize vectors
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    # Inner Product on normalized vectors = cosine similarity
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


def search_faiss(index, query_embedding, k=3):
    """
    Search FAISS using cosine similarity.
    """

    if index is None or index.ntotal == 0:
        return np.array([]), np.array([])

    query_embedding = np.asarray(query_embedding).astype("float32")

    query_embedding = query_embedding.reshape(1, -1)

    # Normalize query vector
    faiss.normalize_L2(query_embedding)

    search_k = min(k, index.ntotal)

    similarities, indices = index.search(
        query_embedding,
        search_k
    )

    return similarities[0], indices[0]
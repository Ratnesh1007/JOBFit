import numpy as np
from fastembed import TextEmbedding


MODEL_NAME = "BAAI/bge-small-en-v1.5"


model = TextEmbedding(
    model_name=MODEL_NAME
)


def generate_embeddings(text_chunks):
    if not text_chunks:
        return np.empty((0, 384), dtype="float32")

    embeddings = list(
        model.embed(text_chunks)
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    return embeddings
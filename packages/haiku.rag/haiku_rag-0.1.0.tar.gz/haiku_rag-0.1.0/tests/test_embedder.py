import numpy as np
import pytest

from haiku.rag.embeddings import get_embedder


@pytest.mark.asyncio
async def test_embedder():
    embedder = get_embedder()
    embedding = await embedder.embed("hello world")
    assert len(embedding) == embedder._vector_dim


@pytest.mark.asyncio
async def test_similarity():
    embedder = get_embedder()
    phrases = [
        "I enjoy eating great food.",
        "Python is my favorite programming language.",
        "I love to travel and see new places.",
    ]
    embeddings = [np.array(await embedder.embed(phrase)) for phrase in phrases]

    # Calculate cosine similarity
    def similarities(embeddings, test_embedding):
        return [
            np.dot(embedding, test_embedding)
            / (np.linalg.norm(embedding) * np.linalg.norm(test_embedding))
            for embedding in embeddings
        ]

    test_phrase = "I am going for a camping trip."
    test_embedding = await embedder.embed(test_phrase)

    sims = similarities(embeddings, test_embedding)
    assert max(sims) == sims[2]

    test_phrase = "When is dinner ready?"
    test_embedding = await embedder.embed(test_phrase)

    sims = similarities(embeddings, test_embedding)
    assert max(sims) == sims[0]

    test_phrase = "I work as a software developer."
    test_embedding = await embedder.embed(test_phrase)

    sims = similarities(embeddings, test_embedding)
    assert max(sims) == sims[1]

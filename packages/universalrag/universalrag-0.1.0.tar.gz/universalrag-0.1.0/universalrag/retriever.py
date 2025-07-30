import faiss
import numpy as np

class Retriever:
    def __init__(self, vectors, chunks):
        self.index = faiss.IndexFlatL2(len(vectors[0]))
        self.index.add(np.array(vectors).astype("float32"))
        self.chunks = chunks

    def get_top_chunks(self, query_vector, k=3):
        D, I = self.index.search(np.array([query_vector]).astype("float32"), k)
        return [self.chunks[i] for i in I[0]]
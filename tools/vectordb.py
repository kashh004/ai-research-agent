from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings

class VectorDB:
    def __init__(self, persist_dir: str, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.Client(ChromaSettings(is_persistent=True, persist_directory=persist_dir))
        self.col = self.client.get_or_create_collection("papers")

    def add_doc(self, doc_id: str, text: str, metadata: dict):
        emb = self.model.encode([text], normalize_embeddings=True).tolist()[0]
        self.col.add(ids=[doc_id], embeddings=[emb], metadatas=[metadata], documents=[text])

    def search(self, query: str, k: int = 5):
        qemb = self.model.encode([query], normalize_embeddings=True).tolist()[0]
        return self.col.query(query_embeddings=[qemb], n_results=k)

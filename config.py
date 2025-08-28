from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    data_dir: str = os.getenv("DATA_DIR", "data")
    pdf_dir: str = os.getenv("PDF_DIR", "data/pdfs")
    chroma_dir: str = os.getenv("CHROMA_DIR", "data/chroma")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()

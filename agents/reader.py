from tools.pdf_utils import download_pdf, extract_text_sections
from tools.vectordb import VectorDB

class Reader:
    def __init__(self, vdb: VectorDB):
        self.vdb = vdb

    def process_paper(self, title: str, pdf_url: str, entry_id: str):
        fname = entry_id.split("/")[-1] + ".pdf"
        path = download_pdf(pdf_url, fname)
        sections = extract_text_sections(path)
        # simple heuristic summary
        abstract = sections.get("abstract") or sections["full_text"][:1500]
        summary = abstract.strip().replace("\n", " ")
        self.vdb.add_doc(entry_id, sections["full_text"][:8000], {"title": title, "pdf": path})
        return {"summary": summary, "sections": sections, "pdf_path": path}

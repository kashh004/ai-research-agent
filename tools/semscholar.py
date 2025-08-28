import requests

BASE = "https://api.semanticscholar.org/graph/v1/paper/"
FIELDS = "title,authors,year,citationCount,referenceCount,openAccessPdf"

class SemanticScholarTool:
    def by_doi(self, doi: str):
        url = f"{BASE}DOI:{doi}?fields={FIELDS}"
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return None
        return r.json()
    
    def by_title(self, title: str):
        url = f"{BASE}search?query={title}&fields={FIELDS}&limit=1"
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get('data', [{}])[0] if data.get('data') else None

import arxiv
from typing import List, Dict

class ArxivTool:
    def __init__(self):
        self.client = arxiv.Client()

    def search(self, query: str, max_results: int = 20, since: str | None = None) -> List[Dict]:
        # Improve query to be more specific and use relevance sorting
        search = arxiv.Search(
            query=query, 
            max_results=max_results * 2,  # Get more results to filter
            sort_by=arxiv.SortCriterion.Relevance  # Use relevance instead of date
        )
        results = []
        for r in self.client.results(search):
            if since and r.published.date().isoformat() < since:
                continue
            # Filter results to ensure they're actually relevant to the query
            title_lower = r.title.lower()
            summary_lower = r.summary.lower()
            query_words = query.lower().split()
            
            # Check if at least one query word appears in title or summary
            relevant = any(word in title_lower or word in summary_lower for word in query_words)
            
            if relevant:
                results.append({
                    "title": r.title,
                    "authors": [a.name for a in r.authors],
                    "summary": r.summary,
                    "pdf_url": r.pdf_url,
                    "entry_id": r.entry_id,
                    "published": r.published.date().isoformat(),
                })
            
            # Stop when we have enough relevant results
            if len(results) >= max_results:
                break
                
        return results

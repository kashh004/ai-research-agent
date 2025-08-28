from tools.arxiv_tool import ArxivTool
from rank_bm25 import BM25Okapi

class Hunter:
    def __init__(self):
        self.ax = ArxivTool()

    def find(self, query: str, max_results=20, since=None):
        # Enhance query for better arXiv search
        enhanced_query = self._enhance_query(query)
        raw = self.ax.search(enhanced_query, max_results=max_results, since=since)
        
        if not raw:
            # Fallback to original query if enhanced query returns nothing
            raw = self.ax.search(query, max_results=max_results, since=since)
        
        # Re-rank with BM25 over title+summary
        corpus = [ (r["title"] + " " + r["summary"]).split() for r in raw ]
        if not corpus:
            return []
        bm25 = BM25Okapi(corpus)
        scores = bm25.get_scores(query.split())
        ranked = [r for _, r in sorted(zip(scores, raw), key=lambda x: x[0], reverse=True)]
        return ranked
    
    def _enhance_query(self, query: str) -> str:
        """Enhance query for better arXiv search results"""
        query_lower = query.lower()
        
        # Add relevant terms for specific domains
        if any(word in query_lower for word in ['dental', 'tooth', 'dentistry', 'oral']):
            return f"({query}) AND (deep learning OR machine learning OR neural network OR AI OR computer vision)"
        elif any(word in query_lower for word in ['medical', 'healthcare', 'clinical']):
            return f"({query}) AND (deep learning OR machine learning OR neural network OR AI)"
        elif any(word in query_lower for word in ['vision', 'image', 'segmentation']):
            return f"({query}) AND (computer vision OR deep learning OR neural network)"
        else:
            return query

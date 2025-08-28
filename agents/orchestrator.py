from agents.hunter import Hunter
from agents.reader import Reader
from agents.critic import Critic
from agents.hypothesis import Hypothesis
from agents.gemini_agent import GeminiAgent
from tools.vectordb import VectorDB

class Orchestrator:
    def __init__(self, persist_dir: str, model_name: str):
        self.vdb = VectorDB(persist_dir, model_name)
        self.hunter = Hunter()
        self.reader = Reader(self.vdb)
        self.critic = Critic()
        self.hypo = Hypothesis()
        self.gemini = GeminiAgent()

    def run(self, query: str, max_results=10, since=None):
        hits = self.hunter.find(query, max_results=max_results, since=since)
        outputs = []
        for h in hits:
            try:
                read = self.reader.process_paper(h["title"], h["pdf_url"], h["entry_id"])
                
                # Use Gemini for enhanced analysis if available
                if self.gemini.enabled:
                    summary = self.gemini.generate_summary(read["sections"])
                    gemini_critique = self.gemini.generate_critique(summary, read["sections"])
                    gemini_ideas = self.gemini.generate_hypotheses(summary, str(gemini_critique))
                else:
                    summary = read["summary"]
                    gemini_critique = {}
                    gemini_ideas = []
                
                # Still run basic critic and hypothesis for comparison
                review = self.critic.review(read["sections"])
                ideas = self.hypo.propose(summary)
                
                # Combine results
                combined_review = {**review, **gemini_critique}
                combined_ideas = gemini_ideas if gemini_ideas else ideas
                
                outputs.append({
                    "title": h["title"],
                    "authors": h["authors"],
                    "published": h["published"],
                    "summary": summary,
                    "review": combined_review,
                    "ideas": combined_ideas,
                    "pdf_path": read["pdf_path"],
                    "gemini_enhanced": self.gemini.enabled,
                })
            except Exception as e:
                outputs.append({"title": h["title"], "error": str(e)})
        return outputs

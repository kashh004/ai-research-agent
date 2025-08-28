import json
import os
from typing import Dict, List
from tools.vectordb import VectorDB

class ChromaStore:
    def __init__(self, persist_dir: str, model_name: str):
        self.vdb = VectorDB(persist_dir, model_name)
        self.profiles_path = os.path.join("memory", "profiles.json")
    
    def load_profiles(self) -> Dict:
        if os.path.exists(self.profiles_path):
            with open(self.profiles_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_profiles(self, profiles: Dict):
        os.makedirs("memory", exist_ok=True)
        with open(self.profiles_path, 'w') as f:
            json.dump(profiles, f, indent=2)
    
    def add_paper(self, paper_id: str, content: str, metadata: Dict):
        self.vdb.add_doc(paper_id, content, metadata)
    
    def search_papers(self, query: str, k: int = 5):
        return self.vdb.search(query, k)
    
    def update_interests(self, new_interests: List[str]):
        profiles = self.load_profiles()
        current_interests = set(profiles.get("research_interests", []))
        current_interests.update(new_interests)
        profiles["research_interests"] = list(current_interests)
        self.save_profiles(profiles)

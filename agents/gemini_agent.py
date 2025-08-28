import google.generativeai as genai
from config import settings
from typing import Dict, List

class GeminiAgent:
    def __init__(self):
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.enabled = True
        else:
            self.enabled = False
    
    def generate_summary(self, sections: Dict[str, str]) -> str:
        """Generate enhanced summary using Gemini"""
        if not self.enabled:
            return sections.get("abstract", sections["full_text"][:1500])
        
        prompt = f"""
        Analyze this research paper and provide a concise, structured summary:
        
        Abstract: {sections.get('abstract', 'N/A')}
        Introduction: {sections.get('introduction', 'N/A')[:1000]}
        Method: {sections.get('method', 'N/A')[:1000]}
        Results: {sections.get('results', 'N/A')[:1000]}
        
        Provide a 3-4 sentence summary covering:
        1. Main contribution/problem addressed
        2. Key methodology or approach
        3. Primary results or findings
        4. Significance or impact
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback to simple summary
            return sections.get("abstract", sections["full_text"][:1500])
    
    def generate_critique(self, summary: str, sections: Dict[str, str]) -> Dict[str, str]:
        """Generate detailed critique using Gemini"""
        if not self.enabled:
            return {"critique": "Gemini API not configured - using basic heuristics"}
        
        prompt = f"""
        Critically analyze this research paper and identify potential issues:
        
        Summary: {summary}
        
        Full text excerpt: {sections.get('full_text', '')[:2000]}
        
        Evaluate the paper on these dimensions and provide specific concerns:
        1. Experimental design and methodology
        2. Statistical rigor and evidence quality
        3. Baseline comparisons and fairness
        4. Reproducibility and code availability
        5. Limitations and potential biases
        6. Novelty and significance of contributions
        
        Format as bullet points with specific actionable feedback.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {"gemini_critique": response.text.strip()}
        except Exception as e:
            return {"critique_error": f"Gemini API error: {str(e)}"}
    
    def generate_hypotheses(self, summary: str, critique: str) -> List[str]:
        """Generate research hypotheses and follow-up experiments"""
        if not self.enabled:
            return ["Gemini API not configured - using rule-based suggestions"]
        
        prompt = f"""
        Based on this paper analysis, propose 3-4 concrete follow-up research directions:
        
        Paper Summary: {summary}
        Critical Analysis: {critique}
        
        For each suggestion, provide:
        1. Specific research question or hypothesis
        2. Experimental approach or methodology
        3. Expected timeline and resources needed
        4. Potential impact if successful
        
        Focus on actionable, feasible experiments that could be completed within 3-6 months.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Split response into individual suggestions
            suggestions = [s.strip() for s in response.text.split('\n\n') if s.strip()]
            return suggestions[:4]  # Limit to 4 suggestions
        except Exception as e:
            return [f"Gemini API error: {str(e)}"]
    
    def expand_query(self, original_query: str) -> List[str]:
        """Generate related search terms to expand the original query"""
        if not self.enabled:
            return [original_query]
        
        prompt = f"""
        Given this research query: "{original_query}"
        
        Generate 3-4 related search terms or phrases that would help find relevant papers.
        Include:
        1. Synonyms and alternative terminology
        2. Related technical concepts
        3. Broader and narrower topic variations
        4. Cross-disciplinary connections
        
        Return only the search terms, one per line.
        """
        
        try:
            response = self.model.generate_content(prompt)
            terms = [term.strip() for term in response.text.split('\n') if term.strip()]
            return [original_query] + terms[:3]  # Include original + 3 expansions
        except Exception as e:
            return [original_query]

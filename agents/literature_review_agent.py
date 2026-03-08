from agents.base_agent import BaseAgent

class LiteratureReviewAgent(BaseAgent):
    def run(self, research_question: str, citations: str, notes: str) -> str:
        prompt = f"""
        You are a Literature Review Agent.

        Based on the research question, citations, and notes below,
        generate a structured literature review.

        Research Question:
        {research_question}

        Citations:
        {citations[:3000]}

        Notes:
        {notes[:3000]}

        Include:
        - key themes
        - major findings
        - comparison of prior work
        - research gaps
        - relevance to the research question

        Keep the tone academic and clear.
        """
        return self.call_ollama(prompt)
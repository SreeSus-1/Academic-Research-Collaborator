from agents.base_agent import BaseAgent

class DraftPolisherAgent(BaseAgent):
    def run(self, research_question: str, draft_text: str) -> str:
        prompt = f"""
        You are a Draft Polisher Agent for academic writing.

        Improve the following research draft for clarity, coherence,
        tone, and academic style.

        Research Question:
        {research_question}

        Draft:
        {draft_text[:4000]}

        Return:
        - a polished version
        - brief notes on key improvements made
        """
        return self.call_ollama(prompt)
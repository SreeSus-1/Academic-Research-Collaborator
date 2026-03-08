from agents.base_agent import BaseAgent

class HypothesisValidatorAgent(BaseAgent):
    def run(self, research_question: str, hypothesis: str, citations: str, notes: str) -> str:
        prompt = f"""
        You are a Hypothesis Validator Agent.

        Evaluate the hypothesis below using the provided research question,
        citations, and notes.

        Research Question:
        {research_question}

        Hypothesis:
        {hypothesis}

        Citations:
        {citations[:2500]}

        Notes:
        {notes[:2500]}

        Provide:
        - whether the hypothesis is reasonable
        - supporting evidence mentioned in the references
        - missing evidence or assumptions
        - limitations
        - suggestions to refine the hypothesis
        """
        return self.call_ollama(prompt)
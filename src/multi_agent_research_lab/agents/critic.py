"""Optional critic agent skeleton for bonus work."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings.

        TODO(student): Add fact-check, citation coverage, or hallucination checks.
        """

        from multi_agent_research_lab.services.llm_client import LLMClient
        from multi_agent_research_lab.core.schemas import AgentResult, AgentName

        if not state.final_answer:
            return state

        system_prompt = "You are a Critic Agent. Review the final answer against the research notes. Reply with 'PASS' if valid, or point out hallucinations."
        user_prompt = f"Notes: {state.research_notes}\n\nFinal Answer: {state.final_answer}"

        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        
        state.agent_results.append(AgentResult(
            agent=AgentName.CRITIC,
            content=response.content
        ))

        return state

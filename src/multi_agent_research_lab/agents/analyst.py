"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`.

        TODO(student): Extract key claims, compare viewpoints, and flag weak evidence.
        """

        from multi_agent_research_lab.services.llm_client import LLMClient
        from multi_agent_research_lab.core.schemas import AgentResult, AgentName

        system_prompt = "You are an Analyst Agent. Analyze the provided research notes. Extract key claims, compare viewpoints, and flag any weak evidence."
        user_prompt = f"Query: {state.request.query}\nResearch Notes:\n{state.research_notes}\n\nPlease generate analysis notes."

        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        state.analysis_notes = response.content

        state.agent_results.append(AgentResult(
            agent=AgentName.ANALYST,
            content=state.analysis_notes
        ))

        return state

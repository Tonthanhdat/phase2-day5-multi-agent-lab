"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`.

        TODO(student): Synthesize a clear response with citations or source references.
        """

        from multi_agent_research_lab.services.llm_client import LLMClient
        from multi_agent_research_lab.core.schemas import AgentResult, AgentName

        system_prompt = "You are a Writer Agent. Write a final comprehensive response based on the research notes and analysis notes. Include citations."
        user_prompt = f"""
        Query: {state.request.query}
        Audience: {state.request.audience}
        Research Notes: {state.research_notes}
        Analysis Notes: {state.analysis_notes}

        Please generate the final answer.
        """

        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        state.final_answer = response.content

        state.agent_results.append(AgentResult(
            agent=AgentName.WRITER,
            content=state.final_answer
        ))

        return state

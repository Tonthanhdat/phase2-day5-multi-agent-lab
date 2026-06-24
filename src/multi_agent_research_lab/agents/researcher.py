"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`.

        TODO(student): Implement search, source filtering, citation capture, and notes.
        """

        from multi_agent_research_lab.services.search_client import SearchClient
        from multi_agent_research_lab.services.llm_client import LLMClient
        from multi_agent_research_lab.core.schemas import AgentResult, AgentName

        searcher = SearchClient()
        sources = searcher.search(state.request.query, max_results=state.request.max_sources)
        state.sources.extend(sources)

        context = "\n".join([f"[{i+1}] {s.title}: {s.snippet}" for i, s in enumerate(sources)])
        
        system_prompt = "You are a Researcher Agent. Summarize the provided sources into concise research notes."
        user_prompt = f"Query: {state.request.query}\nSources:\n{context}\n\nPlease generate research notes."

        llm = LLMClient()
        response = llm.complete(system_prompt, user_prompt)
        state.research_notes = response.content

        state.agent_results.append(AgentResult(
            agent=AgentName.RESEARCHER,
            content=state.research_notes,
            metadata={"sources_count": len(sources)}
        ))

        return state

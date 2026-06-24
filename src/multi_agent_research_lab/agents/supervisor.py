"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route.

        TODO(student): Implement routing policy. Suggested steps:
        - Inspect request, current notes, and missing fields.
        - Choose one of: researcher, analyst, writer, done.
        - Enforce max iterations and failure fallback.
        """

        import os
        from multi_agent_research_lab.services.llm_client import LLMClient

        max_iter = int(os.getenv("MAX_ITERATIONS", "6"))
        if state.iteration >= max_iter:
            state.record_route("done")
            return state

        # Use deterministic routing for 1.5B model instead of LLM inference
        if not state.research_notes:
            next_route = "researcher"
        elif not state.analysis_notes:
            next_route = "analyst"
        elif not state.final_answer:
            next_route = "writer"
        else:
            next_route = "done"

        state.record_route(next_route)
        return state

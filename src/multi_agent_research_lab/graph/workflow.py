"""LangGraph workflow skeleton."""

from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> object:
        """Create a LangGraph graph.

        TODO(student): Implement nodes, edges, conditional routing, and stop condition.
        Suggested nodes: supervisor, researcher, analyst, writer, optional critic.
        """

        from langgraph.graph import StateGraph, END
        from multi_agent_research_lab.agents.supervisor import SupervisorAgent
        from multi_agent_research_lab.agents.researcher import ResearcherAgent
        from multi_agent_research_lab.agents.analyst import AnalystAgent
        from multi_agent_research_lab.agents.writer import WriterAgent
        from multi_agent_research_lab.agents.critic import CriticAgent

        builder = StateGraph(ResearchState)

        builder.add_node("supervisor", SupervisorAgent().run)
        builder.add_node("researcher", ResearcherAgent().run)
        builder.add_node("analyst", AnalystAgent().run)
        builder.add_node("writer", WriterAgent().run)
        builder.add_node("critic", CriticAgent().run)

        builder.set_entry_point("supervisor")

        def route_next(state: ResearchState) -> str:
            if not state.route_history:
                return END
            last = state.route_history[-1]
            if last == "done":
                return END
            return last

        builder.add_conditional_edges(
            "supervisor",
            route_next,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                END: END
            }
        )

        builder.add_edge("researcher", "supervisor")
        builder.add_edge("analyst", "supervisor")
        builder.add_edge("writer", "critic")
        builder.add_edge("critic", "supervisor")

        self.graph = builder.compile()
        return self.graph

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state.

        TODO(student): Compile graph, invoke it, and convert result back to ResearchState.
        """

        if not hasattr(self, "graph"):
            self.build()
        result = self.graph.invoke(state)
        if isinstance(result, dict):
            return ResearchState(**result)
        return result

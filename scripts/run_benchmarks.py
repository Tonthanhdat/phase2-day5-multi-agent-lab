import os
import json
from multi_agent_research_lab.cli import _init
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient

def run_baseline(query: str) -> ResearchState:
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    searcher = SearchClient()
    sources = searcher.search(query)
    context = "\n".join([f"[{i+1}] {s.title}: {s.snippet}" for i, s in enumerate(sources)])
    sys_p = "You are a helpful AI assistant. Answer the user's query using the provided context."
    user_p = f"Query: {query}\nContext:\n{context}"
    llm = LLMClient()
    res = llm.complete(sys_p, user_p)
    state.final_answer = res.content
    state.sources = sources
    return state

def run_multi_agent(query: str) -> ResearchState:
    request = ResearchQuery(query=query)
    state = ResearchState(request=request)
    workflow = MultiAgentWorkflow()
    return workflow.run(state)

if __name__ == "__main__":
    _init()
    query = "Research GraphRAG state-of-the-art and write a 500-word summary"
    
    print("Running baseline...")
    base_state, base_metrics = run_benchmark("Baseline", query, run_baseline)
    
    print("Running multi-agent...")
    ma_state, ma_metrics = run_benchmark("Multi-Agent", query, run_multi_agent)
    
    report_content = render_markdown_report([base_metrics, ma_metrics])
    report_content += "\n## Outputs\n"
    report_content += "### Baseline Output\n"
    report_content += (base_state.final_answer or "No baseline answer") + "\n\n"
    report_content += "### Multi-Agent Output\n"
    report_content += (ma_state.final_answer or "No multi-agent answer") + "\n\n"
    
    report_content += "### Agent Outputs (Trace)\n"
    for result in ma_state.agent_results:
        report_content += f"#### {result.agent}\n"
        report_content += f"{result.content}\n\n"
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/benchmark_report.md", "w") as f:
        f.write(report_content)
        
    print("Benchmark saved to reports/benchmark_report.md")

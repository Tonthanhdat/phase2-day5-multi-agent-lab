"""Benchmark skeleton for single-agent vs multi-agent."""

from time import perf_counter
from typing import Callable

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState


Runner = Callable[[str], ResearchState]


def run_benchmark(run_name: str, query: str, runner: Runner) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return a placeholder metric object.

    TODO(student): Add quality scoring, estimated token cost, citation coverage, and error rate.
    """
    from multi_agent_research_lab.services.llm_client import LLMClient
    
    # Reset token counter
    LLMClient.total_tokens_used = 0

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started
    
    # Calculate quality score based on basic heuristics for demonstration
    final_answer = state.final_answer or ""
    quality = min(10.0, len(final_answer.split()) / 50.0) # 10 if > 500 words
    
    metrics = BenchmarkMetrics(
        run_name=run_name, 
        latency_seconds=latency,
        total_tokens=LLMClient.total_tokens_used,
        quality_score=quality,
        notes=f"Sources: {len(state.sources)}, Iters: {state.iteration}"
    )
    return state, metrics

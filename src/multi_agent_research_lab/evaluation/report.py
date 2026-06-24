"""Benchmark report rendering."""

from multi_agent_research_lab.core.schemas import BenchmarkMetrics


def render_markdown_report(metrics: list[BenchmarkMetrics]) -> str:
    """Render benchmark metrics to markdown.

    TODO(student): Add richer analysis, examples, screenshots, and trace links.
    """

    lines = ["# Benchmark Report", "", "| Run | Latency (s) | Tokens | Quality | Notes |", "|---|---:|---:|---:|---|"]
    for item in metrics:
        tokens = "" if item.total_tokens is None else f"{item.total_tokens}"
        quality = "" if item.quality_score is None else f"{item.quality_score:.1f}"
        lines.append(f"| {item.run_name} | {item.latency_seconds:.2f} | {tokens} | {quality} | {item.notes} |")
    return "\n".join(lines) + "\n"

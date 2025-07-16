from pydantic import BaseModel

from agents import Agent

# Writer agent compiles the search results into a concise markdown report.
# Focus on summarizing the most important headlines from the past week and list the sources.
WRITER_PROMPT = (
    "You are a financial news analyst. You will receive the original query and a set of search summaries. "
    "Compose a short markdown report highlighting the most significant headlines from the last seven days. "
    "Include a brief executive summary at the top and mention the source for each headline if possible."
)


class FinancialReportData(BaseModel):
    short_summary: str
    """A short 2‑3 sentence executive summary."""

    markdown_report: str
    """The full markdown report."""

    follow_up_questions: list[str]
    """Suggested follow‑up questions for further research."""


# Note: We will attach handoffs to specialist analyst agents at runtime in the manager.
# This shows how an agent can use handoffs to delegate to specialized subagents.
writer_agent = Agent(
    name="FinancialWriterAgent",
    instructions=WRITER_PROMPT,
    model="gpt-4.5-preview-2025-02-27",
    output_type=FinancialReportData,
)

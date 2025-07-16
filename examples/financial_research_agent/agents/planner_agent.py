from pydantic import BaseModel

from agents import Agent

# Generate a plan of searches to gather relevant news headlines.
# Focus on stories from the last 7 days about the target company.
PROMPT = (
    "You are a research planner tasked with surfacing important news. "
    "Given a request, produce concise search queries that will locate the most "
    "notable headlines about the company from the past week (the past 7 days). Only suggest terms "
    "that are likely to reveal significant events or announcements. Output between 5 and 10 queries."
)


class FinancialSearchItem(BaseModel):
    reason: str
    """Your reasoning for why this search is relevant."""

    query: str
    """The search term to feed into a web (or file) search."""


class FinancialSearchPlan(BaseModel):
    searches: list[FinancialSearchItem]
    """A list of searches to perform."""


planner_agent = Agent(
    name="FinancialPlannerAgent",
    instructions=PROMPT,
    model="o3-mini",
    output_type=FinancialSearchPlan,
)

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

# Given a search term, use web search to pull back a concise summary.
# Limit the results to news from the last 7 days and include the source name if available.
INSTRUCTIONS = (
    "You are a research assistant summarizing recent financial news. "
    "Given a search term, search the web for articles published in the past week "
    "and produce a short summary (max 300 words) mentioning the source for each key point."
)

search_agent = Agent(
    name="FinancialSearchAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
)

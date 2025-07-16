import asyncio
import os

PORTFOLIO_COMPANIES = [
    "Apple Inc.",
    "Microsoft Corporation",
]

EMAIL_RECIPIENTS = ["team@example.com"]

# The "From" address for the report emails.
EMAIL_SENDER = "analyst@example.com"

from .manager import FinancialResearchManager


# Entrypoint for the financial bot example.
# Run this as `python -m examples.financial_research_agent.main` to generate
# research reports for the companies listed above and email them to the
# configured recipients.
async def main() -> None:
    # Use a preset SMTP username so the email sender agent has a from address.
    os.environ.setdefault("SMTP_USERNAME", EMAIL_SENDER)
    mgr = FinancialResearchManager()
    for company in PORTFOLIO_COMPANIES:
        query = f"Summarize the most important news about {company} from the last 7 days."
        for recipient in EMAIL_RECIPIENTS:
            await mgr.run(query, recipient=recipient)


if __name__ == "__main__":
    asyncio.run(main())

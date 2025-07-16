from __future__ import annotations

import asyncio
import time
from collections.abc import Sequence

from rich.console import Console

from agents import Runner, RunResult, custom_span, gen_trace_id, trace
from .agents.planner_agent import FinancialSearchItem, FinancialSearchPlan, planner_agent
from .agents.search_agent import search_agent
from .agents.verifier_agent import VerificationResult, verifier_agent
from .agents.writer_agent import FinancialReportData, writer_agent
from .printer import Printer
from .agents.send_email_agent import EmailParams, send_email_agent

class FinancialResearchManager:
    """
    Orchestrates the full flow: planning, searching, sub‑analysis, writing, and verification.
    """

    def __init__(self) -> None:
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, query: str, recipient: str | None = None) -> None:
        trace_id = gen_trace_id()
        with trace("Financial research trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )
            self.printer.update_item("start", "Starting financial research...", is_done=True)
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            if not search_results:
                self.printer.update_item("no_results", "No relevant news found", is_done=True)
                self.printer.end()
                return
            report = await self._write_report(query, search_results)
            verification = await self._verify_report(report)
            if recipient is not None:
                await self._send_email(recipient, f"Research report: {query}", report.markdown_report)

            final_report = f"Report summary\n\n{report.short_summary}"
            self.printer.update_item("final_report", final_report, is_done=True)

            self.printer.end()

        # Print to stdout
        print("\n\n=====REPORT=====\n\n")
        print(f"Report:\n{report.markdown_report}")
        print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
        print("\n".join(report.follow_up_questions))
        print("\n\n=====VERIFICATION=====\n\n")
        print(verification)

    async def _plan_searches(self, query: str) -> FinancialSearchPlan:
        self.printer.update_item("planning", "Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        self.printer.update_item(
            "planning",
            f"Will perform {len(result.final_output.searches)} searches",
            is_done=True,
        )

    async def _perform_searches(self, search_plan: FinancialSearchPlan) -> Sequence[str]:
        with custom_span("Search the web"):
            self.printer.update_item("searching", "Searching...")
            tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
            results: list[str] = []
            num_completed = 0
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
                self.printer.update_item(
                    "searching", f"Searching... {num_completed}/{len(tasks)} completed"
                )
            self.printer.mark_item_done("searching")
            return results

    async def _search(self, item: FinancialSearchItem) -> str | None:
        input_data = f"Search term: {item.query}\nReason: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_data)
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: Sequence[str]) -> FinancialReportData:
        # For this news-focused workflow we call the writer directly without sub-analyst tools.
        writer_with_tools = writer_agent
        self.printer.update_item("writing", "Thinking about report...")
        input_data = f"Original query: {query}\nSummarized search results: {search_results}"
        result = Runner.run_streamed(writer_with_tools, input_data)
        update_messages = [
            "Planning report structure...",
            "Writing sections...",
            "Finalizing report...",
        ]
        last_update = time.time()
        next_message = 0
        async for _ in result.stream_events():
            if time.time() - last_update > 5 and next_message < len(update_messages):
                self.printer.update_item("writing", update_messages[next_message])
                next_message += 1
                last_update = time.time()
        self.printer.mark_item_done("writing")
        return result.final_output_as(FinancialReportData)

    async def _verify_report(self, report: FinancialReportData) -> VerificationResult:
        self.printer.update_item("verifying", "Verifying report...")
        result = await Runner.run(verifier_agent, report.markdown_report)
        self.printer.mark_item_done("verifying")
        return result.final_output_as(VerificationResult)

    async def _send_email(self, recipient: str, subject: str, body: str) -> None:
        self.printer.update_item("email", "Sending email...")
        params = EmailParams(recipient=recipient, subject=subject, body=body)
        await Runner.run(send_email_agent, params)
        self.printer.mark_item_done("email")

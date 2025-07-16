# Financial Research Agent Example

This example demonstrates how to build a weekly news digest for a set of portfolio companies using the Agents SDK.
The flow is:

1. **Planning**: The planner agent creates search queries to surface the most important headlines from the past week.
2. **Search**: The search agent gathers recent news snippets for each query.
3. **Writing**: The writer agent compiles a short markdown summary and lists the news sources.
4. **Verification**: A verifier agent checks the output for consistency.

You can run the example with:

```bash
python -m examples.financial_research_agent.main
```

The script generates reports for the companies listed in `main.py` and emails
them to the configured recipients.
Edit the `PORTFOLIO_COMPANIES`, `EMAIL_RECIPIENTS`, and `EMAIL_SENDER`
constants in that file to customize the run.

### Starter prompt

The writer agent is seeded with instructions similar to:

```
You are a financial news analyst. You will be provided with the original query
and recent search summaries. Produce a concise markdown report summarizing the
most relevant headlines from the past week and list the sources.
```

You can tweak these prompts and sub‑agents to suit your own data sources and preferred report structure.

This example already loops over a short list of portfolio companies and emails
a weekly digest. Use `send_email_agent` (see `agents/send_email_agent.py`) if
you want to integrate with your own SMTP settings. The manager exposes a
`recipient` argument on `run()` so you can forward the final markdown to any
address.
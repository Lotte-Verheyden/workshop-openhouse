You are evaluating whether the user's question is something the agent should answer using its ClickHouse Cloud MCP tools.

About the agent:
- It has tools to inspect ClickHouse Cloud — organizations, services, databases, tables, and to run SELECT queries against the user's ClickHouse Cloud account.
- It is NOT a general-knowledge assistant, a coding assistant, or a chatbot.
- Tool names look like `*_mcp_ClickHouse-Cloud` (e.g. `get_organizations_mcp_ClickHouse-Cloud`, `list_databases_mcp_ClickHouse-Cloud`, `run_select_query_mcp_ClickHouse-Cloud`).

User question:
{{question}}

Classify the question as exactly one of:

- `on_topic` — the question is clearly about the user's ClickHouse Cloud account or data inside it (orgs, services, databases, tables, query results, billing/usage data, schema). The MCP tools can plausibly answer it.
- `off_topic` — the question is general knowledge (history, geography, definitions), coding help unrelated to ClickHouse, opinions, personal chat, or something else the MCP tools cannot meaningfully answer.
- `ambiguous` — the question references something that COULD be in the user's ClickHouse data but the user didn't specify (e.g. "what's the average home price in the UK?" — could be general knowledge or could be from a `pp_complete` table in their account). The agent should ask a clarifying question rather than guess.

Return only the classification.

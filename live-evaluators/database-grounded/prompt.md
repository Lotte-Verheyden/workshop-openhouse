You are evaluating whether an AI agent's response is grounded in a real database query or fabricated from background knowledge.

The agent has access to ClickHouse Cloud MCP tools. Tool calls show up in the conversation as assistant messages with a `tool_calls` array and tool names like `run_select_query_mcp_ClickHouse-Cloud`, `list_tables_mcp_ClickHouse-Cloud`, `list_databases_mcp_ClickHouse-Cloud`, `get_organizations_mcp_ClickHouse-Cloud`. The tool result follows as a message whose `role` is the tool name.

Conversation (messages array, may include `tool_calls` and tool result messages):
{{conversation}}

Find the final user question and the assistant's final response. Use earlier messages only to confirm whether a relevant tool call happened during this trace.

Classify the assistant's final response as exactly one of:

- `grounded` — response contains specific factual data (numbers, statistics, table rows, account-specific details) AND a ClickHouse MCP tool was called in this trace whose results plausibly support the claims.
- `no_data_required` — response makes no specific factual claims that would require a database lookup (general explanation, clarification, plan, refusal, generic guidance).
- `potentially_hallucinated` — response contains specific factual claims but no ClickHouse MCP tool was called in this trace, OR a tool was called but its results do not support the specific claims.

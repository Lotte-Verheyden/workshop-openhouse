# `database-grounded` — Langfuse setup

Detects whether the agent answered using a real ClickHouse Cloud MCP tool call (grounded) or fabricated specifics from background knowledge (hallucinated).

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ❌ (requires live DB access during the run)

## Score config

Categorical with three labels:

| Value | Label |
|---|---|
| 2 | `grounded` |
| 1 | `no_data_required` |
| 0 | `potentially_hallucinated` |

## Steps in the Langfuse UI

1. **Settings → LLM Connections** — add an LLM API key if one isn't configured yet (any model with structured-output support).
2. **Evaluators → + Set up evaluator → Custom evaluator**
3. **Name:** `database-grounded`
4. **Score type:** Categorical → select existing score config `database-grounded`
5. **Prompt:** paste from [`prompt.md`](./prompt.md)
6. **Target:** Live Traces
7. **Filter:** `Trace name = AgentRun`
8. **Sampling:** 100%
9. **Backfill:** on (if you want to score existing traces)
10. **Variable mapping:**

| Variable | Source | Field |
|---|---|---|
| `conversation` | Trace | `output` |

11. **Reasoning prompt (optional):**

```
In 1-2 sentences, state whether a ClickHouse MCP tool was called in this trace and whether the assistant's final response makes specific factual claims that depend on database results.
```

## Why trace `output`

The trace `output` field contains the full LangGraph message thread including any `tool_calls` and tool result messages. The judge can see in one pass whether a `*_mcp_ClickHouse-Cloud` tool was actually invoked, so a single variable is enough.

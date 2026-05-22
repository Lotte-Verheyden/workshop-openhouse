# `on-topic` — Langfuse setup

Judges whether the user's question is something the ClickHouse MCP agent should answer at all, or whether it should defer. Catches scope drift.

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ✅ (only needs the question and the response, both available in any experiment trace)

## Score config

Categorical with three labels:

| Value | Label |
|---|---|
| 2 | `on_topic` |
| 1 | `ambiguous` |
| 0 | `off_topic` |

## Steps in the Langfuse UI

1. **Settings → LLM Connections** — add an LLM API key if one isn't configured yet.
2. **Evaluators → + Set up evaluator → Custom evaluator**
3. **Name:** `on-topic`
4. **Score type:** Categorical → select existing score config `on-topic`
5. **Prompt:** paste from [`prompt.md`](./prompt.md)
6. **Target:** Live Traces (for production monitoring) AND attach to experiment runs (for offline iteration)
7. **Filter (live):** `Trace name = AgentRun`
8. **Sampling:** 100%
9. **Backfill:** on (if you want to score existing traces)
10. **Variable mapping:**

| Variable | Source | Field |
|---|---|---|
| `conversation` | Trace | `output` |

11. **Reasoning prompt (optional):**

```
In one sentence, identify the final user question and explain whether the ClickHouse Cloud MCP tools can plausibly answer it.
```

## Pairing with `database-grounded`

| `on-topic` | `database-grounded` | meaning |
|---|---|---|
| `on_topic` | `grounded` | ✅ ideal — agent did its job |
| `on_topic` | `potentially_hallucinated` | 🚨 real bug — should have queried DB |
| `on_topic` | `no_data_required` | usually fine — clarifying, planning |
| `off_topic` | `no_data_required` | ✅ correct refusal |
| `off_topic` | `grounded` | weird — agent over-eager to query |
| `ambiguous` | any | agent should have asked to clarify |

## Use in experiments

`on-topic` is the one evaluator that travels cleanly from live → offline. Attach it to any experiment run scoring a dataset of off-topic / ambiguous questions to measure scope adherence across prompt versions.

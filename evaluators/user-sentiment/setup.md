# `user-sentiment` — Langfuse setup

Reads the user's messages and labels their emotional state. Catches frustration and confusion that wouldn't show up in correctness metrics.

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ❌ (no real user means no sentiment signal)

## Score config

Categorical with three labels:

| Value | Label |
|---|---|
| 2 | `positive` |
| 1 | `neutral` |
| 0 | `negative` |

## Steps in the Langfuse UI

1. **Settings → LLM Connections** — add an LLM API key if one isn't configured yet.
2. **Evaluators → + Set up evaluator → Custom evaluator**
3. **Name:** `user-sentiment`
4. **Score type:** Categorical → select existing score config `user-sentiment`
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
In one sentence, point to the strongest sentiment signal in the user's messages.
```

## Note on multi-turn traces

The trace `output` contains the full session-to-date message thread. Every `AgentRun` in a session re-scores sentiment across all earlier turns — usually what you want (sentiment trend per session). To score only the latest user turn, change the prompt to "judge only the FINAL user message."

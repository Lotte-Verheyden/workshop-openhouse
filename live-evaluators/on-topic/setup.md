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

---

## Visual walkthrough

> Same 8 steps as [`database-grounded/setup.md`](../database-grounded/setup.md). Only the name, prompt, and category labels change. Walkthrough below shows just the screens you'll see for this one.

### 1. Open LLM-as-a-Judge → + Set up evaluator

LLM connection is already configured from the `database-grounded` setup, so no default-model warning this time.

![Set up evaluator](../../images/on-topic-01-set-up-evaluator.png)

### 2. Create a new custom evaluator

`database-grounded` shows up in the list now — ignore it and click **+ Create Custom Evaluator**.

![Select evaluator → Create Custom](../../images/on-topic-02-select-evaluator.png)

### 3. Name and prompt

- **Name:** `on-topic`
- **Prompt:** paste from [`prompt.md`](./prompt.md)

![Create evaluator form](../../images/on-topic-03-create-form.png)

### 4. Score type and categories

- **Score type:** Categorical
- **Categories:** `on_topic`, `ambiguous`, `off_topic`
- **Score reasoning prompt** (optional):

  ```
  In one sentence, identify the final user question and explain whether the ClickHouse Cloud MCP tools can plausibly answer it.
  ```

![Categories: on_topic / ambiguous / off_topic](../../images/on-topic-04-categories.png)

### 5. Run on Traces

**Traces (Legacy)**, same as before.

![Run on Traces](../../images/on-topic-05-run-on-traces.png)

### 6. Filter, sampling, delay

- **Evaluate:** check both **New traces** and **Existing traces** (backfill the 17 traces already in the project)
- **Filter:** `Name = any of → AgentRun`
- **Sampling:** 100%
- **Delay:** 30s (default — gives ingestion time to finish before the judge reads the trace)

![Filter and sampling](../../images/on-topic-06-filter-sampling.png)

### 7. Variable mapping

| Variable | Source | Field |
|---|---|---|
| `conversation` | Trace | `output` |

Same as `database-grounded` — the trace `output` contains the full message thread, which is all the judge needs.

![Variable mapping](../../images/on-topic-07-variable-mapping.png)

---

## Also attach to experiments

`on-topic` is the only one of the three that travels cleanly from live → offline. When you run a dataset experiment (e.g. scope-stress questions against a candidate system prompt), attach this evaluator to the experiment run so each generated output gets scored automatically.

## Pairing with `database-grounded`

| `on-topic` | `database-grounded` | meaning |
|---|---|---|
| `on_topic` | `grounded` | ✅ ideal — agent did its job |
| `on_topic` | `potentially_hallucinated` | 🚨 real bug — should have queried DB |
| `on_topic` | `no_data_required` | usually fine — clarifying, planning |
| `off_topic` | `no_data_required` | ✅ correct refusal |
| `off_topic` | `grounded` | weird — agent over-eager to query |
| `ambiguous` | any | agent should have asked to clarify |

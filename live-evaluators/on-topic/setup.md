# `on-topic` — Langfuse setup

Judges whether the user's question is something the ClickHouse MCP agent should answer at all, or whether it should defer. Catches scope drift.

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ✅ (only needs the question — map `{{question}}` to the experiment item's `input`)

## Visual walkthrough

> This is the canonical **LLM-as-a-judge** walkthrough for the repo. `user-sentiment` follows the same flow — only the name, prompt, and category labels change. (`database-grounded` is a [code evaluator](../database-grounded/) — a different setup.) This evaluator maps the root **`AgentRun` observation's `input`** — just the user's question.

### 1. Open Evaluators → + Set up evaluator

Sidebar → **Evaluation → Evaluators → + Set up evaluator**, then under **Create from scratch** pick **LLM as a judge evaluator**.

![Set up evaluator](../../images/on-topic-01-set-up-evaluator.png)

### 2. Configure a default judge model (one-time)

If no default model is set yet, the wizard asks you to add one. Click **Set up** and add an LLM connection (any model with structured-output support — `gpt-4o-mini` and `claude-haiku-4-5` are cheap defaults). Later LLM evaluators reuse this connection.

![Default model warning](../../images/03-default-model.png)

### 3. Create a custom evaluator

Click **+ Create Custom Evaluator**.

![Select evaluator → Create Custom](../../images/on-topic-02-select-evaluator.png)

### 4. Name and prompt

- **Name:** `on-topic`
- **Prompt:** paste from [`prompt.md`](./prompt.md)

![Create evaluator form](../../images/on-topic-03-create-form.png)

### 5. Score type and categories

- **Score type:** Categorical
- **Categories:** `on_topic`, `ambiguous`, `off_topic`
- **Score reasoning prompt** (optional):

  ```
  In one sentence, identify the user question and explain whether the ClickHouse Cloud MCP tools can plausibly answer it.
  ```

![Categories: on_topic / ambiguous / off_topic](../../images/on-topic-04-categories.png)

### 6. Run on Observations

Pick **Observations**.

![Run on Observations](../../images/on-topic-05-run-on-traces.png)

### 7. Filter, sampling, delay

- **Filter:** `Name = any of → AgentRun` — this matches the root **`AgentRun` observation** (the agent run's overall request/response), whose `input` is the user's question.
- **Sampling:** 100%
- **Delay:** 30s (default — gives ingestion time to finish before the judge reads the observation)

![Filter and sampling](../../images/on-topic-06-filter-sampling.png)

> The filter screenshot above still shows the older trace-level view (the `New/Existing traces` toggles and trace preview); the filter value `Name = AgentRun` is unchanged and is what matters. Note that only new-format traces have an `AgentRun` observation, so backfilling older traces won't score them.

### 8. Variable mapping

This evaluator only judges the question, so map the single `{{question}}` variable to the `AgentRun` observation's `input`:

| Variable | Source | Field |
|---|---|---|
| `question` | Observation | `input` |

![Variable mapping](../../images/on-topic-07-variable-mapping.png)

---

## Also attach to experiments

`on-topic` travels cleanly from live → offline. When you run a dataset experiment (e.g. scope-stress questions against a candidate system prompt), attach this evaluator to the experiment run so each generated output gets scored automatically.

## Pairing with `database-grounded`

The [`database-grounded`](../database-grounded/) code evaluator scores `grounded` / `metadata_only` / `no_tool_call`. Crossed with `on-topic`:

| `on-topic` | `database-grounded` | meaning |
|---|---|---|
| `on_topic` | `grounded` | ✅ ideal — agent queried and answered |
| `on_topic` | `no_tool_call` | 🚨 real bug — should have queried the DB but answered without it |
| `on_topic` | `metadata_only` | inspected schema/listings but ran no data query — often an incomplete answer |
| `off_topic` | `no_tool_call` | ✅ correct refusal — didn't query for an off-topic question |
| `off_topic` | `grounded` | weird — agent queried for an off-topic question |
| `ambiguous` | any | agent should have asked to clarify |

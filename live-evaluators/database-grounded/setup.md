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

---

## Visual walkthrough

> The flow below is the canonical setup for this repo. `user-sentiment` and `on-topic` follow the exact same steps — only the **name**, the **prompt** (paste from each folder's `prompt.md`), and the **category labels** change. The pasteable values for each are in the respective `setup.md`.

### 1. Open LLM-as-a-Judge

Sidebar → **Evaluation → LLM-as-a-Judge**.

![Sidebar: LLM-as-a-Judge](../../images/01-sidebar-llm-as-a-judge.png)

### 2. Set up evaluator

Click **+ Set up evaluator** (top right).

![Evaluators page](../../images/02-set-up-evaluator.png)

### 3. Configure a default judge model (one-time)

If no default model is set, the wizard blocks you here. Click **Set up** and add an LLM connection (any model with structured-output support — `gpt-4o-mini` and `claude-haiku-4-5` are cheap defaults).

![Default model warning](../../images/03-default-model.png)

### 4. Name and prompt

- **Name:** `database-grounded`
- **Prompt:** paste from [`prompt.md`](./prompt.md)

![Create evaluator form](../../images/04-create-evaluator-form.png)

### 5. Score type and categories

- **Score type:** Categorical
- **Categories** (exact labels, in this order is fine):
  - `potentially_hallucinated`
  - `no_data_required`
  - `grounded`
- **Allow multiple matches:** off
- **Score reasoning prompt:** leave default, or use:

  ```
  In 1-2 sentences, state whether a ClickHouse MCP tool was called in this trace and whether the assistant's final response makes specific factual claims that depend on database results.
  ```

- **Category selection prompt:** leave default

![Score type and categories](../../images/05-score-type-categories.png)

### 6. Run on Traces

Pick **Traces (Legacy)** as the target. Observation evaluators are the newer pattern, but the trace-level `output` already contains the full message thread we need, so Traces is simpler for this workshop.

![Run on Traces](../../images/06-run-on-traces.png)

### 7. Filter to `AgentRun`

- Filter: **Name = any of → `AgentRun`**

The preview confirms which traces will match — this skips the `TitleRun` traces that only generate session titles.

![Filter to AgentRun](../../images/07-filter-trace-name.png)

Optional: enable backfill if you want existing traces scored too. Sampling 100% is fine for a workshop project; lower it for production cost control.

### 8. Map variables

Map the prompt's `{{conversation}}` variable to the trace's **output** field. The trace output contains the full LangGraph message thread including any `tool_calls`, so this one mapping gives the judge everything it needs.

| Variable | Source | Field |
|---|---|---|
| `conversation` | Trace | `output` |

![Variable mapping](../../images/08-variable-mapping.png)

Save → the evaluator runs on every new `AgentRun` trace.

---

## Why trace `output`

The trace `output` field contains the full LangGraph message thread including any `tool_calls` and tool result messages. The judge can see in one pass whether a `*_mcp_ClickHouse-Cloud` tool was actually invoked, so a single variable is enough.

# `database-grounded` — Langfuse setup

Detects whether the agent answered using a real ClickHouse Cloud MCP tool call (grounded) or fabricated specifics from background knowledge (hallucinated).

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ❌ (requires live DB access during the run)

## Visual walkthrough

> The flow below is the canonical setup for this repo. `user-sentiment` and `on-topic` follow the same steps — they differ only in the **name**, the **prompt** (paste from each folder's `prompt.md`), the **category labels**, and the **target observation** (`user-sentiment`/`on-topic` map the root `AgentRun` observation's `input`; this one maps the `LangGraph` span's `output`). The per-evaluator deltas are in the respective `setup.md`.

### 1. Open Evaluators

Sidebar → **Evaluation → Evaluators**. (This section was previously labelled "LLM-as-a-Judge".)

![Sidebar: Evaluators](../../images/01-sidebar-llm-as-a-judge.png)

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

### 6. Run on Observations

Pick **Observations** as the target (Traces is now marked *Legacy*). We evaluate observations because, on the current LibreChat trace structure, the full message thread lives on a specific observation — not on the trace `output`, which is now just the assistant's final answer string. Leave **Run on live incoming observations** on.

![Run on Observations](../../images/06-run-on-traces.png)

### 7. Filter to the `LangGraph` span

- Filter: **Name = any of → `LangGraph`**

Each `AgentRun` trace contains exactly one `LangGraph` span, and its `output` is the complete message thread (assistant messages with `tool_calls`, plus tool-result messages). The preview confirms the match. Because only `AgentRun` traces have a `LangGraph` span, this also skips the `TitleRun` traces that just generate session titles — one score per trace, same as before.

![Filter to LangGraph](../../images/07-filter-trace-name.png)

Sampling 100% is fine for a workshop project; lower it for production cost control.

### 8. Map variables

Map the prompt's `{{conversation}}` variable to the observation's **output** field. The `LangGraph` span's `output` is the full message thread including any `tool_calls`, so this one mapping gives the judge everything it needs.

| Variable | Source | Field |
|---|---|---|
| `conversation` | Observation | `output` |

![Variable mapping](../../images/08-variable-mapping.png)

Save → the evaluator runs on the `LangGraph` span of every new `AgentRun` trace.

---

## Why the `LangGraph` span `output`

On the current (OTel SDK v5) trace structure, the trace-level `input`/`output` are plain strings — just the user's question and the assistant's final answer — and each tool call is its own `TOOL` observation. An LLM-as-a-Judge maps variables from a **single** object and can't reach sibling observations, so a plain-string mapping would leave the judge blind to whether a tool ran.

The `LangGraph` span is the one observation that still carries the whole thread in its `output`: assistant messages with a `tool_calls` array, and tool-result messages whose `role` is the tool name (e.g. `run_select_query_mcp_ClickHouse-Cloud`). Mapping that one field lets the judge see in one pass whether a `*_mcp_ClickHouse-Cloud` tool was actually invoked.

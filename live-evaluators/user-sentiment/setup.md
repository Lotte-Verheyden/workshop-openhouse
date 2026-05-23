# `user-sentiment` — Langfuse setup

Reads the user's messages and labels their emotional state. Catches frustration and confusion that wouldn't show up in correctness metrics.

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ❌ (no real user means no sentiment signal)

## Visual walkthrough

> Same 8 steps as [`database-grounded/setup.md`](../database-grounded/setup.md). Only the name, prompt, and category labels change. Walkthrough below shows just the screens you'll see for this one.

### 1. Open LLM-as-a-Judge → + Set up evaluator

![Set up evaluator](../../images/user-sentiment-01-set-up-evaluator.png)

### 2. Create a new custom evaluator

`database-grounded` is in the list now — click **+ Create Custom Evaluator** to add this one.

![Select evaluator → Create Custom](../../images/user-sentiment-02-select-evaluator.png)

### 3. Name and prompt

- **Name:** `user-sentiment`
- **Prompt:** paste from [`prompt.md`](./prompt.md)

![Create evaluator form](../../images/user-sentiment-03-create-form.png)

### 4. Score type and categories

- **Score type:** Categorical
- **Categories:** `positive`, `neutral`, `negative`
- **Score reasoning prompt** (optional):

  ```
  In one sentence, point to the strongest sentiment signal in the user's messages.
  ```

![Categories: positive / neutral / negative](../../images/user-sentiment-04-categories.png)

### 5. Skip Experiments — pick Traces

The wizard offers **Experiments** as a target. **Skip it for this evaluator.** An experiment has no real user reacting — there's no sentiment to score.

![Experiments tab — don't pick this](../../images/user-sentiment-05-experiments-tab.png)

### 6. Run on Traces

**Traces (Legacy)**, **New traces** + **Existing traces** both checked.

![Run on Traces](../../images/user-sentiment-06-run-on-traces.png)

### 7. Filter, sampling, delay

- **Filter:** `Name = any of → AgentRun`
- **Sampling:** 100%
- **Delay:** 30s (default)

![Filter and sampling](../../images/user-sentiment-07-filter-sampling.png)

### 8. Variable mapping

| Variable | Source | Field |
|---|---|---|
| `conversation` | Trace | `output` |

The Langfuse UI also shows a live preview of the prompt with one matched trace's data filled in — useful sanity check before saving.

![Variable mapping with prompt preview](../../images/user-sentiment-08-variable-mapping.png)

---

## Note on multi-turn traces

The trace `output` contains the full session-to-date message thread. Every `AgentRun` in a session re-scores sentiment across all earlier turns — usually what you want (sentiment trend per session). To score only the latest user turn, change the prompt to "judge only the FINAL user message."

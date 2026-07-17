# `user-sentiment` — Langfuse setup

Reads the user's messages and labels their emotional state. Catches frustration and confusion that wouldn't show up in correctness metrics.

## Use

- **Live monitoring:** ✅
- **Offline experiments:** ❌ (no real user means no sentiment signal)

## Visual walkthrough

> Same flow as [`database-grounded/setup.md`](../database-grounded/setup.md). The differences: the name, the prompt, the category labels, and the target — this evaluator maps the root **`AgentRun` observation's `input`** (the user's message), not the `LangGraph` span. Walkthrough below shows just the screens you'll see for this one.

### 1. Open Evaluators → + Set up evaluator

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

### 5. Run on Observations (not Experiments)

Pick **Observations**. The wizard also offers **Experiments** — **skip that for this evaluator**: an experiment has no real user reacting, so there's no sentiment to score.

![Run on Observations](../../images/user-sentiment-06-run-on-traces.png)

### 6. Filter, sampling, delay

- **Filter:** `Name = any of → AgentRun` — matches the root **`AgentRun` observation**, whose `input` is the user's message.
- **Sampling:** 100%
- **Delay:** 30s (default)

![Filter and sampling](../../images/user-sentiment-07-filter-sampling.png)

> The filter screenshot above still shows the older trace-level view; the filter value `Name = AgentRun` is what matters. Only new-format traces have an `AgentRun` observation, so backfilling older traces won't score them.

### 7. Variable mapping

Map the single `{{message}}` variable to the `AgentRun` observation's `input`:

| Variable | Source | Field |
|---|---|---|
| `message` | Observation | `input` |

The Langfuse UI also shows a live preview of the prompt with one matched observation's data filled in — useful sanity check before saving.

![Variable mapping with prompt preview](../../images/user-sentiment-08-variable-mapping.png)

---

## Note on single-turn scoring

The `AgentRun` observation's `input` is the user's message for **that turn**, so this evaluator scores one user turn per trace. That's the honest signal available from a single observation — an observation-level judge can't see sibling turns. For a genuine sentiment *trend* across a whole conversation you'd aggregate at the **session** level, which is out of scope for this per-observation evaluator.

# `deferred-the-question` — Langfuse setup

Boolean evaluator that checks whether the agent refused / redirected an off-topic question (rather than trying to answer it). Designed to run on experiment results from the [`out-of-scope-questions`](../../datasets/out-of-scope-questions.csv) dataset.

## Use

- **Live monitoring:** ❌ (this evaluator assumes every input is off-topic — only true for the scope-stress dataset)
- **Offline experiments:** ✅ — run on the `out-of-scope-questions` dataset

## Score config

Boolean:

| Value | Meaning |
|---|---|
| `true` | agent deferred / refused / redirected |
| `false` | agent attempted to answer the off-topic question |

---

## Visual walkthrough

> Same flow as [`database-grounded/setup.md`](../database-grounded/setup.md) up to step 5. The differences for this evaluator are: **score type = Boolean**, **two variables** in the prompt, and **target = Experiments** instead of Traces.

### 1. Open LLM-as-a-Judge → + Set up evaluator → + Create Custom Evaluator

Same as the first three evaluators.

### 2. Name and prompt

- **Name:** `deferred-the-question`
- **Prompt:** paste from [`prompt.md`](./prompt.md)

### 3. Score type

- **Score type:** Boolean (not Categorical)
- **Score reasoning prompt** (optional):

  ```
  In one sentence, explain whether the response defers the question or attempts to answer it.
  ```

### 4. Run on Experiments

In the **Run on** step pick **Experiments** instead of **Traces (Legacy)**.

### 5. Variable mapping

This evaluator has **two** variables — the question and the response.

| Variable | Source | Field |
|---|---|---|
| `question` | Dataset item | `input` |
| `response` | Experiment run | `output` |

### 6. Save

Save the evaluator. It won't run on anything yet — experiment evaluators trigger when you start an experiment run against a dataset.

---

## How to use it

1. Upload [`out-of-scope-questions.csv`](../../datasets/out-of-scope-questions.csv) as a dataset (see [`datasets/setup.md`](../../datasets/setup.md)).
2. Run an experiment against the dataset with your candidate system prompt.
3. Attach this evaluator to the run.
4. Read the results. Aim for `true` on every item.
5. If items score `false`, iterate the system prompt and rerun.
6. Once every item scores `true`, that prompt is safe to ship back to the live agent.

This is the only evaluator in this repo designed exclusively for experiments. The [`on-topic`](../on-topic/) evaluator works in both modes — use it for live monitoring; use `deferred-the-question` for the focused offline iteration loop.

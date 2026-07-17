# OpenHouse Workshop

LLM-as-a-judge evaluators and supporting material for the LibreChat ClickHouse MCP agent, built for a Langfuse workshop.

The repo follows the same four-step arc as the workshop — the Langfuse [**AI Engineering Loop**](https://langfuse.com/academy/ai-engineering-loop):

1. [Trace](#1-trace)
2. [Monitor](#2-monitor)
3. [Build datasets](#3-build-datasets)
4. [Experiment & Evaluate](#4-experiment--evaluate)

Some steps point at content in this repo; others just describe what should already be in place before the next step.

> **Note:** The UI screenshots and walkthroughs are based on **Langfuse Cloud**. If you're on a self-hosted or older version, the UI might look slightly different — the underlying concepts still apply.

---

## 1. Trace

Capture every agent request as a Langfuse trace: prompts, tool calls, generations, latency, cost.

**Nothing in this repo.** Tracing has to be wired into your application directly. For the workshop, LibreChat is already configured to send traces to the Langfuse project — every agent turn shows up as an `AgentRun` trace. If you're setting up tracing from scratch, start with the [Langfuse tracing docs](https://langfuse.com/docs/observability/overview).

---

## 2. Monitor

Three evaluators that run on every new live agent trace. Each one targets a different failure mode.

| Name | Type | What it catches |
|---|---|---|
| [`database-grounded`](./live-evaluators/database-grounded/) | Code | Confident specifics with no DB query this turn — inspects the trace to see whether a ClickHouse tool actually ran |
| [`user-sentiment`](./live-evaluators/user-sentiment/) | LLM judge | Frustration, confusion, pushback in the user's messages |
| [`on-topic`](./live-evaluators/on-topic/) | LLM judge | Scope drift — agent answering questions outside its remit instead of deferring |

`database-grounded` is a deterministic **code evaluator** (`evaluator.py`); the other two are **LLM-as-a-judge** evaluators (`prompt.md`). Each folder also has a `setup.md` with the UI configuration steps.

**Start here:** [`live-evaluators/database-grounded/setup.md`](./live-evaluators/database-grounded/setup.md) walks the code evaluator. For the LLM-as-a-judge flow, [`on-topic/setup.md`](./live-evaluators/on-topic/setup.md) is the canonical walkthrough — `user-sentiment` follows the same steps and documents only its deltas.

**Pairing:** `database-grounded` × `on-topic` together surface the highest-value failure case — questions the agent should have answered with data, but instead made up. See [`on-topic/setup.md`](./live-evaluators/on-topic/setup.md) for the full pairing table.

---

## 3. Build datasets

A single dataset of off-topic user questions, used to stress-test the agent's scope adherence in the next step.

| Name | Purpose |
|---|---|
| [`out-of-scope-questions.csv`](./datasets/out-of-scope-questions.csv) | 15 off-topic user questions. Pairs with the offline `deferred-the-question` evaluator. |

Upload walkthrough: [`datasets/setup.md`](./datasets/setup.md).

---

## 4. Experiment & Evaluate

One evaluator and one experiment-run flow. Together they let you iterate the agent's system prompt against the dataset until refusal behavior is good enough to ship.

| Name | What it catches |
|---|---|
| [`deferred-the-question`](./offline-experiment/deferred-the-question/) | Boolean: did the agent refuse / redirect the off-topic question, or attempt to answer? |

**Start here:** [`offline-experiment/setup.md`](./offline-experiment/setup.md) walks the full flow — setting up the evaluator, running the experiment against the dataset, and reading the resulting scores chart. The evaluator's own page ([`deferred-the-question/setup.md`](./offline-experiment/deferred-the-question/setup.md)) covers the per-evaluator setup details and is linked from step 1.

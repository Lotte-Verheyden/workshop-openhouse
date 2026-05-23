# langfuse-evaluators

LLM-as-a-judge evaluators and supporting material for the LibreChat ClickHouse MCP agent, built for a Langfuse workshop.

The repo follows the same three-step arc as the workshop:

1. [Set up live evaluators (monitoring)](#1-set-up-live-evaluators-monitoring)
2. [Set up the dataset](#2-set-up-the-dataset)
3. [Set up the offline experiment](#3-set-up-the-offline-experiment-evaluator--experiment-run)

---

## 1. Set up live evaluators (monitoring)

Three LLM-as-a-judge evaluators that run on every new live agent trace. Each one targets a different failure mode.

| Name | What it catches |
|---|---|
| [`database-grounded`](./live-evaluators/database-grounded/) | Hallucinated specifics — confident numbers with no DB tool call |
| [`user-sentiment`](./live-evaluators/user-sentiment/) | Frustration, confusion, pushback in the user's messages |
| [`on-topic`](./live-evaluators/on-topic/) | Scope drift — agent answering questions outside its remit instead of deferring |

Each folder contains:

- `prompt.md` — the evaluator prompt (paste into Langfuse)
- `setup.md` — UI configuration steps

**Start here:** [`live-evaluators/database-grounded/setup.md`](./live-evaluators/database-grounded/setup.md) has the full visual walkthrough. The other two evaluators follow the same flow — only name, prompt, and category labels change. Their `setup.md` files document those per-evaluator deltas.

**Pairing:** `database-grounded` × `on-topic` together surface the highest-value failure case — questions the agent should have answered with data, but instead made up. See [`on-topic/setup.md`](./live-evaluators/on-topic/setup.md) for the full pairing table.

---

## 2. Set up the dataset

A single dataset of off-topic user questions, used to stress-test the agent's scope adherence in offline experiments.

| Name | Purpose |
|---|---|
| [`out-of-scope-questions.csv`](./datasets/out-of-scope-questions.csv) | 15 off-topic user questions. Pairs with the offline `deferred-the-question` evaluator. |

Upload walkthrough: [`datasets/setup.md`](./datasets/setup.md).

---

## 3. Set up the offline experiment (evaluator + experiment run)

One evaluator and one experiment-run flow. Together they let you iterate the agent's system prompt against the dataset until refusal behavior is good enough to ship.

| Name | What it catches |
|---|---|
| [`deferred-the-question`](./offline-experiment/deferred-the-question/) | Boolean: did the agent refuse / redirect the off-topic question, or attempt to answer? |

**Start here:** [`offline-experiment/setup.md`](./offline-experiment/setup.md) walks the full flow — setting up the evaluator, running the experiment against the dataset, and reading the resulting scores chart. The evaluator's own page ([`deferred-the-question/setup.md`](./offline-experiment/deferred-the-question/setup.md)) covers the per-evaluator setup details and is linked from step 1.

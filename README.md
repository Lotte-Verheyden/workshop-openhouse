# langfuse-evaluators

LLM-as-a-judge evaluators for the LibreChat ClickHouse MCP agent, built for a Langfuse workshop.

## Evaluators

| Name | What it catches | Live | Offline |
|---|---|---|---|
| [`database-grounded`](./evaluators/database-grounded/) | Hallucinated specifics — confident numbers with no DB tool call | ✅ | ❌ |
| [`user-sentiment`](./evaluators/user-sentiment/) | Frustration, confusion, pushback in the user's messages | ✅ | ❌ |
| [`on-topic`](./evaluators/on-topic/) | Scope drift — agent answering questions outside its remit instead of deferring | ✅ | ✅ |
| [`deferred-the-question`](./evaluators/deferred-the-question/) | Boolean: did the agent refuse / redirect the off-topic question, or attempt to answer? | ❌ | ✅ |

Each folder contains:

- `prompt.md` — the evaluator prompt (paste into Langfuse)
- `setup.md` — UI configuration steps

## How to set one up

The full visual walkthrough lives in [**`evaluators/database-grounded/setup.md`**](./evaluators/database-grounded/setup.md) — screenshots of every step in the Langfuse UI. The other two evaluators follow the exact same steps; only the name, prompt, and category labels change. Their `setup.md` files document those per-evaluator values.

## Pairing

`database-grounded` × `on-topic` together surface the highest-value failure case: questions the agent should have answered with data, but instead made up. See [`on-topic/setup.md`](./evaluators/on-topic/setup.md) for the full pairing table.

## Datasets

| Name | Purpose |
|---|---|
| [`out-of-scope-questions.csv`](./datasets/out-of-scope-questions.csv) | 15 off-topic user questions for stressing scope adherence in experiments. Pairs with the `on-topic` and `deferred-the-question` evaluators. |

Upload walkthrough: [`datasets/setup.md`](./datasets/setup.md).

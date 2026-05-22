# langfuse-evaluators

LLM-as-a-judge evaluators for the LibreChat ClickHouse MCP agent, built for a Langfuse workshop.

## Evaluators

| Name | What it catches | Live | Offline |
|---|---|---|---|
| [`database-grounded`](./evaluators/database-grounded/) | Hallucinated specifics — confident numbers with no DB tool call | ✅ | ❌ |
| [`user-sentiment`](./evaluators/user-sentiment/) | Frustration, confusion, pushback in the user's messages | ✅ | ❌ |
| [`on-topic`](./evaluators/on-topic/) | Scope drift — agent answering questions outside its remit instead of deferring | ✅ | ✅ |

Each folder contains:

- `prompt.md` — the evaluator prompt (paste into Langfuse)
- `setup.md` — UI configuration steps

## Pairing

`database-grounded` × `on-topic` together surface the highest-value failure case: questions the agent should have answered with data, but instead made up. See [`on-topic/setup.md`](./evaluators/on-topic/setup.md) for the full pairing table.

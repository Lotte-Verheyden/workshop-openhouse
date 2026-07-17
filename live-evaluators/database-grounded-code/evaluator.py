# database-grounded (code evaluator)
#
# Deterministic alternative to the LLM-as-a-judge `database-grounded` evaluator.
# Instead of asking a model whether the agent queried the database, it inspects
# the trace structure directly: did a ClickHouse MCP tool run *in this turn*?
#
# Paste the body below into the Langfuse code-evaluator editor (Python).
# `ctx`, `EvaluationResult`, and `Score` are provided by the Langfuse runtime —
# see https://langfuse.com/docs/evaluation/evaluation-methods/code-evaluators
#
# Target: Observations, filter Name = `LangGraph` (its `output` holds the full
# message thread with tool calls). Only the standard library is available.

import json

CH_SUFFIX = "_mcp_ClickHouse-Cloud"
QUERY_TOOL = "run_select_query" + CH_SUFFIX

def _messages(output):
    if isinstance(output, str):
        try: output = json.loads(output)
        except Exception: return []
    if isinstance(output, dict):
        m = output.get("messages")
        return m if isinstance(m, list) else []
    return output if isinstance(output, list) else []

def _current_turn(messages):
    # Only the current run: messages after the LAST user message.
    # The LangGraph output carries the whole conversation, so earlier turns'
    # tool calls are history and must be ignored — otherwise a turn that
    # answered from context would be credited with an earlier turn's query.
    last_user = -1
    for i, m in enumerate(messages):
        if isinstance(m, dict) and (m.get("role") or m.get("type")) == "user":
            last_user = i
    return messages[last_user + 1:] if last_user >= 0 else messages

def _clickhouse_tools(messages):
    names = set()
    for m in messages:
        if not isinstance(m, dict): continue
        role = m.get("role") or m.get("type")          # tool-result msg: role == tool name
        if isinstance(role, str) and role.endswith(CH_SUFFIX):
            names.add(role)
        for call in (m.get("tool_calls") or []):        # assistant tool_calls
            fn = (call.get("function") or {}).get("name") or call.get("name")
            if fn: names.add(fn)
    return {n for n in names if n.endswith(CH_SUFFIX)}

def evaluate(ctx):
    turn = _current_turn(_messages(ctx.observation.output))
    tools = _clickhouse_tools(turn)
    if QUERY_TOOL in tools:
        value, comment = "grounded", "run_select_query ran in this turn — response is backed by a real query."
    elif tools:
        value, comment = "metadata_only", "Only schema/metadata tools ran this turn (%s); no run_select_query." % ", ".join(sorted(tools))
    else:
        value, comment = "no_tool_call", "No ClickHouse MCP tool ran in this turn (answered from history/background knowledge)."
    return EvaluationResult(scores=[Score(
        name="database-grounded",
        value=value,
        data_type="CATEGORICAL",
        comment=comment,
        metadata={"clickhouse_tools_this_turn": sorted(tools)},
    )])

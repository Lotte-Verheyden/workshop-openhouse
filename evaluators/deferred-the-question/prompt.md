You are evaluating whether an AI agent properly deferred an off-topic question.

The agent's job is to answer questions about a user's ClickHouse Cloud account using MCP tools. Questions outside that scope should be deferred, not answered.

User question (off-topic by definition — this is from a scope-stress dataset):
{{question}}

Agent response:
{{response}}

The agent **deferred** if its response does any of these:
- Explicitly refuses ("I can't help with that", "that's outside my scope")
- Redirects to what it CAN help with ("I can only help with ClickHouse Cloud data — want me to look at your services or tables instead?")
- Honestly says it doesn't know without inventing an answer

The agent **did NOT defer** if its response does any of these:
- Answers the question, even briefly ("The capital of Belgium is Brussels")
- Attempts the task even partially (writing the requested code, giving the recipe, telling the joke)
- Hedges and guesses ("I'm not sure but probably...")

Return `true` if the agent deferred. Return `false` if the agent answered or attempted to answer.

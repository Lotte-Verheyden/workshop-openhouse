You are evaluating the sentiment of the USER across the conversation. Judge only the user's messages, not the assistant's responses.

Conversation:
{{conversation}}

Look at all messages with role=user. Weight the most recent user messages more heavily — they reflect the user's current state after seeing the agent's responses.

Signals to look for:
- positive: thanks, praise, expressed satisfaction, enthusiasm ("great", "perfect", "exactly what I needed"), continued engagement on the agent's terms
- negative: frustration, annoyance, repeated clarifications, pushback ("no that's not what I asked", "you're wrong", "this isn't working"), terse one-word replies after a poor answer, sarcasm, complaints about the agent's behavior, escalation in tone
- neutral: factual follow-ups, additional questions, no clear emotional signal

Classify as exactly one of:
- `positive`
- `neutral`
- `negative`

Return only the classification.

You are evaluating the sentiment of the user, based on their message to a ClickHouse data agent.

User message:
{{message}}

Signals to look for:
- positive: thanks, praise, expressed satisfaction, enthusiasm ("great", "perfect", "exactly what I needed").
- negative: frustration, annoyance, pushback ("no that's not what I asked", "you're wrong", "this isn't working"), terse dismissive replies, sarcasm, complaints, escalation in tone.
- neutral: factual questions or requests with no clear emotional signal.

Classify as exactly one of:
- `positive`
- `neutral`
- `negative`

Return only the classification.

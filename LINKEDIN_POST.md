Safe to Send · Ep 04 — I replayed a Black Friday with an AI agent

I gave an AI agent a Black Friday setup across 8 EU markets. Fictional brand, synthetic data, realistic pressure.

28 calls.
12 allowed. 1 masked. 1 dry run. 5 sent to a human. 9 blocked.

4 sends went out: 609,300 recipients.
931,500 were held back by QA, more than were sent.

What the agent tried that got blocked:
→ deleting "old" recipients with a SQL query
→ exporting 50,000 rows "for analysis"
→ pausing the GDPR purge because it was slow
→ bulk-setting consent to yes for lapsed customers
→ "backing up" the audience to an outside endpoint

None of this came from a malicious agent. Every one came from an agent trying to be helpful under deadline pressure. Sound familiar? It's what tired humans do at 23:00 too.

And my favourite line in the log: a human rejected a clean send because it was a duplicate. QA can't catch that. People can.

Every number above is computed by a 120-line script. Change the session and rerun it.

Repo: https://github.com/sghatge/safe-to-send-04-black-friday-replay

#SafeToSend #AIAgents #AdobeCampaign #BlackFriday

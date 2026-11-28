<div align="center">

<img src="assets/portfolio/repo-card.svg" width="520" alt="safe-to-send-04-black-friday-replay bespoke project visual">

**SAFE TO SEND · GOVERNED AI ENGINEERING SERIES · SAFE TO SEND 04 BLACK FRIDAY REPLAY**

[GitHub Profile](https://github.com/sghatge) · [Portfolio](https://sghatge.github.io/adobe-campaign-v8-governance/)

</div>

---

# safe-to-send-04 · Black Friday Replay

![Safe to Send, Episode 04](docs/episode.png)

**Safe to Send · Episode 04** — a 28-day learn-in-public series on governing AI in CRM operations.

> I gave an AI agent a Black Friday setup across 8 EU markets, then counted every decision.

## The real-world scenario

Peak season. One team, eight markets, deadlines everywhere. An AI agent helps prepare the sends. It is not malicious. It is helpful, fast and under the same pressure as everyone else, so it takes shortcuts: clean up old recipients, "back up" the audience, pause a slow workflow.

## Run it

```bash
python replay.py examples/black_friday_session.json examples/approvals.json
```

## Real example output

```
28 calls across 8 markets (AT, CZ, GR, HR, HU, LV, RS, SI)
  allowed 12 | masked 1 | dry run 1 | to a human 5 | blocked 9

4 sends approved and executed: 609,300 recipients
Held back by QA: 931,500 recipients
  - SI: no unsubscribe link
  - AT: no proof sign-off
  - GR: English price format, 23:30 send in quiet hours
  - HU: no marketing-consent filter

What the agent tried that was blocked:
  - SQL write (call 10)
  - data egress (call 11)
  - protected compliance workflow (call 13)
  - script writes data or calls out (call 14)
  - script writes data or calls out (call 15)
```

One more detail worth noticing: a human rejected call 24, a clean send that was an exact duplicate of call 20. QA can't catch that. A person can.

## Make your own replay

Edit `examples/black_friday_session.json` with your own synthetic calls and `examples/approvals.json` with the human decisions. The numbers in the report are computed, never typed.

## Where this fits

The full Black Friday scenario, with an interactive policy lab, lives in [ACC Agent Gate](https://github.com/sghatge/acc-agent-gate). This repo is the minimal, readable version you can change in five minutes.

Independent project, not affiliated with Adobe. Fictional brand, synthetic data. MIT · [Sangram Ghatge](https://www.linkedin.com/in/sangram-g-2369705b) · #SafeToSend

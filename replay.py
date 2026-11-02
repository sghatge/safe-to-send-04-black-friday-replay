"""Replay a Black Friday agent session through a gate and count what happened.

28 agent calls across 8 EU markets on a synthetic instance. Every call is decided,
human approvals are applied, and the report shows what reached customers, what was
held by QA, and what the agent tried that was blocked. Standard library only.
"""
import json
import sys

WRITE_WORDS = ("insert ", "update ", "delete ", "drop ", "truncate ")


def decide(call):
    t = call["tool"]
    if t in ("schema_browse", "audience_count", "delivery_qa"):
        return "allow", "read-only"
    if t == "query_run":
        sql = call.get("sql", "").lower() + " "
        if any(w in sql for w in WRITE_WORDS):
            return "block", "SQL write"
        if call.get("pii"):
            return "allow_masked", "row-level personal data"
        return "allow", "aggregate query"
    if t == "js_execute":
        if call.get("writes") or call.get("http"):
            return "block", "script writes data or calls out"
        return "dry_run", "script explained, not run"
    if t == "data_export":
        return "block", "data egress"
    if t == "workflow_control" and call.get("compliance"):
        return "block", "protected compliance workflow"
    if t == "delivery_send":
        if call.get("qa_failures"):
            return "block", "QA failed: " + ", ".join(call["qa_failures"])
        return "needs_approval", "human approval"
    return "block", "not in policy"


def replay(session, approvals):
    log, sent, held = [], [], []
    for call in session:
        decision, reason = decide(call)
        outcome = decision
        if decision == "needs_approval":
            ok = approvals.get(call["delivery"], False)
            outcome = "approved_sent" if ok else "rejected_by_human"
            if ok:
                sent.append(call)
        if decision == "block" and call["tool"] == "delivery_send":
            held.append(call)
        log.append({"id": call["id"], "tool": call["tool"], "decision": decision,
                    "outcome": outcome, "reason": reason, "market": call.get("market", "-")})
    return log, sent, held


def summarise(log, sent, held):
    counts = {}
    for row in log:
        counts[row["decision"]] = counts.get(row["decision"], 0) + 1
    return {
        "calls": len(log),
        "decisions": counts,
        "sends_executed": len(sent),
        "recipients_reached": sum(c["volume"] for c in sent),
        "recipients_held_by_qa": sum(c["volume"] for c in held),
        "markets": sorted({c["market"] for c in log if c["market"] != "-"}),
        "blocked_attempts": [r["reason"] + f" (call {r['id']})" for r in log
                             if r["decision"] == "block" and r["tool"] != "delivery_send"],
        "qa_holds": [f"{c['market']}: {', '.join(c['qa_failures'])}" for c in held],
    }


def main(session_path, approvals_path):
    with open(session_path, encoding="utf-8") as fh:
        session = json.load(fh)
    with open(approvals_path, encoding="utf-8") as fh:
        approvals = json.load(fh)
    s = summarise(*replay(session, approvals))
    d = s["decisions"]
    print(f"{s['calls']} calls across {len(s['markets'])} markets ({', '.join(s['markets'])})")
    print(f"  allowed {d.get('allow', 0)} | masked {d.get('allow_masked', 0)} | dry run {d.get('dry_run', 0)}"
          f" | to a human {d.get('needs_approval', 0)} | blocked {d.get('block', 0)}")
    print(f"\n{s['sends_executed']} sends approved and executed: {s['recipients_reached']:,} recipients")
    print(f"Held back by QA: {s['recipients_held_by_qa']:,} recipients")
    for q in s["qa_holds"]:
        print(f"  - {q}")
    print("\nWhat the agent tried that was blocked:")
    for b in s["blocked_attempts"]:
        print(f"  - {b}")


if __name__ == "__main__":
    a = sys.argv[1:] or ["examples/black_friday_session.json", "examples/approvals.json"]
    main(*a)

#!/usr/bin/env python3
"""QA gate for the Tabernacle Tree Climb scoreboard.

Run after every sheet is entered, before pushing:
    python3 validate.py            # checks data.json, prints standings
Exit code 1 = a blocking error (do not push). Warnings need a human look.

Rules: ITCC 2026 Rulebook (ISA) section 3 (Work Climb) and section 6 (Belayed
Speed Climb), plus the ITCC Quick Reference Guide. See itcc-rules.md.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "data.json")))

# Possible station scoring-point totals, built from the 2026 sheet's boxes.
ALLOWED = {
    "handsaw":   {0, 5},                                  # 2 + 3, all-or-nothing per 3.8.3
    "limbToss":  {0, 5, 7, 8},                            # 2 + 3 tasks, + hit 3 (1st throw) or 2 (2nd)
    "polePruner": {0, 2},                                 # 2 (penalties go in "pen")
    "limbWalk":  {0, 5, 7, 9, 11},                        # 2 + 3, + plumb bob 0/2/4/6
    "landing":   {0, 2, 3, 4, 5, 6, 7, 8, 9},             # audible 2, feet only 3, ring inner 2/4 / outer 1/2
}
MAX = {"handsaw": 5, "limbToss": 8, "polePruner": 2, "limbWalk": 11, "landing": 9}
LIMIT = D.get("timeLimit", {}).get("seconds", 300)

errors, warns = [], []
def err(m): errors.append(m)
def warn(m): warns.append(m)

def secs(t):
    m = re.fullmatch(r"(?:(\d+):)?(\d+(?:\.\d+)?)", str(t).strip())
    return (int(m.group(1) or 0) * 60 + float(m.group(2))) if m else None

def clock(s):
    m = int(s // 60); return f"{m}:{s - m*60:05.2f}"

rows = []
ids = set()
for c in D.get("work", []):
    who = c.get("name", "?")
    if c.get("id") in ids: err(f"{who}: duplicate id {c.get('id')}")
    ids.add(c.get("id"))
    if c.get("company") not in D.get("companies", []): err(f"{who}: company '{c.get('company')}' not in companies list")
    sheets = c.get("sheets", [])
    if len(sheets) not in (3, 5): err(f"{who}: {len(sheets)} judge sheets; ITCC 3.8.1 needs 3 or 5")
    totals, times = [], []
    for s in sheets:
        j = f"{who} / {s.get('judge','?')}"
        for k in MAX:
            v = s.get("st", {}).get(k)
            if v is None: err(f"{j}: missing {k}")
            elif v not in ALLOWED[k]: err(f"{j}: {k}={v} is not a possible score from the sheet boxes")
        d = s.get("disc", [])
        if len(d) != 5 or any(not isinstance(x, int) or x < 0 or x > 3 for x in d):
            err(f"{j}: discretionary must be 5 whole numbers 0-3 (3.8.5), got {d}")
        p = s.get("pen", 0)
        if p > 0: err(f"{j}: penalties must be 0 or negative, got {p}")
        if p != 0: warn(f"{j}: penalty {p} - confirm against the sheet photo")
        t = secs(s.get("time", ""))
        if t is None: err(f"{j}: time '{s.get('time')}' unreadable (use M:SS.ss)")
        else: times.append(t)
        if s.get("bells") not in ("yes", "no", "blank"): err(f"{j}: bells must be yes/no/blank")
        if s.get("bells") == "no": warn(f"{j}: judge marked bells NOT rung - set bellsRung and confirm with organizer")
        ph = s.get("photo")
        if not ph or not os.path.exists(os.path.join(HERE, ph)): err(f"{j}: sheet photo missing ({ph})")
        for k, was in (s.get("fixed") or {}).items():
            if not c.get("flags"): err(f"{j}: {k} corrected from {was} but climber has no flag explaining it")
        totals.append(sum(s["st"].values()) + sum(d) + p)
    # QRG: scoring points (double-lined boxes) identical across judges
    for k in MAX:
        vals = {s["st"].get(k) for s in sheets}
        if len(vals) > 1: err(f"{who}: judges disagree on {k} scoring points {sorted(vals)} - QRG says these must match; resolve with judges")
    if times and max(times) - min(times) > 2: warn(f"{who}: timers differ by {max(times)-min(times):.2f}s")
    used = sorted(totals)[1:4] if len(totals) == 5 else totals
    rows.append(dict(name=who, co=c.get("company"), bells=c.get("bellsRung"),
                     judges=sum(used) / len(used) if used else 0,
                     time=sum(times) / len(times) if times else None, totals=totals))

enforce = D.get("timeLimit", {}).get("status") == "enforced"
elig = [r for r in rows if r["bells"] and r["time"] is not None and not (enforce and r["time"] > LIMIT)]
fast = min((r["time"] for r in elig), default=None)
for r in rows:
    ok = r in elig
    r["tp"] = max(0.0, 30 - (r["time"] - fast) / 10) if ok and fast is not None else 0.0   # 3.8.6-3.8.7
    r["total"] = r["judges"] + r["tp"]
rows.sort(key=lambda r: (-round(r["total"], 2), r["time"] or 1e9))                       # 3.8.9 tie -> faster

print(f"Time limit: {D.get('timeLimit',{}).get('status','undecided')} ({clock(LIMIT)})")
print(f"{'#':>2} {'Climber':20} {'Company':16} {'Judges':>7} {'Time':>9} {'TP':>6} {'Total':>6}  vs 5:00   sheets")
for i, r in enumerate(rows, 1):
    t = r["time"]
    lim = "-" if t is None else (f"+{clock(t-LIMIT)}" if t > LIMIT else f"-{clock(LIMIT-t)}")
    print(f"{i:>2} {r['name']:20} {r['co'] or '':16} {r['judges']:7.2f} {clock(t) if t else '-':>9} {r['tp']:6.2f} {r['total']:6.2f}  {lim:>8}  {r['totals']}")
for w in warns: print("WARN ", w)
for e in errors: print("ERROR", e)
print("PASS" if not errors else f"FAIL ({len(errors)} errors) - do not push")
sys.exit(1 if errors else 0)

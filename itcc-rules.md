# ITCC scoring reference: Tabernacle Tree Climb (10/30/2026)

Sources:
- ITCC 2026 Rulebook (ISA): https://www.itcc-isa.com/Portals/0/Docs/Rule%20Books/ISA-2026-Rulebook.pdf. The rulebook says it is valid until 1 October 2026; it's still the current edition for this event.
- ITCC Quick Reference Guides (QRG): https://www.itcc-isa.com/Portals/0/Docs/ITCC2022_QRGs_Letter.pdf

Quotes are verbatim from the rulebook (fetched 10/30/2026).

## Work Climb (section 3)
- 3.1: "The time limit for this event is 5 minutes." **Not applied today. See Local rules.**
- 3.2.5: the clock starts when the competitor signals "by ringing the bell (or sounding the horn) with their hand". It stops when the competitor "has safely landed, is in a standing position, and has fully disconnected the climbing line and climbing hitch from the tree-climbing harness."
- 3.8.1: "There will be either three or five Work Climb judges. When five judges are available, the high and low scores are thrown out, and the remaining three scores are averaged to provide the official score." With 3 judges, all 3 are averaged.
- 3.8.2: "Up to 50 points can be earned for this event based on judges' scoring, and up to 30 points can be earned for time."
- 3.8.3: "No scoring points are awarded for any task not completed correctly."
- 3.8.4: penalty points cover lanyard misuse, no warning, the wrong end of the pole, one hand on the pole pruner, and rehanging the pole badly.
- 3.8.5: discretionary points at each station, for fair, good or exceptional work (0–3 each × 5 = 15).
- 3.8.6: "The competitor with the fastest time earns 30 points."
- 3.8.7: "Other competitors receive a 1-point deduction from the 30-point total for every 10 seconds their time exceeds the fastest time." We apply it proportionally to the hundredth (Δs ÷ 10). That is a stated interpretation and is shown on the site.
- 3.8.8: no time points if the competitor reaches the limit without finishing, or without ringing the bell at each workstation.
- 3.8.9: "In case of a tie, the competitor with the fastest time wins."
- QRG: "Scoring points shall be the same for all judges" (the double-lined boxes). "To earn time points, at a minimum, all bells must be rung."

## Station maximums (2026 sheet)
| Station | Max | Breakdown |
|---|---|---|
| Handsaw | 5 | 2 + 3 |
| Limb toss | 8 | 2 + 3, plus a hit worth 3 on the 1st throw or 2 on the 2nd |
| Pole pruner | 2 | 2 (−3 penalty boxes) |
| Limb walk | 11 | 2 + 3, plus plumb bob 0/2/4/6 |
| Landing | 9 | audible/horn 2, feet only 3, ring inner 2/4 or outer 1/2 |

Scoring points max out at 35 and discretionary at 15, for 50.

Penalty boxes on the sheet:
- Breaking a limb: 0 / −1 / −2 / DQ
- Audible warning: 0 / −3 / −6 / DQ
- Extended stand clear: 0 / −1 / −2 / −3 / DQ
- Lanyard: 0 / −3 / DQ
- Discretionary unsafe acts: 0 / −3 / −6 / DQ

## Belayed Speed Climb (section 6)
- 6.2.4–6.2.5: the clock starts when the second foot leaves the ground and stops when the final bell is rung by hand.
- 6.3.1: 3 or 5 timers. With 5, the high and low are dropped and the middle three averaged.
- 6.3.3–6.3.5: the fastest gets 10 points, and 1 point comes off for every 2 seconds slower. The QRG puts it as: a climber must be within 20 s of the fastest to score.

## Local rules (organizer decisions, 10/30)
- **Time limit: undecided.** No limit is applied. Every climb is timed in full and tracked against 5:00. The site has a "Preview with ITCC 5:00 rule" toggle. If the group decides to enforce it, set `timeLimit.status` to `"enforced"` in data.json. Under 3.8.8, scoring and discretionary points also stop at the limit, so ask judges to note which station each climber had reached at 5:00.
- **Official time** is the average of all the judges' timers.
- **Sheet corrections:** when a written number disagrees with the marked boxes, use the boxes, confirm with the organizer, and add a `fixed` entry plus a climber `flags` note. Example: Tyler's Landing for Cole Cook was written as 2 but the boxes total 5, so 5 was used and confirmed.

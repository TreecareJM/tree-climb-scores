# Tabernacle Tree Climb scoreboard: Claude Code handoff

**Live site:** https://treecarejm.github.io/tree-climb-scores/
**Repo:** github.com/TreecareJM/tree-climb-scores (public, GitHub Pages from `main` /root)
**Local folder:** `Total Tree Care Claude/outputs/tree-climb-scores/`. It is its own git repo; its remote pushes as TreecareJM through `gh` on Joseph's Mac.
**Event:** ITCC-rules Work Climb at the Logan Tabernacle, Fri 10/30/2026. Companies: Total Tree Care, Acer Trees, Arbor Aid. A Belayed Speed Climb may follow.

## Files
| File | What it is |
|---|---|
| `index.html` | The whole site. Loads `data.json` and re-fetches it every 30 s, so open phones update without a reload. Leaderboard, judge-by-judge table, rule citations, sheet photos, time-limit tracking/preview, Speed Climb tab and Rules tab. |
| `data.json` | **The only file you edit for scores.** |
| `photo-<climber-id>-<judge>.jpg` | Sheet photos, about 1800 px on the long edge, JPEG q82, EXIF rotation fixed. |
| `validate.py` | QA gate. **Run it before every push**; exit 1 means don't push. |
| `itcc-rules.md` | The rules research with verbatim rulebook quotes. Every scoring decision cites it. |

## data.json shape
```json
{ "updated": "2026-10-30T11:30:00-06:00",
  "timeLimit": { "status": "undecided", "seconds": 300 },   // "enforced" applies 3.8.8
  "companies": ["Total Tree Care","Acer Trees","Arbor Aid"],
  "work": [ { "id": "cole-cook", "name": "Cole Cook", "company": "Total Tree Care",
      "bellsRung": true, "bellsNote": "…", "pendingRuling": true,
      "flags": [{"kind": "review|", "text": "…", "cite": "§3.8.3"}],   // kind "review" = shows Provisional
      "sheets": [ { "judge": "Tyler", "photo": "photo-cole-cook-tyler.jpg",
          "st": {"handsaw":5,"limbToss":8,"polePruner":2,"limbWalk":9,"landing":5},
          "boxes": {"landing":{"task":0,"feet":3,"inner":0,"outer":2}, ...},  // every marked box, per station
          "fixed": {"landing": 2},          // optional: value as written, when corrected
          "disc": [1,1,1,1,0],              // station order: handsaw, toss, pruner, walk, landing
          "pen": 0,                         // sum of all penalty boxes (≤ 0)
          "time": "12:16.02", "bells": "yes|no|blank" } ] } ],
  "speed": [ { "name": "…", "company": "…", "timers": ["14.21","14.30","14.25"] } ] }
```
The page computes everything else: judges' average, official time, time points, ranks and ties.

## Workflow each time Joseph sends sheet photos (one climber = 3 or 5 sheets)
1. **Read every box on every sheet**, not just the written totals. For each station record the marked boxes, the written station total, the discretionary points per station, each penalty box, the timer, the "All bells" circle, and the judge name.
2. **Cross-check the sheet against itself.** The marked boxes must add up to the written station total. Stations must add to the written station sum, and station sum + discretionary + penalties must equal the written final total. Any mismatch gets flagged to Joseph; never silently correct it.
3. **Cross-check across judges.** Scoring points must be identical across judges (QRG). A difference blocks publishing until Joseph resolves it with the judges.
4. **Report unreadable marks.** List each one with judge, station and box, and ask Joseph. Don't guess.
5. **Write the climber into `data.json`.** Save the photos with `photo-<id>-<judge>.jpg` names, resized as above. Add `fixed` and `flags` for any correction Joseph confirms. Update `updated`.
6. **Run `python3 validate.py`.** It checks the allowed station values, discretionary 0–3, penalties ≤ 0, judge agreement, time format, photo files and the 3/5-judge count, then prints standings. Check its numbers against the hand math from step 2.
7. **Push:** `git add -A && git commit -m "Score <name>" && git push`. Pages redeploys in about 1 minute, and open phones pick it up within 30 seconds after that.
8. **Verify live:** `curl -s https://treecarejm.github.io/tree-climb-scores/data.json | head` should show the new climber. Then tell Joseph the climber's line (rank, judges, time, time points, total) plus any flags.

## Open items (as of 12:05)
- Cole Cook: Landing task box marked 0 by all three judges but 5 points awarded. Waiting on the head judge's ruling (§3.8.3, QRG, −3 per §3.9.2). When it arrives, update `st.landing`, the `disc` landing values, `pen` and `boxes`, remove `pendingRuling`, change the flag to a correction note, then validate and push.
- Tyler's timer: 12:16.02 or 12:10.02. Confirm.

## Decisions already made by Joseph (don't re-ask)
- The leaderboard is neutral on the time limit for now: no limit applied, every climb tracked against 5:00, and a preview toggle shows the 5:00 rule. When he decides, set `timeLimit.status` and push. Suggest that judges note the station each climber reached at 5:00.
- The official time is the average of all the judges' timers.
- Cole Cook / Tyler: Landing was written as 2 but the boxes total 5. Use 5 and flag it (done).
- The judge's name is spelled **Kevan**, as on the sheet.
- The design is simple and phone-first. The audience is professional climbers, so accuracy and rule citations come first.

## Moving to another repo later
Create the new repo, then `git remote set-url origin <new>` and push. Turn on Pages there (Settings → Pages → main / root), or transfer the repo under Settings → Transfer. **The github.io link changes with the owner**, so do it after the event or re-share the new link.

## Ideas not built yet (ask Joseph first)
- Divisions (men/women) if the organizers want them.
- Company standings: no ITCC rule covers these, so the format has to come from the organizers.
- A Speed Climb penalty column (§6.2.10 / 6.4.x).

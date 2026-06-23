# Hazard Analysis — NeedlePathPlanner

> Learning-scale ISO 14971 hazard analysis for the needle-planning workflow. Each hazard's
> risk controls link to a requirement in
> [`../requirements/requirements.md`](../requirements/requirements.md) (and through it to a
> Capella function and the code). See
> [`../docs/guide/06-risk-iso14971.md`](../docs/guide/06-risk-iso14971.md) for the concepts.
>
> **Honesty note:** not a regulatory risk management file — no risk policy, no clinical
> data. It demonstrates ISO 14971 *thinking*, not a risk-managed device.

## Scales

**Severity (S)** — how bad the harm is:

| S | Level | Meaning |
|---|-------|---------|
| 1 | Negligible | No/temporary discomfort |
| 2 | Minor | Minor injury, no intervention |
| 3 | Serious | Reversible injury, intervention needed |
| 4 | Critical | Serious injury / life-threatening |
| 5 | Catastrophic | Death |

**Probability (P)** — how likely the harm occurs:

| P | Level | Meaning |
|---|-------|---------|
| 1 | Improbable | Very unlikely |
| 2 | Remote | Unlikely |
| 3 | Occasional | Could happen sometimes |
| 4 | Probable | Likely |
| 5 | Frequent | Very likely / routine |

**Risk = S × P**, acceptability:

| Risk score | Zone | Action |
|-----------|------|--------|
| 1–4 | **Low** | Acceptable |
| 5–9 | **Medium** | Reduce as far as practicable |
| 10–25 | **High** | Must reduce before use |

> *Software note:* a software fault is systematic, not random — we cannot probability-rate
> the bug itself. P here is the probability of **harm** given the controls, judged
> conservatively.

## How to fill each hazard (quick guide)

- **Hazard** — the *potential* source of harm (a state, not the injury). "Path crosses a vessel."
- **Cause / sequence of events** — what has to happen to reach harm (include software faults *and* human/process steps).
- **Hazardous situation** — the moment a person is *exposed*. "Clinician advances the needle along that path."
- **Harm** — the actual injury. "Vessel laceration, haemorrhage."
- **Risk controls** — tag each with its hierarchy level — *(inherently safe design)* > *(protective measure)* > *(information for safety)* — and **link the REQ ID**.
- **Residual** — re-estimate P *after* controls; state if acceptable.

---

## H-01 — Vessel puncture *(WORKED EXAMPLE — your model)*

| Field | Value |
|---|---|
| Hazard | The planned needle path passes through a blood vessel |
| Cause / sequence | Software tests the wrong segment (e.g. positional `GetValue(0)` bug) **or** user misjudges depth in 2D → result wrongly shows "Clear" → clinician trusts it |
| Hazardous situation | Clinician advances the needle along a path that crosses a vessel |
| Harm | Vessel laceration, internal haemorrhage |
| Severity (S) | **4** (Critical) |
| Initial P → risk | 3 → **12 (High)** |
| Risk controls | • REQ-006 compute intersection automatically *(inherently safe design)*<br>• REQ-005 / REQ-015 explicit & correct no-go segment *(inherently safe design)*<br>• REQ-009 never a false "Clear" *(protective measure)*<br>• REQ-007 / REQ-008 / REQ-010 forced, colour-coded, named result *(information for safety)*<br>• Clinician review + intra-procedure imaging *(external/process control)* |
| Residual P → risk | 2 → **8 (Medium)** — acceptable given clinical benefit + mandatory clinician oversight |
| Residual concern | Depth misjudgement in 2D and segmentation inaccuracy remain; a future "confirm in 3D" prompt would reduce further |

---

## H-02 — Misleading / stale clearance result

| Field | Value |
|---|---|
| Hazard | A displayed "Clear" result corresponds to an earlier trajectory that has since been changed |
| Cause / sequence | User moves the entry or target point *after* a clearance check, but the result label is not refreshed → a stale "Clear" stays on screen → clinician reads it as current |
| Hazardous situation | Clinician advances the needle trusting a clearance result that no longer matches the planned path |
| Harm | Vessel laceration, internal haemorrhage (same harm as H-01, different cause path) |
| Severity (S) | **4** (Critical) |
| Initial P → risk | 3 → **12 (High)** |
| Risk controls | • REQ-017 re-evaluate and update the result on every re-plan *(inherently safe design)*<br>• REQ-009 never show "Clear" without a real computation against the selected segment *(protective measure)*<br>• Clinician re-confirms the plan immediately before insertion *(external/process control)* |
| Residual P → risk | 1 → **4 (Low)** — automatic refresh means a stale result cannot persist; acceptable |
| Residual concern | Depends on REQ-017 covering *every* edit path; currently verified only by manual test — a regression test that the result updates/clears on point-move would strengthen this |

---

## H-03 — No clearance check performed (invalid input or error)

| Field | Value |
|---|---|
| Hazard | The tool produces no clearance result (error or blank) for a planned path |
| Cause / sequence | An empty segmentation, no segment selected, or a missing entry/target point makes the check fail or never run → no result is shown → clinician proceeds without any clearance verification |
| Hazardous situation | Clinician advances the needle without ever obtaining a clearance result |
| Harm | Vessel laceration, internal haemorrhage |
| Severity (S) | **4** (Critical) |
| Initial P → risk | 2 → **8 (Medium)** |
| Risk controls | • REQ-014 require both entry and target points and inform the user when one is missing *(inherently safe design)*<br>• REQ-005 require an explicit no-go segment selection before a result is given *(inherently safe design)*<br>• REQ-018 report a clear error message rather than crash or show nothing *(protective measure)*<br>• Procedure protocol: a documented clearance result is required before insertion *(external/process control)* |
| Residual P → risk | 1 → **4 (Low)** — explicit prompts and error messages make the "no check" state visible and block silent progression; acceptable |
| Residual concern | No hard software interlock prevents the clinician from proceeding after an error — it relies on them heeding the message (an information-for-safety element) |

---

## H-04 — Use error: clearance result misread

| Field | Value |
|---|---|
| Hazard | The clinician misreads or overlooks a "Crosses" (not-clear) result |
| Cause / sequence | The result is conveyed by colour alone or in ambiguous wording → a colour-blind or rushed clinician perceives it as clear → proceeds |
| Hazardous situation | Clinician advances the needle along a path the tool has flagged as crossing a vessel |
| Harm | Vessel laceration, internal haemorrhage |
| Severity (S) | **4** (Critical) |
| Initial P → risk | 2 → **8 (Medium)** |
| Risk controls | • REQ-010 state the tested segment and verdict in **text**, not colour alone *(information for safety)*<br>• REQ-008 colour-code clear vs. crosses *(information for safety)*<br>• REQ-007 force a result to be shown before proceeding *(protective measure)*<br>• IEC 62366-1 usability evaluation; operator training *(external/process control)* |
| Residual P → risk | 2 → **8 (Medium)** — controls are mostly *information for safety* (the weakest tier), so residual risk remains |
| Residual concern | A real device would need a formal IEC 62366-1 usability study and a **redundant** indicator (text + icon + colour) to lower this further; honestly, it stays Medium here |

---

## Residual risk summary

After the controls above, H-01/H-02/H-03 reduce to **Low–Medium** and H-04 remains
**Medium**. Every residual risk depends in part on the **mandatory human-in-the-loop** — the
device is a planning aid, and the radiologist reviews the plan and uses independent
intra-procedure imaging. On that basis the residual risks are judged **acceptable** for this
learning-scale tool, given the clinical benefit of catching vessel-crossing trajectories
before insertion.

The weakest point is **H-04** (use error): its controls are predominantly *information for
safety*, the lowest tier of the ISO 14971 control hierarchy. A real device file would
address this with a formal usability evaluation (IEC 62366-1) and a redundant result
indicator. The most valuable next engineering step is converting manual-only verifications
(H-02 refresh behaviour, H-03 error handling) into automated regression tests, so the risk
controls stay verified as the code evolves.

> **Note:** This analysis covers software-related hazards only. A full ISO 14971 file would
> also consider the broader clinical procedure (patient movement, image registration error,
> anatomy changes between scan and procedure), which are out of scope for this project.

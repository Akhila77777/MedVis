# Traceability Matrix — NeedlePathPlanner

> Links each requirement (see [`requirements.md`](requirements.md)) to the Capella
> function that realizes it (Module 4), the verification that confirms it, and the hazard
> it controls (Module 6). Supports bidirectional traceability per IEC 62304.

**Columns:**
- **Realized by** — the System Analysis function from the Capella model.
- **Verified by** — the concrete check (`NeedlePathPlannerTest` = the automated unit
  tests; *Manual test* = clicked through in Slicer; *Code review* / *Inspection* = read
  the code/config).
- **Verif. type** — *Verification* (meets the requirement) or *Validation* (meets the
  intended purpose).
- **Related hazard** — the Module 6 hazard this requirement mitigates (`—` if none).

| Req | Realized by (Capella function) | Verified by | Verif. type | Related hazard |
|-----|--------------------------------|-------------|-------------|----------------|
| REQ-001 | Load image | Manual test | Verification | — |
| REQ-002 | Define entry & target | Manual test | Verification | — |
| REQ-003 | Define entry & target | Manual test | Verification | — |
| REQ-004 | Compute trajectory | `NeedlePathPlannerTest` (unit) + manual | Verification | — |
| REQ-005 | Verify clearance | `NeedlePathPlannerTest` (invalid-segment) + manual | Verification | Vessel puncture |
| REQ-006 | Verify clearance | `NeedlePathPlannerTest` (crossing / clear) + manual | Verification | Vessel puncture |
| REQ-007 | Display result | Manual test | Verification | Vessel puncture |
| REQ-008 | Display result | Manual test (visual) | Verification | Vessel puncture |
| REQ-009 | Verify clearance | `NeedlePathPlannerTest` (invalid-segment) + code review | Verification | Vessel puncture |
| REQ-010 | Display result | Manual test | Verification | — |
| REQ-011 | (platform constraint) | Inspection | Verification | — |
| REQ-012 | (coordinate constraint) | Code review | Verification | — |
| REQ-013 | Define entry & target / Verify clearance | Manual test | Verification | — |
| REQ-014 | Verify clearance | Manual test + code review | Verification | Vessel puncture |
| REQ-015 | Verify clearance | Manual test (real Decathlon data) | Verification | Vessel puncture |
| REQ-016 | Compute trajectory / Display result | Manual test | Verification | — |
| REQ-017 | Verify clearance / Display result | Manual test | Verification | Vessel puncture |
| REQ-018 | Verify clearance | `NeedlePathPlannerTest` (invalid-segment) + manual | Verification | Vessel puncture |
| REQ-019 | Verify clearance | Performance test (manual timing) | Verification | — |
| REQ-020 | (architecture constraint) | Code review | Verification | — |
| (Intended purpose) | — | Clinician usability / workflow review | **Validation** | — |

## Coverage notes (honest gaps)

- **Unit-tested today:** REQ-004, REQ-005, REQ-006, REQ-009, REQ-018 (via
  `NeedlePathPlannerTest`). Everything else relies on manual test / review.
- **REQ-015** (multi-segment) is currently verified only by manual testing on real
  Decathlon data; a dedicated multi-segment unit test is a sensible future addition.
- **REQ-019** (performance) has no automated timing test yet — manual observation only.
- The **validation** row is aspirational: no clinician has reviewed the workflow. In a
  real device file this is where formative/summative usability evaluation (IEC 62366-1)
  would sit.

# Module 5: Requirements Engineering (IREB) — in a Medical-Device Context

> **Status: ready.** This module turns the Capella model (Module 4) into a written
> **software requirements specification** plus a **traceability matrix**, structured the
> way the medical-device standards expect. It's the artifact that links *intended purpose*
> → *what the software must do* → *how it was verified* → *which risk it controls*.

> **Honesty note (read this).** What you build here is a **learning-scale** specification
> that *emulates the structure* of a real medical-device software requirements artifact.
> It is **not** a regulatory deliverable: there's no quality management system behind it,
> no formal review/approval, no full risk file. The value for a German medtech employer is
> that it shows you understand *how* requirements, standards, and traceability fit
> together — say exactly that in interviews, don't overclaim.

## What is this?

**Requirements engineering (RE)** is the systematic work of determining, writing down,
and managing *what a system must do and how well*. **IREB CPRE** publishes a free,
vendor-neutral Foundation syllabus that defines the vocabulary and the quality bar for a
good requirement. We **apply the practices, we don't sit the exam.**

A requirement is one testable sentence stating something the system must do, written so
precisely nobody can argue about whether it's met.

## The regulatory landscape (German / EU medtech)

In Germany the rules are the EU ones (plus national law like the *Medizinprodukte­durchführungs­gesetz, MPDG*). For **software** that is itself a medical device, these are the standards that govern requirements:

| Standard / regulation | What it governs | How it touches *requirements* |
|---|---|---|
| **EU MDR 2017/745** | Market access for medical devices in the EU | Demands a defined **intended purpose** and conformance to the **General Safety & Performance Requirements (GSPRs, Annex I)**. Software-as-a-medical-device (**MDSW**) is classified via **Rule 11**. |
| **ISO 13485** | Quality Management System | **Design controls**: requirements are the *design inputs*; verification checks design output against them. |
| **IEC 62304** | Medical device **software** lifecycle | The central one here. Requires a **software safety classification (A/B/C)**, a **software requirements analysis (§5.2)**, and **bidirectional traceability** (system req ↔ software req ↔ architecture ↔ test). |
| **ISO 14971** | Risk management (Module 6) | Every **risk control** must trace to a requirement. Risk controls *become* requirements. |
| **IEC 62366-1** | Usability engineering | Use-related requirements (avoiding *use error*) come from here — relevant to our "result must be clearly visible" requirements. |

The mental model: **MDR** says "you may sell it if it's safe and does what you claim";
**ISO 13485** is the process that produces the evidence; **IEC 62304** is that process
applied to software; **ISO 14971 / IEC 62366-1** feed safety- and use-related
requirements in. Your requirements spec is the hub they all connect to.

## Why it matters here

A clean, traceable requirements spec is the connective tissue of a device file, and it's
precisely the thinking German medtech roles screen for. For our needle planner:

- Module 4 Capella functions trace **into** requirements (each function → 1–4 reqs).
- Module 6 hazards and the verification methods trace **out of** them.
- The whole thing hangs off one **intended purpose** statement.

## Intended purpose (the root of everything)

Under MDR, requirements are *derived from* a stated intended purpose. Write it first. For
this project:

> **Intended purpose (draft):** *NeedlePathPlanner is research/educational software that
> assists a trained interventional radiologist in pre-procedure planning of a percutaneous
> needle trajectory on CT/MR images, by letting them define an entry and target point and
> flagging whether the planned straight-line path intersects a user-designated no-go
> structure (e.g. a vessel). It is a planning aid only; it does not control any device and
> the clinician remains responsible for the final decision.*

That last sentence matters — it's a **risk control by design** (human-in-the-loop), and it
affects the safety classification below.

## Software safety classification (IEC 62304)

IEC 62304 makes you classify the software by the **worst-case harm** if it fails:

- **Class A** — no injury possible.
- **Class B** — non-serious injury possible.
- **Class C** — death or serious injury possible.

**Reason it through for our tool:** a false "Clear" over a vessel could contribute to a
vessel puncture → internal bleeding → *serious* injury. Taken alone that points to
**Class C**. But it's a *planning aid* with a trained clinician making the final call and
independent intra-procedure imaging — those external risk controls reduce the residual
software risk. A defensible portfolio answer: **"I'd argue Class B given the mandatory
human-in-the-loop control, and document why; a conservative reviewer might hold it at C."**
Being able to *argue the classification* (not just state one) is the skill.

## Key terms

- **Functional requirement** — *what* the system does.
- **Non-functional / quality requirement** — *how well* (performance, usability,
  reliability, safety).
- **Constraint** — externally imposed restriction (must run in 3D Slicer; RAS
  coordinates).
- **Quality criteria** (IEC 62304 §5.2.6 echoes IREB): **unambiguous, verifiable, atomic,
  necessary, feasible, consistent, non-contradictory.**
- **"Shall"** — binding obligation (vs. should/may).
- **Requirement ID** — a *stable, never-reused* identifier (`REQ-006`); IEC 62304 requires
  each requirement be uniquely identifiable for traceability.
- **Verification vs. validation** — *verification* = "did we build it right?" (meets the
  requirement); *validation* = "did we build the right thing?" (meets the intended
  purpose / user need).
- **Bidirectional traceability** — you can go requirement → test *and* test → requirement;
  IEC 62304 wants both directions.
- **Risk control requirement** — a requirement that exists specifically to mitigate a
  hazard (ISO 14971); these are flagged so they aren't accidentally deleted.

## Step-by-step

Output: two files in `requirements/` — a **specification** and a **traceability matrix**.

1. **State the intended purpose** (above) at the top of the spec.
2. **Record the software safety classification** and the one-line justification.
3. **Derive requirements from the model** — walk each SA function and each known hazard;
   ask "what must the system *guarantee*?" IEC 62304 §5.2 prompts categories:
   functional capabilities, **inputs/outputs**, **interfaces**, **safety/risk controls**,
   and **use/usability**.
4. **Write each canonically:** `REQ-0xx — The system shall <one verifiable behaviour>.`
   Keep it **atomic**.
5. **Classify** (F / NF / C) and tag **risk-control** requirements.
6. **Assign a verification method:** manual test, unit test (`NeedlePathPlannerTest`),
   or review/inspection.
7. **Build the traceability matrix:** REQ → Capella function → verification → related
   hazard (Module 6).
8. **Save & commit** under `requirements/`.

### Example requirements (starter set — grounded in this project)

| ID | Requirement | Type | Risk control? |
|---|---|---|---|
| REQ-001 | The system shall let the user select one CT/MR volume as the planning image. | F | |
| REQ-002 | The system shall let the user place exactly one entry point. | F | |
| REQ-003 | The system shall let the user place exactly one target point. | F | |
| REQ-004 | The system shall compute a straight-line trajectory between the entry and target points. | F | |
| REQ-005 | The system shall require the user to explicitly select which segment is the no-go structure before a clearance result is given. | F | ✔ |
| REQ-006 | The system shall determine whether the trajectory intersects the selected no-go segment. | F | ✔ |
| REQ-007 | The system shall display a pass/fail clearance result before the user proceeds. | F | ✔ |
| REQ-008 | The clearance result shall be visually distinguishable (colour-coded clear vs. crosses) to avoid use error. | NF (usability, IEC 62366-1) | ✔ |
| REQ-009 | The system shall not display "Clear" unless a clearance computation has actually been performed against a selected segment. | NF (safety) | ✔ |
| REQ-010 | The system shall name the specific segment tested in the clearance result. | NF (usability) | |
| REQ-011 | The system shall run as a scripted module within 3D Slicer 5.x. | C | |
| REQ-012 | The system shall handle all point coordinates in the RAS coordinate system. | C | |

> **REQ-005 / REQ-009 are gold:** they came directly from the real `GetValue(0)` bug you
> fixed (a false "Clear"). A requirement that exists to prevent a failure you've actually
> seen — and that traces to a hazard — is the strongest evidence of design-for-safety
> thinking. Lead with that story in interviews.

### Traceability matrix shape

| Req | Realized by (Capella function) | Verified by | Verif. type | Related hazard (Module 6) |
|---|---|---|---|---|
| REQ-006 | Verify clearance | `NeedlePathPlannerTest` + manual test | Verification | Vessel puncture |
| REQ-007 | Display result | Manual test | Verification | Vessel puncture |
| REQ-009 | Verify clearance | Code review + manual test | Verification | Vessel puncture |
| (purpose) | — | Clinician usability check | Validation | — |

## Checkpoint

You're done with Module 5 when `requirements/` contains:

- An **intended purpose** statement and a recorded **software safety classification** with
  justification.
- **15–25 requirements**, each with a stable ID, a "shall" statement, a type, and
  risk-control tagging where relevant.
- A **traceability matrix** linking every requirement to a Capella function and a
  verification method, with the hazard column ready for Module 6.
- Every requirement passing the quality checklist (atomic, unambiguous, verifiable).

## Revision notes (worked Q&A)

Quick self-check material — the kind of thing an interviewer probes.

**1. The three requirement types, with a tell for each.**
- *Functional (F)* — what the system **does** ("shall compute a trajectory").
- *Non-functional / quality (NF)* — **how well** (performance, usability, reliability,
  safety; "shall colour-code the result").
- *Constraint (C)* — an externally **imposed restriction** you don't get to choose; tell:
  it names a specific technology/standard/environment.
  → *"The system shall run inside 3D Slicer 5.x" = Constraint.*

**2. Spotting a bad requirement.** Take *"The system shall quickly and clearly handle the
trajectory and segmentation."* Faults:
- *Not verifiable / ambiguous* — "quickly" (no number), "clearly" (subjective), "handle"
  (do what?). No objective pass/fail test possible.
- *Not atomic* — bundles two subjects (trajectory **and** segmentation) in one statement.
- *Vague verb* — "handle" hides the real action; good requirements name it
  ("compute", "display", "flag").
  → Fix by splitting into atomic, measurable requirements (e.g. "shall complete the
  clearance check within 2 s"; "shall colour-code clear vs. crosses").

**3. Why stable IDs (not document order).** Traceability links point at the ID — the
matrix, the tests, and the hazard table all reference `REQ-006`. If you numbered by
position, inserting one requirement renumbers everything below it and silently breaks
every trace link. Stable, never-reused IDs survive insertion/deletion/reordering. IEC
62304 requires each requirement be uniquely and persistently identifiable for this reason.

**4. Why our tool's safety class (B vs C) is arguable.** The deciding factor is the
**human-in-the-loop**: it's a *planning aid*; a trained radiologist reviews the plan and
independent intra-procedure imaging exists. IEC 62304 lets you count **risk controls
external to the software** when classifying — those controls keep the software from
*directly* causing serious harm, supporting **Class B**. Honest counter: a conservative
reviewer could hold it at **C** because a false "Clear" *could* contribute to serious
harm. The skill is *arguing and documenting* the classification, not memorising one answer.

**5. Verification vs. validation.** *Verification* = "did we build it right?" (the output
meets the requirement — e.g. unit test of `checkClearance()`). *Validation* = "did we
build the right thing?" (it meets the intended purpose / real clinical need — e.g. a
clinician confirms the workflow actually helps planning).

## The artifact

The completed spec lives in [`../../requirements/`](../../requirements/):
[`requirements.md`](../../requirements/requirements.md) (20 requirements) and
[`traceability-matrix.md`](../../requirements/traceability-matrix.md). A
standards-annotated study version is at
[`../requirements-spec.html`](../requirements-spec.html) — each requirement tagged with the
standard behind it, plus a per-standard reference section.

## Further resources

- [IREB CPRE Foundation Level syllabus (free PDF)](https://www.ireb.org/en/cpre/)
- [IEC 62304 overview](https://en.wikipedia.org/wiki/IEC_62304) — software lifecycle,
  safety classification, traceability
- [MDR 2017/745 & MDSW classification (Rule 11)](https://eur-lex.europa.eu/eli/reg/2017/745/oj)
- [IEC 62366-1](https://en.wikipedia.org/wiki/IEC_62366) — usability engineering for
  medical devices

# Software Requirements Specification — NeedlePathPlanner

> Learning-scale specification (not a regulatory deliverable) for the image-guided
> needle-insertion planning module. Structured per IREB / IEC 62304 §5.2. See
> [`../docs/guide/05-requirements-ireb.md`](../docs/guide/05-requirements-ireb.md) for the
> concepts, and [`../docs/requirements-spec.html`](../docs/requirements-spec.html) for a
> standards-annotated study version.

## Document conventions

- Each requirement uses a binding **"shall"** and a stable, never-reused ID (`REQ-0xx`).
- **Type:** `F` functional · `NF` non-functional (quality) · `C` constraint.
- **Risk control?** ✔ = this requirement exists to mitigate a hazard (see Module 6).
- **Standards basis** names the standard/clause the requirement chiefly satisfies.
- Each requirement is **atomic, unambiguous, and verifiable** (IREB quality criteria).

## Intended purpose

NeedlePathPlanner is research/educational software intended to assist a trained
interventional radiologist in planning a percutaneous needle path on a patient's CT/MR
images. Given a user-chosen skin **insertion (entry) point** and a **target** lesion
(e.g. a tumour), the software displays the straight-line needle trajectory between them
and indicates whether that path would intersect a user-designated **no-go structure**
such as a blood vessel — helping the clinician choose a route that reaches the target
without rupturing critical vessels in the surrounding area. It is intended to support
pre-procedure planning for percutaneous **surgery, intervention, and diagnostic**
procedures (e.g. biopsy or tumour ablation).

It is a **planning aid only**: it does not control any instrument, does not make the
clinical decision, and the radiologist remains fully responsible for reviewing the plan
and conducting the procedure. (This is a learning/portfolio project and is **not** a
clinically validated or regulatory-cleared medical device.)

## Software safety classification (IEC 62304)

**Class B** — justification: planning aid with a mandatory human-in-the-loop (the
radiologist reviews the plan and makes the final decision) and independent
intra-procedure imaging as external risk controls. A conservative reviewer could argue
Class C, since a false "Clear" could contribute to a vessel puncture (serious harm).

## Requirements

| ID | Requirement | Type | RC? | Standards basis |
|----|-------------|------|-----|-----------------|
| REQ-001 | The system shall let the user select one CT/MR volume as the planning image. | F | | IEC 62304 §5.2 |
| REQ-002 | The system shall let the user place exactly one entry point. | F | | IEC 62304 §5.2 |
| REQ-003 | The system shall let the user place exactly one target point. | F | | IEC 62304 §5.2 |
| REQ-004 | The system shall compute a straight-line trajectory between the entry and target points. | F | | IEC 62304 §5.2 |
| REQ-005 | The system shall require the user to explicitly select which segment is the no-go structure before a clearance result is given. | F | ✔ | ISO 14971 (risk control); IEC 62304 §5.2.2 |
| REQ-006 | The system shall determine whether the trajectory intersects the selected no-go segment. | F | ✔ | ISO 14971; IEC 62304 §5.2 |
| REQ-007 | The system shall display a pass/fail clearance result before the user proceeds. | F | ✔ | ISO 14971; IEC 62366-1 |
| REQ-008 | The clearance result shall be visually distinguishable (colour-coded clear vs. crosses). | NF (usability) | ✔ | IEC 62366-1 (use error) |
| REQ-009 | The system shall not display "Clear" unless a clearance computation has actually been performed against a selected segment. | NF (safety) | ✔ | ISO 14971; IEC 62304 §5.2.2 |
| REQ-010 | The system shall name the specific segment tested in the clearance result. | NF (usability) | | IEC 62366-1 |
| REQ-011 | The system shall run as a scripted module within 3D Slicer 5.x. | C | | Design constraint (IEC 62304 §5.1) |
| REQ-012 | The system shall handle all point coordinates in the RAS coordinate system. | C | | Design constraint |
| REQ-013 | The system shall allow the user to re-place the entry and/or target point and re-run the clearance check. | F | | IEC 62304 §5.2 |
| REQ-014 | The system shall not perform a clearance check unless both an entry and a target point have been placed, and shall inform the user when one is missing. | F | ✔ | ISO 14971; IEC 62304 §5.2 |
| REQ-015 | When the selected segmentation contains multiple segments, the system shall test the trajectory only against the user-selected segment. | F | ✔ | ISO 14971; IEC 62304 §5.2 |
| REQ-016 | The system shall display the planned trajectory length in millimetres. | F | | IEC 62304 §5.2 |
| REQ-017 | The system shall re-evaluate and update the clearance result each time the trajectory is re-planned. | F | ✔ | ISO 14971 (no stale result) |
| REQ-018 | The system shall report an error message, rather than crashing or producing a result, when given invalid input (e.g. a segmentation with no segments). | NF (reliability) | ✔ | IEC 62304 §5.2; ISO 14971 |
| REQ-019 | The clearance check shall return a result within 2 seconds for a no-go surface of up to ~100,000 triangles on a typical workstation. | NF (performance) | | IEC 62304 §5.2; MDR Annex I (performance) |
| REQ-020 | The system shall access the input volume and segmentation via the 3D Slicer MRML scene. | C | | Design constraint |

> **REQ-005 / REQ-009 / REQ-015** came directly from the real `GetValue(0)` bug that gave
> a false "Clear" — requirements that exist to prevent a failure actually observed.

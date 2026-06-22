# Systems-Engineering Model (Capella / Arcadia)

A Model-Based Systems Engineering (MBSE) description of the **image-guided needle
insertion planning** workflow — the same system implemented by the
[`NeedlePathPlanner`](../SlicerModule/MedVisExtension/NeedlePathPlanner) 3D Slicer module.

Built with [Capella](https://www.eclipse.org/capella/) using the **Arcadia** method.
See [`docs/guide/04-arcadia-capella.md`](../docs/guide/04-arcadia-capella.md) for the full
walkthrough and concepts.

## Contents

- `NeedlePlanningModel/` — the Capella project (`.capella` semantic model, `.aird`
  diagrams). Open it by pointing a Capella workspace at this folder and importing the
  project.
- `diagrams/` — exported snapshots of the key diagrams, viewable without Capella.

## The four Arcadia layers

| Layer | Diagram | Captures |
|---|---|---|
| Operational Analysis | OCB | The radiologist and the goal "perform safe percutaneous insertion" |
| System Analysis | SDFB | Five system functions: Load image → Define entry & target → Compute trajectory → **Verify clearance** → Display result |
| Logical Architecture | LAB | Components: Image Loader, Trajectory Planner, **Clearance Checker**, Viewer (functions allocated) |
| Physical Architecture | PAB | The real implementation: the `NeedlePathPlanner.py` scripted module |

## The traceability thread

The point of the model is a single navigable chain from clinical need to code:

> *Avoid critical vessels* (Operational) → *Verify clearance* (System function) →
> *Clearance Checker* (Logical component) → `checkClearance()` in `NeedlePathPlanner.py`
> (Physical).

This is what Modules 5 (requirements) and 6 (ISO 14971 hazard analysis) will trace
against.

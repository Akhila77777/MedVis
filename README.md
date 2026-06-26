# Image-Guided Needle Insertion Planning — Portfolio Project

A combined **systems engineering** + **medical visualization** portfolio project: a small
3D Slicer module for planning a percutaneous needle insertion (e.g. liver biopsy or
ablation), paired with a full set of systems-engineering artifacts that describe and
de-risk the *same* clinical workflow — from clinical hazard all the way down to the line
of code, and back.

See [`docs/plan.html`](docs/plan.html) for the goal, method stack, and roadmap. New to
these concepts? Start with the module-by-module [learning guide](docs/guide/00-overview.md).

## The traceability chain (what makes this project whole)

The point of the project is a single thread you can follow across every artifact — and
walk in *either* direction (ISO 14971 / IEC 62304 bidirectional traceability). Taking the
headline hazard as the example:

| Artifact (discipline) | Element | What it says |
|---|---|---|
| **Risk analysis** (ISO 14971) | **H-01 vessel puncture** | A planned path that crosses a vessel can cause laceration/haemorrhage → a risk control is required |
| **Requirement** (IREB) | **REQ-006** | "The system *shall* determine whether the trajectory intersects the selected no-go segment" |
| **Architecture** (Arcadia / Capella) | **"Verify clearance"** function | The system/logical function that realizes the requirement |
| **Code** (3D Slicer module) | **`checkClearance()`** | The implementation in `NeedlePathPlanner.py` |
| **Verification** | **`NeedlePathPlannerTest`** | Unit tests proving a line through the segment → crosses, clear → clear, invalid input → raises |

> The strongest part of the story: **REQ-005 / REQ-009 / REQ-015** exist because of a real
> bug — a hardcoded `GetValue(0)` that produced a false "Clear" against the wrong segment.
> A real failure, traced to a hazard, controlled by requirements, fixed in code, and locked
> down by tests.

Follow the thread in the artifacts themselves:
- 🛡️ Risk — [`risk-analysis/hazard-analysis.md`](risk-analysis/hazard-analysis.md) · study view: [`docs/risk-analysis.html`](docs/risk-analysis.html)
- 📋 Requirements + matrix — [`requirements/`](requirements/) · study view: [`docs/requirements-spec.html`](docs/requirements-spec.html)
- 🧩 Architecture model — [`se-model/`](se-model/) (Capella / Arcadia, 4 layers)
- 💻 Code + tests — [`SlicerModule/MedVisExtension/NeedlePathPlanner/NeedlePathPlanner.py`](SlicerModule/MedVisExtension/NeedlePathPlanner/NeedlePathPlanner.py) · tests study view: [`docs/unit-tests.html`](docs/unit-tests.html)

## What this project demonstrates

- **Software:** a Python scripted module for [3D Slicer](https://www.slicer.org/) that lets
  a user place an entry point and target on a CT volume, computes the needle trajectory, and
  checks it against a segmented "no-go" structure (e.g. a vessel) — with unit tests.
- **Systems engineering:**
  - An [Arcadia](https://www.eclipse.org/capella/arcadia.html) model in
    [Capella](https://www.eclipse.org/capella/): operational analysis → system functions →
    logical architecture → physical architecture.
  - An IREB-style requirements specification (20 requirements) with a traceability matrix
    linking each to a Capella function and a verification method.
  - An ISO 14971-style hazard analysis (four hazards) with risk controls tagged by the
    ISO 14971 hierarchy and linked back to requirement IDs.
- **Regulatory framing** for the EU/German medtech context (IEC 62304 software safety
  class, MDR intended purpose, IEC 62366-1 usability) — kept honest about its
  learning-scale scope.
- *(Stretch)* A MONAI-based U-Net segmentation on a public dataset, visualized in Slicer.

## Repository structure

```
.
├── docs/               Project plan, learning guide, and HTML study pages
├── SlicerModule/       Python scripted module for 3D Slicer (NeedlePathPlanner)
├── se-model/           Capella project (Arcadia model) + diagram snapshots
├── requirements/       Requirements specification + traceability matrix
├── risk-analysis/      ISO 14971 hazard analysis
└── ml/                 (optional) MONAI segmentation experiments
```

## Status

Core portfolio complete — software + the full SE/regulatory artifact set are in place and
traceable end to end.

| Module | Topic | Status |
|---|---|---|
| 1 | Version control | ✅ Done |
| 2 | 3D Slicer basics | In progress |
| 3 | Slicer Python module (+ unit tests) | ✅ Done |
| 4 | Arcadia / Capella model | ✅ Done |
| 5 | Requirements engineering (IREB) | ✅ Done |
| 6 | Risk management (ISO 14971) | ✅ Done |
| 7 | MONAI ML segmentation | Optional / stretch |

> **Honesty note:** this is a self-study portfolio that *emulates* the structure of a
> medical-device development file. It is not a regulated device — there is no quality
> management system, clinical data, or formal review behind it.

## License

TBD

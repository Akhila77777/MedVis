# Learning Guide: Overview

This is the starting point for the learning curriculum behind this project. Each module
below explains the **concepts** you need (what they are, why they matter here) and then
walks through the **hands-on steps** for that part of the project. Work through them in
order — each builds on the previous one.

If you just want the project roadmap/timeline view, see [`../plan.html`](../plan.html).
This guide is the "textbook" companion to that roadmap.

## The two halves of this project

1. **Build it** — a small 3D Slicer module that helps plan a percutaneous needle
   insertion: place an entry point and a target on a CT scan, draw the trajectory, and
   check whether it crosses a structure it shouldn't (e.g. a major vessel).
2. **Describe and de-risk it** — model that same workflow using professional
   systems-engineering methods: a Capella/Arcadia model, an IREB-style requirements
   spec with traceability, and an ISO 14971-style hazard analysis.

Both halves describe **the same system** — concepts you define in the SE artifacts
(functions, components, hazards) map directly onto things you build in the Slicer
module. That mapping *is* the portfolio piece.

## Modules

| # | Module | Covers | Status |
|---|--------|--------|--------|
| 1 | [Version control basics](01-version-control.md) | Git/GitHub setup | ✅ Done |
| 2 | [3D Slicer basics](02-slicer-basics.md) | Installing Slicer, medical image formats, the Slicer data model, getting a dataset | Ready |
| 3 | [Building a Slicer Python module](03-slicer-python-module.md) | Scripted modules, fiducials, trajectory line, vessel clearance check | Ready |
| 4 | [MBSE with Capella/Arcadia](04-arcadia-capella.md) | Model-based systems engineering, the Arcadia method, building the model | ✅ Done |
| 5 | [Requirements engineering (IREB)](05-requirements-ireb.md) | Writing requirements, traceability matrix | Outline |
| 6 | [Risk management (ISO 14971)](06-risk-iso14971.md) | Hazard analysis | Outline |
| 7 | [VTK/ITK deep dive](07-vtk-itk-deepdive.md) | Visualization pipeline, reproducing a technique from Preim's book | Outline |
| 8 | [MONAI deep learning (stretch)](08-monai-deep-learning.md) | U-Net segmentation, bridging ML and visualization | Outline |

**"Outline" modules** contain the structure (what you'll learn, key terms, the steps
ahead) but the full concept explanations are written just before you start that module
— so they reflect exactly what's been built so far and don't go stale.

## Recommended order

Modules 1–2 first (tooling + data), then module 3 (the core software deliverable).
Modules 4–6 (the SE artifacts) are easiest once module 3 exists, because they describe
*it*. Module 7 can happen alongside module 3. Module 8 is a stretch goal for the end.

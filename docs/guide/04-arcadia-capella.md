# Module 4: MBSE with Capella/Arcadia

> **Status: outline.** This module covers tasks #3 and #6 of the roadmap. Full concept
> explanations will be added when we start this module — what's below is the structure
> and the terms you'll need.

## What is this?

*(To be filled in: what MBSE is and how it differs from writing requirements as plain
documents; what Capella is (free, Eclipse-based, originally Thales); what "Arcadia" is
as a method.)*

## Why it matters here

This module produces a model of the **same workflow** built in Module 3, described
through four layers that go from "what the clinician needs" down to "what the software
component does" — directly traceable to the requirements (Module 5) and hazards
(Module 6).

## Key terms

- **MBSE (Model-Based Systems Engineering)** — describing a system through connected
  models/diagrams rather than free-text documents
- **Arcadia method** — the methodology Capella implements, with four analysis layers
- **Operational Analysis** — who needs to do what, and why (the clinician's
  perspective)
- **System Analysis** — what the system-to-be must do (functions)
- **Logical Architecture** — how those functions are grouped into logical components
- **Physical Architecture** — concrete components/interfaces (maps to actual code)
- **Capability / Mission** — high-level operational goals
- **Function / Functional Chain** — system behaviors and their sequencing
- **Traceability link** — explicit connection between model elements across layers

## Step-by-step (high level — to be expanded)

1. Install Capella (Product build, bundled Java) and run the in-tool Arcadia
   tutorial/welcome project.
2. Operational Analysis: capture "interventional radiologist needs to reach a target
   lesion without damaging major vessels."
3. System Analysis: define functions — acquire/load image, define entry & target,
   compute trajectory, verify clearance, display result.
4. Logical Architecture: group functions into logical components (Image Loader,
   Trajectory Planner, Clearance Checker, Viewer).
5. Physical Architecture: map logical components to the actual Slicer module
   structure from Module 3.

## Checkpoint

*(To be filled in.)*

## Further resources

- [Capella download](https://www.eclipse.org/capella/download.html)
- [Arcadia method overview](https://www.eclipse.org/capella/arcadia.html)

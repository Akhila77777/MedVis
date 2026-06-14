# Module 3: Building a Slicer Python Module

> **Status: ready.** This module covers tasks #4 and #5 of the roadmap. The full
> step-by-step build walkthrough — with reasoning, instructions, and the underlying
> concept for each step — lives in [`../steps.html`](../steps.html). This page stays as
> the conceptual summary/glossary; work through `steps.html` hands-on.

## What is this?

A **scripted module** is a Slicer module written in Python that plugs into the same
"Modules" menu as Slicer's built-in modules (Volume Rendering, Segment Editor, etc.).
Slicer's **Extension Wizard** scaffolds the boilerplate (file layout + required class
names) so your module is discovered and loaded automatically. The generated file
contains a Widget class (UI) and a Logic class (computation), kept separate so the
underlying logic can be tested and reused independently of the UI — see `steps.html`
Step 1 for the full breakdown.

## Why it matters here

This is the core software deliverable: a module that lets a user place an entry point
and a target on a loaded CT volume, draws the planned needle trajectory between them,
and checks whether that line crosses a segmented vessel ("no-go zone").

## Key terms

- **Scripted module** — a Python file + descriptor that Slicer loads as a UI panel
- **Extension Wizard** — Slicer's tool for scaffolding a new module
- **`vtkMRMLScene`** — the live data scene your module reads/writes
- **Markups / fiducial nodes** — how entry/target points are represented and read
- **`qt` widgets** — how the module's UI panel is built
- **Line–mesh intersection** — the geometric check for "does the trajectory cross the
  vessel?"
- **`vtkOBBTree` / `vtkModifiedBSPTree`** — VTK classes commonly used for
  intersection tests against a surface mesh

## Step-by-step

The detailed walkthrough (What / Why / How / Underlying concept for each step) is in
[`../steps.html`](../steps.html):

1. Scaffold a new scripted module with the Extension Wizard.
2. Add UI elements: volume/segmentation selectors, "place entry point" / "place target
   point" buttons, a "Plan trajectory" button, a result label.
3. On "Plan trajectory": read the two fiducial positions, create a line model between
   them.
4. Convert the vessel segmentation to a closed surface; test the line against it for
   intersection.
5. Display a pass ("clear") / fail ("crosses vessel") result.

## Checkpoint

See the checkpoint box at the end of Step 5 in [`../steps.html`](../steps.html): the
module appears in the Modules dropdown, you can place both points, the trajectory line
draws in the 3D view, and the result label correctly reports "Clear" vs. "Crosses
vessel" for at least one test case of each.

## Further resources

- [Slicer scripted module developer tutorial](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
- [Slicer Python scripting documentation](https://slicer.readthedocs.io/en/latest/developer_guide/python_faq.html)

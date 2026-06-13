# Module 3: Building a Slicer Python Module

> **Status: outline.** This module covers tasks #4 and #5 of the roadmap. Full concept
> explanations will be added when we start this module — what's below is the structure
> and the terms you'll need.

## What is this?

*(To be filled in: scripted modules vs. built-in modules, the Extension Wizard, the
anatomy of a scripted module file.)*

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

## Step-by-step (high level — to be expanded)

1. Scaffold a new scripted module with the Extension Wizard.
2. Add UI elements: volume/segmentation selectors, "place entry point" / "place target
   point" buttons, a "Plan trajectory" button, a result label.
3. On "Plan trajectory": read the two fiducial positions, create a line model between
   them.
4. Convert the vessel segmentation to a closed surface; test the line against it for
   intersection.
5. Display a pass ("clear") / fail ("crosses vessel") result.

## Checkpoint

*(To be filled in.)*

## Further resources

- [Slicer scripted module developer tutorial](https://slicer.readthedocs.io/en/latest/developer_guide/script_repository.html)
- [Slicer Python scripting documentation](https://slicer.readthedocs.io/en/latest/developer_guide/python_faq.html)

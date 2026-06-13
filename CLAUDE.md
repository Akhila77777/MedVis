# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project overview

This repo is a self-study portfolio project combining medical visualization software
with systems-engineering artifacts for the same workflow (image-guided needle insertion
planning). See [`README.md`](README.md) and [`docs/plan.html`](docs/plan.html) for the
full plan and roadmap.

Planned structure:

```
.
├── docs/               Project plan, write-ups
├── slicer-module/      Python scripted module for 3D Slicer
├── se-model/           Capella project (Arcadia model)
├── requirements/       Requirements specification + traceability matrix
├── risk-analysis/      ISO 14971 hazard analysis
└── ml/                  Optional MONAI segmentation experiments
```

## Working alongside other agents

The user works on multiple files/areas of this project at once, sometimes with
multiple Claude Code sessions running in parallel (one per area, e.g. one on the
Slicer module, one on the SE docs).

- **Do not edit a file that another agent/session is currently working on.** If you're
  unsure whether a file is in active use elsewhere, ask the user before modifying it.
- Stick to the area of the project you were asked to work on. Avoid making
  "drive-by" edits to unrelated files (e.g. don't touch `requirements/` while working
  on `slicer-module/`) unless explicitly asked.
- Before committing, run `git status` / `git diff` and double-check that staged
  changes only include files relevant to the current task — this helps avoid
  accidentally including another session's in-progress edits.

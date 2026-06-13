# Image-Guided Needle Insertion Planning — Portfolio Project

A combined **systems engineering** + **medical visualization** portfolio project: a small
3D Slicer module for planning a percutaneous needle insertion (e.g. liver biopsy or
ablation), paired with a full set of systems-engineering artifacts that describe and
de-risk the same clinical workflow.

See [`docs/plan.html`](docs/plan.html) for the full explanation of the goal, the
method stack, tool installation, and the week-by-week roadmap. New to these concepts?
Start with the module-by-module [learning guide](docs/guide/00-overview.md).

## What this project demonstrates

- **Software:** a Python scripted module for [3D Slicer](https://www.slicer.org/) that
  lets a user place an entry point and target on a CT volume, computes the needle
  trajectory, and checks it against a segmented "no-go" structure (e.g. a vessel).
- **Systems engineering:**
  - An [Arcadia](https://www.eclipse.org/capella/arcadia.html) model in
    [Capella](https://www.eclipse.org/capella/) covering operational analysis → system
    functions → logical architecture → physical architecture.
  - An IREB-style requirements specification with a traceability matrix linking
    requirements to model elements.
  - An ISO 14971-style hazard analysis (hazard → cause → effect → severity/probability
    → mitigation → linked requirement).
- *(Stretch)* A MONAI-based U-Net segmentation on a public dataset, visualized in Slicer.

## Repository structure

```
.
├── docs/               Project plan, write-ups (this is the HTML documentation)
├── slicer-module/      Python scripted module for 3D Slicer
├── se-model/           Capella project (Arcadia model)
├── requirements/       Requirements specification + traceability matrix
├── risk-analysis/      ISO 14971 hazard analysis
└── ml/                  Optional MONAI segmentation experiments
```

## Status

🚧 Just getting started — see [`docs/plan.html`](docs/plan.html) for the roadmap.

## License

TBD

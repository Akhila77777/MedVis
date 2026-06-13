# Module 7: VTK/ITK Deep Dive

> **Status: outline.** This module covers task #9 of the roadmap. Full concept
> explanations will be added when we start this module — what's below is the structure
> and the terms you'll need.

## What is this?

*(To be filled in: the VTK visualization pipeline (source → filter → mapper → actor),
and how it relates to the techniques covered in Preim & Botha's *Visual Computing for
Medicine*.)*

## Why it matters here

Reproducing a technique from the textbook (rather than just calling a high-level Slicer
feature) demonstrates you understand *how* medical visualization works underneath the
tools — directly relevant to a visualization research group.

## Key terms

- **Visualization pipeline** — source → filter(s) → mapper → actor → renderer
- **Marching cubes** — algorithm for extracting a surface mesh from a volume
  (isosurface extraction)
- **Transfer function** — mapping from voxel intensity to color/opacity, used in
  volume rendering
- **Volume rendering vs. surface rendering** — rendering the full 3D data directly vs.
  extracting and rendering a mesh
- **Isosurface / iso-value** — the threshold value used for surface extraction

## Step-by-step (high level — to be expanded)

1. Pick one technique from the relevant chapter(s) of *Visual Computing for Medicine*
   (e.g. marching cubes surface extraction, or a custom transfer function for volume
   rendering).
2. Implement it using VTK (either inside a Slicer scripted module or as a standalone
   Python/VTK script).
3. Apply it to the dataset from Module 2 and compare against Slicer's built-in
   equivalent.

## Checkpoint

*(To be filled in.)*

## Further resources

- [VTK examples](https://examples.vtk.org/site/)
- Preim & Botha, *Visual Computing for Medicine* (relevant chapters on visualization
  pipelines, isosurfaces, and transfer functions)

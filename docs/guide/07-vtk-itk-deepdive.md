# Module 7: VTK/ITK Deep Dive

> **Status: ready.** This module goes *under the hood* of medical visualization: instead of
> clicking a Slicer button, you build the visualization pipeline yourself in VTK and
> reproduce a classic technique (surface extraction via marching cubes) from Preim &
> Botha's *Visual Computing for Medicine*. The payoff: you can explain *how* the rendering
> works, not just that Slicer does it.

## What is this?

- **VTK (Visualization Toolkit)** is the C++/Python library that does the actual 3D
  graphics inside 3D Slicer (and ParaView, and much of medical-imaging research). You've
  already used pieces of it in the needle planner — `vtkLineSource`, `vtkOBBTree`,
  `vtkPolyData`.
- **ITK (Insight Toolkit)** is its sibling for *image processing*: filtering,
  segmentation, registration on n-dimensional images. Slicer uses ITK to read many formats
  and to run image filters.

Rough division of labour: **ITK processes the image, VTK renders it.** This module is
mostly VTK (the rendering), with ITK/SimpleITK optionally doing a preprocessing step.

> **Why this is the most research-relevant module for you:** reproducing a textbook
> technique from scratch is exactly what a visualization research group looks for — and
> Preim's group is at your university (OvGU Magdeburg). This is strong material for a thesis
> pitch or a research-assistant application.

## The VTK visualization pipeline (the core mental model)

Everything in VTK is a pipeline. Data flows left to right:

> **Source** → **Filter(s)** → **Mapper** → **Actor** → **Renderer** → **RenderWindow** (+ **Interactor**)

- **Source** — where data enters: a reader (`vtkNIFTIImageReader`) or a generator
  (`vtkLineSource`, `vtkCubeSource` — you used these).
- **Filter** — transforms data: marching cubes, smoothing, decimation.
- **Mapper** — turns data into graphics primitives (`vtkPolyDataMapper`).
- **Actor** — the mapper plus *appearance* (color, opacity, line width). You set color on a
  model's display node in Slicer; that's the actor layer.
- **Renderer** — collects actors and draws them; lives inside a **RenderWindow**.
- **Interactor** — handles mouse/keyboard so you can rotate/zoom.

Slicer hides most of this behind its node model, but it's all VTK underneath. Doing it by
hand is the whole point of this module.

## Surface rendering vs. volume rendering

Two fundamentally different ways to see 3D image data:

| | Surface rendering | Volume rendering |
|---|---|---|
| Idea | Extract a **mesh** at a threshold, draw polygons | Ray-cast through the **whole volume**, no mesh |
| Technique | Marching cubes (isosurface) | Transfer function + ray casting |
| Good for | Well-defined boundaries (bone, a segmented organ/vessel) | Showing internal structure, soft-tissue gradients |
| Cost | Cheap once extracted | More expensive (samples the full volume) |

## Key terms

- **Isosurface / iso-value** — the surface of constant intensity you extract (e.g. ~300 HU
  ≈ bone in CT). The iso-value *is* the threshold.
- **Marching cubes** — the classic isosurface algorithm: it "marches" through each cube of
  8 neighbouring voxels, checks which corners are above/below the iso-value (256 cases,
  reduced to 15 by symmetry), and emits the triangles where the surface cuts that cube. VTK:
  `vtkMarchingCubes` (or the faster `vtkFlyingEdges3D`).
- **Transfer function** — for volume rendering, the mapping from voxel intensity to
  **colour** (`vtkColorTransferFunction`) and **opacity** (`vtkPiecewiseFunction`). Designing
  it (air transparent, bone opaque) is the craft of volume rendering.
- **Decimation / smoothing** — marching-cubes meshes are dense and "stair-stepped";
  `vtkWindowedSincPolyDataFilter` smooths and `vtkDecimatePro` reduces triangle count.

## Step-by-step (the hands-on)

The deliverable is a small standalone **VTK Python script** that extracts and renders an
isosurface from the Module 2 dataset, plus a short note comparing it to Slicer's built-in.

1. **Load a volume.** Read the CT (or the segmentation labelmap) with `vtkNIFTIImageReader`.
2. *(Optional)* **Smooth** with a Gaussian (`vtkImageGaussianSmooth` or SimpleITK) to reduce
   marching-cubes noise.
3. **Marching cubes.** Run `vtkFlyingEdges3D` at a chosen iso-value → a `vtkPolyData` surface.
4. **Clean up the mesh.** Smooth (`vtkWindowedSincPolyDataFilter`) and optionally decimate.
5. **Render.** Mapper → actor (set colour/opacity) → renderer → render window → interactor;
   rotate it.
6. **Compare.** Do the same in Slicer (Segment Editor → *Show 3D*, or the Volume Rendering
   module) and note what the built-in does for you that your script did by hand.

> **Project tie-in:** extract the **vessel surface from the segmentation** — that's the same
> "no-go structure" your needle planner checks against. Module 7 then shows you *building*
> the very mesh that `checkClearance()` consumed via `GetClosedSurfaceRepresentation()` in
> Module 3.

## Checkpoint

You're done when you have:
- A working VTK script that loads the dataset, runs marching cubes, and renders the
  isosurface interactively.
- A short written comparison to Slicer's built-in surface/volume rendering, naming each
  pipeline stage (source → filter → mapper → actor → renderer).
- A one-line explanation of how this connects to the closed-surface mesh used in the
  clearance check.

## Further resources

- [VTK examples (Python)](https://examples.vtk.org/site/) — especially *Medical* and
  *PolyData* sections
- Preim & Botha, *Visual Computing for Medicine* — chapters on the visualization pipeline,
  isosurface extraction, and transfer functions
- [vtkFlyingEdges3D](https://vtk.org/doc/nightly/html/classvtkFlyingEdges3D.html) /
  [vtkMarchingCubes](https://vtk.org/doc/nightly/html/classvtkMarchingCubes.html)

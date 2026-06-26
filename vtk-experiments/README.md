# VTK Experiments (Module 7)

Hands-on VTK visualization, built by hand to understand what 3D Slicer does under the hood.
See [`../docs/guide/07-vtk-itk-deepdive.md`](../docs/guide/07-vtk-itk-deepdive.md) for the
concepts.

## `marching_cubes.py`

Extracts the **vessel surface** from a Task08 (Hepatic Vessel) label map using an explicit
VTK pipeline (read → threshold → smooth → marching cubes → mesh smooth → mapper → actor →
renderer). This is the same "no-go" mesh the needle planner checked against in Module 3.

**Run inside Slicer's Python console:**
1. Edit `SEG_PATH` in the script to point at your label file, e.g.
   `.../Task08_HepaticVessel/labelsTr/hepaticvessel_248.nii.gz`.
2. Paste:
   ```python
   exec(open(r"D:/MedVis/vtk-experiments/marching_cubes.py").read())
   ```
3. The vessel mesh appears in Slicer's 3D view; rotate it with the mouse.

It also runs standalone (`python marching_cubes.py`) if `vtk` is pip-installed — it opens
its own render window instead.

## Compare with Slicer's built-in (the learning point)

Load the same label map as a Segmentation in Slicer, then Segment Editor → **Show 3D**.
Slicer runs essentially this same pipeline (marching cubes + smoothing) for you behind one
button. Doing it by hand shows each stage you otherwise never see.

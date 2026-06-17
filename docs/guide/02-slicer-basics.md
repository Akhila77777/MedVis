# Module 2: 3D Slicer Basics

## What is this?

[3D Slicer](https://www.slicer.org/) is a free, open-source desktop application for
medical image analysis and visualization. It's built on two lower-level C++ libraries
that you'll hear about constantly in this field:

- **VTK** (Visualization Toolkit) — handles rendering: turning data (images, meshes,
  points) into pictures on screen. 3D views, slice views, volume rendering, surface
  models all go through VTK.
- **ITK** (Insight Toolkit) — handles image *processing*: filters, segmentation
  algorithms, registration (aligning two images), resampling, etc.

Slicer wraps both of these in a desktop app with a UI, and bundles its own Python 3.9
interpreter with VTK/ITK/numpy already wired up. You write small Python files
("scripted modules") that plug into the app and get full access to whatever data is
loaded — that's how you'll build the needle-planning tool in Module 3.

## Why it matters here

Slicer is your entire workspace for the technical half of this project: loading CT
scans, viewing them, segmenting structures, and running your custom module. Getting
comfortable with its UI and data model now makes Module 3 much easier.

## Module types: how custom code plugs into Slicer

When you use the **Extension Wizard** to create a new module (Module 3), it asks you to
pick a **type**. These are the six options and what they mean:

| Type | What it is | When you'd use it |
|---|---|---|
| **cli** | A standalone command-line executable (usually C++) that Slicer runs as a *separate process*, with a GUI auto-generated from an XML description of its parameters. | Long-running batch computations (registration, filtering) that shouldn't block Slicer's UI, or that need to run outside Slicer too. |
| **loadable** | A C++ module compiled into a shared library and loaded directly into Slicer's process, with full low-level access to MRML/VTK/Qt. | Performance-critical modules, or when you need C++-only libraries. Requires a full Slicer SDK build (CMake, compiler) — heavy to set up. |
| **loadablecustommarkups** | A specialized loadable-module template for adding a brand-new *type* of Markups annotation (e.g. a custom ROI shape). | Niche — extending the Markups toolset with a new annotation type. |
| **scripted** | A Python file, loaded directly by Slicer's built-in Python interpreter at runtime. Same access to the MRML scene/VTK/Qt as C++ modules (via PythonQt), but no compilation step. | General-purpose custom modules and prototyping — **this is what we use for the needle-planning module.** |
| **scriptedcli** | Like `cli`, but the executable is a Python script instead of C++. | Long-running Python computations run out-of-process (e.g. heavy MONAI inference) with an auto-generated GUI. |
| **scriptedsegmenteditoreffect** | A Python template for adding a new *tool/brush* to the Segment Editor's effect list. | Custom segmentation tools only. |

**Why Module 3 uses `scripted`:** no C++ toolchain or build step is needed — edit the
`.py` file and click "Reload" in Slicer to see changes instantly. Python has full access
to everything the project needs: the MRML scene, Markups/fiducial nodes, VTK geometry
classes (`vtkOBBTree`, etc.) for the intersection test, and Qt widgets for the UI. The
computation itself (placing two points, building a line, one intersection test) is fast
enough to run directly in the UI thread, so the heavier `cli`/`loadable` options would
be unnecessary overhead.

## Key terms

- **DICOM:** the standard file format/protocol hospitals use to store and exchange
  medical images (CT, MRI, etc.). A single scan is often hundreds of individual DICOM
  files (one per slice).
- **NIfTI (`.nii` / `.nii.gz`):** a simpler single-file format for 3D medical images,
  very common in research datasets (including the Medical Segmentation Decathlon).
  Slicer can load both DICOM and NIfTI.
- **Volume:** a 3D grid of intensity values (e.g. a CT scan) — the main thing you load
  and view.
- **Segmentation:** a labeling of *which voxels belong to which structure* (e.g.
  "liver", "vessel", "background"). Created either manually, with built-in tools, or by
  an algorithm (like the MONAI stretch goal in Module 8).
- **Markups (fiducials):** points, lines, or other annotations placed on top of a
  volume — this is how you'll mark "entry point" and "target point" in Module 3.
- **Scene (`vtkMRMLScene`):** Slicer's internal data structure holding everything
  that's currently loaded (volumes, segmentations, markups, models). Your Python module
  reads/writes this scene.
- **Slice views vs. 3D view:** Slicer shows three 2D cross-sections (axial/sagittal/
  coronal, conventionally colored red/yellow/green) plus a 3D view for volume rendering
  and surface models.

## Step-by-step

### A. Install 3D Slicer

1. **Download:** Go to [download.slicer.org](https://download.slicer.org/) and get the
   **stable release** for Windows (~600MB installer).
2. **Install:** Run the installer with default options.
3. **First launch:** You'll see the Modules dropdown (top toolbar), slice views (left),
   and the 3D view (right).
4. **Run the built-in tutorial:** `Help > Tutorials`, or visit
   [training.slicer.org](https://training.slicer.org/). Start with the "Welcome to 3D
   Slicer" tutorial. It covers:
   - Loading a sample dataset (`File > Sample Data`, e.g. "CTChest" or "MRHead")
   - Navigating slice views and the 3D view
   - Using the **Markups** module to place a fiducial point — this is exactly what
     Module 3's script will do programmatically
   - Basic volume rendering
5. **Try the Python console:** `View > Python Console` (or the `>>>` icon, bottom
   right). Run:
   ```python
   slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')
   ```
   This lists loaded volumes — confirming you can script against the scene.

### B. Get a working dataset (Medical Segmentation Decathlon)

The [Medical Segmentation Decathlon](http://medicaldecathlon.com/) provides public CT
datasets with ground-truth segmentations — exactly the kind of organ + vessel data this
project needs.

1. Download **Task03_Liver** or **Task08_HepaticVessel** (Task08 is a good fit since it
   includes vessel segmentations directly — useful for the "no-go zone" in Module 3).
2. Each task is a `.tar` containing `imagesTr/` (CT volumes, `.nii.gz`) and
   `labelsTr/` (corresponding segmentation masks).
3. In Slicer, use `File > Add Data` (or drag-and-drop) to load one `imagesTr/*.nii.gz`
   volume and its matching `labelsTr/*.nii.gz` segmentation. The segmentation should
   load as a **Segmentation** node and can be shown as an outline in the slice views or
   a 3D surface.

## Checkpoint

You can:
- Load a CT volume (sample data or from the Decathlon) and navigate it in the slice and
  3D views.
- Load a matching segmentation and toggle its visibility.
- Place a fiducial point via the Markups module.
- Run a one-line command in the Python console that lists loaded volumes.

## Further resources

- [Slicer training materials](https://training.slicer.org/)
- [Slicer documentation](https://slicer.readthedocs.io/)
- [Medical Segmentation Decathlon](http://medicaldecathlon.com/)

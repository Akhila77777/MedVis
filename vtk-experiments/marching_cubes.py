"""
Module 7 (VTK/ITK deep dive) — marching-cubes surface extraction, by hand.

Reproduces what Slicer's "Show 3D" does for you, but built explicitly as a VTK
visualization pipeline so you can see every stage:

    Source (read NIfTI)  ->  Filters (threshold -> smooth -> marching cubes -> mesh smooth)
                          ->  Mapper -> Actor -> Renderer -> RenderWindow

It extracts the *vessel* surface from a Task08 (Hepatic Vessel) label map — the same
"no-go structure" that the needle planner's checkClearance() consumed in Module 3.

HOW TO RUN (inside Slicer's Python console):
    1. Set SEG_PATH below to your label file, e.g.
       .../Task08_HepaticVessel/labelsTr/hepaticvessel_248.nii.gz
    2. Paste this into the Python console:
       exec(open(r"D:/MedVis/vtk-experiments/marching_cubes.py").read())
    The vessel mesh is added to Slicer's 3D view. Rotate it with the mouse.

It also runs standalone (python marching_cubes.py) if `vtk` is pip-installed — it
opens its own render window instead.
"""

import vtk

# --- configure -------------------------------------------------------------
SEG_PATH = r"D:/MedVisData/Task08_HepaticVessel/labelsTr/hepaticvessel_248.nii.gz"
LABEL_VALUE = 1        # 1 = vessel, 2 = tumor in the Task08 Hepatic Vessel labels
ISO_VALUE = 0.5        # halfway between background (0) and foreground (1) after thresholding

# --- 1. SOURCE: read the label volume from disk ----------------------------
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(SEG_PATH)
reader.Update()

# --- 2. FILTER: isolate just the chosen label as a clean 0/1 mask ----------
# Marching cubes at iso 0.5 would otherwise grab every label > 0.5 (vessel AND tumor).
threshold = vtk.vtkImageThreshold()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdBetween(LABEL_VALUE, LABEL_VALUE)
threshold.SetInValue(1.0)
threshold.SetOutValue(0.0)
threshold.ReplaceInOn()
threshold.ReplaceOutOn()
threshold.SetOutputScalarTypeToFloat()
threshold.Update()

# --- 3. FILTER: light Gaussian smoothing to soften voxel "stair steps" -----
gauss = vtk.vtkImageGaussianSmooth()
gauss.SetInputConnection(threshold.GetOutputPort())
gauss.SetStandardDeviations(1.0, 1.0, 1.0)
gauss.SetRadiusFactors(1.5, 1.5, 1.5)
gauss.Update()

# --- 4. FILTER: marching cubes (Flying Edges = fast modern variant) --------
# This is the heart of the module: it walks every cube of 8 voxels and emits the
# triangles where the iso-surface (0.5) cuts through, turning a voxel volume into a mesh.
mc = vtk.vtkFlyingEdges3D()
mc.SetInputConnection(gauss.GetOutputPort())
mc.SetValue(0, ISO_VALUE)
mc.ComputeNormalsOn()
mc.Update()

if mc.GetOutput().GetNumberOfPoints() == 0:
    raise RuntimeError(
        "Marching cubes produced an empty mesh. Check SEG_PATH points to a real label "
        "file and that LABEL_VALUE ({}) exists in it.".format(LABEL_VALUE))

# --- 5. FILTER: smooth the extracted mesh ----------------------------------
meshSmooth = vtk.vtkWindowedSincPolyDataFilter()
meshSmooth.SetInputConnection(mc.GetOutputPort())
meshSmooth.SetNumberOfIterations(20)
meshSmooth.SetPassBand(0.1)
meshSmooth.BoundarySmoothingOff()
meshSmooth.FeatureEdgeSmoothingOff()
meshSmooth.NonManifoldSmoothingOn()
meshSmooth.NormalizeCoordinatesOn()
meshSmooth.Update()

normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(meshSmooth.GetOutputPort())
normals.SetFeatureAngle(60.0)
normals.Update()

surface = normals.GetOutput()
print("[marching_cubes] vessel surface: {} points, {} triangles".format(
    surface.GetNumberOfPoints(), surface.GetNumberOfCells()))

# --- 6. MAPPER + ACTOR: geometry -> something drawable with appearance -----
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.85, 0.10, 0.10)   # vessel red
actor.GetProperty().SetOpacity(1.0)

# --- 7. RENDERER + WINDOW: show it -----------------------------------------
try:
    import slicer  # running inside Slicer: reuse its 3D render window (no Qt conflict)
    renderer = (slicer.app.layoutManager()
                .threeDWidget(0).threeDView()
                .renderWindow().GetRenderers().GetItemAsObject(0))
    renderer.AddActor(actor)
    renderer.ResetCamera()
    slicer.app.layoutManager().threeDWidget(0).threeDView().renderWindow().Render()
    print("[marching_cubes] added the vessel actor to Slicer's 3D view — rotate it with the mouse.")
except ImportError:
    # standalone: build our own renderer/window/interactor
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.2)
    renderer.ResetCamera()

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(900, 700)
    renderWindow.SetWindowName("Module 7 — vessel isosurface (marching cubes)")

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    renderWindow.Render()
    interactor.Start()

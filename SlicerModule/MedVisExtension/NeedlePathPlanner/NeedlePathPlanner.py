import logging
import math
import os
import vtk

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
)

from slicer import vtkMRMLScalarVolumeNode


#
# NeedlePathPlanner
#


class NeedlePathPlanner(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("NeedlePathPlanner")  # TODO: make this more human readable by adding spaces
        # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "Examples")]
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        # _() function marks text as translatable to other languages
        self.parent.helpText = _("""
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#NeedlePathPlanner">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#


def registerSampleData():
    """Add data sets to Sample Data module."""
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData

    iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # NeedlePathPlanner1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="NeedlePathPlanner",
        sampleName="NeedlePathPlanner1",
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, "NeedlePathPlanner1.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames="NeedlePathPlanner1.nrrd",
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        # This node name will be used when the data set is loaded
        nodeNames="NeedlePathPlanner1",
    )

    # NeedlePathPlanner2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="NeedlePathPlanner",
        sampleName="NeedlePathPlanner2",
        thumbnailFileName=os.path.join(iconsPath, "NeedlePathPlanner2.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames="NeedlePathPlanner2.nrrd",
        checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        # This node name will be used when the data set is loaded
        nodeNames="NeedlePathPlanner2",
    )


#
# NeedlePathPlannerParameterNode
#


@parameterNodeWrapper
class NeedlePathPlannerParameterNode:
    """The CT volume the needle path is planned on."""

    inputVolume: vtkMRMLScalarVolumeNode


#
# NeedlePathPlannerWidget
#


class NeedlePathPlannerWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/NeedlePathPlanner.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = NeedlePathPlannerLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.placeEntryButton.connect("clicked(bool)", self.onPlaceEntryButton)
        self.ui.placeTargetButton.connect("clicked(bool)", self.onPlaceTargetButton)
        self.ui.planTrajectoryButton.connect("clicked(bool)", self.onPlanTrajectoryButton)

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self) -> None:
        """Called when the application closes and the module widget is destroyed."""
        self.removeObservers()

    def enter(self) -> None:
        """Called each time the user opens this module."""
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """Called each time the user opens a different module."""
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None

    def onSceneStartClose(self, caller, event) -> None:
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """Ensure parameter node exists and observed."""
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

        # Select default input nodes if nothing is selected yet to save a few clicks for the user
        if not self._parameterNode.inputVolume:
            firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
            if firstVolumeNode:
                self._parameterNode.inputVolume = firstVolumeNode

    def setParameterNode(self, inputParameterNode: NeedlePathPlannerParameterNode | None) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)

    def onPlaceEntryButton(self) -> None:
        """Start interactive placement of the needle entry point."""
        self.logic.startPlacingPoint("EntryPoint")

    def onPlaceTargetButton(self) -> None:
        """Start interactive placement of the needle target point."""
        self.logic.startPlacingPoint("TargetPoint")

    def onPlanTrajectoryButton(self) -> None:
        """Draw the trajectory line and check it against the selected segmentation."""
        with slicer.util.tryWithErrorDisplay(_("Failed to plan trajectory."), waitCursor=True):
            self.logic.planTrajectory()

            trajectoryModel = slicer.mrmlScene.GetFirstNodeByName("TrajectoryLine")
            segmentationNode = self.ui.segmentationSelector.currentNode()
            segmentId = self.ui.segmentationSelector.currentSegmentID()
            if segmentationNode and segmentId:
                # Human-readable name of the chosen segment (e.g. "Segment_1"), so the
                # result reports exactly what was tested instead of always saying "vessel".
                segment = segmentationNode.GetSegmentation().GetSegment(segmentId)
                segmentName = segment.GetName() if segment else segmentId
                logging.info(f"[NeedlePathPlanner] Checking clearance against segmentation "
                             f"'{segmentationNode.GetName()}', segment '{segmentName}'")
                crossesVessel = self.logic.checkClearance(segmentationNode, segmentId)
                logging.info(f"[NeedlePathPlanner] Result: {'CROSSES' if crossesVessel else 'CLEAR'}")
                if crossesVessel:
                    self.ui.resultLabel.setText(f"Crosses '{segmentName}' — re-plan")
                    self.ui.resultLabel.setStyleSheet("color: #b91c1c; font-weight: bold;")
                    if trajectoryModel and trajectoryModel.GetDisplayNode():
                        trajectoryModel.GetDisplayNode().SetColor(0.8, 0.1, 0.1)  # red
                else:
                    self.ui.resultLabel.setText(f"Clear of '{segmentName}'")
                    self.ui.resultLabel.setStyleSheet("color: #15803d; font-weight: bold;")
                    if trajectoryModel and trajectoryModel.GetDisplayNode():
                        trajectoryModel.GetDisplayNode().SetColor(0.1, 0.7, 0.1)  # green
            else:
                logging.info("[NeedlePathPlanner] No segmentation/segment selected — trajectory drawn without a clearance check")
                self.ui.resultLabel.setText("Trajectory drawn (select a segmentation + segment to check clearance)")
                self.ui.resultLabel.setStyleSheet("")


#
# NeedlePathPlannerLogic
#


class NeedlePathPlannerLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return NeedlePathPlannerParameterNode(super().getParameterNode())

    def startPlacingPoint(self, nodeName: str) -> None:
        """
        Create (or reuse) a single-point fiducial node called `nodeName` and put
        the application into interactive "Place" mode so the next click in a
        slice/3D view drops a point into that node.
        """
        fiducialNode = slicer.mrmlScene.GetFirstNodeByName(nodeName)
        if not fiducialNode:
            fiducialNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", nodeName)
            fiducialNode.CreateDefaultDisplayNodes()
            logging.info(f"[NeedlePathPlanner] Created new fiducial node '{nodeName}'")
        else:
            logging.info(f"[NeedlePathPlanner] Reusing fiducial node '{nodeName}' "
                         f"(clearing {fiducialNode.GetNumberOfControlPoints()} existing point(s))")

        # Clear any previous point so clicking the button again lets the user redo it
        fiducialNode.RemoveAllControlPoints()

        selectionNode = slicer.app.applicationLogic().GetSelectionNode()
        selectionNode.SetActivePlaceNodeID(fiducialNode.GetID())
        interactionNode = slicer.app.applicationLogic().GetInteractionNode()
        interactionNode.SetCurrentInteractionMode(interactionNode.Place)
        logging.info(f"[NeedlePathPlanner] Entered place mode for '{nodeName}' — click in a slice/3D view")

    def planTrajectory(self) -> None:
        """
        Read the entry and target point positions and draw a line model between them.
        """
        entryNode = slicer.mrmlScene.GetFirstNodeByName("EntryPoint")
        targetNode = slicer.mrmlScene.GetFirstNodeByName("TargetPoint")

        if not entryNode or entryNode.GetNumberOfControlPoints() == 0:
            raise ValueError("Place the entry point first")
        if not targetNode or targetNode.GetNumberOfControlPoints() == 0:
            raise ValueError("Place the target point first")

        entryRAS = [0.0, 0.0, 0.0]
        targetRAS = [0.0, 0.0, 0.0]
        entryNode.GetNthControlPointPositionWorld(0, entryRAS)
        targetNode.GetNthControlPointPositionWorld(0, targetRAS)
        logging.info(f"[NeedlePathPlanner] Entry RAS={[round(v, 1) for v in entryRAS]}, "
                     f"Target RAS={[round(v, 1) for v in targetRAS]}, "
                     f"length={math.dist(entryRAS, targetRAS):.1f} mm")

        lineSource = vtk.vtkLineSource()
        lineSource.SetPoint1(entryRAS)
        lineSource.SetPoint2(targetRAS)
        lineSource.Update()

        trajectoryModel = slicer.mrmlScene.GetFirstNodeByName("TrajectoryLine")
        if not trajectoryModel:
            trajectoryModel = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "TrajectoryLine")
            trajectoryModel.CreateDefaultDisplayNodes()
        trajectoryModel.SetAndObservePolyData(lineSource.GetOutput())
        trajectoryModel.GetDisplayNode().SetLineWidth(3)
        trajectoryModel.GetDisplayNode().SetColor(1.0, 1.0, 1.0)  # white until clearance is checked

    def checkClearance(self, segmentationNode, segmentId: str) -> bool:
        """
        Test whether the current trajectory intersects the given segment.
        `segmentId` is the explicit segment chosen by the user as the no-go
        structure — never assume an index/order, since a segmentation can hold
        several segments (e.g. vessel + tumor) in an order we don't control.
        Returns True if the line crosses that segment (unsafe), False if clear.
        """
        entryNode = slicer.mrmlScene.GetFirstNodeByName("EntryPoint")
        targetNode = slicer.mrmlScene.GetFirstNodeByName("TargetPoint")

        if not entryNode or entryNode.GetNumberOfControlPoints() == 0:
            raise ValueError("No entry point — plan a trajectory first")
        if not targetNode or targetNode.GetNumberOfControlPoints() == 0:
            raise ValueError("No target point — plan a trajectory first")

        entryRAS = [0.0, 0.0, 0.0]
        targetRAS = [0.0, 0.0, 0.0]
        entryNode.GetNthControlPointPositionWorld(0, entryRAS)
        targetNode.GetNthControlPointPositionWorld(0, targetRAS)

        # Step 1 — convert the segmentation's label map to a closed surface mesh
        segmentationNode.CreateClosedSurfaceRepresentation()
        segmentation = segmentationNode.GetSegmentation()
        if segmentation.GetNumberOfSegments() == 0:
            raise ValueError("The segmentation has no segments")
        if not segmentId or not segmentation.GetSegment(segmentId):
            raise ValueError("No valid segment selected to check the trajectory against")

        logging.info(f"[NeedlePathPlanner] Segmentation '{segmentationNode.GetName()}' "
                     f"— testing against user-selected segment '{segmentId}'")

        polyData = vtk.vtkPolyData()
        segmentationNode.GetClosedSurfaceRepresentation(segmentId, polyData)
        if polyData.GetNumberOfPoints() == 0:
            raise ValueError("Could not get a closed surface from the segmentation")
        logging.info(f"[NeedlePathPlanner] Closed surface for '{segmentId}': "
                     f"{polyData.GetNumberOfPoints()} points, {polyData.GetNumberOfCells()} triangles")

        # Step 2 — build an OBB tree (spatial index) over the mesh
        # vtkOBBTree wraps groups of triangles in oriented bounding boxes so the
        # intersection test prunes most of the mesh in O(log n) instead of brute-force
        obbTree = vtk.vtkOBBTree()
        obbTree.SetDataSet(polyData)
        obbTree.BuildLocator()

        # Step 3 — test the entry->target line segment against the surface
        intersectionPoints = vtk.vtkPoints()
        hit = obbTree.IntersectWithLine(entryRAS, targetRAS, intersectionPoints, None)
        crossesVessel = bool(hit) and intersectionPoints.GetNumberOfPoints() > 0
        logging.info(f"[NeedlePathPlanner] IntersectWithLine against '{segmentId}': hit={bool(hit)}, "
                     f"intersection points={intersectionPoints.GetNumberOfPoints()} -> crosses={crossesVessel}")
        return crossesVessel


#
# NeedlePathPlannerTest
#


class NeedlePathPlannerTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Reset state before each test by clearing the scene."""
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run each test in isolation (clearing the scene before each)."""
        self.setUp()
        self.test_logicLoads()
        self.setUp()
        self.test_planTrajectory_buildsLine()
        self.setUp()
        self.test_checkClearance_crossing_returnsTrue()
        self.setUp()
        self.test_checkClearance_clear_returnsFalse()
        self.setUp()
        self.test_checkClearance_invalidSegment_raises()
        self.setUp()
        self.test_planTrajectory_missingTarget_raises()
        self.setUp()
        self.test_checkClearance_emptySegmentation_raises()
        self.setUp()
        self.test_checkClearance_recomputesAfterReplan()

    # --- helpers -------------------------------------------------------------

    def _createPointNode(self, name, position):
        """Add a single-point fiducial node at the given RAS position."""
        node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", name)
        node.AddControlPoint(vtk.vtkVector3d(position[0], position[1], position[2]))
        return node

    def _createCubeSegmentation(self, bounds=(-10, 10, -10, 10, -10, 10)):
        """
        Build a segmentation containing a single cube-shaped segment with known
        geometry, so we can predict exactly which lines cross it. Returns
        (segmentationNode, segmentId).
        """
        cube = vtk.vtkCubeSource()
        cube.SetBounds(*bounds)
        triangulate = vtk.vtkTriangleFilter()  # OBB tree wants triangles
        triangulate.SetInputConnection(cube.GetOutputPort())
        triangulate.Update()

        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", "TestSeg")
        segmentationNode.CreateDefaultDisplayNodes()
        segmentId = segmentationNode.AddSegmentFromClosedSurfaceRepresentation(
            triangulate.GetOutput(), "TestCube")
        return segmentationNode, segmentId

    def _setSinglePoint(self, name, position):
        """Create or update a single-point fiducial node, so a point can be 'moved'."""
        node = slicer.mrmlScene.GetFirstNodeByName(name)
        if not node:
            node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", name)
        node.RemoveAllControlPoints()
        node.AddControlPoint(vtk.vtkVector3d(position[0], position[1], position[2]))
        return node

    # --- tests ---------------------------------------------------------------

    def test_logicLoads(self):
        """Smoke test: confirm the logic class instantiates without error."""
        self.delayDisplay("test_logicLoads")
        logic = NeedlePathPlannerLogic()
        self.assertIsNotNone(logic)

    def test_planTrajectory_buildsLine(self):
        """planTrajectory should create a TrajectoryLine model with two endpoints."""
        self.delayDisplay("test_planTrajectory_buildsLine")
        self._createPointNode("EntryPoint", [0.0, 0.0, 0.0])
        self._createPointNode("TargetPoint", [10.0, 0.0, 0.0])

        NeedlePathPlannerLogic().planTrajectory()

        model = slicer.mrmlScene.GetFirstNodeByName("TrajectoryLine")
        self.assertIsNotNone(model)
        self.assertEqual(model.GetPolyData().GetNumberOfPoints(), 2)

    def test_checkClearance_crossing_returnsTrue(self):
        """A line driven straight through the cube must be reported as crossing."""
        self.delayDisplay("test_checkClearance_crossing_returnsTrue")
        self._createPointNode("EntryPoint", [-50.0, 0.0, 0.0])
        self._createPointNode("TargetPoint", [50.0, 0.0, 0.0])
        segmentationNode, segmentId = self._createCubeSegmentation()

        crosses = NeedlePathPlannerLogic().checkClearance(segmentationNode, segmentId)
        self.assertTrue(crosses)

    def test_checkClearance_clear_returnsFalse(self):
        """A line passing well clear of the cube must be reported as clear."""
        self.delayDisplay("test_checkClearance_clear_returnsFalse")
        self._createPointNode("EntryPoint", [-50.0, 100.0, 0.0])
        self._createPointNode("TargetPoint", [50.0, 100.0, 0.0])
        segmentationNode, segmentId = self._createCubeSegmentation()

        crosses = NeedlePathPlannerLogic().checkClearance(segmentationNode, segmentId)
        self.assertFalse(crosses)

    def test_checkClearance_invalidSegment_raises(self):
        """Passing a segment id that does not exist must raise, not silently pass."""
        self.delayDisplay("test_checkClearance_invalidSegment_raises")
        self._createPointNode("EntryPoint", [-50.0, 0.0, 0.0])
        self._createPointNode("TargetPoint", [50.0, 0.0, 0.0])
        segmentationNode, _ = self._createCubeSegmentation()

        with self.assertRaises(ValueError):
            NeedlePathPlannerLogic().checkClearance(segmentationNode, "no-such-segment")

    def test_planTrajectory_missingTarget_raises(self):
        """REQ-014 / H-03: with only an entry point placed, planning must raise."""
        self.delayDisplay("test_planTrajectory_missingTarget_raises")
        self._createPointNode("EntryPoint", [0.0, 0.0, 0.0])  # no TargetPoint placed

        with self.assertRaises(ValueError):
            NeedlePathPlannerLogic().planTrajectory()

    def test_checkClearance_emptySegmentation_raises(self):
        """REQ-018 / H-03: a segmentation with no segments must raise, not give a result."""
        self.delayDisplay("test_checkClearance_emptySegmentation_raises")
        self._createPointNode("EntryPoint", [-50.0, 0.0, 0.0])
        self._createPointNode("TargetPoint", [50.0, 0.0, 0.0])
        emptySeg = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", "EmptySeg")
        emptySeg.CreateDefaultDisplayNodes()

        with self.assertRaises(ValueError):
            NeedlePathPlannerLogic().checkClearance(emptySeg, "anything")

    def test_checkClearance_recomputesAfterReplan(self):
        """REQ-017 / H-02: the result must follow the current points, never go stale."""
        self.delayDisplay("test_checkClearance_recomputesAfterReplan")
        segmentationNode, segmentId = self._createCubeSegmentation()
        logic = NeedlePathPlannerLogic()

        # First plan: line driven through the cube -> crosses.
        self._setSinglePoint("EntryPoint", [-50.0, 0.0, 0.0])
        self._setSinglePoint("TargetPoint", [50.0, 0.0, 0.0])
        self.assertTrue(logic.checkClearance(segmentationNode, segmentId))

        # Re-plan with the points moved well clear -> must now report clear,
        # proving the result is recomputed from the live points (not cached/stale).
        self._setSinglePoint("EntryPoint", [-50.0, 100.0, 0.0])
        self._setSinglePoint("TargetPoint", [50.0, 100.0, 0.0])
        self.assertFalse(logic.checkClearance(segmentationNode, segmentId))

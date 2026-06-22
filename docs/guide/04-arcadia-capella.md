# Module 4: MBSE with Capella/Arcadia

> **Status: ready.** This module covers the "Capella model" part of the roadmap. It
> describes — as a formal model — the *same* needle-planning workflow you built in
> Module 3 (`NeedlePathPlanner`). Nothing here invents new behavior; it re-expresses the
> behavior that already exists in code.

## What is this?

**Systems engineering (SE)** is the discipline of describing a whole system — what it's
for, what it must do, and how its parts fit together — *before and alongside* building
it, so the pieces actually work together and you can show *why* each part exists.

**MBSE (Model-Based Systems Engineering)** does this with a connected **model** (boxes,
functions, links you can navigate) instead of a pile of Word documents. The advantage:
in a document, the sentence "the system checks the trajectory against the vessel" is just
text. In a model, "Verify clearance" is an *element* you can click — and follow its links
up to the clinician need it serves and down to the software component that implements it.
Change one, and the model shows you everything connected to it.

**Capella** is a free, open-source MBSE tool (Eclipse-based, originally built by Thales
for real aerospace/defense systems). **Arcadia** is the *method* Capella implements — a
fixed way of structuring the description into **four layers**, each answering one
question:

| Arcadia layer | The question it answers | Whose viewpoint |
|---|---|---|
| **Operational Analysis (OA)** | What does the user need to accomplish, and why? | The clinician — *no software mentioned yet* |
| **System Analysis (SA)** | What must the system-to-be *do* to support that? | The system as a black box |
| **Logical Architecture (LA)** | How do we break that into logical components? | The designer — *components, still tech-neutral* |
| **Physical Architecture (PA)** | What are the concrete components/interfaces? | The implementer — *maps to real code* |

The order matters: you go **top-down**, from human need to concrete implementation. Each
layer is traceable to the one above it ("this function exists *because* of that need").

## Why it matters here

For a German medtech employer, this is the artifact that proves you don't just code — you
think about a medical device the way the regulated industry requires: need → function →
component → implementation, with **traceability** all the way through. It's the same
spine that IEC 62304 (software lifecycle) and ISO 14971 (risk) hang off.

And you've already built the thing it describes. Here's the whole `NeedlePathPlanner`
mapped onto the four layers — this table *is* the deliverable in miniature:

| Layer | Element | Where it lives in your project |
|---|---|---|
| OA | "Reach a target lesion without damaging a major vessel" | The clinical goal behind the whole module |
| SA | Function: **Load image** | `inputSelector` / the loaded `vtkMRMLScalarVolumeNode` |
| SA | Function: **Define entry & target** | "Place Entry/Target Point" → `vtkMRMLMarkupsFiducialNode`s |
| SA | Function: **Compute trajectory** | `planTrajectory()` → the `TrajectoryLine` model |
| SA | Function: **Verify clearance** | `checkClearance()` → `vtkOBBTree.IntersectWithLine` |
| SA | Function: **Display result** | the `resultLabel` ("Clear of '…'" / "Crosses '…'") |
| LA | Component: **Image Loader** | volume selection logic |
| LA | Component: **Trajectory Planner** | `planTrajectory()` |
| LA | Component: **Clearance Checker** | `checkClearance()` |
| LA | Component: **Viewer** | the slice/3D views + result label |
| PA | Slicer scripted module | `NeedlePathPlanner.py` (Widget + Logic classes) |
| PA | Scene data nodes | the MRML nodes: volume, fiducials, segmentation, model |

> Note the recent bug fix lands here too: making the *no-go segment* an explicit user
> choice (the `qMRMLSegmentSelectorWidget`) is, in Arcadia terms, an **input** to the
> "Verify clearance" function — the system needs the operator to designate *which*
> structure is the hazard. That's exactly the kind of detail the model forces you to make
> explicit instead of leaving it as an accidental `GetValue(0)`.

## Key terms

- **MBSE** — describing a system through a connected model rather than free-text docs.
- **Arcadia** — the four-layer method Capella implements (OA → SA → LA → PA).
- **Operational Analysis (OA)** — the user's world and goals; no system/software yet.
- **System Analysis (SA)** — what the system-to-be must do, as **functions**.
- **Logical Architecture (LA)** — functions grouped into **logical components**
  (tech-neutral "what parts").
- **Physical Architecture (PA)** — the concrete implementation those components map to
  (your `.py` module, the MRML nodes).
- **Actor** — someone/something outside the system that interacts with it (here: the
  interventional radiologist).
- **Capability / Mission** — a high-level goal the system enables (e.g. "Plan a safe
  percutaneous insertion").
- **Function** — a behavior the system performs (e.g. *Verify clearance*). Functions
  have inputs/outputs (**function ports**) and can be chained.
- **Functional Chain** — an ordered path through several functions describing one
  scenario end-to-end (load → place points → compute → verify → display).
- **Traceability link** — an explicit, navigable connection between elements across
  layers ("this LA component *realizes* that SA function").

## Step-by-step

The output of this module is a Capella project saved under `se-model/` in this repo.
Build it in this order — **resist the urge to skip to the architecture**; the value is in
doing OA → SA → LA → PA in sequence.

**Setup (done):** Capella installed, workspace at `D:\MedVis\se-model\`, project
`NeedlePlanningModel` created with the four layer folders.

> **How to work the canvas (applies to every diagram):** open a diagram, and a vertical
> **palette** of tools appears on the right. Click a tool, then click the canvas to drop
> that element; for a *link* tool, click the source element then the target. Name an
> element by typing right after you drop it (or double-click it later). Select any element
> and the **Properties** tab (bottom) shows its details. **Ctrl+S** saves.
>
> **The Activity Explorer** (the guided "Operational Analysis → System Analysis →…" screen
> with numbered sections) is your friend — each section's link creates the right diagram
> for that step. Follow it top to bottom.
>
> **Transitions save redrawing.** Capella can carry elements down a layer automatically:
> right-click an element (or the layer) → **Transitions** → e.g. *Functional Transition*
> or *Actors Transition*. Use this to copy actors/functions from one layer to the next
> instead of recreating them by hand.

### Layer 1 — Operational Analysis (OA): the clinician's world

Open the **Operational Analysis** tab in the Activity Explorer.

1. **Operational Capabilities diagram [OCB].** Click *"Create a new Operational
   Capabilities diagram"*, name it `OCB - Needle Planning`.
   - Drop an **Operational Capability** → name it `Perform safe percutaneous insertion`.
   - Drop an **Operational Actor** → name it `Interventional Radiologist`.
   - Use the **Involvement** link tool: click the Radiologist, then the Capability.
2. **Operational Activities (section "Define Operational Activities").** Create an
   **Operational Activity Breakdown [OABD]** (or add activities in the activity diagram)
   and add these activities (what the clinician *does*, no software):
   - `Identify target lesion`
   - `Choose skin entry site`
   - `Avoid critical vessels`
   - `Verify path is safe`
3. **Allocate activities to the actor (section "Allocate Operational Activities…").**
   Assign all four activities to `Interventional Radiologist`.
4. **Ctrl+S.** OA done — notice there is still **zero** mention of Slicer.

### Layer 2 — System Analysis (SA): what the tool must do

Switch to the **System Analysis** tab in the Activity Explorer. Here the tool becomes a
single black box called the **System**.

1. **Bring the actor down.** Right-click `Interventional Radiologist` → **Transitions →
   Actor transition** (or just re-create a System Actor with the same name).
2. **Name the system.** In the System Analysis, rename the root **System** element to
   `NeedlePathPlanner`.
3. **System Data Flow / Functions [SDFB].** Create a **System Data Flow Blank** diagram,
   name it `SDFB - Needle Planning`, and add **five System Functions** (these mirror your
   code exactly):
   - `Load image`
   - `Define entry & target`
   - `Compute trajectory`
   - `Verify clearance`
   - `Display result`
4. **Chain them with functional exchanges.** Use the **Functional Exchange** link tool to
   connect them in order: Load image → Define entry & target → Compute trajectory →
   Verify clearance → Display result. (Optionally wrap them in a **Functional Chain** so
   the whole path is one named scenario.)
5. **Allocate functions to the system/actor.** In a **System Architecture Blank [SAB]**,
   show `NeedlePathPlanner` and the Radiologist; allocate the five functions to the system
   (the Radiologist *triggers* "Define entry & target" — that's the human input).
6. **Ctrl+S.** This is the heart of the model. Map to code:

   | System function | Your code |
   |---|---|
   | Load image | `inputSelector` + loaded volume node |
   | Define entry & target | "Place Point" buttons → fiducial nodes |
   | Compute trajectory | `planTrajectory()` → `TrajectoryLine` |
   | Verify clearance | `checkClearance()` (OBB-tree intersection) |
   | Display result | slice/3D views + `resultLabel` |

### Layer 3 — Logical Architecture (LA): the components

Switch to the **Logical Architecture** tab.

1. **Transition the functions down.** Right-click the System functions →
   **Transitions → Functional transition** to copy the five functions into LA.
2. **Logical Architecture Blank [LAB].** Create one, name it `LAB - Needle Planning`, and
   add four **Logical Components**:
   - `Image Loader`
   - `Trajectory Planner`
   - `Clearance Checker`
   - `Viewer`
3. **Allocate each function to a component** (drag the function into the component box, or
   use the allocation tool):
   - Load image → **Image Loader**
   - Define entry & target → **Trajectory Planner**
   - Compute trajectory → **Trajectory Planner**
   - Verify clearance → **Clearance Checker**
   - Display result → **Viewer**
4. **Ctrl+S.** These components are still tech-neutral — no Slicer/Python named yet.

### Layer 4 — Physical Architecture (PA): the real implementation

Switch to the **Physical Architecture** tab. This is where the model finally touches your
actual code.

1. **Transition the logical components down** (Transitions → from LA), or create
   **Physical Components** directly.
2. **Physical Architecture Blank [PAB].** Create one, name it `PAB - Needle Planning`,
   and represent:
   - A **behaviour** physical component `NeedlePathPlanner scripted module`
     (this hosts the Widget + Logic classes from `NeedlePathPlanner.py`).
   - **Node / data** physical components for the MRML scene nodes:
     `Scalar Volume node`, `Markups Fiducial nodes`, `Segmentation node`, `Model node`.
3. **Map logical → physical:** the four logical components are all realized inside the one
   `NeedlePathPlanner scripted module`; the data they act on is the MRML nodes.
4. **Ctrl+S.** You can now trace any function end-to-end, e.g.:
   *Verify clearance* (SA) → *Clearance Checker* (LA) → `checkClearance()` in the
   *NeedlePathPlanner scripted module* (PA).

### Wrap up — export and commit

1. **Export diagrams as images** so they're viewable without Capella: right-click a
   diagram → **Export diagrams as images…** → save the PNGs under `se-model/diagrams/`
   (create the folder). Do this for the OCB, SDFB, LAB, and PAB at minimum.
2. **Commit.** Stage the new `se-model/` files (the `.capella`, `.aird`, `.afm`, and the
   exported PNGs) and commit. Ask Claude for the exact `git add`/`commit` commands when
   you're at this point.

## Checkpoint

You're done with Module 4 when:

- A Capella project exists under `se-model/` and is committed.
- All four Arcadia layers are populated, and the five SA functions are allocated to the
  four LA components.
- You can point at any element and explain it both ways: "this *Verify clearance*
  function is realized by the *Clearance Checker* component, which in the physical layer
  is `checkClearance()` in `NeedlePathPlanner.py`" — that round-trip *is* the skill being
  demonstrated.

This sets up Module 5 (requirements trace to these functions) and Module 6 (hazards trace
to these requirements).

## Further resources

- [Capella download](https://www.eclipse.org/capella/download.html) — choose the Product build
- [Arcadia method overview](https://www.eclipse.org/capella/arcadia.html)
- [Capella in-tool guide] — the Welcome screen's Arcadia tutorial is the best first stop

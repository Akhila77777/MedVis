# Module 8: MONAI Deep Learning (Stretch Goal)

> **Status: ready.** This is the optional stretch module. It bridges deep learning and
> visualization: use a U-Net to *produce* a segmentation, then feed that prediction into
> the Module 3 needle planner as the "no-go" structure — closing the last loop
> (ML → segmentation → surface → clearance check).

> **Honesty note (important).** This is genuinely heavier than every other module, and
> hepatic-vessel segmentation is one of the *hardest* Decathlon tasks (thin structures,
> severe class imbalance). On a CPU-only machine you will not train a good vessel model in
> a reasonable time. So the goal here is to **learn and demonstrate the DL pipeline
> end-to-end**, framed honestly as a learning experiment — not to claim a performant,
> validated model. Say exactly that in your portfolio.

## What is this?

- **PyTorch** is the deep-learning framework (tensors, autograd, training loops).
- **MONAI** (Medical Open Network for AI) is a library built *on* PyTorch, specialized for
  medical imaging: medical image transforms, ready-made network architectures (U-Net), loss
  functions (Dice), and a **Model Zoo** of pretrained "bundles."
- **U-Net** is the standard segmentation architecture: an encoder that downsamples the
  image to capture context, a decoder that upsamples back to full resolution, with
  "skip connections" linking matching levels so fine detail is preserved. Output: a
  per-voxel class label (e.g. background / vessel).

## Why it matters here

Until now you've *used* the dataset's hand-drawn label as the vessel. Module 8 replaces
that human step with a model: the U-Net predicts the segmentation, you export it as NIfTI,
load it into Slicer, and run the same `checkClearance()` against it. That demonstrates the
full modern pipeline — image → deep-learning segmentation → 3D surface → safety check.

## Two honest paths (pick one)

| | Path A — Pretrained inference | Path B — Tiny training demo |
|---|---|---|
| What you do | Download a pretrained MONAI **Bundle** and run *inference* on one CT volume | Train a small U-Net yourself for a few epochs on a cropped subset |
| Teaches | The inference + export + Slicer loop; how bundles work | The *training loop*: transforms, Dice loss, epochs, validation |
| Cost | Light (no training); minutes on CPU | Heavier, but a *deliberately small* demo runs on CPU in minutes |
| Result quality | Good (it's a trained model), but not vessel-specific | Poor (that's expected and fine — it's a mechanics demo) |
| Honest claim | "Ran a pretrained MONAI model and integrated its output" | "Built and trained a U-Net pipeline with MONAI (small-scale demo)" |

**Recommendation:** if you want a clean result to load into Slicer, do **Path A**. If you
want to *learn how training works* (more valuable for understanding ML), do **Path B** with
a tiny configuration and accept poor accuracy. Doing both is ideal but not required.

## Key terms

- **Dice loss** — a loss based on the Dice overlap score; standard for segmentation because
  it handles class imbalance better than plain cross-entropy.
- **MONAI transforms** — the preprocessing pipeline (load image, add channel, resample
  spacing, scale intensity, crop) applied to each sample, composed with `Compose`.
- **MONAI Bundle / Model Zoo** — a packaged, versioned model (weights + config + transforms)
  you can download and run with a few lines.
- **Epoch / validation** — one pass over the training data; periodically check Dice on a
  held-out validation set to watch for overfitting.
- **Decathlon format** — the `imagesTr/` + `labelsTr/` folder structure (you have it at
  `D:/MedVisData/Task08_HepaticVessel`).
- **NIfTI export** — saving the prediction as `.nii.gz` so Slicer can load it.

## Prerequisite: a standalone Python ML environment

Slicer's bundled Python is separate and we won't install heavy ML libs into it. Set up a
clean environment (commands for *you* to run in a terminal):

```bash
# 1. Install Python 3.11 from https://www.python.org/downloads/ (tick "Add to PATH").
#    Verify in a NEW terminal:
py --version

# 2. Create and activate a project virtual environment:
py -m venv D:\MedVis\ml\.venv
D:\MedVis\ml\.venv\Scripts\activate

# 3. Install the libraries (CPU build of PyTorch — no GPU needed for this):
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "monai[nibabel,tqdm]" matplotlib
```

(If you prefer Miniconda, that works too; the venv route above is the lightest.)

## Path A — pretrained bundle inference (high level)

1. List/download a bundle from the MONAI Model Zoo (e.g. a CT organ-segmentation bundle).
2. Run its inference on one volume from `imagesTr/`.
3. Save the predicted labelmap as `.nii.gz`.
4. Load it into Slicer (next section).

## Path B — tiny training demo (high level)

1. Build a MONAI transform pipeline for the Task08 images/labels.
2. Define a small `monai.networks.nets.UNet` and `DiceLoss`.
3. Train for a few epochs on a small cropped subset (CPU-friendly), watching the loss drop.
4. Run inference on a held-out volume and export the prediction as `.nii.gz`.

We'll write the actual script under `ml/` once you've picked a path and the environment is
ready.

## Loading the prediction into Slicer (closing the loop)

1. In Slicer: **File → Add Data**, choose your predicted `.nii.gz`, and load it
   **as a Segmentation** (or load as labelmap, then convert).
2. Open the **NeedlePathPlanner** module, select the predicted segmentation as the
   vessel/organ no-go structure.
3. Place entry/target and run the clearance check — now against a *model-generated* no-go
   zone instead of the hand-drawn one.

## Checkpoint

You're done when you have:
- A standalone Python ML environment with PyTorch + MONAI working.
- A predicted segmentation (`.nii.gz`) from either a pretrained bundle (Path A) or your own
  small U-Net (Path B).
- That prediction loaded into Slicer and used as the no-go structure in a clearance check.
- An honest one-paragraph write-up of what the model is and is not (especially: not a
  validated vessel segmenter).

## Further resources

- [MONAI documentation](https://docs.monai.io/)
- [MONAI tutorials](https://github.com/Project-MONAI/tutorials) — see `2d_segmentation`
  and `3d_segmentation`, and the spleen segmentation tutorial
- [MONAI Model Zoo / Bundles](https://monai.io/model-zoo.html)

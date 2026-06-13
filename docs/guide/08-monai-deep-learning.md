# Module 8: MONAI Deep Learning (Stretch Goal)

> **Status: outline.** This module covers task #10 of the roadmap (stretch goal). Full
> concept explanations will be added when we start this module — what's below is the
> structure and the terms you'll need.

## What is this?

*(To be filled in: what MONAI is, how it relates to PyTorch, and what a U-Net
segmentation model does at a high level.)*

## Why it matters here

This bridges deep learning and visualization: train a small segmentation model, then
feed its output into the Module 3 Slicer module as the "no-go zone" for trajectory
checking — showing the modern DL+visualization pipeline end to end.

## Key terms

- **U-Net** — a common encoder-decoder architecture for image segmentation
- **MONAI transforms / dataset utilities** — preprocessing pipeline for medical images
- **Training loop** — epochs, loss function (e.g. Dice loss), validation
- **NIfTI export** — saving a predicted segmentation so Slicer can load it
- **Decathlon task format** — `imagesTr` / `labelsTr` structure used as training data

## Step-by-step (high level — to be expanded)

1. Install standalone Python + PyTorch + MONAI (separate from Slicer's bundled Python).
2. Train a small U-Net on the Decathlon task downloaded in Module 2 (liver or hepatic
   vessel).
3. Run inference on a held-out volume, export the predicted segmentation as NIfTI.
4. Load the predicted segmentation into the Module 3 Slicer module as the vessel
   "no-go zone" and run the clearance check against it.

## Checkpoint

*(To be filled in.)*

## Further resources

- [MONAI documentation](https://docs.monai.io/)
- [MONAI tutorials repository](https://github.com/Project-MONAI/tutorials)

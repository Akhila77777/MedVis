# Module 1: Version Control Basics

## What is this?

**Git** is a tool that tracks changes to files over time — every saved set of changes
("commit") is recorded, so you can see history, undo mistakes, and work on multiple
things without losing work. **GitHub** is a website that hosts Git repositories online,
so others can see your code and you have an off-machine backup.

## Why it matters here

Every part of this project — code, documentation, the SE artifacts — lives in one Git
repository, hosted publicly on GitHub. This is also the "show your work" mechanism: a
clean, well-organized public repo with a good README *is* part of the portfolio.

## Key terms

- **Repository (repo):** a folder tracked by Git, containing your files plus a hidden
  `.git/` folder with the history.
- **Commit:** a saved snapshot of changes, with a message describing what/why.
- **Remote:** a copy of the repo hosted elsewhere (here, on GitHub) that you push to /
  pull from.
- **Branch:** a named line of development. `main` is the default branch.
- **Push / pull:** send your local commits to the remote / fetch the remote's commits
  to your local copy.
- **SSH key:** a credential that lets your machine authenticate to GitHub without
  typing a password each time.

## Step-by-step (already done for this project)

1. ✅ Initialized a local repo in `D:\MedVis` (`git init`).
2. ✅ Created an empty repository on GitHub (`Akhila77777/MedVis`).
3. ✅ Added it as the `origin` remote via SSH
   (`git@github.com:Akhila77777/MedVis.git`) and confirmed SSH auth works.
4. ✅ Committed the initial files and pushed to `main` with
   `git push -u origin main`.

## Ongoing workflow

For every module/step going forward, the pattern is:

```bash
git status              # see what changed
git add <files>          # stage the files you want to commit
git commit -m "message"  # commit with a descriptive message
git push                  # send to GitHub
```

## Checkpoint

You can run `git status` in `D:\MedVis` and see "nothing to commit, working tree clean"
after a push, and your changes are visible at
`https://github.com/Akhila77777/MedVis`.

## Further resources

- [GitHub Docs: Git and GitHub learning resources](https://docs.github.com/en/get-started)
- [Pro Git book (free)](https://git-scm.com/book/en/v2)

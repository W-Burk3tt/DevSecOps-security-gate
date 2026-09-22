# DevSecOps Demo: SAST Security Gate

A minimal demonstration of a CI/CD security gate — a GitHub Actions
pipeline that runs static code analysis (SAST) on every push and fails
the build if a real vulnerability is detected, rather than letting
insecure code merge silently.

## What's here
- `app.py` — a small Python file with three intentionally introduced,
  well-known vulnerability patterns (see comments in the file):
  hardcoded secret, SQL injection via string concatenation, and OS
  command injection via `shell=True`
- `.github/workflows/security-scan.yml` — a GitHub Actions workflow
  that runs [Bandit](https://bandit.readthedocs.io/) (a Python-specific
  SAST tool) on every push and pull request to `main`, and fails the
  job if anything at medium severity or higher is found

## The point
This repo is not meant to run as a real application. It exists to prove
a specific thing: **that broken code cannot pass CI**. The workflow has
no bypass — no `continue-on-error`, no suppressed exit code — so a real
finding genuinely blocks the pipeline, the same way it would in a real
organization's merge-gate policy.

## How it was tested
1. Pushed the vulnerable `app.py` as-is → pipeline **failed**, Bandit
   correctly identified all three issues
2. Fixed each vulnerability (parameterized query, environment-variable
   secret, removed `shell=True`) → pushed again → pipeline **passed**

Both runs are visible in this repo's **Actions** tab as a permanent,
verifiable record.

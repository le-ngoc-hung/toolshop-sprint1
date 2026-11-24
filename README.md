# toolshop-sprint1

[![CI](https://github.com/le-ngoc-hung/toolshop-sprint1/actions/workflows/ci.yml/badge.svg)](https://github.com/le-ngoc-hung/toolshop-sprint1/actions/workflows/ci.yml)

## Sprint 2B

This repository contains Playwright Python tests for the Toolshop UI and API,
including a BDD cart flow implemented with pytest-bdd. The BDD feature covers
opening a product, adding a quantity, and verifying line and cart totals.

### Run locally

Start the private Toolshop environment and run the full suite:

```powershell
bash toolshop/start.sh
$env:BASE_URL = "http://localhost:4200"
$env:API_URL = "http://localhost:8091"
$env:GITHUB_API_URL = "https://api.github.com"
pytest
```

Run only the BDD cart scenarios:

```powershell
pytest tests/bdd -v
```

CI runs the complete suite in three matrix jobs, using the Docker Toolshop
service and retaining the HTML report, screenshots, and Playwright traces for
seven days.

### Evidence

Screenshots from a real GitHub Actions run and Playwright Trace Viewer should
be added under `docs/screenshots/` after the first successful/diagnostic CI
run. No generated or simulated evidence is included.

# MT-Lane-Follow-RL-Safety

Master thesis repository for a **reinforcement-learning lane-following system with a safety cage**, developed in the context of SE4AI (Samuel ASM, 2026).

## Project goal

This project defines and evaluates a safety-oriented pipeline for lane following in a scale-model autonomous driving setting:

- Train an RL policy for lane keeping.
- Constrain policy actions with a rule-based **Safety Cage**.
- Define a clear **Operational Design Domain (ODD)**.
- Link hazards, safety requirements, cage rules, scenarios, metrics, and evidence through a **traceability matrix**.

The repository is organized to support both engineering work (training, tests, scripts) and thesis writing (structured chapters and appendices).

## Current status

The repository currently contains:

- A detailed ODD and requirements-traceability chapter draft (`docs/00_odd_specification.md`).
- Initial templates for hazard analysis, safety requirements, cage specification, scenario library, and V-model adaptation (`docs/01` to `docs/07`).
- Draft thesis chapters and appendices under `thesis/`.
- Placeholder code structure for training, analysis, and cage tests under `training/`, `scripts/`, and `tests/`.

Several implementation files are still placeholders and are intended to be completed iteratively.

## Repository structure

```text
.
├── docs/
│   ├── 00_odd_specification.md
│   ├── 01_hazard_register.md
│   ├── 02_safety_requirements.md
│   ├── 03_cage_specification.md
│   ├── 04_scenario_library.md
│   ├── 05_traceability_matrix.csv
│   ├── 05_traceability_matrix.md
│   ├── 06_conventions.md
│   ├── 07_v_model_adapted.md
│   ├── DECISIONS.md
│   └── CHANGELOG.md
├── scripts/
│   ├── check_traceability.py
│   ├── analyze_logs.py
│   └── plot_results.py
├── training/
│   ├── train_ppo.py
│   └── env_wrapper.py
├── tests/
│   └── cage/
│       └── test_C01.py
├── thesis/
│   ├── chapter_01_introduction.md
│   ├── chapter_02_related_work.md
│   ├── chapter_03_methodology.md
│   ├── chapter_04_hazard_analysis.md
│   ├── appendix_A_v_model.md
│   └── appendix_F_traceability.md
├── pyproject.toml
└── README.md
```

## Safety engineering workflow (intended)

1. Define/update hazards in `docs/01_hazard_register.md`.
2. Derive falsifiable safety requirements in `docs/02_safety_requirements.md`.
3. Implement requirements through cage rules in `docs/03_cage_specification.md` and code.
4. Define verification scenarios in `docs/04_scenario_library.md`.
5. Maintain bidirectional coverage in `docs/05_traceability_matrix.csv`.
6. Validate consistency with `scripts/check_traceability.py`.
7. Feed evidence into thesis chapters and appendices.

## Getting started

### Prerequisites

- Python 3.11+
- `pip` (or an equivalent Python package manager)

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> Note: dependency configuration is still minimal (`pyproject.toml` is currently a placeholder), so additional packages may be required as implementation progresses.

## Running checks

Traceability validation script (current template):

```bash
python scripts/check_traceability.py
```

As the repository matures, add this check to pre-commit and CI to enforce safety-document consistency.

## Thesis context

This repository is intentionally documentation-first: the ODD, requirements and traceability artifacts are meant to drive implementation and evaluation, not the other way around. The thesis narrative is developed in parallel in `thesis/` and mirrors the safety lifecycle represented in `docs/`.

## License

This project is distributed under the terms of the `LICENSE` file in the repository root.

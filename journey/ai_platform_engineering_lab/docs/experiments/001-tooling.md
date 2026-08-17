# Experiment 001 — Python Tooling

## Question

What problem does each tool solve?

## Setup

- uv project, Python `>=3.12`, src-layout (`src/engineering_lab/`), build backend `uv_build`.
- Tools, dev group only: mypy 2.3.1 · pre-commit 4.6.2 · pytest 9.1.1 · ruff 0.16.3

**Where the interpreter is, and why I never activated it**

```
$ uv run python -c "import sys; print(sys.executable)"
...\ai_platform_engineering_lab\.venv\Scripts\python.exe
```

`uv run` finds `pyproject.toml`, resolves the `.venv` next to it, syncs it if it's stale, then
execs inside it. Activation is a convenience for typing bare `python` — it is not a prerequisite
for `uv run`.

**Why `import engineering_lab` works**

```
$ uv run python -c "import engineering_lab; print(engineering_lab.__file__)"
...\src\engineering_lab\__init__.py

$ uv pip list
ai-platform-engineering-lab 0.1.0   (Editable project location: ...)
```

The project itself is installed into the venv as an **editable** install — a link back to the
source tree. `src/` is not on `sys.path`; the package is genuinely installed. That is also why
`tests/test_calculator.py` can `from engineering_lab.calculator import add` with no path hacks.

**Runtime or development dependency?**

```
$ uv remove pytest ruff mypy pre-commit
Resolved 24 packages
Uninstalled 1 package / Installed 1 package
 ~ ai-platform-engineering-lab==0.1.0

$ uv run pytest --version
pytest 9.1.1
```

`uv remove` emptied `[project].dependencies` to `[]` and rebuilt only the project. All four tools
still run, because `[dependency-groups].dev` still declares them and `uv sync` installs the dev
group by default. So: **development dependencies.** Someone installing this package to *use* it
should not be forced to install a linter. `uv sync --no-dev` is what a production image runs.

**`uv.lock` vs `pyproject.toml`**

> _(fill in: `pyproject.toml` says `pytest>=9.1.1` — a range. What does the lock say for the same
> package? What else is in the lock that pyproject has no room for?)_

## Experiments

### Ruff

_Rounds 2, 3, 6._

What did it catch?

<!--
  Per experiment: what I changed → command → exact output (rule code, file, line)
  → what it did NOT report → did it fix anything, or only report it?
  Must cover:
    - `ruff check` vs `ruff format --check` on the SAME file (the stray space in `def add (a, b)`)
    - F401 unused imports, and whether `--fix` removed them
    - which of E (bad names) / F (needless if-else) / G (unreachable) appeared only AFTER
      select = ["E","F","I","SIM","UP","B"] was added to pyproject.toml — and which never appeared
-->

### mypy

_Rounds 4, 5, 6._

What did it catch?

<!--
    - wrong return type (`-> int` but `return "hello"`)
    - wrong argument type at the call site (`calculate("hello", 10)`)
    - the control: `uv run python src/engineering_lab/bad_code.py`. Did mypy have to RUN the code
      to find that? What did Python find that mypy didn't, and vice versa?
    - what did `strict = true` start complaining about in files that were already green?
-->

### pytest

_Round 7._

What does it actually verify?

<!--
    - `return a - b` → pytest oum  tput (actual vs expected) while ruff + mypy stay green on it
    - then the test edited to agree with the broken code → it passes
    - what did that passing test prove? what does a passing test mean?
-->

### pre-commit

_Round 8._

What happens when I commit bad code?

<!--
  The six questions, answered from the output in front of me:
    1. which hooks ran
    2. which failed
    3. did the hook modify my files (`git status` / `git diff` BEFORE touching anything)
    4. did git create the commit (`git log --oneline`)
    5. what gets the commit through
    6. do I have to re-run the hook manually
  Plus: `pre-commit run --all-files` vs on-commit — which set of files does each look at?
-->

## What I initially misunderstood

<!--
  Only genuine ones. Delete any I never actually believed.
  Candidates from the rounds so far:
    - that a virtual environment has to be activated manually
    - that uv.lock and pyproject.toml say the same thing
  More will come out of Rounds 2-8.
-->

## What I learned

<!--
  Where the tools overlap, where they don't, and which tool "opinions" turned out to be
  configuration rather than facts about Python.
-->

## Acceptance

<!--
  Final green output of:
    uv run pytest
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy .
  Plus one recorded deliberate failure each for Ruff, mypy, pytest, pre-commit.
-->

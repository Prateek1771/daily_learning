These tools are best understood as **one Python project workflow**, not as isolated technologies.

The mental model is:

> **uv** manages Python + environments + dependencies → **pyproject.toml** describes the project → **uv.lock** freezes exact dependency versions → **Ruff/mypy** enforce code quality → **pytest** tests behavior → **pre-commit** runs checks automatically → **Makefile** gives convenient commands → **CI** runs the same checks on GitHub.

---

# 1. First: what problem is this structure solving?

Suppose you build an AI platform engineering project.

Without a standardized setup, you might have:

```text
project/
├── main.py
├── random_script.py
├── requirements.txt
├── test.py
└── ...
```

And eventually:

* "Which Python version should I use?"
* "Which version of Pydantic?"
* "Why does it work on my machine but not yours?"
* "Did someone forget to run formatting?"
* "How do we run all tests?"
* "How do we ensure CI uses the same dependencies?"
* "Where should production code go?"
* "Where should experiments go?"

The structure you posted solves these problems systematically.

---

# 2. `uv`

![Image](https://images.openai.com/static-rsc-4/a_vSH8e2-mAFJBODasy7_qsV349SkqF-t3nWs5SWgwj9h5pE6fzRtXT0uxV4Y1NH_rWjeV9VoY1Z1etHr5Ox6BKRu2wuBogbAJm5alL80FdIhaXbJXy9U7pIYGcCiwSH1G2mCt-Pttbf-P9Cnw5UrKZ-pXrjJurK1BgHce8OU3yEqbFIyOmgoCdX0hvcQImJ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/faffk_GJPUKm5YqkrORYkDdfhTmSB53hjlHypw43UDk12oYB1YLTdrr98YQLhF5GlhRc0It2G4QFZxnqnoKzeNFJm8fj5mTuoDcTKUjry9Yd3zL7hm0TCi_0gAHt7x53Sq2MBvpeUOVFRFrBdiP7l6E0ZpDJiXcB41G2k_JKbuKhqLL7ANQ-0sDKf5RYUM7Q?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dE-OFM26rYf4HmGXZv2YWr-hFqWE73un8L8r4Ze0vvAvnochK1hl96uy7ScxB2oT5N7Y3EUqy7JY0eFVqifLgLuuuuzKxVvMKf5MxPPF2VvRC6BVrDjnhabUDStS-UIuwTuUPuHFGeUD_Ls1dsIIxI_Qj6gvawmdO7PPCvAAopkKuBMxwN5dB3v0NPw8BsI5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/WBAFOzvdRg0CoptgcuJXH3OiFcWnBxkspPpFcbOhI3UkUJt4jgRyGfhGPdS-vEy-fpdD5-hMrLAm-ovxyPiKXId5-AoUiJMqUVjigz1_AR4m-YNOeyZiU0uz074HF_Oob0D4aD-MTfbkdqehw6sm7NZTesr3Tdis8Zx8WOauCNF9oS-mJ3RH0BQc-5guSFvk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IeVeqJ4lN4G0ABwijy_LSbW_ua4PC9_yAemPXgE6lSv0Wq-Q99SRiCiMr-Me53bzeYteOOjoRm3IcmiQANfsgxoo7ip5qSjPaGJi1-TteQsRz07SWIkJ5p-tSeH2BnXpO46u7eXNKG_PoAdC9r07C1CTgEb6G0dricurHy8IaFx6gC3hpsxI_qPNuJha86ci?purpose=fullsize)

**uv is a fast Python package and project manager.**

Think of it as a modern tool that can handle several things traditionally handled by:

* `pip`
* `venv`
* `pip-tools`
* parts of `poetry`
* Python version management

Instead of manually doing:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
pip install ruff
pip install mypy
```

you can use:

```bash
uv sync
```

and uv creates/synchronizes the environment according to your project configuration and lock file.

### Common commands

```bash
uv init
```

Creates a Python project.

```bash
uv add pytest
```

Adds a dependency.

```bash
uv add ruff mypy
```

Adds development dependencies.

```bash
uv remove pytest
```

Removes a dependency.

```bash
uv sync
```

Creates/updates the virtual environment.

```bash
uv run pytest
```

Runs pytest inside the project's environment.

```bash
uv run python src/engineering_lab/main.py
```

Runs Python using the project's environment.

### Why `uv run` is useful

Instead of:

```bash
source .venv/bin/activate
pytest
```

you can simply:

```bash
uv run pytest
```

You don't have to manually activate the environment.

---

# 3. Virtual environments

A **virtual environment isolates the dependencies of one Python project from another**.

Imagine you have:

```text
Project A
FastAPI 0.100
```

and:

```text
Project B
FastAPI 0.120
```

If both use the system Python environment, versions can conflict.

A virtual environment gives each project its own environment:

```text
Machine
│
├── Python
│
├── Project A
│   └── .venv/
│       ├── FastAPI 0.100
│       └── ...
│
└── Project B
    └── .venv/
        ├── FastAPI 0.120
        └── ...
```

For your project:

```text
ai-platform-engineering-lab/
└── .venv/
```

`uv` generally manages this environment for you.

You normally **do not commit `.venv/` to Git**.

That's why `.gitignore` contains:

```gitignore
.venv/
```

---

# 4. `pyproject.toml`

This is one of the most important files.

It is essentially the **central configuration file for a modern Python project**.

It can describe:

* project name
* version
* Python version
* dependencies
* development dependencies
* build configuration
* Ruff configuration
* pytest configuration
* other tool configuration

For example:

```toml
[project]
name = "engineering-lab"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "fastapi",
    "pydantic",
]

[dependency-groups]
dev = [
    "pytest",
    "ruff",
    "mypy",
]
```

Conceptually:

```text
pyproject.toml
       │
       ├── What is this project?
       ├── Which Python version?
       ├── What packages does production need?
       └── What tools does development need?
```

---

# 5. Dependency locking

This is where `uv.lock` comes in.

Suppose your `pyproject.toml` says:

```toml
dependencies = [
    "fastapi>=0.100"
]
```

This does **not necessarily mean exactly one version**.

It could install:

```text
FastAPI 0.110
```

today and:

```text
FastAPI 0.115
```

six months later.

That can create:

> "It worked yesterday but doesn't work today."

Dependency locking solves this.

---

# 6. `uv.lock`

`uv.lock` records the **exact dependency resolution**.

Conceptually:

```text
pyproject.toml

"Give me:
 FastAPI >= 0.100"

        ↓

uv dependency resolver

        ↓

uv.lock

"Use:
 FastAPI 0.115.2
 Starlette 0.47.1
 Pydantic 2.11.x
 ...
"
```

So:

### `pyproject.toml`

describes what you **want**.

### `uv.lock`

describes exactly what was **resolved**.

This gives reproducibility.

When another developer clones your repository:

```bash
git clone ...
cd ai-platform-engineering-lab
uv sync
```

uv can reproduce the locked dependency environment.

---

# 7. Dependency locking vs virtual environments

These are easy to confuse.

### Virtual environment

Answers:

> Where are my Python packages installed?

```text
.venv/
```

### Lock file

Answers:

> Exactly which versions should be installed?

```text
uv.lock
```

### `pyproject.toml`

Answers:

> What dependencies does this project require?

```text
pyproject.toml
```

Together:

```text
pyproject.toml
       │
       │ requirements
       ↓
    uv.lock
       │
       │ exact versions
       ↓
     .venv
       │
       │ installed packages
       ↓
    Application
```

---

# 8. Ruff

![Image](https://images.openai.com/static-rsc-4/F0ZMDlaBo4BMcrtsIjsXmqb1kzrCn7rYclMxBpVHFZQxvf-XlR7YtwbbJbHr-JwKROKH8LTwASlUrB4JmtMyeXItR42IWjxb4xCIFBfH8BZ53bUU32X-wQ0rhIUGZ-K3hOoXxKz1jU5unL3BozcLXM4vvw-jEU8vOmHNybmrbOMskfuBNYcypdHnn84ZUn78?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/gTc0ozBMrkOr_6XFib_zNNae8ozsqqXzAPqp8rJCH2VkynsQkRRTQ46TILQMUVDbDtxGwMkYkwj8aqPP6q4AhC2YAgxzUnzPxjGu2QCrL4xNBDbo4gcnag-RQ2UrVcrS_aHz_XKM6afvgISEleLO6gQhhLDnWV9BylpiejX6HdlncZLV2Q9ZIfXsHC_S0wtD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zHtpvb35YvgoWHt1ilEPZXLuiDUaNjefVj5mZgEydVXXBi6KhBKJHGNJnIsEznGd6UewpV0bic58iQ52bCTiLDGebOG0exi3p3VORg1aRFtQYxEoO8CMZLaJlQP8F7-Awtf5aSuj4wJktooij8XvOGKeByOLNhWIe882BaJeFeX7efWfc7eqYLzvHWWLruDf?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/imAXygoO61LkPG9c7Fo6LxTqVxI_LQZFbD2m7QwbJBZYCtP70evKQyleWt8QsvhECoLwdPKWJx3i7I2ecx5TyJ1Yk37FCTwb9HpJmjL0jvbQBo9TkxagxfGoQdlHo1QahBfsAh84lukcPtnatSdjmGLmQAk3K2WHchwI5-2hfJx3IKvbc-YaaegbDZLU_RZT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Oudtjlg77CURyha47DvE3WWH_MSek5Zt3mZzdAsE6Z0qOdLsqUt-klkTWBihObeoO-V4_udBuFelzsgHLuD8dJqUjjxKdBfey-OsNGA68K3O_ynUrfGpcMb4n6fAIG2J0FKPWZSTzu6i_76M6jxjFjzHpeatRJ7QoPoGbnzvp-e_9DWHZ7ixbTb1ESmQCVUU?purpose=fullsize)

**Ruff is a Python linter and formatter.**

It helps catch problems and enforce consistent code style.

For example:

```python
import os
import sys

x = 10
```

Ruff may tell you that imports are unused or improperly organized.

It can also format code.

Instead of manually formatting:

```python
def hello(name):
    print("Hello", name)
```

Ruff can format it into:

```python
def hello(name):
    print("Hello", name)
```

Typical commands:

```bash
uv run ruff check .
```

Check code.

```bash
uv run ruff format .
```

Format code.

You can think of Ruff as:

> **"Is this Python code clean and stylistically consistent?"**

---

# 9. `ruff.toml`

This controls Ruff's behavior.

For example:

```toml
line-length = 100

[lint]
select = ["E", "F", "I"]

[format]
quote-style = "double"
```

So:

```text
ruff.toml
    │
    └── Rules for Ruff
```

Modern projects can also put Ruff configuration directly inside `pyproject.toml`, so a separate `ruff.toml` isn't mandatory.

---

# 10. mypy

![Image](https://images.openai.com/static-rsc-4/1U6NP4HsdR0ljmW18uPkYxLyDPJey1tti6Bo2pNvy_5PaYP3VcmdY-uj4YD6Vy_xVeoNW5n79q3Ke-_DjCr7LdumyH0KAh9FwzQ8mhHDA9zwSgcn8EcDj6j7vcKVNRDTKcHmNvqfmkct8z2rhsudEVjzPbU4uSsvgfbdk4wEjE0H54f6cwX6tl1flik4j4xu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/jfD7dRcT-OLt9gaumHb_JU1smU_xFLD5tqkIyRfzBl9NUbNEBy_4zMz877Fe2AeG2f-Pc5OqUUgO0wRSYp2yyXDTy6RUkj5SwKHOxbNwxBUi5GkSCLbKdIK8EJCeATpkWLegDsdHE8V8KuR5H6SO0FnYsrJtvZtKAgC-WVCjDshUHrShBxbSTlFKatwG-X1Y?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/MTHg0q5YxwKoKIpVblDtZpXZtf3nsQodBrI0svMpP4ggPXGVQ6LdlX82hjSRbSTxg0PHeAAm0f8i_vIShppL9akQOGPFeC2TWu32F4c_ZJM1f2KOTwDk6Bc9mi-IDQY6VCZxL2jLZdtgEpusg4sVCjtjMtDMlvcdMC9pS4f6_MSeN2cx9gIy1gL1VWtsjAsi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xsGk40YGzMHYSIKk5t6kywc7PtWZsiclUvdSoDK5BjEbQ6nDqSgNg9_cU1B9vys4zUwnn0eWYauCT2O35PE8hKSfuM4tlItvhS1cKMdQJcHA6Ytl6psstMTDcGEc-CktoOl6Y92ol8W7dpbYiGzWvytsW6hdrCRBxA7_5eC0PTIjNM__Uc78ct09wsWwttni?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/m9pijr8kAimHwz4g8VpuqR6Us69PIbvlkY6U_xdweahte3h_hp98nc32EIvIkZLCasCrh64Bsopkav7cHLqADchbRWLcz4ya1NWCxMK3f6-l8JOkLSsSoV1QHHlMec5iBbHHmmTDbrWkcPsehKrwTt9iUuh81M8AiLxvbeynwxtVHWPl0fzIIQVkfMK9r0GQ?purpose=fullsize)

**mypy is a static type checker.**

Consider:

```python
def add(a: int, b: int) -> int:
    return a + b
```

You are explicitly saying:

```text
a → int
b → int
return → int
```

Now someone writes:

```python
add("hello", "world")
```

Python itself may not complain until runtime.

mypy can detect this before running the program.

Run:

```bash
uv run mypy src/
```

Think of it as:

> **"Do the types in my Python code make logical sense?"**

---

# 11. `mypy.ini`

This configures mypy.

For example:

```ini
[mypy]
python_version = 3.12
strict = true
```

You can control things such as:

* Python version
* strictness
* missing type annotations
* third-party library handling
* error reporting

So:

```text
mypy.ini
   │
   └── Rules for mypy
```

Again, modern projects can also put this configuration in `pyproject.toml`.

---

# 12. pytest

![Image](https://images.openai.com/static-rsc-4/-3nYxLFA7IsrM1_KDYP4JT1Lvg4QxF5Qp9KnRg5ydRcxxYhed5LyDEpiC9xxy4HT5xXelGlwWRznIZZFG6DXPkLlFt5QeD72vNN61NIw7egYQe01G9ytcLHH7NgK4epvQP51ZhREzxmpQ1Ek3gCk2f5mdVL5yXrZLHDFaVEDvKSOtp9RKG0r-dsi9CfyIvZO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/iueJCVw6YOr9V6ekDcVURRGQpUc8tQzFvhcs7xpgFm6BBaQegFCxcg1WG7LZI5Ibq9hGpSdbg1IWWrbY5qhh4ihMMzFXamIVbTsLDRDGtga1a6Dsu7SNOsrEvBYycSreHO5xMtXDtnjqHOGuIOFfVDAKdG-3PQrpcNOkjLZNiNi29VkbK0IbIzuyidNa4Xpi?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/AHzLqpurwGCrceHmq6jrlKJxXKIbAHl6ZV8gTe1Flyc4d4-dZ7oGXYqgnAkX7AocBxtyo2UucyypjV8oDyxN_vymKHh4FPHlpMGEiueuTlm63cnfFl1w_FsQHDFlAl1ueA6GteXCKxIbBvZQLeY9za_N46V1j06KULIycEr6RosjlF4MGqHIhdQTMiLIHEu5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DldyKBfCOrVXiUb30gTuNk-1fRrND6Flnf-Jz95Jdnr-L5GnXXVS2kCgd6VCJGxUSS6-sBHiQdLGM1WlK6z_2ljde1otLxY7lze2ud2qmvblu8C-xFNraUIfbCWUVigB34eLij0u2tBersa-Q_u4hwo2zk6tDH39nVC0N8fBN3P5R4uVjNNSmTdKNyhiCCSl?purpose=fullsize)

**pytest is a Python testing framework.**

Suppose:

```python
def add(a, b):
    return a + b
```

You create:

```python
def test_add():
    assert add(2, 3) == 5
```

Then:

```bash
uv run pytest
```

pytest runs the tests.

If everything passes:

```text
5 passed
```

If something breaks:

```text
1 failed
```

The important idea is:

> Tests verify that your software behaves correctly.

---

# 13. Unit tests vs integration tests

Your structure has:

```text
tests/
├── unit/
└── integration/
```

These have different purposes.

### Unit test

Tests one small component.

Example:

```text
config.py
    ↓
test_config.py
```

You might test:

```python
assert load_config().environment == "development"
```

The test should be fast and isolated.

### Integration test

Tests multiple components working together.

For example:

```text
API
 ↓
Service
 ↓
Database
```

An integration test checks that they actually work together.

So:

```text
Unit tests
    ↓
"Does this component work?"

Integration tests
    ↓
"Do these components work together?"
```

---

# 14. pre-commit

![Image](https://images.openai.com/static-rsc-4/KildoYcQaVmxmxKAayIqrMFJ4Qx7H1vk7p2dI4rMHZoRrRhDjFeKeOxqGH8WwIIi0b1SeKnOrOFtNV3WCuP_yiEqVt6U2m9L_Tj7wfe6fuJAhZhP3h1Nv_RmWmvo_uRRQiqWDF42IY8yaoF7dfyL2BI42M30nilWMER2bPCpPQ43QCsw4BRZfbsRdqjMLsPW?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Dt0nZ6VqGJ2N-PgEe1onfxBLS794a_l8fqwLF0pM4ev0hIJ47AFMferx495UH2bQmYQ9UbQP_ojdxFvIcYnrmP_zlVci_e_h4mEr6RgSaCfPRecXK512-jiOaxPu0NX4CPMOheWeLwAWcMVDVWUUuKFDDeyoNLiM3D5l3uKQhROWeTEhcsjUGOJpJK3Q_CE1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0oOkpbYcLHKvrt5DGbj1qkv_AR7icOb_dI-6-d3b43y6tOeax2I14eslMmRSIkw923aPlL6I-soXsGG7Rrg8qGjh4AkSB1GckmkGJ-AFO-x2llkuKipmfsCW3aLEK5JRiWBupFaiHz8o8PBGlGERqrWFUDtl11bSgqhRb477vfhOVsH1c3_HMAyF2XhqJxZw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/gSanslGEOoEhs1DRIiVHFwavYRc9kUcOpAAc0zfNBHNBNE82PpYZmTJl7kZoxKOUSmCCa9E8xfBIfEkOCiDkry4JvSl2x30X2QGTaln_hTjqV310BPAwZrvMiI6J0YTiQgYL0nzM9LppqBZBaXV-ATpvvpHttLDWjmFGhUSWld--Cam4Pkl4BEJ3hYi9ft5J?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KFOhwsdoGziGjnCd_e_0BvpzmfmBC_6XhpVn94_o-qYqaM0v1SHqqx6-7yg4Waw5fH8DtwU5nIm6I4_E71psL0LI6WHB13zRcW2VwcSoPPomZut2BaGmcj5HSEZ7Prsbz42MKRMIh2HGJtSD_TXwcIj9s1aGFQ9FNR9Xb6ISxWNZl0Sc96tmAHOiRXkYUPXJ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ToR-WtItVPoa775SjjR9FEijG8wGxajyeVRrG0UOyQWJStDuClBk-Jlv4ztPM5OgX_tZx5gpMaCxADC1ILwVJAw_TEUknayvGtvbxal35c7L5MY2wfcUnmq_kluxcTmOg3Ioppji7sCWhUdT6Aa1efC8sh3CWYA1s9jBK5dbQ1ryR3fiaevECJwtsygXsKNn?purpose=fullsize)

`pre-commit` automates checks **before you commit code to Git**.

Imagine you write:

```python
def hello(name):
    print("Hello", name)
```

Then you execute:

```bash
git add .
git commit -m "add hello"
```

Before Git creates the commit, pre-commit can automatically run:

```text
Ruff
   ↓
mypy
   ↓
other checks
   ↓
commit
```

If Ruff detects an error:

```text
Commit rejected
```

You fix it and try again.

---

# 15. `.pre-commit-config.yaml`

This defines what pre-commit should run.

Conceptually:

```yaml
repos:
  - repo: ...
    hooks:
      - id: ruff
      - id: ruff-format
```

So:

```text
.pre-commit-config.yaml
          │
          ├── Ruff
          ├── formatting
          ├── other checks
          └── ...
```

The benefit is that developers don't have to remember:

```bash
ruff check
ruff format
mypy
pytest
...
```

every time.

The Git workflow enforces it.

---

# 16. Makefile

A `Makefile` is basically a **command shortcut system**.

Without a Makefile:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy src/
uv run pytest
```

You can define:

```makefile
lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

typecheck:
	uv run mypy src/
```

Then:

```bash
make lint
```

or:

```bash
make test
```

or:

```bash
make format
```

You can also create a single command:

```makefile
check:
	uv run ruff check .
	uv run mypy src/
	uv run pytest
```

Then:

```bash
make check
```

runs the project's quality checks.

The Makefile isn't specifically Python technology. It's a **developer task runner**, commonly used in software projects.

---

# 17. `.gitignore`

This tells Git:

> Don't track these files.

For Python projects, you'd commonly have:

```gitignore
.venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.env
*.pyc
```

For example:

```text
.venv/
```

means:

```text
Don't upload the virtual environment to GitHub.
```

Because the environment can be recreated using:

```bash
uv sync
```

---

# 18. `README.md`

This is the project's **documentation entry point**.

Usually contains:

```text
What is this?
How do I install it?
How do I run it?
How do I test it?
How does it work?
```

A good README might have:

```text
# AI Platform Engineering Lab

## Setup

uv sync

## Run

uv run ...

## Test

uv run pytest

## Lint

uv run ruff check .
```

Think:

> **README = onboarding manual**

---

# 19. `src/`

This is your actual application source code.

```text
src/
└── engineering_lab/
```

The `src` layout is common in professional Python projects.

You don't generally put application code directly in the repository root.

Instead:

```text
src/
└── engineering_lab/
```

means:

```text
src/
   ↓
Python source code
```

---

# 20. `engineering_lab/`

This is the actual Python package.

```text
src/
└── engineering_lab/
    ├── __init__.py
    ├── main.py
    ├── config.py
    └── ...
```

The name:

```text
engineering_lab
```

is your Python package name.

You can then have imports such as:

```python
from engineering_lab.config import settings
```

---

# 21. `__init__.py`

This tells Python that this directory is a Python package.

```text
engineering_lab/
└── __init__.py
```

It can be completely empty:

```python
```

or contain package-level definitions.

For beginners, the simplest mental model is:

> `__init__.py` = package marker/initializer.

Modern Python has namespace packages, so it isn't technically required in every situation, but it's still common and useful in conventional package layouts.

---

# 22. `main.py`

This is usually the application's entry point.

For example:

```python
def main():
    print("Starting engineering lab")


if __name__ == "__main__":
    main()
```

Then:

```bash
uv run python -m engineering_lab.main
```

runs it.

In a larger application, `main.py` might initialize:

```text
Configuration
     ↓
Logging
     ↓
Database
     ↓
AI services
     ↓
API server
     ↓
Application
```

Don't assume `main.py` must contain all application logic. Ideally it should mostly **wire components together**.

---

# 23. `config.py`

Configuration belongs here.

For example:

```text
config.py
    │
    ├── API settings
    ├── database URL
    ├── environment
    ├── logging settings
    └── feature flags
```

For an AI platform, you might have:

```text
OPENAI_API_KEY
DATABASE_URL
REDIS_URL
ENVIRONMENT
LOG_LEVEL
```

You generally don't hardcode secrets:

```python
OPENAI_API_KEY = "sk-..."
```

Instead, read them from environment variables or a secret-management system.

---

# 24. `docs/`

This is where you document the engineering process.

This is particularly useful for your **AI Platform Engineering Lab** because you're presumably learning/building multiple infrastructure concepts.

```text
docs/
├── engineering-log.md
├── decisions/
└── experiments/
```

---

# 25. `engineering-log.md`

This is basically your **engineering journal**.

You could document:

```text
2026-08-16

Learned:
- uv
- dependency locking
- Ruff
- mypy

Built:
- initial project structure

Problems:
- mypy configuration issue

Solution:
...
```

This becomes valuable because you're recording not just **what you built**, but **what you learned**.

---

# 26. `docs/decisions/`

This can contain architectural decisions.

For example:

```text
docs/
└── decisions/
    ├── 001-use-postgres.md
    ├── 002-use-redis.md
    └── 003-use-kafka.md
```

Each decision can explain:

```text
Problem
    ↓
Options considered
    ↓
Decision
    ↓
Why?
    ↓
Trade-offs
```

This is often called an **ADR — Architecture Decision Record**.

Example:

```text
Decision:
Use PostgreSQL instead of MongoDB.

Why:
- relational data
- transactions
- strong consistency
- mature ecosystem

Trade-off:
- less flexible schema
```

---

# 27. `docs/experiments/`

This is where you keep experiments.

For example:

```text
docs/experiments/
├── redis-caching.md
├── llm-latency.md
├── postgres-benchmark.md
└── vector-search.md
```

Suppose you're comparing:

```text
OpenAI
vs
Gemini
vs
Ollama
```

You could document:

```text
Experiment
     ↓
Hypothesis
     ↓
Setup
     ↓
Measurements
     ↓
Results
     ↓
Conclusion
```

This is particularly relevant for platform engineering because performance and infrastructure decisions should ideally be evidence-based.

---

# 28. `scripts/`

This contains utility scripts that aren't really part of your core application.

For example:

```text
scripts/
├── seed_database.py
├── benchmark.py
├── generate_data.py
└── cleanup.py
```

You might run:

```bash
uv run python scripts/seed_database.py
```

Think:

```text
src/
    production/application code

scripts/
    developer/operational utilities
```

---

# 29. `.github/workflows/ci.yml`

This is where **GitHub Actions CI** comes in.

```text
.github/
└── workflows/
    └── ci.yml
```

CI means **Continuous Integration**.

Whenever you push code:

```text
git push
     ↓
GitHub
     ↓
GitHub Actions
     ↓
uv sync
     ↓
Ruff
     ↓
mypy
     ↓
pytest
     ↓
PASS / FAIL
```

For example:

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        ...

      - name: Install dependencies
        run: uv sync

      - name: Lint
        run: uv run ruff check .

      - name: Type check
        run: uv run mypy src/

      - name: Test
        run: uv run pytest
```

The exact configuration will vary, but the architecture is this:

```text
Developer
    │
    │ git commit
    ↓
pre-commit
    │
    ├── Ruff
    └── other checks
    │
    ↓
git push
    │
    ↓
GitHub Actions
    │
    ├── install dependencies
    ├── Ruff
    ├── mypy
    └── pytest
    │
    ↓
    PASS ✅
```

---

# 30. The entire structure

Now put everything together:

```text
ai-platform-engineering-lab/
│
├── README.md
│
├── pyproject.toml
│       │
│       └── Project definition + dependencies
│
├── uv.lock
│       │
│       └── Exact dependency versions
│
├── Makefile
│       │
│       └── Convenient developer commands
│
├── .gitignore
│       │
│       └── Files Git should ignore
│
├── .pre-commit-config.yaml
│       │
│       └── Checks before Git commits
│
├── ruff.toml
│       │
│       └── Ruff configuration
│
├── mypy.ini
│       │
│       └── mypy configuration
│
├── src/
│   └── engineering_lab/
│       │
│       ├── __init__.py
│       │       └── Python package
│       │
│       ├── main.py
│       │       └── Application entry point
│       │
│       ├── config.py
│       │       └── Application configuration
│       │
│       └── ...
│
├── tests/
│   ├── unit/
│   │       └── Individual component tests
│   │
│   └── integration/
│           └── Component interaction tests
│
├── docs/
│   ├── engineering-log.md
│   │       └── Learning/build log
│   │
│   ├── decisions/
│   │       └── Architecture decisions
│   │
│   └── experiments/
│           └── Experiments/benchmarks
│
├── scripts/
│       └── Utility/automation scripts
│
└── .github/
    └── workflows/
        └── ci.yml
                └── Automated CI pipeline
```

---

# 31. How you actually use all of this

Imagine you make a change to your application.

### Step 1 — Write code

```text
src/engineering_lab/
```

↓

### Step 2 — Write tests

```text
tests/
```

↓

### Step 3 — Check formatting/linting

```bash
uv run ruff check .
uv run ruff format .
```

↓

### Step 4 — Check types

```bash
uv run mypy src/
```

↓

### Step 5 — Run tests

```bash
uv run pytest
```

↓

### Step 6 — Commit

```bash
git add .
git commit -m "add configuration system"
```

`pre-commit` automatically runs configured checks.

↓

### Step 7 — Push

```bash
git push
```

↓

### Step 8 — GitHub Actions

```text
CI
│
├── uv sync
├── Ruff
├── mypy
└── pytest
```

↓

### Step 9

```text
Everything passes ✅
```

---

# 32. The most important distinction

If you're learning this for **platform engineering**, remember these categories:

| Tool/File                 | Main responsibility                                     |
| ------------------------- | ------------------------------------------------------- |
| `uv`                      | Python project/dependency/environment management        |
| `.venv`                   | Isolated Python environment                             |
| `pyproject.toml`          | Project metadata + dependency declaration + tool config |
| `uv.lock`                 | Exact dependency versions                               |
| Ruff                      | Linting + formatting                                    |
| `ruff.toml`               | Ruff configuration                                      |
| mypy                      | Static type checking                                    |
| `mypy.ini`                | mypy configuration                                      |
| pytest                    | Automated testing                                       |
| `pre-commit`              | Automated checks before commits                         |
| `.pre-commit-config.yaml` | pre-commit configuration                                |
| Makefile                  | Developer command shortcuts                             |
| `.gitignore`              | Files Git shouldn't track                               |
| `src/`                    | Application source                                      |
| `tests/`                  | Automated tests                                         |
| `docs/`                   | Engineering documentation                               |
| `scripts/`                | Utility/automation scripts                              |
| `.github/workflows/`      | CI/CD automation                                        |

---

# 33. The bigger picture

The important part isn't memorizing individual tools.

It's understanding the **software engineering pipeline**:

```text
                    PYTHON PROJECT
                         │
                         ▼
                  ┌──────────────┐
                  │ pyproject.toml│
                  └──────┬───────┘
                         │
                  dependencies
                         │
                         ▼
                    ┌─────────┐
                    │   uv    │
                    └────┬────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        uv.lock                    .venv
     exact versions             isolated env
             │                       │
             └───────────┬───────────┘
                         ▼
                    APPLICATION
                         │
             ┌───────────┼────────────┐
             ▼           ▼            ▼
           Ruff         mypy        pytest
             │           │            │
             └───────────┼────────────┘
                         ▼
                    pre-commit
                         │
                         ▼
                    git commit
                         │
                         ▼
                    git push
                         │
                         ▼
                  GitHub Actions
                         │
                 ┌───────┼────────┐
                 ▼       ▼        ▼
               Ruff     mypy    pytest
                 │       │        │
                 └───────┼────────┘
                         ▼
                    CI PASSED
```

That is the real purpose of this repository structure: **reproducibility, code quality, automated verification, and a predictable developer workflow**.

For an **AI Platform Engineering Lab**, this is a good foundation because you can later layer in Docker, PostgreSQL, Redis, Kafka, observability, CI/CD, Kubernetes, model serving, LLM gateways, evaluation, and infrastructure-as-code without turning the repository into an unstructured collection of experiments.

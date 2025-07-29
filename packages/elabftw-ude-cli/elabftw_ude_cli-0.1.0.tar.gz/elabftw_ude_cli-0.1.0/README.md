# elabftw\_ude\_cli

`elabftw_ude_cli` is a Python-based CLI and importable API for interacting with the [eLabFTW](https://www.elabftw.net) electronic lab notebook system, tailored for use at the University of Duisburg-Essen.

It provides:

* A command-line interface to create, modify, search, and read experiments.
* A Python API for programmatic integration with pipelines and notebooks.
* Tab-autocomplete support for fast CLI access.
* Optional integration with Python-based workflows like Snakemake.

---

## 🛠 Installation

```bash
pip install elabftw_ude_cli
```

### 🔑 Step 0: Add your API key and base URL

After installation, locate and edit your `config.py`:

```bash
python -c "import elabftw_ude_cli.config as c; print(c.get_config_file_path())"
```

Open this file and configure your `servers` dictionary and `server_to_use` key.

---

## ⚡ CLI Usage

After installation, use `elabftw-cli` from the command line.

### ♻️ Enable tab-completion (recommended)

```bash
activate-global-python-argcomplete --user
```

Or for bash/zsh:

```bash
eval "$(register-python-argcomplete elabftw-cli)"
```

### 📋 CLI Commands

```bash
elabftw-cli create_experiment --name "Exp Title" --body path/to/body.md --steps path/to/steps.json
elabftw-cli modify_experiment --exp_id 123 --body new_body.md --steps new_steps.json
elabftw-cli search_experiments --name-like "test"
elabftw-cli read_experiment --exp_id 123
```

#### Common CLI Options

* `--json`: Provide a JSON file with experiment metadata.
* `--body`: Text or HTML/Markdown file to use as body content.
* `--steps`: JSON file with step definitions.
* `--first` / `--all`: Control read behavior when multiple matches are found.
* `--outfile`: Save experiment(s) to a custom file.
* `-f`: Force title changes in modification.

---

## 🧑‍💻 Python API Usage

```python
import elabftw_ude_cli.api as elf

# Create an experiment
exp_id = elf.create_experiment(
    name="My Experiment",
    body="<h1>Intro</h1><p>This is HTML</p>",
    content_type=2
)

# Modify with body append and steps
elf.modify_experiment(
    exp_id=exp_id,
    body_append="Done.\nAll checked.",
    steps=[{"body": "step_3: summary"}]
)

# Complete step
elf.complete_step(exp_id, pattern="step_3", change="first", done_by="Alice")

# Search and read
ids, names = elf.search_experiments("test")
data = elf.read_experiment(exp_id=ids[0])
```

---

## 🧬 Snakemake Integration

Because Snakemake supports native Python and shell calls, you can use this library in rules:

```python
# In a rule or script:
import elabftw_ude_cli.api as elf

def report_to_elab(title, body, steps):
    return elf.create_experiment(name=title, body=body, steps=steps)
```

Or from the shell using `elabftw-cli`.

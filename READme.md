# ML Experiment Tracker MCP

> Query your MLflow experiments in plain English using Claude Desktop. No dashboards, no SQL — just ask.

![FastMCP](https://img.shields.io/badge/FastMCP-3.4.2-blue)
![MLflow](https://img.shields.io/badge/MLflow-3.x-orange)
![Python](https://img.shields.io/badge/Python-3.11+-green)

---

## What It Does

Connect Claude Desktop to your MLflow experiment tracker via an MCP server. Ask natural language questions and Claude queries your experiments automatically.

**Example questions you can ask Claude:**
- *"List all my ML experiments"*
- *"Which run had the best val_f1 in pothole-detector?"*
- *"What hyperparameters did the best model use?"*
- *"Compare the top 5 runs in road-crack-detection by accuracy"*
- *"Show me the metric history for run ID xyz"*

---

## Tools Exposed

| Tool | Description |
|---|---|
| `list_experiments` | Lists all experiments in MLflow |
| `compare_runs` | Ranks top N runs by a given metric |
| `get_best_model` | Returns the single best run for a metric |
| `fetch_metric_history` | Returns epoch-by-epoch metric history for a run |

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.11+** installed
- **uv** package manager (`pip install uv`)
- **Claude Desktop** downloaded from https://claude.ai/download
- **Git** installed

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/experiments-mcp.git
cd experiments-mcp
```

### 2. Create virtual environment with Python 3.11

```bash
uv venv --python /opt/homebrew/opt/python@3.11/bin/python3.11
source .venv/bin/activate
```

> **Windows:** use `.venv\Scripts\activate` instead

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

`requirements.txt` contains:
```
fastmcp
mlflow
pandas
```

### 4. Verify installation

```bash
python --version    # Should show Python 3.11.x
mlflow --version    # Should show mlflow, version 3.x.x
```

---

## Seed Fake Experiment Data (Optional)

If you don't have real MLflow experiments, run the seed script to populate fake but realistic data:

```bash
python seed_mlflow.py
```

This creates 2 experiments with 35 total runs:
- `pothole-detector` — 20 runs
- `road-crack-detection` — 15 runs

Each run has params (`learning_rate`, `batch_size`, `backbone`, `optimizer`) and metrics (`val_f1`, `val_accuracy`, `val_loss`, `train_f1`).

---

## Connect to Claude Desktop

### 1. Find your Python path

```bash
which python
# Example output: /Users/yourname/experiments-mcp/.venv/bin/python
```

### 2. Find your project path

```bash
pwd
# Example output: /Users/yourname/experiments-mcp
```

### 3. Edit Claude Desktop config

Open the config file:

```bash
# Mac
open ~/Library/Application\ Support/Claude/

# Windows
# %APPDATA%\Claude\claude_desktop_config.json
```

Add the `mcpServers` block to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ml-experiment-tracker": {
      "command": "/Users/yourname/experiments-mcp/.venv/bin/python",
      "args": [
        "/Users/yourname/experiments-mcp/server.py"
      ]
    }
  }
}
```

> Replace `/Users/yourname/experiments-mcp` with your actual paths from steps 1 and 2.

### 4. Restart Claude Desktop

```
Cmd + Q  →  reopen Claude Desktop
```

### 5. Verify connection

Click the **`+`** button in the chat input → **Add plugins** → your server should appear as connected.

Or simply type in chat:
```
List all my ML experiments
```

---

## Project Structure

```
experiments-mcp/
├── server.py           # MCP server — all 4 tools
├── mlflow_client.py    # MLflow SDK wrapper
├── seed_mlflow.py      # Fake data generator
├── requirements.txt    # Dependencies
└── README.md
```

---

## Using Your Own MLflow Data

By default the server points to a SQLite DB at `~/mcp/experiments-mcp/mlflow.db`.

To point it to your own MLflow instance, edit the top of `mlflow_client.py`:

```python
# Local SQLite (default)
mlflow.set_tracking_uri("sqlite:///path/to/your/mlflow.db")

# Remote MLflow server
mlflow.set_tracking_uri("http://your-mlflow-server:5000")
```

---

## Common Errors & Fixes

### `PermissionError: Operation not permitted: .venv/pyvenv.cfg`

**Cause:** Project is inside `~/Desktop` — Claude Desktop cannot access Desktop on Mac due to macOS security.

**Fix:** Move the project out of Desktop:
```bash
mv ~/Desktop/experiments-mcp ~/experiments-mcp
cd ~/experiments-mcp
```
Update the paths in `claude_desktop_config.json` accordingly.

---

### `ModuleNotFoundError: No module named 'mlflow'`

**Cause:** Wrong Python being used — system Python instead of venv Python.

**Fix:**
```bash
# Check which python is active
which python

# If it shows /usr/bin/python or /opt/homebrew/bin/python — wrong one
# Re-activate your venv:
source /full/path/to/experiments-mcp/.venv/bin/activate

# Then reinstall
uv pip install -r requirements.txt
```

---

### `MlflowException: filesystem tracking backend is in maintenance mode`

**Cause:** MLflow 3.x dropped file-based storage (`mlruns/` folder). Requires SQLite.

**Fix:** Make sure `mlflow_client.py` uses SQLite URI:
```python
import os
mlflow.set_tracking_uri(
    f"sqlite:///{os.path.expanduser('~/experiments-mcp/mlflow.db')}"
)
```
Also add the same line to `seed_mlflow.py` before running it.

---

### `sqlite3.OperationalError: unable to open database file`

**Cause:** The `.db` file doesn't exist yet — seed script hasn't been run, or was run from a different directory.

**Fix:**
```bash
cd ~/experiments-mcp
source .venv/bin/activate
python seed_mlflow.py
```

---

### `NameError: name 'os' is not defined`

**Cause:** Missing `import os` at the top of `mlflow_client.py`.

**Fix:** Add to the very first line of `mlflow_client.py`:
```python
import os
```

---

### `Server disconnected` in Claude Desktop

**Cause:** Could be any Python error in `server.py` or `mlflow_client.py`.

**Fix:** Check the logs:
```bash
tail -f ~/Library/Logs/Claude/mcp-server-ml-experiment-tracker.log
```
The last error in the log will tell you exactly what went wrong.

---

### `zsh: command not found: python`

**Cause:** On newer Macs, `python` is not aliased — use `python3` or activate venv properly.

**Fix:**
```bash
# Option 1: use python3
python3 seed_mlflow.py

# Option 2: recreate venv with correct python
uv venv --python /opt/homebrew/opt/python@3.11/bin/python3.11
source .venv/bin/activate
# now 'python' works
```

---

## Do I Need MLflow UI Running?

**No.** The MCP server reads directly from the SQLite database. You do NOT need to keep `mlflow ui` running for Claude to query your experiments.

---

## Tech Stack

- **FastMCP** — MCP server framework
- **MLflow 3.x** — Experiment tracking (SQLite backend)
- **pandas** — DataFrame processing for run results
- **Claude Desktop** — MCP client

---

## License

MIT
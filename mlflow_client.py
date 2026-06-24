import os
import mlflow
from mlflow.tracking import MlflowClient

# Use SQLite backend — no need to keep mlflow ui running
DB_PATH = os.path.expanduser("~/mcp/experiments-mcp/mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{DB_PATH}")

client = MlflowClient()


def get_all_experiments() -> list[dict]:
    experiments = mlflow.search_experiments()
    return [
        {
            "experiment_id": exp.experiment_id,
            "name": exp.name,
        }
        for exp in experiments
        if exp.name != "Default"
    ]


def get_runs(experiment_name: str, metric: str, top_n: int = 5) -> list[dict]:
    runs = mlflow.search_runs(
        experiment_names=[experiment_name],
        order_by=[f"metrics.{metric} DESC"],
    )
    if runs.empty:
        return []

    top_runs = runs.head(top_n)
    results = []

    for _, row in top_runs.iterrows():
        params  = {k.replace("params.",  ""): v for k, v in row.items() if k.startswith("params.")}
        metrics = {k.replace("metrics.", ""): v for k, v in row.items() if k.startswith("metrics.")}
        results.append({
            "run_id":   row["run_id"],
            "run_name": row.get("tags.mlflow.runName", "unknown"),
            "params":   params,
            "metrics":  metrics,
        })

    return results


def get_best_run(experiment_name: str, metric: str) -> dict:
    runs = get_runs(experiment_name, metric, top_n=1)
    if not runs:
        return {"error": f"No runs found in experiment '{experiment_name}'"}
    return runs[0]


def get_metric_history(run_id: str, metric: str) -> list[float]:
    history = client.get_metric_history(run_id, metric)
    return [m.value for m in history]
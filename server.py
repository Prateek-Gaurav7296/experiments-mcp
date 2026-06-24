from fastmcp import FastMCP
from mlflow_client import (
    get_all_experiments,
    get_runs,
    get_best_run,
    get_metric_history,
)

mcp = FastMCP("ML Experiment Tracker")


@mcp.tool()
def list_experiments() -> list[dict]:
    """
    Lists all available ML experiments tracked in MLflow.
    Call this first when the user wants to explore what experiments exist.
    Returns experiment names and IDs.
    """
    return get_all_experiments()


@mcp.tool()
def compare_runs(experiment_name: str, metric: str, top_n: int = 5) -> list[dict]:
    """
    Compares the top N runs in an experiment ranked by a given metric.
    Use this when the user wants to compare runs or find the best performing ones.

    Args:
        experiment_name: Name of the experiment (e.g. 'pothole-detector')
        metric: Metric to rank by (e.g. 'val_f1', 'val_accuracy', 'val_loss')
        top_n: Number of top runs to return (default 5)

    Returns:
        List of runs with their params and metrics, sorted best first.
    """
    return get_runs(experiment_name, metric, top_n)


@mcp.tool()
def get_best_model(experiment_name: str, metric: str) -> dict:
    """
    Returns the single best run in an experiment for a given metric.
    Use this when the user asks 'which model is best' or 'what are the
    best hyperparameters'. Always prefer this over compare_runs when
    the user wants just one answer.

    Args:
        experiment_name: Name of the experiment (e.g. 'pothole-detector')
        metric: Metric to optimize (e.g. 'val_f1', 'val_accuracy')

    Returns:
        Single best run with run_id, params, and metrics.
    """
    return get_best_run(experiment_name, metric)


@mcp.tool()
def fetch_metric_history(run_id: str, metric: str) -> list[float]:
    """
    Fetches the full history of a metric across all epochs for a specific run.
    Use this when the user wants to see how a metric changed during training,
    or to check if a model was overfitting.

    Args:
        run_id: The MLflow run ID (get this from compare_runs or get_best_model)
        metric: Metric name (e.g. 'val_f1', 'val_loss')

    Returns:
        List of metric values across epochs, in order.
    """
    return get_metric_history(run_id, metric)


if __name__ == "__main__":
    mcp.run()
# This script is used to seed the MLflow database with some dummy data. Completely optional.

import mlflow
import random
import os

DB_PATH = os.path.expanduser("~/mcp/experiments-mcp/mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{DB_PATH}")

random.seed(42)

backbones  = ["resnet50", "efficientnet_b0", "vit_base", "mobilenet_v3"]
optimizers = ["adam", "sgd", "adamw"]

# ── Experiment 1 ──────────────────────────────────────────
mlflow.set_experiment("pothole-detector")

for i in range(20):
    with mlflow.start_run(run_name=f"run_{i+1}"):
        lr     = random.choice([0.1, 0.01, 0.001, 0.0001])
        bs     = random.choice([16, 32, 64])
        epochs = random.randint(10, 50)
        bb     = random.choice(backbones)
        opt    = random.choice(optimizers)

        mlflow.log_param("learning_rate", lr)
        mlflow.log_param("batch_size",    bs)
        mlflow.log_param("epochs",        epochs)
        mlflow.log_param("backbone",      bb)
        mlflow.log_param("optimizer",     opt)

        val_f1       = round(random.uniform(0.65, 0.96), 4)
        val_accuracy = round(val_f1 + random.uniform(-0.02, 0.03), 4)
        val_loss     = round(random.uniform(0.10, 0.55), 4)
        train_f1     = round(val_f1 + random.uniform(0.01, 0.05), 4)

        mlflow.log_metric("val_f1",       val_f1)
        mlflow.log_metric("val_accuracy", val_accuracy)
        mlflow.log_metric("val_loss",     val_loss)
        mlflow.log_metric("train_f1",     train_f1)

# ── Experiment 2 ──────────────────────────────────────────
mlflow.set_experiment("road-crack-detection")

for i in range(15):
    with mlflow.start_run(run_name=f"run_{i+1}"):
        mlflow.log_param("learning_rate", random.choice([0.001, 0.0001]))
        mlflow.log_param("batch_size",    random.choice([32, 64]))
        mlflow.log_param("backbone",      random.choice(backbones))
        mlflow.log_param("optimizer",     random.choice(optimizers))

        mlflow.log_metric("val_f1",       round(random.uniform(0.60, 0.92), 4))
        mlflow.log_metric("val_accuracy", round(random.uniform(0.65, 0.94), 4))
        mlflow.log_metric("val_loss",     round(random.uniform(0.15, 0.60), 4))

print("✅ Done! Open http://localhost:5000 to see your experiments")
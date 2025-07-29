import argparse
import yaml
import pandas as pd
import joblib
from raikura.core.pipeline import AutoMLPipeline
from raikura.core.utils import set_seed, log_info, save_model
from raikura.core.preprocess import Preprocessor

def train_from_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    log_info("Starting training...")

    df = pd.read_csv(config["data"]["path"])
    target_col = config["data"]["target"]
    y = df[target_col].values
    X = df.drop(columns=[target_col])

    preprocessing_config = config.get("preprocessing", {})
    pre = Preprocessor()
    X_processed = pre.fit_transform(X, config=preprocessing_config)

    pipeline = AutoMLPipeline(
        task_type=config.get("task", "classification"),
        model_type=config["model"]["type"],
        problem=config.get("problem", "tabular")
    )
    pipeline.configure(**config["model"].get("params", {}))
    result = pipeline.train(X_processed, y)

    save_model(pipeline.model, config["output"]["model_path"])
    joblib.dump(X.columns.tolist(), config["output"]["columns_path"])

    log_info(f"Training complete. Accuracy: {result.get('accuracy', 'N/A')}")

def predict_from_file(model_path, columns_path, input_file):
    model = joblib.load(model_path)
    columns = joblib.load(columns_path)
    input_data = pd.read_json(input_file)
    input_data = input_data[columns]
    preds = model.predict(input_data)
    print({"predictions": preds.tolist()})

def run_cli():
    parser = argparse.ArgumentParser(description="Raikura Command Line Interface")
    subparsers = parser.add_subparsers(dest="command")

    train_parser = subparsers.add_parser("train")
    train_parser.add_argument("--config", required=True, help="Path to YAML config file")

    predict_parser = subparsers.add_parser("predict")
    predict_parser.add_argument("--model", required=True, help="Path to saved model file")
    predict_parser.add_argument("--columns", required=True, help="Path to column names file")
    predict_parser.add_argument("--input", required=True, help="Path to input JSON file")

    args = parser.parse_args()

    if args.command == "train":
        train_from_config(args.config)
    elif args.command == "predict":
        predict_from_file(args.model, args.columns, args.input)
    else:
        parser.print_help()

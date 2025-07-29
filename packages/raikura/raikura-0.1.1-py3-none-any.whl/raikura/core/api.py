import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union
import numpy as np
import pandas as pd
from joblib import load
from raikura.core.utils import load_config, explain_model
from raikura.core.metrics import Metrics
from raikura.core.preprocess import Preprocessor

app = FastAPI(title="Raikura Model API")

class PredictRequest(BaseModel):
    data: List[List[Union[float, int, str]]]
    columns: List[str]
    explain: Optional[bool] = False

class EvaluateRequest(BaseModel):
    X: List[List[Union[float, int, str]]]
    y: List[Union[int, float]]
    columns: List[str]

model = None
metrics = None
columns = None
preprocessor = None
preprocessing_config = None

@app.on_event("startup")
def load_resources():
    global model, metrics, columns, preprocessor, preprocessing_config
    model = load("raikura_model.pkl")
    columns = load("raikura_columns.pkl")
    preprocessing_config = load_config("preprocessing_config.json")
    preprocessor = Preprocessor()
    preprocessor.auto_detect_columns(pd.DataFrame(columns=columns))
    preprocessor.build_pipeline(config=preprocessing_config)
    metrics = Metrics(task_type="classification")

@app.post("/predict")
def predict(req: PredictRequest):
    global model, metrics, columns, preprocessor
    try:
        df = pd.DataFrame(req.data, columns=req.columns)
        df = df[columns]
        X_processed = preprocessor.pipeline.transform(df)
        preds = model.predict(X_processed)
        response = {"predictions": preds.tolist()}
        if req.explain:
            try:
                explain_model(model, df)
                response["explanation"] = "SHAP plot generated"
            except:
                response["explanation"] = "Explanation failed"
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    global model, metrics, columns, preprocessor
    try:
        X = pd.DataFrame(req.X, columns=req.columns)
        X = X[columns]
        X_processed = preprocessor.pipeline.transform(X)
        y = req.y
        y_pred = model.predict(X_processed)
        report = metrics.evaluate(y, y_pred)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/info")
def model_info():
    global model
    return {
        "model_type": str(type(model)),
        "columns": columns,
        "status": "Ready"
    }

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

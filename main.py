from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from joblib import load

from data_loader import load_and_consolidate
from train_model import select_features
from pricing_optimizer import run_optimization_sweep

MODEL_PATH = "xgb_sales_rate_model.pkl"
import numpy as np

app = FastAPI(title="CampNou Pricing API", version="1.0")

model = None
reference_features = None
static_data = None


class PredictRequest(BaseModel):
    match_id: int
    sector_id: int
    days_to_match: int
    occupancy_rate: float = Field(0.5, ge=0.0, le=1.0)
    match_importance: int = Field(7, ge=1, le=10)
    competition_type: str = Field("LaLiga")
    competition_phase: str = Field("Regular Season")
    is_derby: bool = Field(False)
    is_holiday_period: bool = Field(False)


class PredictResponse(BaseModel):
    match_id: int
    sector_id: int
    base_price: float
    xgboost_raw_prediction: float
    suggested_optimal_price: float
    expected_revenue: float
    message: str


@app.on_event("startup")
def startup_event():
    global model, reference_features, static_data

    try:
        model = load(MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(f"No se pudo cargar el modelo desde {MODEL_PATH}: {exc}")

    df = load_and_consolidate()

    if df.empty:
        raise RuntimeError("Data consolidada vacía en startup")

    static_data = df.set_index(["match_id", "sector_id"])

    # Construir esquema de features esperadas por el modelo
    reference_features = select_features(df).columns.tolist()


@app.post("/predict-price", response_model=PredictResponse)
def predict_price(req: PredictRequest):
    if model is None or reference_features is None or static_data is None:
        raise HTTPException(status_code=500, detail="Modelo o datos no inicializados")

    match_sector_key = (req.match_id, req.sector_id)
    if match_sector_key not in static_data.index:
        raise HTTPException(status_code=404, detail="Combinación Match/Sector no encontrada")

    static_row = static_row.iloc[0].copy()

    # Inyectar valores de la petición en la fila estática para construir el contexto
    static_row['days_to_match'] = req.days_to_match
    static_row['occupancy_rate'] = req.occupancy_rate
    static_row['match_importance'] = req.match_importance
    static_row['competition_type'] = req.competition_type
    static_row['competition_phase'] = req.competition_phase
    static_row['is_derby'] = req.is_derby
    static_row['is_holiday_period'] = req.is_holiday_period

    # Rango de barrido para optimización (ej: desde 50% hasta 250% del precio base)
    base_p = float(static_row["base_price"])
    p_range = np.linspace(base_p * 0.5, base_p * 2.5, 50)

    # Llamada al motor centralizado de optimización
    sweep_df, optimal, raw_ai_rate = run_optimization_sweep(
        model, reference_features, static_row, p_range
    )

    return PredictResponse(
        match_id=req.match_id,
        sector_id=req.sector_id,
        base_price=round(base_p, 2),
        xgboost_raw_prediction=round(raw_ai_rate, 2),
        suggested_optimal_price=round(optimal["Precio"], 2),
        expected_revenue=round(optimal["Ingresos"], 2),
        message="Optimización de precio completada con éxito",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

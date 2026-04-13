from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from joblib import load

from data_loader import load_and_consolidate
from train_model import select_features

MODEL_PATH = "xgb_current_price_model.pkl"

app = FastAPI(title="CampNou Pricing API", version="1.0")

model = None
reference_features = None
static_data = None


class PredictRequest(BaseModel):
    match_id: int
    sector_id: int
    days_to_match: int
    occupancy_rate: float = Field(..., ge=0.0, le=1.0)


class PredictResponse(BaseModel):
    match_id: int
    sector_id: int
    predicted_price: float
    suggested_price: float
    base_price: float
    predicted_revenue_potential: Optional[float]
    rule_applied: str
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

    static_row = static_data.loc[match_sector_key]
    if isinstance(static_row, pd.DataFrame):
        static_row = static_row.iloc[0]

    base_price = float(static_row["base_price"])
    opponent_ranking = int(static_row["opponent_ranking"])
    city_event = static_row.get("city_event", "No Event")

    # Payload -> DataFrame
    raw = pd.DataFrame([
        {
            "days_to_match": req.days_to_match,
            "opponent_ranking": opponent_ranking,
            "base_price": base_price,
            "occupancy_rate": req.occupancy_rate,
            "city_event": city_event,
            "sales_velocity": static_row.get("sales_velocity", 0.0),
            "revenue_potential": static_row.get("revenue_potential", 0.0),
        }
    ])

    print("[predict_price] raw dataframe columns:", raw.columns.tolist())

    # Usar la misma función de selección de features del entrenamiento
    X = select_features(raw)
    print("[predict_price] after select_features columns:", X.columns.tolist())

    # Forzar orden y llenar cualquier columna faltante esperada por el modelo
    X = X.reindex(columns=reference_features, fill_value=0.0)
    print("[predict_price] final feature matrix columns:", X.columns.tolist())

    print("[predict_price] input X:\n", X)

    pred_price = float(model.predict(X)[0])

    suggested_price = max(pred_price, base_price)
    rule_applied = "Ajuste aplicado: no sugerir precio menor al base_price." if suggested_price > pred_price else "No adjustment needed"

    predicted_revenue_potential = None
    if pd.notna(static_row.get("tickets_sold")):
        predicted_revenue_potential = suggested_price * float(static_row.get("tickets_sold", 0.0))

    return PredictResponse(
        match_id=req.match_id,
        sector_id=req.sector_id,
        predicted_price=round(pred_price, 2),
        suggested_price=round(suggested_price, 2),
        base_price=round(base_price, 2),
        predicted_revenue_potential=round(predicted_revenue_potential, 2) if predicted_revenue_potential is not None else None,
        rule_applied=rule_applied,
        message="Predicción completada con éxito",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

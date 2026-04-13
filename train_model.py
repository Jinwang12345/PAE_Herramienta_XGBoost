import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
import joblib

from data_loader import load_and_consolidate

MODEL_PATH = "xgb_sales_rate_model.pkl"

def select_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Columnas a excluir (IDs, targets, y redundantes)
    exclude = [
        "snapshot_id", "match_id", "sector_id", "sector_name", 
        "y_sales_rate_per_day", "y_tickets_sold_delta", 
        "tickets_sold", "tickets_remaining", "revenue_potential"
    ]
    
    # Identificar columnas categóricas para encoding
    categorical_cols = [
        "visibility_category", "time_bucket", "opponent", 
        "competition_type", "competition_phase", "match_importance"
    ]
    
    # Identificar columnas base de features
    features = [c for c in df.columns if c not in exclude]
    df_sub = df[features].copy()

    # Procesar categóricas con OneHotEncoder
    existing_cats = [c for c in categorical_cols if c in df_sub.columns]
    if existing_cats:
        enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        cat_enc = enc.fit_transform(df_sub[existing_cats].fillna("Unknown"))
        cat_cols = enc.get_feature_names_out(existing_cats)
        df_cat = pd.DataFrame(cat_enc, columns=cat_cols, index=df_sub.index)
        df_sub = pd.concat([df_sub.drop(columns=existing_cats), df_cat], axis=1)

    # Reemplazar nulos numéricos con la mediana
    df_sub = df_sub.fillna(df_sub.median(numeric_only=True))

    return df_sub

def train():
    df = load_and_consolidate()

    # Target: y_sales_rate_per_day
    target = "y_sales_rate_per_day"
    if target not in df.columns:
        raise ValueError(f"No se encontró {target} en el set de datos.")

    X = select_features(df)
    y = df[target].astype(float)

    print(f"Features seleccionadas: {X.shape[1]}")
    print(f"Registros para entrenamiento: {X.shape[0]}")

    # Validación temporal (TimeSeriesSplit)
    tscv = TimeSeriesSplit(n_splits=5)

    fold_results = []
    importances = []

    for fold, (train_idx, val_idx) in enumerate(tscv.split(X), start=1):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = XGBRegressor(
            n_estimators=1000,
            learning_rate=0.05,
            max_depth=6,
            early_stopping_rounds=20,
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1,
        )

        model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )

        y_pred = model.predict(X_val)
        mse = mean_squared_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)
        fold_results.append({"fold": fold, "mse": mse, "r2": r2})
        importances.append(model.feature_importances_)

        print(f"Fold {fold}: MSE={mse:.4f}, R2={r2:.4f}")

    mean_importance = np.mean(importances, axis=0)
    importance_df = pd.DataFrame({"feature": X.columns, "importance": mean_importance}).sort_values("importance", ascending=False)
    
    print("\nTop 15 Feature Importances:\n", importance_df.head(15))

    # Registro en memoria (Engram) de importancia de variables
    with open("feature_importance_engraving.txt", "w", encoding="utf-8") as f:
        f.write(f"Modelo: {MODEL_PATH}\n")
        f.write(f"Target: {target}\n")
        f.write("Importancia de features tras entrenamiento (Top 20):\n")
        for _, row in importance_df.head(20).iterrows():
            f.write(f"{row['feature']}: {row['importance']:.6f}\n")

    # Entrenar modelo final en todo el set
    print("\nEntrenando modelo final...")
    final_model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1,
    )
    final_model.fit(X, y)
    joblib.dump(final_model, MODEL_PATH)
    
    # Guardar las columnas del modelo para asegurar consistencia en la inferencia
    import json
    with open("model_features.json", "w") as f:
        json.dump(X.columns.tolist(), f)

    print(f"✓ Modelo final entrenado y guardado en {MODEL_PATH}")
    print(f"✓ Columnas del modelo guardadas en model_features.json")

if __name__ == "__main__":
    train()
if __name__ == "__main__":
    train()

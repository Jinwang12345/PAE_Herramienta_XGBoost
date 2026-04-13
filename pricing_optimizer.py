import pandas as pd
import numpy as np
import joblib
import os
import json
from data_loader import load_and_consolidate, CSV_DASHBOARD_PATH
from train_model import select_features, MODEL_PATH

FEATURES_PATH = "model_features.json"

def optimize_pricing():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(FEATURES_PATH):
        print(f"Error: No se encontró el modelo o las columnas en {MODEL_PATH}/{FEATURES_PATH}. Ejecuta train_model.py primero.")
        return

    # 1. Cargar el modelo y la lista de features
    print(f"Cargando modelo {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)
    with open(FEATURES_PATH, "r") as f:
        model_features = json.load(f)

    # 2. Cargar la plantilla del dashboard (contexto fijo)
    print(f"Cargando plantilla desde {CSV_DASHBOARD_PATH}...")
    template_df = load_and_consolidate(CSV_DASHBOARD_PATH)
    
    results = []

    # 3. Procesar cada fila (sector/partido) de la plantilla
    for idx, row in template_df.iterrows():
        sector_name = row.get("sector_name", f"Sector {row['sector_id']}")
        base_p = float(row["base_price"])
        horizon = float(row["horizon_days"])
        
        print(f"\nOptimizando {sector_name} (Base: {base_p:.2f}€, Horizonte: {horizon} días)")
        
        # Barrer precios: desde -30% hasta +30% del base
        price_range = np.linspace(base_p * 0.7, base_p * 1.3, 30)
        
        sector_results = []
        
        for price in price_range:
            # Duplicar el contexto y variar el precio
            temp_row = row.copy()
            temp_row["current_price"] = price
            temp_row["price_vs_base"] = price / base_p
            
            # Convertir a DataFrame para preprocessing
            input_df = pd.DataFrame([temp_row])
            X = select_features(input_df)
            
            # --- ASEGURAR CONSISTENCIA DE COLUMNAS ---
            # Reindexar para tener las mismas columnas que el modelo (rellenando con 0 las faltantes)
            X = X.reindex(columns=model_features, fill_value=0)
            
            # Predecir Sales Rate (Tasa Base)
            base_rate = model.predict(X)[0]
            base_rate = max(0, base_rate) # No tasas negativas
            
            # --- INYECCIÓN DE ELASTICIDAD DINÁMICA ---
            occ = float(row.get('occupancy_rate', 0.5))
            days = float(row.get('days_to_match', 30))
            
            E = 2.8 - (occ * 1.8)
            if days < 7:
                E -= 0.5
            E = max(0.1, E)
            
            price_ratio = price / base_p
            elasticity_factor = 1.0 - (price_ratio - 1.0) * E
            predicted_rate = max(0, base_rate * elasticity_factor)
            
            # Calcular demanda y revenue
            # Q = rate * horizon
            q = predicted_rate * horizon
            revenue = price * q
            
            sector_results.append({
                "price": price,
                "predicted_rate": predicted_rate,
                "expected_demand": q,
                "expected_revenue": revenue,
                "price_diff_pct": (price / base_p - 1) * 100
            })
        
        # Encontrar el precio óptimo
        sector_df = pd.DataFrame(sector_results)
        optimal = sector_df.loc[sector_df["expected_revenue"].idxmax()]
        
        print(f"  > Precio Óptimo: {optimal['price']:.2f}€ ({optimal['price_diff_pct']:+.1f}%)")
        print(f"  > Ingreso Esperado: {optimal['expected_revenue']:.2f}€")
        print(f"  > Venta Diaria Proyectada: {optimal['predicted_rate']:.2f} tickets/día")
        
        results.append({
            "sector": sector_name,
            "base_price": base_p,
            "optimal_price": optimal["price"],
            "optimal_revenue": optimal["expected_revenue"],
            "rate": optimal["predicted_rate"]
        })

    # Guardar resumen de optimización
    if results:
        summary_df = pd.DataFrame(results)
        summary_df.to_csv("pricing_optimization_results.csv", index=False)
        print("\n✓ Resultados guardados en pricing_optimization_results.csv")

        # Registrar en Engram (Simulando guardado de métricas clave)
        with open("feature_importance_engraving.txt", "a", encoding="utf-8") as f:
            f.write("\n" + "="*50 + "\n")
            f.write("Resultados de Optimización de Precios:\n")
            for res in results:
                f.write(f"Sector {res['sector']}: Cambio a {res['optimal_price']:.2f}€ (Rev: {res['optimal_revenue']:.2f}€)\n")
    else:
        print("\nNo se pudieron generar resultados de optimización.")

if __name__ == "__main__":
    optimize_pricing()
if __name__ == "__main__":
    optimize_pricing()

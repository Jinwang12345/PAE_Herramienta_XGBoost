import pandas as pd

CSV_TRAIN_PATH = "FCB_XGB_TRAIN_READY_excel_es.csv"
CSV_DASHBOARD_PATH = "FCB_DASHBOARD_INPUT_TEMPLATE_excel_es.csv"

def load_and_consolidate(csv_path: str = CSV_TRAIN_PATH) -> pd.DataFrame:
    """Carga el dataset consolidado listo para entrenamiento o inferencia."""
    print(f"Cargando dataset desde {csv_path}...")
    df = pd.read_csv(csv_path, sep=";")
    
    # Feature engineering adicional si fuera necesario
    # (El set base de FCB_XGB_TRAIN_READY ya viene filtrado y listo, 
    # pero podemos hacer limpiezas o transformaciones menores aquí).
    
    # Asegurar que los booleanos son interpretados correctamente
    bool_cols = ["is_derby", "star_signing_debut", "is_weekend", "is_holiday_period", "is_public_holiday"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(bool)
            
    # Tratar comas como decimales en columnas numéricas si pandas las lee como strings
    num_cols = ["y_sales_rate_per_day", "y_tickets_sold_delta", "base_price", "current_price", 
                "price_vs_base", "occupancy_rate", "sales_velocity", "team_availability_index", 
                "opponent_availability_index", "historical_goals_avg", "horizon_days", 
                "days_to_match", "opponent_ranking", "match_importance", "kickoff_hour", 
                "match_month", "match_dow", "is_weekend", "is_holiday_period", "is_public_holiday"]
                
    for col in num_cols:
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].str.replace(",", ".").astype(float)
            
    return df

def main() -> None:
    df = load_and_consolidate()
    print("Carga completada: registros finales =", len(df))
    print(df.head())

if __name__ == "__main__":
    main()

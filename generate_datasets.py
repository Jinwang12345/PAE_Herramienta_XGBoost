import json
import pandas as pd

def generate():
    print("Iniciando generación de dataset_v2_EQUIPO_FINAL.csv y dataset_v2_XGBOOST_encoded_FINAL.csv...")

    # Cargar el orden exacto de features que requiere el modelo XGBoost
    with open("model_features.json", "r", encoding="utf-8") as f:
        model_features = json.load(f)

    # 1. Definición de todos los Sectores y Zonas del Camp Nou
    sectors = [
        {"sector_id": 1, "sector_name": "Gol Nord 1", "item_area": "Gol Nord", "item_level": "1", "sector_family": "Gol", "visibility_category": "Standard", "capacity": 3200, "base_price": 35.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 2, "sector_name": "Gol Nord 2", "item_area": "Gol Nord", "item_level": "2", "sector_family": "Gol", "visibility_category": "Good", "capacity": 2800, "base_price": 42.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 3, "sector_name": "Gol Nord 3", "item_area": "Gol Nord", "item_level": "3", "sector_family": "Gol", "visibility_category": "Limited", "capacity": 3500, "base_price": 28.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 4, "sector_name": "Gol Sud 1", "item_area": "Gol Sud", "item_level": "1", "sector_family": "Gol", "visibility_category": "Standard", "capacity": 3200, "base_price": 35.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 5, "sector_name": "Gol Sud 2", "item_area": "Gol Sud", "item_level": "2", "sector_family": "Gol", "visibility_category": "Good", "capacity": 2800, "base_price": 42.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 6, "sector_name": "Gol Sud 3", "item_area": "Gol Sud", "item_level": "3", "sector_family": "Gol", "visibility_category": "Limited", "capacity": 3500, "base_price": 28.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 7, "sector_name": "Lateral 1", "item_area": "Lateral", "item_level": "1", "sector_family": "Lateral", "visibility_category": "Good", "capacity": 4000, "base_price": 75.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 8, "sector_name": "Lateral 2", "item_area": "Lateral", "item_level": "2", "sector_family": "Lateral", "visibility_category": "Premium", "capacity": 3800, "base_price": 88.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 9, "sector_name": "Lateral 3", "item_area": "Lateral", "item_level": "3", "sector_family": "Lateral", "visibility_category": "Standard", "capacity": 4200, "base_price": 60.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 10, "sector_name": "Tribuna 1", "item_area": "Tribuna", "item_level": "1", "sector_family": "Tribuna", "visibility_category": "Premium", "capacity": 3000, "base_price": 110.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 11, "sector_name": "Tribuna 2", "item_area": "Tribuna", "item_level": "2", "sector_family": "Tribuna", "visibility_category": "Premium", "capacity": 2800, "base_price": 135.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 12, "sector_name": "Tribuna 3", "item_area": "Tribuna", "item_level": "3", "sector_family": "Tribuna", "visibility_category": "Good", "capacity": 3200, "base_price": 95.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 13, "sector_name": "Corner Nord 1", "item_area": "Corner Nord", "item_level": "1", "sector_family": "Corner", "visibility_category": "Standard", "capacity": 1800, "base_price": 45.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 14, "sector_name": "Corner Sud 1", "item_area": "Corner Sud", "item_level": "1", "sector_family": "Corner", "visibility_category": "Standard", "capacity": 1800, "base_price": 45.0, "vip_type": "No_VIP", "vip_product": "none"},
        {"sector_id": 15, "sector_name": "VIP Tribuna 1", "item_area": "VIP Tribuna", "item_level": "1", "sector_family": "VIP", "visibility_category": "VIP", "capacity": 450, "base_price": 320.0, "vip_type": "VIP_Premium", "vip_product": "VIP_Tribuna"},
        {"sector_id": 16, "sector_name": "VIP Lateral 1", "item_area": "VIP Lateral", "item_level": "1", "sector_family": "VIP", "visibility_category": "VIP", "capacity": 500, "base_price": 260.0, "vip_type": "VIP_Normal", "vip_product": "VIP_Lateral"},
        {"sector_id": 17, "sector_name": "VIP Gol 1", "item_area": "VIP Gol", "item_level": "1", "sector_family": "VIP", "visibility_category": "VIP", "capacity": 350, "base_price": 190.0, "vip_type": "VIP_Normal", "vip_product": "VIP_Gol"}
    ]

    # 2. Partidos representativos de diversas competiciones
    matches = [
        {"match_id": 1, "opponent": "Real Betis", "competition_type": "Supercopa", "competition_phase": "Semifinal", "match_importance": 8, "is_derby": False, "opponent_ranking": 22, "kickoff_hour": 16, "match_month": 8, "match_dow": 0, "is_weekend": False},
        {"match_id": 2, "opponent": "Real Madrid", "competition_type": "LaLiga", "competition_phase": "Regular Season", "match_importance": 10, "is_derby": True, "opponent_ranking": 2, "kickoff_hour": 21, "match_month": 10, "match_dow": 6, "is_weekend": True},
        {"match_id": 3, "opponent": "Atlético Madrid", "competition_type": "LaLiga", "competition_phase": "Regular Season", "match_importance": 9, "is_derby": False, "opponent_ranking": 12, "kickoff_hour": 21, "match_month": 12, "match_dow": 6, "is_weekend": True},
        {"match_id": 4, "opponent": "Bayern Munich", "competition_type": "Champions League", "competition_phase": "League Phase", "match_importance": 10, "is_derby": False, "opponent_ranking": 4, "kickoff_hour": 21, "match_month": 11, "match_dow": 2, "is_weekend": False},
        {"match_id": 5, "opponent": "Espanyol", "competition_type": "LaLiga", "competition_phase": "Regular Season", "match_importance": 8, "is_derby": True, "opponent_ranking": 45, "kickoff_hour": 18, "match_month": 9, "match_dow": 5, "is_weekend": True},
        {"match_id": 6, "opponent": "Paris Saint-Germain", "competition_type": "Champions League", "competition_phase": "Round of 16", "match_importance": 10, "is_derby": False, "opponent_ranking": 6, "kickoff_hour": 21, "match_month": 2, "match_dow": 3, "is_weekend": False},
        {"match_id": 7, "opponent": "Sevilla FC", "competition_type": "LaLiga", "competition_phase": "Regular Season", "match_importance": 7, "is_derby": False, "opponent_ranking": 28, "kickoff_hour": 19, "match_month": 1, "match_dow": 6, "is_weekend": True},
        {"match_id": 8, "opponent": "Athletic Club", "competition_type": "Copa del Rey", "competition_phase": "Quarterfinal", "match_importance": 8, "is_derby": False, "opponent_ranking": 25, "kickoff_hour": 21, "match_month": 1, "match_dow": 3, "is_weekend": False},
        {"match_id": 9, "opponent": "Girona FC", "competition_type": "LaLiga", "competition_phase": "Regular Season", "match_importance": 7, "is_derby": True, "opponent_ranking": 35, "kickoff_hour": 16, "match_month": 3, "match_dow": 5, "is_weekend": True},
        {"match_id": 10, "opponent": "Inter Milan", "competition_type": "Champions League", "competition_phase": "Quarterfinal", "match_importance": 9, "is_derby": False, "opponent_ranking": 8, "kickoff_hour": 21, "match_month": 4, "match_dow": 2, "is_weekend": False},
        {"match_id": 11, "opponent": "Valencia CF", "competition_type": "LaLiga", "competition_phase": "Regular Season", "match_importance": 7, "is_derby": False, "opponent_ranking": 38, "kickoff_hour": 18, "match_month": 4, "match_dow": 6, "is_weekend": True},
        {"match_id": 12, "opponent": "Manchester City", "competition_type": "Champions League", "competition_phase": "Semifinal", "match_importance": 10, "is_derby": False, "opponent_ranking": 1, "kickoff_hour": 21, "match_month": 5, "match_dow": 2, "is_weekend": False}
    ]

    # 3. Línea temporal de ventas por partido
    time_snapshots = [
        {"days_to_match": 150, "time_bucket": "D91-150", "horizon_days": 30},
        {"days_to_match": 90, "time_bucket": "D61-90", "horizon_days": 30},
        {"days_to_match": 45, "time_bucket": "D31-60", "horizon_days": 15},
        {"days_to_match": 20, "time_bucket": "D15_30", "horizon_days": 7},
        {"days_to_match": 10, "time_bucket": "D8_14", "horizon_days": 5},
        {"days_to_match": 5, "time_bucket": "D4_7", "horizon_days": 3},
        {"days_to_match": 2, "time_bucket": "D1_3", "horizon_days": 1}
    ]

    equipo_rows = []
    encoded_rows = []
    snapshot_counter = 1

    for m in matches:
        for s in sectors:
            match_factor = (m["match_importance"] / 10.0) * (1.2 if m["is_derby"] else 1.0)
            sector_factor = 1.1 if s["sector_family"] in ["Gol", "Lateral"] else 0.95
            if s["sector_family"] == "VIP":
                sector_factor = 0.85
            
            final_occ = min(0.99, max(0.55, 0.65 * match_factor * sector_factor))

            for t in time_snapshots:
                d = t["days_to_match"]
                progress = (150 - d) / 148.0
                curr_occ = round(min(0.99, max(0.02, final_occ * (progress ** 1.3))), 4)
                
                tickets_sold = int(round(curr_occ * s["capacity"]))
                tickets_remaining = s["capacity"] - tickets_sold
                rem_pct = round(tickets_remaining / s["capacity"] * 100, 2)

                price_mult = 1.0 + (curr_occ * 0.35) + ((150 - d) / 150.0 * 0.15)
                if m["match_importance"] >= 9:
                    price_mult += 0.2
                if m["is_derby"]:
                    price_mult += 0.15
                
                curr_price = round(s["base_price"] * price_mult, 2)
                price_vs_base = round(curr_price / s["base_price"], 4)
                anchor_gap = round((price_vs_base - 1.0) * 100, 2)

                sales_velocity = round(max(0.1, (curr_occ * 3.5) + (m["match_importance"] * 0.3) - (d * 0.01)), 2)
                revenue_so_far = round(tickets_sold * (s["base_price"] * (1.0 + (price_mult - 1.0) * 0.6)), 2)
                rem_rev_pot = round(tickets_remaining * curr_price, 2)
                total_sec_rev = round(revenue_so_far + rem_rev_pot, 2)
                rev_per_cap = round(total_sec_rev / s["capacity"], 2)

                if curr_occ > 0.85:
                    scarcity = "critical"
                elif curr_occ > 0.65:
                    scarcity = "high"
                elif curr_occ > 0.40:
                    scarcity = "medium"
                else:
                    scarcity = "low"

                fomo = round(min(100.0, max(5.0, 30.0 + (curr_occ * 45.0) + (m["match_importance"] * 2.5) - (d * 0.15))), 1)
                social_proof = round(min(100.0, max(10.0, 15.0 + (curr_occ * 75.0))), 1)
                perceived_excl = round(min(100.0, max(10.0, 35.0 if s["sector_family"] != "VIP" else 85.0 + (curr_occ * 15.0))), 1)
                emotional_pull = round(min(100.0, max(20.0, 30.0 + (m["match_importance"] * 6.0) + (10.0 if m["is_derby"] else 0.0))), 1)
                price_fairness = round(min(100.0, max(10.0, 75.0 - (anchor_gap * 0.5) + (m["match_importance"] * 2.0))), 1)
                decision_pressure = round(min(100.0, max(5.0, 20.0 + (curr_occ * 40.0) + (m["match_importance"] * 2.0) - (d * 0.25))), 1)
                prem_anchor = round(min(100.0, max(20.0, 50.0 + (m["match_importance"] * 3.5))), 1)

                is_last_min = bool(d <= 3)
                is_fin_wk = bool(d <= 7)
                is_low_avail = bool(curr_occ >= 0.8)

                rate_per_day = round(max(0.1, sales_velocity * (1.1 - (price_vs_base - 1.0) * 0.5)), 3)
                delta_tickets = round(rate_per_day * t["horizon_days"], 1)

                # Diccionario para EQUIPO (legible)
                eq_row = {
                    "snapshot_id": snapshot_counter,
                    "match_id": m["match_id"],
                    "sector_id": s["sector_id"],
                    "horizon_days": t["horizon_days"],
                    "sector_name": s["sector_name"],
                    "visibility_category": s["visibility_category"],
                    "sector_capacity": s["capacity"],
                    "base_price": s["base_price"],
                    "days_to_match": d,
                    "time_bucket": t["time_bucket"],
                    "current_price": curr_price,
                    "price_vs_base": price_vs_base,
                    "tickets_sold": tickets_sold,
                    "tickets_remaining": tickets_remaining,
                    "occupancy_rate": curr_occ,
                    "sales_velocity": sales_velocity,
                    "opponent": m["opponent"],
                    "initial_sales_horizon": 150,
                    "opponent_ranking": m["opponent_ranking"],
                    "match_importance": m["match_importance"],
                    "is_derby": m["is_derby"],
                    "team_form": 14,
                    "league_position": 1,
                    "team_availability_index": 85.0,
                    "opponent_availability_index": 78.0,
                    "historical_goals_avg": 2.1,
                    "star_signing_debut": False,
                    "kickoff_hour": m["kickoff_hour"],
                    "match_month": m["match_month"],
                    "match_dow": m["match_dow"],
                    "is_weekend": m["is_weekend"],
                    "is_holiday_period": False,
                    "is_public_holiday": False,
                    "competition_type": m["competition_type"],
                    "competition_phase": m["competition_phase"],
                    "sector_family": s["sector_family"],
                    "vip_type": s["vip_type"],
                    "vip_product": s["vip_product"],
                    "price_scenario": "standard",
                    "zone_elasticity_class": "medium",
                    "scarcity_level": scarcity,
                    "broadcast_type": "pay",
                    "tourism_season_index": "medium",
                    "weather_temperature": 19.5,
                    "rain_probability": 0.1,
                    "bad_weather_flag": False,
                    "is_televised": True,
                    "competing_event_city": False,
                    "is_premium_experience": bool(s["sector_family"] == "VIP"),
                    "hospitality_included": bool(s["sector_family"] == "VIP"),
                    "is_low_availability": is_low_avail,
                    "is_last_minute": is_last_min,
                    "is_final_week": is_fin_wk,
                    "remaining_capacity_pct": rem_pct,
                    "urgency_score": float(m["match_importance"]),
                    "willingness_to_pay_index": round(30.0 + (m["match_importance"] * 5) + (curr_occ * 20), 1),
                    "perceived_value_score": round(40.0 + (m["match_importance"] * 4), 1),
                    "price_sensitivity_score": round(max(10.0, 70.0 - (m["match_importance"] * 3)), 1),
                    "fomo_index": fomo,
                    "social_proof_index": social_proof,
                    "perceived_exclusivity_index": perceived_excl,
                    "emotional_pull_index": emotional_pull,
                    "price_fairness_score": price_fairness,
                    "decision_pressure_index": decision_pressure,
                    "anchor_price_gap": anchor_gap,
                    "premium_anchor_strength": prem_anchor,
                    "revenue_so_far": revenue_so_far,
                    "remaining_revenue_potential": rem_rev_pot,
                    "total_sector_revenue_potential": total_sec_rev,
                    "revenue_per_capacity": rev_per_cap,
                    "y_sales_rate_per_day": rate_per_day,
                    "y_tickets_sold_delta": delta_tickets,
                    "item_area": s["item_area"],
                    "item_level": s["item_level"]
                }
                equipo_rows.append(eq_row)

                # Construir mapa completo de valores para el encoded
                enc_data = {
                    "snapshot_id": snapshot_counter,
                    "match_id": m["match_id"],
                    "sector_id": s["sector_id"],
                    "y_sales_rate_per_day": rate_per_day,
                    "y_tickets_sold_delta": delta_tickets,
                    "horizon_days": t["horizon_days"],
                    "sector_capacity": s["capacity"],
                    "base_price": s["base_price"],
                    "days_to_match": d,
                    "current_price": curr_price,
                    "price_vs_base": price_vs_base,
                    "occupancy_rate": curr_occ,
                    "sales_velocity": sales_velocity,
                    "opponent_ranking": m["opponent_ranking"],
                    "match_importance": m["match_importance"],
                    "is_derby": m["is_derby"],
                    "team_form": 14,
                    "league_position": 1,
                    "team_availability_index": 85.0,
                    "opponent_availability_index": 78.0,
                    "historical_goals_avg": 2.1,
                    "star_signing_debut": False,
                    "kickoff_hour": m["kickoff_hour"],
                    "match_month": m["match_month"],
                    "match_dow": m["match_dow"],
                    "is_weekend": m["is_weekend"],
                    "is_holiday_period": False,
                    "is_public_holiday": False,
                    "price_sensitivity_score": round(max(10.0, 70.0 - (m["match_importance"] * 3)), 1),
                    "willingness_to_pay_index": round(30.0 + (m["match_importance"] * 5) + (curr_occ * 20), 1),
                    "perceived_value_score": round(40.0 + (m["match_importance"] * 4), 1),
                    "is_premium_experience": bool(s["sector_family"] == "VIP"),
                    "hospitality_included": bool(s["sector_family"] == "VIP"),
                    "remaining_capacity_pct": rem_pct,
                    "is_low_availability": is_low_avail,
                    "is_last_minute": is_last_min,
                    "is_final_week": is_fin_wk,
                    "urgency_score": float(m["match_importance"]),
                    "weather_temperature": 19.5,
                    "rain_probability": 0.1,
                    "bad_weather_flag": False,
                    "is_televised": True,
                    "competing_event_city": False,
                    "fomo_index": fomo,
                    "social_proof_index": social_proof,
                    "perceived_exclusivity_index": perceived_excl,
                    "emotional_pull_index": emotional_pull,
                    "price_fairness_score": price_fairness,
                    "decision_pressure_index": decision_pressure,
                    "anchor_price_gap": anchor_gap,
                    "premium_anchor_strength": prem_anchor,
                }

                # One-hot features
                for vis in ["Good", "Limited", "Premium", "Standard", "VIP"]:
                    enc_data[f"visibility_category_{vis}"] = 1 if s["visibility_category"] == vis else 0

                for tb in ["D15_30", "D1_3", "D31_60", "D4_7", "D61_90", "D8_14", "D91_150"]:
                    enc_data[f"time_bucket_{tb}"] = 1 if t["time_bucket"] == tb else 0

                c_norm = m["competition_type"].replace(" ", "_")
                for ct in ["Champions_League", "Copa_del_Rey", "Friendly", "LaLiga", "Supercopa"]:
                    enc_data[f"competition_type_{ct}"] = 1 if c_norm == ct else 0

                p_norm = m["competition_phase"].replace(" ", "_")
                phases = ["Final", "League_Phase", "Mid_season", "Playoff", "Pre_season", "Quarterfinal", "Regular_Season", "Round_of_16", "Round_of_32", "Semifinal", "Summer_Tour"]
                for cp in phases:
                    enc_data[f"competition_phase_{cp}"] = 1 if p_norm == cp else 0

                for sf in ["Corner", "Gol", "Lateral", "Tribuna", "VIP"]:
                    enc_data[f"sector_family_{sf}"] = 1 if s["sector_family"] == sf else 0

                v_norm = s["vip_type"].replace(" ", "_")
                for vt in ["No_VIP", "VIP_Normal", "VIP_Premium"]:
                    enc_data[f"vip_type_{vt}"] = 1 if v_norm == vt else 0

                vip_prods = ["Balcony_Corner_Primera_Fila", "Balcony_Gol", "Palco_Presidencial", "Pitch_Row_Lateral", "Pitch_Row_Lateral_Central", "Pitch_Row_Tribuna", "Players_Zone", "VIP_Corner", "VIP_Gol", "VIP_Lateral", "VIP_Tribuna", "none"]
                for vp in vip_prods:
                    enc_data[f"vip_product_{vp}"] = 1 if s["vip_product"] == vp else 0

                for ps in ["bajo_estimado", "extrema_observado", "interpolado", "normal_observado", "standard"]:
                    enc_data[f"price_scenario_{ps}"] = 1 if ps == "standard" else 0

                for ze in ["elastic", "inelastic", "medium", "medium_high", "medium_low", "very_inelastic"]:
                    enc_data[f"zone_elasticity_class_{ze}"] = 1 if ze == "medium" else 0

                for sc in ["critical", "high", "low", "medium"]:
                    enc_data[f"scarcity_level_{sc}"] = 1 if sc == scarcity else 0

                for bt in ["none", "pay"]:
                    enc_data[f"broadcast_type_{bt}"] = 1 if bt == "pay" else 0

                for ts in ["high", "low", "medium"]:
                    enc_data[f"tourism_season_index_{ts}"] = 1 if ts == "medium" else 0

                # Para el dataframe encoded, las columnas deben seguir el orden EXACTO:
                # 1. IDs y targets excluidos del modelo
                # 2. Las 113 features en el orden exacto de model_features.json
                ordered_enc_row = {
                    "snapshot_id": enc_data["snapshot_id"],
                    "match_id": enc_data["match_id"],
                    "sector_id": enc_data["sector_id"],
                    "y_sales_rate_per_day": enc_data["y_sales_rate_per_day"],
                    "y_tickets_sold_delta": enc_data["y_tickets_sold_delta"],
                }
                for feat in model_features:
                    ordered_enc_row[feat] = enc_data.get(feat, 0)

                encoded_rows.append(ordered_enc_row)
                snapshot_counter += 1

    df_equipo = pd.DataFrame(equipo_rows)
    df_encoded = pd.DataFrame(encoded_rows)

    # Exportar con el formato estándar del proyecto (separador ; y coma decimal)
    df_equipo.to_csv("dataset_v2_EQUIPO_FINAL.csv", sep=";", decimal=",", index=False)
    df_encoded.to_csv("dataset_v2_XGBOOST_encoded_FINAL.csv", sep=";", decimal=",", index=False)

    print("Datasets generados con éxito:")
    print(f" - dataset_v2_EQUIPO_FINAL.csv ({len(df_equipo)} filas, {len(df_equipo.columns)} columnas)")
    print(f" - dataset_v2_XGBOOST_encoded_FINAL.csv ({len(df_encoded)} filas, {len(df_encoded.columns)} columnas)")

if __name__ == "__main__":
    generate()

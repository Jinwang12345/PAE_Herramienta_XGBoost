# 📊 FC Barcelona: Motor de Pricing Dinámico

Este repositorio contiene la herramienta de optimización de precios para el FC Barcelona, basada en modelos de Machine Learning (XGBoost) para predecir la demanda y maximizar los ingresos por sección del Camp Nou.

## 🚀 Cómo empezar

Para ejecutar la herramienta en tu ordenador local, sigue estos pasos:

### 1. Requisitos previos
Asegúrate de tener instalado Python 3.8 o superior. Se recomienda usar un entorno virtual.

### 2. Instalación de dependencias
Instala las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación Visual (Streamlit)
La forma más sencilla de probar la herramienta es a través del dashboard interactivo:
```bash
streamlit run app_visual.py
```

## 📂 Estructura del Proyecto

- `app_visual.py`: Dashboard interactivo (Streamlit) para simular escenarios y ver el precio óptimo.
- `pricing_optimizer.py`: Motor de cálculo que realiza el "sweep" de precios y encuentra el máximo de ingresos.
- `train_model.py`: Script para entrenar el modelo XGBoost desde cero.
- `data_loader.py`: Funciones para cargar y consolidar los datasets del proyecto.
- `xgb_sales_rate_model.pkl`: El modelo ya entrenado listo para usar.
- `model_features.json`: Configuración de las variables que el modelo necesita.

## ⚠️ Nota sobre los Datasets
Los archivos de datos de gran tamaño (`.csv` de más de 100MB) no están incluidos en este repositorio por límites de GitHub. Para que la herramienta funcione completamente, asegúrate de tener los archivos `dataset_v2_XGBOOST_encoded.csv` y `dataset_v2_EQUIPO.csv` en la carpeta raíz.

---
**Desarrollado para la optimización de ingresos del FCB.** 🔵🔴

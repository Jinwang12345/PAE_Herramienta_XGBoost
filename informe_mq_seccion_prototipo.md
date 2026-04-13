# Sección del Prototipo: Herramienta de Optimización Dinámica de Precios (Dynamic Pricing Dashboard)

## 1. Introducción y Objetivo del Prototipo
El prototipo desarrollado consiste en una herramienta interactiva e inteligente de *Dynamic Pricing*, diseñada específicamente para maximizar los ingresos por venta de entradas (Ticketing) en las instalaciones del Camp Nou. Integra un motor predictivo basado en Machine Learning con una interfaz analítica en tiempo real que permite al responsable de taquilla evaluar distintos escenarios de demanda y determinar sistemáticamente el precio óptimo para cada encuentro y sector del estadio.

## 2. Arquitectura Tecnológica y Modelado Algorítmico (Back-end)
El núcleo inteligente ("Back-end") del prototipo está sustentado en un pipeline de procesamiento y modelado de datos desarrollado en Python:

*   **Modelo Predictivo Central:** Se ha implementado y entrenado un modelo de regresión avanzada basado en **XGBoost Regressor** (`xgb_sales_rate_model.pkl`). La variable objetivo (Target) es la "Tasa de Venta Diaria" (`y_sales_rate_per_day`), lo que permite proyectar cuántos tickets se venderán en un horizonte temporal determinado.
*   **Gestión de Variables (Feature Engineering):** El pipeline (`train_model.py`) prepara los datos categorizando elementos clave —como la categoría de visibilidad del sector, el rival (opponent), el tipo y fase de la competición, y la importancia del encuentro— utilizando `OneHotEncoder`. Para validar la robustez predictiva, el entrenamiento empleó validación cruzada temporal (`TimeSeriesSplit`).
*   **Algoritmo de Optimización Algorítmica (`pricing_optimizer.py`):** El proceso de optimización toma un estado base y realiza simulaciones de *sweep* (barrido de precios). Genera un intervalo de precios dinámicos (típicamente desde un -30% hasta un +30% del precio base original). Para cada precio teórico, consulta al modelo XGBoost la tasa de ventas esperada bajo esa condición, calculando consecuentemente la Demanda Estimada ($Q = Tasa \times Horizonte$) y el Ingreso Esperado ($Precio \times Q$). El algoritmo devuelve automáticamente el punto de precio que maximiza matemáticamente el volumen total de ingresos.

## 3. Interfaz de Usuario y Analítica Visual (Front-end)
De cara al operador de ticketing, la herramienta presenta una "Admin Console" intuitiva y reactiva desarrollada bajo la librería analítica interactiva **Streamlit**. Destaca por su usabilidad y su arquitectura de información enfocada en la toma de decisiones ágiles.

*   **Estética Corporativa:** Implementa una interfaz "Glassmorphism" adaptada con la paleta de colores oficial y el branding corporativo del FC Barcelona, garantizando una adopción fluida por parte del usuario de negocio.
*   **Parámetros de Simulación *What-If*:** A través del panel lateral y los *sliders* de contexto central, el usuario puede manipular manualmente variables dinámicas clave del mercado (Días restantes para el choque, % de Ocupación actual y Velocidad de ventas).
*   **Cuadro de Mando Integrado (KPIs):** Tras procesar el barrido frente al modelo, el frontend destaca en pantalla las métricas de oro:
    1.  **Precio Óptimo** (junto con la desviación porcentual respecto al precio inicial fijado en pre-temporada).
    2.  Proyección total de ingresos en ese sector.
    3.  Tasa de Ventas Proyectada.
    4.  Demanda esperada al nuevo precio.
*   **Gráficos Inteligentes (`Plotly`):** Renderiza dinámicamente dos gráficas analíticas fundamentales: 
    *   *Curva de Ingresos vs. Precio*, indicando la distribución parabólica y el umbral de máxima rentabilidad.
    *   *Curva de Decaimiento de la Tasa de Ventas*, ilustrando gráficamente la elasticidad-precio de la demanda del aficionado para ese encuentro en particular.

## 4. Flujo de Operación del Sistema ("User Journey")
1.  **Inyección de Datos (Carga de Contexto):** El sistema ingiere una plantilla maestra CSV (`FCB_DASHBOARD_INPUT_TEMPLATE.csv`) u otorga la opción de subir una snapshot en vivo.
2.  **Selección de Escenario:** El usuario filtra el partido y el "Sector Context" sobre el cual desea actuar.
3.  **Ajuste y Recomendación:** El usuario comprueba el estado sugerido, efectúa pequeños ajustes manuales de sensibilidad temporal y visualiza automáticamente la actualización del Precio Óptimo en vivo.
4.  **Trazabilidad:** Todos los ajustes, predicciones recomendadas y métricas de desempeño de las variables (Feature Importance) persisten localmente en registros de trazabilidad y reportes de optimización para revisiones retrospectivas.

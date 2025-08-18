# Desafío 2 — Telecom X · Churn de Clientes

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flacoca1970/Desafio_2/blob/main/notebooks/TelecomX_LATAM_inyectado.ipynb)

Este repositorio contiene el proyecto completo del **Desafío Telecom X**, con un flujo **ETL → EDA → Modelado** listo para ejecutarse en **Google Colab** o localmente.

## 🎯 Objetivo
Entender los factores que explican la **evasión de clientes (churn)** y dejar la base para un modelo predictivo, siguiendo buenas prácticas de **ETL**, **EDA** y **ML** sin fuga de datos.

## 📦 Contenido principal
- `notebooks/TelecomX_LATAM_inyectado.ipynb`: Notebook con el pipeline completo (ETL, aplanado, EDA, dataset model-ready, baseline y balanceo).
- `scripts/run_all.py`: Script CLI para ejecutar el pipeline rápidamente.
- `src/telecomx/*`: Módulos Python (ETL/EDA/Modelado) para reutilización.
- `data/`: Carpeta con datos crudos (JSON), intermedios y procesados.
- `reports/`: Informe y figuras generadas.

## 🚀 Cómo correr en Colab
1. Haz click en el badge **Open in Colab** (arriba).
2. En la celda **Configuración** del notebook, usa:
   - `USE_API=True` y define `API_URL`, **o**
   - `USE_API=False` y sube `data/raw/TelecomX_Data.json` a tu sesión de Colab (o monta Drive).
3. Ejecuta celdas en orden: **Setup → Extracción → Transformación → EDA → Model-ready → Baseline → ROS**.

## 🖥️ Cómo correr localmente
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_all.py
```

---

## 📊 Resumen de resultados (EDA)

- **Filas totales:** 7267
- **Filas con `Churn` vacío:** 224
- **Tasa global de churn (target conocido):** **26.54%**

**Tasas de churn por categoría (si existen en el JSON):**
- **Contract**
  - Month-to-month → 42.71%
  - One year → 11.27%
  - Two year → 2.83%
- **PaymentMethod**
  - Electronic check → 45.29%
  - Mailed check → 19.11%
  - Bank transfer (automatic) → 16.71%
  - Credit card (automatic) → 15.24%
- **InternetService**
  - Fiber optic → 41.89%
  - DSL → 18.96%
  - No → 7.40%

> Estas cifras pueden ser 0.00% si tu JSON no trae esas categorías exactas o si cambió el esquema.

---

## 🧪 Metodología y buenas prácticas

- **ETL**
  - Carga robusta desde API/JSON.
  - Aplanado de estructuras anidadas (`customer`, `phone`, `internet`, `account`).
  - Normalización de `Churn` a `Yes/No/NaN`.
  - Tipificación de numéricos (e.g., `MonthlyCharges`, `TotalCharges`, `tenure`).

- **EDA**
  - Tasas de churn por categorías clave (Contract, PaymentMethod, InternetService).
  - Estadísticos de numéricos por `Churn` (si están presentes).

- **Modelado base**
  - Dataset **model-ready**: `Churn` → 0/1; se excluye target faltante.
  - `train_test_split` **estratificado**.
  - `Pipeline` + `ColumnTransformer` para imputar/escala/OneHot.
  - Baseline con **`LogisticRegression(class_weight="balanced")`**.
  - Variante con **`RandomOverSampler`** (sólo en el **train**) para evitar **data leakage**.

- **Data Leakage — reglas de oro**
  - Balancear **después** del split y sólo sobre `X_train, y_train`.
  - Imputar/escala/encodear dentro del **Pipeline**.
  - No usar información de `test` en selección de features ni tuning.
  - Target encoding sólo con CV o dentro de pipeline apropiado.

---

## 🧠 Conclusiones (para el informe)
- El churn tiende a **concentrarse** en clientes con **contrato mes a mes** y **pago con cheque electrónico**; **fiber optic** suele mostrar mayor churn que DSL/No Internet.
- **Hipótesis:** alta fricción de pago, baja inercia contractual y expectativas de calidad/precio impulsan la evasión.
- **Recomendaciones:** 
  - Incentivos de permanencia para **Month-to-month** (anualización, bundles).
  - Migrar a **pagos automáticos** y mejorar UX de facturación.
  - **Retención temprana** (onboarding proactivo en primeros meses).
  - Monitoreo de satisfacción/tickets especialmente en **Fiber optic**.

**Limitaciones:** filas con `Churn` vacío; posibles variables no observadas (satisfacción, reclamos, competencia).

---

## 📁 Estructura
```
.
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ notebooks/
│  └─ TelecomX_LATAM_inyectado.ipynb
├─ data/
│  ├─ raw/
│  │  └─ TelecomX_Data.json
│  ├─ interim/
│  │  └─ TelecomX_df_flat.csv
│  └─ processed/
│     └─ TelecomX_df_flat_model.csv
├─ reports/
│  ├─ figures/
│  │  ├─ TelecomX_churn_rate_por_contract.png
│  │  ├─ TelecomX_churn_rate_por_payment.png
│  │  └─ TelecomX_churn_rate_por_internet_service.png
└─ src/
   └─ telecomx/
      ├─ __init__.py
      ├─ etl.py
      ├─ eda.py
      └─ modeling.py
```

---

© 2025 — Proyecto académico. Uso educativo.


# Desafío Telecom X — Churn (Colab-only)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flacoca1970/Desafio_2/blob/main/notebooks/TelecomX_LATAM_colab.ipynb)

Este repositorio contiene **un único Notebook** para Google Colab que ejecuta **todo el flujo** de punta a punta: **ETL → EDA → Modelado con GridSearch → Calibración (Platt/Isotónica) → Curva de ganancia/umbral de negocio → Informe automático**.  
Está pensado para que **un perfil no técnico (Ventas/CS/Marketing)** pueda entender los hallazgos y **activarlos en campañas**.

## 🚀 Abrir y ejecutar en Colab (3 pasos)
1. **Clic en el badge** “Open in Colab” (arriba).  
2. En **Parámetros**, elige API o sube `TelecomX_Data.json` a `/content`. Ajusta `VALUE_RETAIN` y `COST_CONTACT` si quieres.
3. Ejecuta celdas en orden. Al final, corre **“Informe automático”** → genera `/content/reports/README_REPORT.md` y CSVs de apoyo.

## 🧩 ETL (qué hace y por qué)
- **Aplanado** a notación punto: `account.Contract`, `internet.InternetService`, `customer.tenure`, etc.
- **Normalización Yes/No** preservando categorías como “No internet service”.
- **Tipificación numérica** de `MonthlyCharges`, `TotalCharges`, `tenure` (y alias).
- **Naming estándar y orden** de columnas clave.  
**Salida**: `/content/data/interim/df_limpo.csv`.

## 🔎 EDA (hallazgos clave)
- **Contract**: Month-to-month ≫ One year ≫ Two year  
- **PaymentMethod**: Electronic check > Mailed check > Bank/Credit (auto)  
- **InternetService**: Fiber optic > DSL > No  
→ Riesgo alto donde hay **baja inercia**, **fricción en pago** y **expectativas altas de servicio**.

## 🤖 Modelado
- Split estratificado 80/20. `ColumnTransformer` (imputación, escalado, One-Hot).
- **Model Zoo + GridSearch** por **PR-AUC**: Logistic (balanced), RF (balanced), GB, HGB, LinearSVC (calibrado).
- **Calibración** de probabilidades (Platt/Isotónica) y evaluación en test (ROC-AUC, PR-AUC).

## 💸 Umbral de negocio
Función de ganancia:
```
Ganancia = (TP × VALUE_RETAIN) − ((TP + FP) × COST_CONTACT)
```
Se barre el umbral y se elige el que **maximiza ganancia**. Exporta **Top N** clientes en riesgo (`/content/reports/clientes_en_riesgo_topN.csv`) listos para CRM.

## 🎯 Playbooks de retención
- **Month-to-month** → oferta de **anualización** (mes gratis/upgrade).  
- **Electronic check** → incentivos a **pagos automáticos**.  
- **Fiber optic** → soporte proactivo, revisión de calidad/visita técnica.  
- **Tenure bajo** → onboarding intensivo.  
- **Cargos altos** → paquetes flex/downsizing preventivo.

## 📈 KPIs
Churn mensual/segmento, adopción de pagos automáticos, % retenidos, ARPU post-retención, costo de intervención, tiempo al primer contacto, NPS post intervención.

## ⚠️ Limitaciones y próximos pasos
Correlacional, no causal. Añadir señales de operación (tickets/velocidad/caídas), calibración por cohorte, orquestar scoring semanal + envío a CRM.

---

© 2025 — Proyecto académico.

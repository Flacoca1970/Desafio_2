# Desafío Telecom X — Churn (Solo para Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flacoca1970/Desafio_2/blob/main/TelecomX_LATAM_colab.ipynb)


Este proyecto entrega un **pipeline 100% en Google Colab** que ejecuta: **ETL → EDA → Modelado con GridSearch → Calibración (Platt/Isotónica) → Curva de ganancia y umbral de negocio → Informe automático + lista de clientes en riesgo (Top N)**.
Está escrito para que **Ventas/CS/Marketing** entiendan **qué hacer** con los resultados y **cómo activarlos** en campañas.

---

## 1) Resumen ejecutivo (con tus métricas reales)

- **Churn global** de la muestra: **{{GLOBAL_CHURN_RATE}}**.
- **Mejor modelo (CV por PR-AUC)**: **{{BEST_MODEL}}** con **PR-AUC (CV)={{PR_AUC_CV}}**.
- En test: **ROC-AUC={{ROC_AUC_TEST}}**, **PR-AUC={{PR_AUC_TEST}}**, **calibración={{CALIBRATION}}**.
- **Umbral óptimo (negocio)**: **{{THRESHOLD}}** ⇒ **Ganancia estimada={{PROFIT}}** (con `VALUE_RETAIN={{VALUE_RETAIN}}` y `COST_CONTACT={{COST_CONTACT}}`).

**Dónde se concentra el churn (EDA)**:
- **Contrato**: mayor tasa en **{{TOP_CONTRACT}}** ({{TOP_CONTRACT_RATE}}).
- **Medio de pago**: mayor tasa en **{{TOP_PAYMENT}}** ({{TOP_PAYMENT_RATE}}).
- **Internet**: mayor tasa en **{{TOP_INTERNET}}** ({{TOP_INTERNET_RATE}}).

**Qué hacer (en simple):**
1. **Exportar** clientes **≥ umbral** (Top N) con su *churn score*.
2. Disparar **campañas** con ofertas y guiones diferenciados por segmento (contrato, pago, internet, tenure).
3. **Medir ROI** por oleada y **ajustar** el umbral según resultados.

---

## 2) Cómo usar (en 3 pasos)

1. **Abrir Colab** con el badge.
2. En **Parámetros**: usa **API** o sube `TelecomX_Data.json` a `/content`. Ajusta `VALUE_RETAIN`/`COST_CONTACT`.
3. Ejecuta en orden: **ETL → EDA → Model → Calibración → Ganancia → Informe**.

Se generan:
- `/content/data/interim/df_limpo.csv` (ETL)
- `/content/reports/metrics.json`, `/content/reports/README_REPORT.md`
- `/content/reports/clientes_en_riesgo_topN.csv` (lista lista para CRM)

---

## 3) Recomendaciones accionables (priorizadas)

1. **Anualización de “Month-to-month”** → 1 mes gratis/upgrade; canal: outbound/WhatsApp; KPI: % anualización, churn 60/90d.
2. **Migración a auto-pay** desde *Electronic check* → bono de adhesión; KPI: adopción, reducción churn/mora.
3. **Programa “Experiencia Fibra”** → soporte proactivo (ONT/router), speed test y visita prioritaria; KPI: reclamos/1000, churn fibra, NPS.
4. **Onboarding de tenure bajo** → secuencia de bienvenida y “health check” a 15–30d; KPI: churn <90d, uso de self-service.
5. **Paquetes flex para cargos altos** → downsell preventivo; KPI: retención vs. ARPU post-retención (margen).

---

## 4) Detalle técnico (resumen)

- Split estratificado 80/20; **sin data leakage**.
- Prepro: imputación (mediana/moda), escalado y One-Hot con `ColumnTransformer`.
- **Model Zoo + GridSearch** por **PR-AUC** (CV=5): Logistic (balanced), RF (balanced), GB, HGB, LinearSVC (calibrado).
- **Calibración**: se compara Platt vs. Isotónica y se elige la mejor en test.
- **Umbral de negocio**: maximiza Ganancia(t) = TP×VALUE_RETAIN − (TP+FP)×COST_CONTACT.

> Este README se autorrellena con las métricas de tu corrida más reciente.

# Desafío 2 — Telecom X (Colab-only)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flacoca1970/Desafio_2/blob/main/notebooks/TelecomX_LATAM_colab.ipynb)

Este repositorio contiene **un único notebook** listo para ejecutarse en Google Colab con **todo el flujo** dentro del notebook: **ETL → EDA → GridSearch → Calibración → Curva de ganancia y umbral de negocio**.

## Uso en Colab
1. Haz clic en el badge **Open in Colab**.
2. En la celda de parámetros, define si usar **API** o subir `TelecomX_Data.json` a `/content`.
3. Ejecuta las celdas en orden. El notebook guardará artefactos en `/content/data/interim/` y `/content/reports/` (opcional).

> No hay scripts externos ni Makefile: *todo está implementado dentro del notebook*.

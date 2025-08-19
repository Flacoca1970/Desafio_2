# Desafío Telecom X — Churn (Solo para Colab)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/flacoca1970/Desafio_2/blob/main/TelecomX_LATAM_colab.ipynb)


Este proyecto entrega un **pipeline 100% en Google Colab** y explica de forma **técnica y de negocio** cómo usarlo para **reducir la evasión de clientes (churn)**.  
Flujo: **ETL → EDA → Modelado (GridSearch) → Calibración → Umbral de negocio y Ganancia → Informe automático → Export Top N para CRM**.

---

## 1) Resumen ejecutivo (con resultados reales de tu corrida)

- **Filas**: 7,267 | **Columnas**: 21  
- **Churn global**: **26.54%**
- **Factores con más churn** (EDA):  
  - **Contract**: *Month-to-month* (**42.71%**) ≫ *One year* (11.27%) ≫ *Two year* (2.83%)  
  - **PaymentMethod**: *Electronic check* (**45.29%**) > *Mailed check* (19.11%) > *Bank transfer (automatic)* (16.71%) > *Credit card (automatic)* (15.24%)  
  - **InternetService**: *Fiber optic* (**41.89%**) > *DSL* (18.96%) > *No* (7.40%)
- **Modelo ganador (CV por PR-AUC)**: **GradientBoosting (`gb`)**  
  - **PR-AUC (CV)**: **0.6612**
  - En test: **ROC-AUC** **0.8481**, **PR-AUC** **0.6639**, **calibración**: *isotonic*
- **Umbral de negocio óptimo**: **0.030**  
  - **Ganancia estimada**: **31,635.00** (con `VALUE_RETAIN=100.0`, `COST_CONTACT=5.0`)
  - **Matriz de confusión (test, al umbral negocio)**  
    |       | Pred No | Pred Yes |
    |-------|:-------:|:--------:|
    | Real No  | 313 | 722 |
    | Real Yes |  3  | 371 |
  - Lectura: **recall muy alto** (371/374 ≈ 99.2%) y **precisión moderada** (371/1093 ≈ 33.9%). Con *VALUE_RETAIN ≫ COST_CONTACT*, conviene **capturar casi todos los churners**, aun a costo de más falsos positivos.

**Qué hacer ahora (en simple):**
1) Exporta la **lista de clientes ≥ umbral** (Top N) ordenada por *churn score*.  
2) Ejecuta **campañas de retención** por **segmento** (ver §6 y §7).  
3) Mide **ROI** por oleada y **ajusta** el umbral si es necesario.

---

## 2) Cómo abrir y ejecutar en Colab (3 pasos)

1. **Clic** en el badge “Open in Colab”.  
2. En la celda **Parámetros**: usa `USE_API=True` + `API_URL` **o** sube `TelecomX_Data.json` a `/content` (`USE_API=False`).  
   Opcional: cambia `VALUE_RETAIN` y `COST_CONTACT` para adaptar el umbral de negocio.  
3. Ejecuta todas las celdas: **ETL → EDA → Model → Calibración → Ganancia → Informe**.  
   El cuaderno generará:
   - `/content/data/interim/df_limpo.csv`
   - `/content/reports/metrics.json` y `/content/reports/README_REPORT.md`
   - `/content/reports/clientes_en_riesgo_topN.csv` (lista para CRM)

---

## 3) ETL — qué hicimos y por qué

- **Aplanado** de estructuras anidadas a notación punto: `account.Contract`, `internet.InternetService`, `customer.tenure`, etc.  
- **Normalización Yes/No** → `Yes`/`No` estándar, **sin forzar** columnas con categorías extra (ej.: *No internet service*).  
- **Conversión numérica** de `MonthlyCharges`, `TotalCharges`, `tenure` (y alias).  
- **Naming estándar** (alias → nombre común) y **orden** de columnas clave.  
- **Target (`Churn`)**: para entrenamiento, se **filtran** filas sin etiqueta clara (`yes/no`) para evitar errores y sesgos. En EDA, se pueden dejar nulos.  
**Salida**: `df_limpo.csv` reproducible desde el JSON original.

---

## 4) EDA — dónde se concentra el churn (tablas)

**Contract**  
| account.Contract | churn_rate |
|---|---:|
| Month-to-month | 42.71% |
| One year | 11.27% |
| Two year | 2.83% |

**PaymentMethod**  
| account.PaymentMethod | churn_rate |
|---|---:|
| Electronic check | 45.29% |
| Mailed check | 19.11% |
| Bank transfer (automatic) | 16.71% |
| Credit card (automatic) | 15.24% |

**InternetService**  
| internet.InternetService | churn_rate |
|---|---:|
| Fiber optic | 41.89% |
| DSL | 18.96% |
| No | 7.40% |

**Lectura de negocio**: mayor churn cuando hay **baja inercia de permanencia** (*Month-to-month*), **fricción de pago** (*Electronic check*) y/o **expectativas de servicio altas** (*Fiber*).

---

## 5) Modelado — cómo comparamos y por qué ganó `gb`

- **Split** estratificado: 80/20 (sin data leakage).  
- **Preprocesamiento** con `ColumnTransformer`: imputación (mediana/moda), *scaling* para numéricas y *One-Hot* para categóricas.  
- **Model Zoo + GridSearch** (selección por **PR-AUC**, CV=5): *Logistic (balanced)*, *RandomForest (balanced)*, *GradientBoosting (gb)*, *HistGradientBoosting*, *LinearSVC (calibrado)*.  
- **Calibración de probabilidades**: *Isotónica* vs *Platt*, se eligió **Isotónica** por mejor desempeño en test.  
- **Resultados**: `gb` entregó **mejor balance de precisión/recall** (PR-AUC 0.6639 en test) y se calibró para umbrales accionables.

---

## 6) Umbral de negocio y ROI (cómo decidir a quién llamar)

La ganancia se calcula como:

```
Ganancia(t) = (TP × VALUE_RETAIN) − ((TP + FP) × COST_CONTACT)
```

Con `VALUE_RETAIN=100` y `COST_CONTACT=5`, el **umbral óptimo** fue `t=0.030`, maximizando **31,635** de ganancia.  
**Implicancia**: conviene **capturar casi todos los churners** (recall≈99.2%), aceptando más contactos innecesarios (precisión≈33.9%). Si subes `COST_CONTACT` o baja `VALUE_RETAIN`, el umbral subirá y contactaremos **menos** clientes (más precisión, menos recall).

> Ajusta estos parámetros antes de cada campaña para alinear el modelo a la **realidad económica** del momento.

---

## 7) Recomendaciones de acción (prioridad descendente)

1. **Anualizar “Month-to-month”**  
   Oferta: 1 mes gratis / upgrade de velocidad / router premium por anualizar.  
   *Canales*: outbound + WhatsApp. *KPIs*: % anualización; churn 60/90 días; margen post-retención.

2. **Migrar de “Electronic check” a auto-pay**  
   Incentivo de adhesión (bono o descuento por 3 meses).  
   *KPIs*: adopción auto-pay; reducción de churn y mora.

3. **Programa “Experiencia Fibra”** (cohortes Fiber)  
   Health-check proactivo: ONT/router, test de velocidad guiado, visita prioritaria.  
   *KPIs*: reclamos/1000; churn fibra; NPS post intervención.

4. **Onboarding reforzado (tenure bajo)**  
   Secuencia de bienvenida, tutoriales, 1er health-check a 15–30 días.  
   *KPIs*: churn <90 días; uso de app/portal; tickets.

5. **Paquetes flex / downsell preventivo (cargos altos)**  
   Evitar fuga por precio con paquetes escalonados.  
   *KPIs*: retención vs ARPU/margen post-retención.

---

## 8) Segmentación accionable para campañas

- **Riesgo alto** (score ≥ umbral):  
  - *Month-to-month + Electronic check + Fiber*: **prioridad 1** (anualización + auto-pay + health-check fibra).  
  - *Month-to-month + auto-pay*: **prioridad 2** (anualización + beneficios de fidelidad).  
  - *Tenure < 3 meses*: **onboarding** + llamada de satisfacción.

- **Riesgo medio** (score a −10% del umbral): nurturing con valor; contacto si hay ticket/reclamo reciente.  
- **Riesgo bajo** (score < −20% del umbral): educación y promos *pull* (sin costo de contacto elevado).

---

## 9) Plan 30-60-90 y KPIs

**30 días (pilotos)**  
- 2 campañas: anualización y migración a auto-pay (Top 5–10k clientes).  
- Umbral según ganancia; medición de conversión y costo real.

**60 días (escalado)**  
- Ajuste de umbral por ROI.  
- Programa Fibra en zonas calientes.  
- Onboarding automatizado.

**90 días (operacionalizar)**  
- Scoring semanal + export a CRM.  
- Playbooks por cohorte (Fiber vs DSL).  
- Tablero de KPIs y alertas.

**KPIs core**: churn total y por segmento; adopción auto-pay; % retenidos; ARPU/margen post-retención; costo por cliente retenido; tiempo a primer contacto; NPS post intervención.

---

## 10) Export a CRM (lista lista para acción)

El notebook genera **`/content/reports/clientes_en_riesgo_topN.csv`** con: `customerID`, `churn_score`, `flag_churn_risk` y atributos clave (contrato, pago, internet, tenure).  
Ordena por `churn_score` desc y **cárgalo al CRM** para priorizar llamadas/WhatsApp/email según el **playbook del segmento**.

---

## 11) Transparencia y próximos pasos

- El modelo es **predictivo, no causal**. Usa campañas y **A/B tests** para validar hipótesis de ofertas.  
- Evita **data leakage**: balanceo/transformaciones, sólo en *train*.  
- Privacidad: aplica la normativa local (uso legítimo, mínimo necesario).  
- Mejoras: señales operativas (tickets/caídas/velocidad), calibración por cohorte, *uplift modeling* para optimizar incentivos.

---

## 12) Estructura mínima del repo

```
/TelecomX_LATAM_colab.ipynb                # cuaderno único (o /notebooks/...)
/content/data/interim/df_limpo.csv         # generado al correr
/content/reports/README_REPORT.md          # informe automático
/content/reports/metrics.json              # métricas reales de tu corrida
/content/reports/clientes_en_riesgo_topN.csv
```

---

### Anexos
- Diccionario de datos: https://github.com/alura-cursos/challenge2-data-science-LATAM/blob/main/TelecomX_diccionario.md
- Nota de clase: **balancear sólo tras el split** y convertir `yes/no` a numérico para modelado; mantener “No internet service” como categoría aparte.

**Contacto**: Equipo Data Science — Proyecto *Churn de Clientes* @ Telecom X.  
**Versión**: Colab-only (autogeneración de informe).

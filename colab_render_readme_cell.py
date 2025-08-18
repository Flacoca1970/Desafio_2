# === Colab: generar README.md autocompletado con métricas reales ===
import os, json, pandas as pd, numpy as np

template_path = "/content/README_TEMPLATE_auto.md"   # sube la plantilla o cópiala aquí
output_path   = "/content/README.md"
metrics_path  = "/content/reports/metrics.json"

# EDA CSVs opcionales
eda_contract_csv = "/content/reports/churn_rate_by_contract.csv"
eda_payment_csv  = "/content/reports/churn_rate_by_paymentmethod.csv"
eda_internet_csv = "/content/reports/churn_rate_by_internetservice.csv"

def pct(x):
    try:
        return f"{100*float(x):.2f}%"
    except:
        return "—"

# 1) Cargar métricas
with open(metrics_path, "r") as f:
    m = json.load(f)

# 2) Encontrar tasa global de churn desde df_limpo si está disponible
global_rate = None
try:
    df = pd.read_csv("/content/data/interim/df_limpo.csv")
    if "Churn" in df.columns:
        global_rate = (df["Churn"].astype(str).str.lower()=="yes").mean()
except Exception:
    pass

# 3) Top categorías de EDA
def top_row(path, col_name):
    try:
        t = pd.read_csv(path)
        t = t.sort_values("churn_rate", ascending=False).iloc[0]
        return str(t[col_name]), pct(t["churn_rate"])
    except Exception:
        return "—", "—"

top_contract, top_contract_rate = top_row(eda_contract_csv, "Contract") if os.path.exists(eda_contract_csv) else ("—","—")
top_payment,  top_payment_rate  = top_row(eda_payment_csv, "PaymentMethod") if os.path.exists(eda_payment_csv) else ("—","—")
top_internet, top_internet_rate = top_row(eda_internet_csv, "InternetService") if os.path.exists(eda_internet_csv) else ("—","—")

# 4) Sustitución de placeholders
with open(template_path, "r", encoding="utf-8") as f:
    txt = f.read()

repls = {
    "{{GLOBAL_CHURN_RATE}}": pct(global_rate) if global_rate is not None else "—",
    "{{BEST_MODEL}}": str(m.get("best_model","—")),
    "{{PR_AUC_CV}}": f"{m.get('cv_best_pr_auc', float('nan')):.4f}" if m.get("cv_best_pr_auc") is not None else "—",
    "{{ROC_AUC_TEST}}": f"{m.get('test_roc_auc', float('nan')):.4f}" if m.get("test_roc_auc") is not None else "—",
    "{{PR_AUC_TEST}}": f"{m.get('test_pr_auc', float('nan')):.4f}" if m.get("test_pr_auc") is not None else "—",
    "{{CALIBRATION}}": str(m.get("calibration","—")),
    "{{THRESHOLD}}": f"{m.get('business_best_threshold', float('nan')):.3f}" if m.get("business_best_threshold") is not None else "—",
    "{{PROFIT}}": f"{m.get('business_best_profit', float('nan')):.2f}" if m.get("business_best_profit") is not None else "—",
    "{{VALUE_RETAIN}}": str(m.get("value_retain","—")),
    "{{COST_CONTACT}}": str(m.get("cost_contact","—")),
    "{{TOP_CONTRACT}}": top_contract,
    "{{TOP_CONTRACT_RATE}}": top_contract_rate,
    "{{TOP_PAYMENT}}": top_payment,
    "{{TOP_PAYMENT_RATE}}": top_payment_rate,
    "{{TOP_INTERNET}}": top_internet,
    "{{TOP_INTERNET_RATE}}": top_internet_rate,
}

for k,v in repls.items():
    txt = txt.replace(k, v)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(txt)

print("README generado en:", output_path)
print("Usó métricas de:", metrics_path)
if os.path.exists(eda_contract_csv):
    print("EDA contrato:", eda_contract_csv)
if os.path.exists(eda_payment_csv):
    print("EDA pago:", eda_payment_csv)
if os.path.exists(eda_internet_csv):
    print("EDA internet:", eda_internet_csv)

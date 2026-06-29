import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from xgboost import XGBClassifier

print("Loading retail data...")

df = pd.read_csv("data/processed/cleaned_retail.csv")

df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# -----------------------------
# Customer Features
# -----------------------------

customer_features = df.groupby("customerid").agg({
    "revenue": ["sum", "mean", "max", "min"],
    "quantity": ["sum", "mean"],
    "invoiceno": "nunique"
})

customer_features.columns = [
    "total_revenue",
    "avg_revenue",
    "max_revenue",
    "min_revenue",
    "total_quantity",
    "avg_quantity",
    "purchase_frequency"
]

customer_features.reset_index(inplace=True)

customer_features["avg_order_value"] = (
    customer_features["total_revenue"]
    / customer_features["purchase_frequency"]
)

# -----------------------------
# Churn Label
# -----------------------------

last_purchase = (
    df.groupby("customerid")["invoicedate"]
      .max()
      .reset_index()
)

reference_date = df["invoicedate"].max()

last_purchase["days_inactive"] = (
    reference_date - last_purchase["invoicedate"]
).dt.days

last_purchase["churn"] = (
    last_purchase["days_inactive"] > 90
).astype(int)

customer_features = customer_features.merge(
    last_purchase[
        ["customerid",
         "days_inactive",
         "churn"]
    ],
    on="customerid"
)

# -----------------------------
# Training
# -----------------------------

X = customer_features.drop(
    ["customerid", "churn"],
    axis=1
)

y = customer_features["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = XGBClassifier(
    n_estimators=244,
    max_depth=3,
    learning_rate=0.12977006615350353,
    subsample=0.7477350208631464,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict_proba(X_test)[:, 1]

auc = roc_auc_score(y_test, preds)

print(f"AUC Score: {auc:.4f}")

joblib.dump(
    model,
    "models/churn_model_latest.pkl"
)

print("Model saved successfully.")
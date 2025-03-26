import pandas as pd 
import numpy as np
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier

df = pd.read_excel(r"C:\Users\Naman jain\Downloads\Customer_churn_Prediction.xlsx")
df.dropna(inplace=True)
df = df.drop(columns=['customerID'])

categorical_columns = df.select_dtypes(include=['object']).columns
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop(columns=["Churn"])
y = df["Churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)

def predict_churn():
    try:
        user_data = np.array([[
            int(gender_var.get()), int(senior_citizen_var.get()), int(partner_var.get()), int(dependents_var.get()),
            int(tenure_entry.get()), int(phone_service_var.get()), int(multiple_lines_var.get()),
            int(internet_service_var.get()), int(online_security_var.get()), int(online_backup_var.get()),
            int(device_protection_var.get()), int(tech_support_var.get()), int(streaming_tv_var.get()),
            int(streaming_movies_var.get()), int(contract_var.get()), int(paperless_billing_var.get()),
            int(payment_method_var.get()), float(monthly_charges_entry.get()), float(total_charges_entry.get())
        ]])
        
        prediction = decision_tree.predict(user_data)[0]
        result = "Customer is likely to churn." if prediction == 1 else "Customer is not likely to churn."
        messagebox.showinfo("Prediction Result", result)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid input values.")

root = tk.Tk()
root.title("Churn Prediction")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Customer Details", font=("Arial", 14)).grid(row=0, columnspan=4, pady=10)

gender_var = tk.StringVar(value="0")
tk.Label(frame, text="Gender:").grid(row=1, column=0)
tk.Radiobutton(frame, text="Female", variable=gender_var, value="0").grid(row=1, column=1)
tk.Radiobutton(frame, text="Male", variable=gender_var, value="1").grid(row=1, column=2)

senior_citizen_var = tk.StringVar(value="0")
tk.Label(frame, text="Senior Citizen:").grid(row=2, column=0)
tk.Radiobutton(frame, text="No", variable=senior_citizen_var, value="0").grid(row=2, column=1)
tk.Radiobutton(frame, text="Yes", variable=senior_citizen_var, value="1").grid(row=2, column=2)

partner_var = tk.StringVar(value="0")
dependents_var = tk.StringVar(value="0")
phone_service_var = tk.StringVar(value="1")
multiple_lines_var = tk.StringVar(value="0")
internet_service_var = tk.StringVar(value="0")
online_security_var = tk.StringVar(value="0")
online_backup_var = tk.StringVar(value="0")
device_protection_var = tk.StringVar(value="0")
tech_support_var = tk.StringVar(value="0")
streaming_tv_var = tk.StringVar(value="0")
streaming_movies_var = tk.StringVar(value="0")
contract_var = tk.StringVar(value="0")
paperless_billing_var = tk.StringVar(value="0")
payment_method_var = tk.StringVar(value="0")

fields = [
    ("Partner:", partner_var, ["No", "Yes"]),
    ("Dependents:", dependents_var, ["No", "Yes"]),
    ("Phone Service:", phone_service_var, ["No", "Yes"]),
    ("Multiple Lines:", multiple_lines_var, ["No", "Yes", "No Phone Service"]),
    ("Internet Service:", internet_service_var, ["DSL", "Fiber Optic", "No"]),
    ("Online Security:", online_security_var, ["No", "Yes", "No Internet Service"]),
    ("Online Backup:", online_backup_var, ["No", "Yes", "No Internet Service"]),
    ("Device Protection:", device_protection_var, ["No", "Yes", "No Internet Service"]),
    ("Tech Support:", tech_support_var, ["No", "Yes", "No Internet Service"]),
    ("Streaming TV:", streaming_tv_var, ["No", "Yes", "No Internet Service"]),
    ("Streaming Movies:", streaming_movies_var, ["No", "Yes", "No Internet Service"]),
    ("Contract:", contract_var, ["Month-to-Month", "One Year", "Two Year"]),
    ("Paperless Billing:", paperless_billing_var, ["No", "Yes"]),
    ("Payment Method:", payment_method_var, ["Bank Transfer", "Credit Card", "Electronic Check", "Mailed Check"])
]

row_idx = 3
for label, var, options in fields:
    tk.Label(frame, text=label).grid(row=row_idx, column=0)
    for col_idx, option in enumerate(options):
        tk.Radiobutton(frame, text=option, variable=var, value=str(col_idx)).grid(row=row_idx, column=col_idx + 1)
    row_idx += 1

tenure_entry = tk.Entry(frame)
tk.Label(frame, text="Tenure (months):").grid(row=row_idx, column=0)
tenure_entry.grid(row=row_idx, column=1)
row_idx += 1

monthly_charges_entry = tk.Entry(frame)
tk.Label(frame, text="Monthly Charges (USD):").grid(row=row_idx, column=0)
monthly_charges_entry.grid(row=row_idx, column=1)
row_idx += 1

total_charges_entry = tk.Entry(frame)
tk.Label(frame, text="Total Charges (USD):").grid(row=row_idx, column=0)
total_charges_entry.grid(row=row_idx, column=1)
row_idx += 1

tk.Button(root, text="Predict Churn", command=predict_churn).pack(pady=10)
root.mainloop()

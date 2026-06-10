from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

model   = joblib.load("model.pkl")
scaler  = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {
            'no_of_dependents':          int(request.form['no_of_dependents']),
            'self_employed':             1 if request.form['self_employed'] == 'Yes' else 0,
            'income_annum':              float(request.form['income_annum']),
            'loan_amount':               float(request.form['loan_amount']),
            'loan_term':                 int(request.form['loan_term']),
            'cibil_score':               int(request.form['cibil_score']),
            'residential_assets_value':  float(request.form['residential_assets_value']),
            'commercial_assets_value':   float(request.form['commercial_assets_value']),
            'luxury_assets_value':       float(request.form['luxury_assets_value']),
            'bank_asset_value':          float(request.form['bank_asset_value']),
            'education_Graduate':        1 if request.form['education'] == 'Graduate' else 0,
            'education_Not Graduate':    1 if request.form['education'] == 'Not Graduate' else 0,
        }

        df = pd.DataFrame([data]).reindex(columns=columns, fill_value=0)

        df[columns] = scaler.transform(df[columns])

        prediction  = model.predict(df)[0]
        probability = model.predict_proba(df)[0]

        result      = "Loan Approved ✅" if prediction == 1 else "Loan Rejected ❌"
        confidence  = f"{max(probability) * 100:.2f}%"

        return render_template("index.html", prediction_text=result, confidence=confidence)

    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {str(e)}", confidence="")

if __name__ == "__main__":
    app.run(debug=True)
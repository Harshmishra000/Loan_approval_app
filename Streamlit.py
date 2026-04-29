import streamlit as st
import pickle
import numpy as np

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title(" Loan Approval Prediction System")
st.subheader("Enter Details")

col1, col2 = st.columns(2)

with col1:
    Applicant_Income = st.number_input("Applicant Income", value=None, placeholder="e.g. 50000")
    Coapplicant_Income = st.number_input("Coapplicant Income", value=None, placeholder="e.g. 20000")

    Employment_Status = st.selectbox("Employment Status", ["Salaried", "Self-Employed", "Unemployed"])
    Age = st.number_input("Age", value=None, placeholder="e.g. 30")

    Marital_Status = st.selectbox("Marital Status", ["Married", "Single"])
    Dependents = st.number_input("Dependents", value=None, placeholder="e.g. 2")

    Credit_Score = st.number_input("Credit Score", value=None, placeholder="e.g. 750")
    Existing_Loans = st.number_input("Existing Loans", value=None, placeholder="e.g. 20000")

    DTI_Ratio = st.number_input(
        "DTI Ratio", min_value=0.0, max_value=1.0, value=None, placeholder="e.g. 0.25"
    )

with col2:
    Savings = st.number_input("Savings", value=None, placeholder="e.g. 100000")
    Collateral_Value = st.number_input("Collateral Value", value=None, placeholder="e.g. 500000")

    Loan_Amount = st.number_input("Loan Amount", value=None, placeholder="e.g. 200000")
    Loan_Term = st.number_input("Loan Term (months)", value=None, placeholder="e.g. 36")

    Loan_Purpose = st.selectbox("Loan Purpose", ["Home", "Education", "Business", "Personal"])
    Property_Area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    Education_Level = st.selectbox("Education", ["Graduate", "Not Graduate"])
    Gender = st.selectbox("Gender", ["Male", "Female"])
    Employer_Category = st.selectbox("Employer Category", ["Private", "Government", "Self", "Other"])

emp_map = {"Salaried":1, "Self-Employed":2, "Unemployed":0}
mar_map = {"Married":1, "Single":0}
gender_map = {"Male":1, "Female":0}
edu_map = {"Graduate":1, "Not Graduate":0}
area_map = {"Urban":2, "Semiurban":1, "Rural":0}
loan_map = {"Home":0, "Education":1, "Business":2, "Personal":3}
employer_map = {"Private":0, "Government":1, "Self":2, "Other":3}

if st.button(" Predict Loan Status"):

    # VALIDATION
    if None in [
        Applicant_Income, Coapplicant_Income, Age, Dependents,
        Credit_Score, Existing_Loans, DTI_Ratio,
        Savings, Collateral_Value, Loan_Amount, Loan_Term
    ]:
        st.warning(" Please fill all numeric fields")
        st.stop()

    input_data = np.array([[  
    Applicant_Income,
    Coapplicant_Income,
    emp_map[Employment_Status],
    Age,
    mar_map[Marital_Status],
    Dependents,
    Credit_Score,
    Existing_Loans,
    DTI_Ratio,
    Savings,
    Collateral_Value,
    Loan_Amount,
    Loan_Term,
    loan_map[Loan_Purpose],
    area_map[Property_Area],
    edu_map[Education_Level],
    gender_map[Gender],
    employer_map[Employer_Category]]])

    input_data = scaler.transform(input_data)

    prob = model.predict_proba(input_data)[0][1]

   
    approved = False

    if Credit_Score < 650:
        st.error(" Loan Rejected (Low Credit Score)")

    elif DTI_Ratio > 0.6:
        st.error(" Loan Rejected (High Debt-to-Income Ratio)")

    elif prob > 0.7:
        st.success(" Loan Approved")
        st.balloons()
        approved = True

    elif prob > 0.4:
        st.warning(" Borderline Case – Improve Profile")

    else:
        st.error(" Loan Rejected")
    

    if not approved:
        st.markdown("###  Quick Insight:")

        if Credit_Score < 650:
            st.warning(" Improve Credit Score")
        elif DTI_Ratio > 0.6:
            st.warning(" Reduce Debt Burden")
        elif prob > 0.4:
            st.warning(" Moderate chances, improve profile")
        else:
            st.error(" Low chances, improve financials")

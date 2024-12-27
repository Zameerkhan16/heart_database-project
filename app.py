import streamlit as st
import mysql.connector
import numpy as np
import joblib

model = joblib.load("logistic.pkl")
# MySQL connection
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",  # Change this
        password="Z@meeR1!9",  # Change this
        database="heart_data"
    )

# Streamlit app
st.title("Heart Disease Prediction")

# User input fields
name = st.text_input('Name')
age = st.number_input('Age', min_value=1, max_value=120)
sex = st.selectbox('Sex (0: Female, 1: Male)', [0, 1])
bp = st.number_input('Blood Pressure (bp)', min_value=80, max_value=200)
cholesterol = st.number_input('Cholesterol (mg/dL)', min_value=100, max_value=600)

# Prediction button
if st.button('Predict'):
    # Prepare data for prediction
    user_data = np.array([[age, sex, bp, cholesterol]])
    
    # Make prediction
    prediction = model.predict(user_data)[0] # 1
    
    st.write(f"Prediction: {'Heart Disease' if prediction == 1 else 'No Heart Disease'}")
    
    # Store user input and prediction in the database
    db = connect_to_db()
    cursor = db.cursor()
    
    query = """
    INSERT INTO user_inputs (name,age, sex, bp, cholesterol, heart_disease)
    VALUES (%s, %s, %s, %s, %s,%s)
    """
    cursor.execute(query, (name,age, sex, bp, cholesterol, int(prediction)))
    db.commit()
    
    st.write("Data saved to the database.")
    
    cursor.close()
    db.close()
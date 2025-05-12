import streamlit as st
import numpy as np
import pandas as pd
import joblib


# Load model dan fitur
model_data = joblib.load('best_gbm_top10.joblib')
model = model_data['model']
features = model_data['features']

# Judul aplikasi
st.markdown('<div class="app-header"><h1>Prediksi Status Mahasiswa: Dropout, Enrolled, atau Graduate</h1></div>', unsafe_allow_html=True)
st.markdown("""
Aplikasi ini memprediksi status mahasiswa berdasarkan data akademik dan sosial.
Masukkan informasi yang diminta untuk mendapatkan prediksi status apakah mahasiswa akan **Graduate**, **Enrolled**, atau **Dropout**.
""")

# Form input
st.subheader("Masukkan informasi berikut:")
user_input = {}

col1, col2 = st.columns(2)

with col1:
    user_input['Curricular_units_2nd_sem_approved'] = st.number_input(
        "Jumlah mata kuliah semester 2 yang disetujui", min_value=0, max_value=50, step=1)
    
    user_input['Curricular_units_1st_sem_approved'] = st.number_input(
        "Jumlah mata kuliah semester 1 yang disetujui", min_value=0, max_value=50, step=1)
    
    user_input['Curricular_units_2nd_sem_enrolled'] = st.number_input(
        "Jumlah mata kuliah semester 2 yang diambil", min_value=0, max_value=50, step=1)
    
    user_input['Curricular_units_1st_sem_enrolled'] = st.number_input(
        "Jumlah mata kuliah semester 1 yang diambil", min_value=0, max_value=50, step=1)
    
    user_input['Age_at_enrollment'] = st.number_input("Usia saat pendaftaran (dalam tahun)", min_value=15, max_value=80, step=1)
    
    user_input['Curricular_units_1st_sem_evaluations'] = st.number_input(
        "Jumlah evaluasi semester 1", min_value=0, max_value=100, step=1)

with col2:
    user_input['Tuition_fees_up_to_date'] = st.selectbox(
        "Apakah pembayaran UKT/SPP tepat waktu?", ['Yes', 'No'])
    
    user_input['Curricular_units_2nd_sem_evaluations'] = st.number_input(
        "Jumlah evaluasi semester 2", min_value=0, max_value=100, step=1)
    
    user_input['Unemployment_rate'] = st.number_input(
        "Tingkat pengangguran (%)", min_value=0.0, max_value=100.0, step=0.1)

    course_options = {
        33: "Biofuel Production Technologies", 171: "Animation and Multimedia Design", 801: "Social Service",
        9003: "Agronomy", 9070: "Communication Design", 9080: "Veterinary Nursing", 9100: "Informatics Engineering",
        9119: "Equinculture", 9130: "Management", 9141: "Social Work", 9146: "Tourism", 9147: "Nursing",
        9238: "Oral Hygiene", 9254: "Advertising and Marketing Management", 9259: "Journalism and Communication",
        9500: "Basic Education", 9556: "Management (evening classes)", 9670: "Tourism (evening classes)",
        9773: "Nursing (evening classes)", 9853: "Informatics Engineering (evening classes)",
        9991: "Computer Engineering", 9992: "Management", 9993: "Social Service", 9994: "Tourism",
        9995: "Nursing", 9996: "Oral Hygiene", 9997: "Marketing", 9998: "Advertising", 9999: "Communication",
        10001: "Psychology", 10002: "Education", 10003: "Architecture", 10004: "Civil Engineering"
    }
    course_choice = st.selectbox("Program Studi", options=list(course_options.items()), format_func=lambda x: x[1])
    user_input['Course'] = course_choice[0]

# Proses input
input_df = pd.DataFrame([user_input])
input_df['Tuition_fees_up_to_date'] = input_df['Tuition_fees_up_to_date'].map({'Yes': 1, 'No': 0})
input_df = input_df[features]

# Prediksi
if st.button("Prediksi Status"):
    with st.spinner("Memproses prediksi..."):
        prediction = model.predict(input_df)[0]
        label_map = {0: "Graduate", 1: "Enrolled", 2: "Dropout"}
        st.success(f"🎓 Prediksi status mahasiswa: **{label_map[prediction]}**")

# Sidebar
st.sidebar.header("Informasi Tambahan")
st.sidebar.markdown("""
Aplikasi ini menggunakan model **Gradient Boosting Machine (GBM)** yang telah dilatih menggunakan fitur-fitur penting dari data mahasiswa.  
Model ini memperhitungkan data seperti jumlah mata kuliah yang diambil, pembayaran UKT, tingkat pengangguran, dan informasi lainnya untuk memberikan prediksi yang akurat.
""")

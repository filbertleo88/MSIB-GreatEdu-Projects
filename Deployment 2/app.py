import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️"
)

# Getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# Loading the saved models
# Definisikan daftar nama file model
model_files = [
    'diabetes_model.sav', 
    'heart_disease_model.sav', 
]

# Inisialisasi dictionary untuk menyimpan model
models = {}

# Loop untuk memuat setiap model
for model_file in model_files:
    model_path = os.path.join(working_dir, 'saved_models', model_file)
    with open(model_path, 'rb') as f:
        models[model_file.split('_')[0]] = pickle.load(f)

diabetes_model = models['diabetes']
heart_disease_model = models['heart']

# sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'Multiple Disease Prediction System',
         [
             'Diabetes Prediction',
             'Heart Disease Prediction',
         ],
        menu_icon='hospital-fill',
        icons=['person', 'activity'],
        default_index=0
)

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':

    # page title
    st.title('Diabetes Prediction using ML (SVM Classifier)')

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')
    with col2:
        Glucose = st.text_input('Glucose Level')
    with col3:
        BloodPressure = st.text_input('Blood Pressure value')
    with col1:
        SkinThickness = st.text_input('Skin Thickness value')
    with col2:
        Insulin = st.text_input('Insulin Level')
    with col3:
        BMI = st.text_input('BMI value')
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
    with col2:
        Age = st.text_input('Age of the Person')

    # Code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction
    if st.button('Diabetes Test Prediction Result'):
        user_input = [
            Pregnancies, Glucose, BloodPressure, 
            SkinThickness, Insulin, BMI, 
            DiabetesPedigreeFunction, Age
        ]
        user_input = [float(x) for x in user_input]
        diab_prediction = diabetes_model.predict([user_input])
        if diab_prediction[0] == 1:
            diab_diagnosis = 'The individual is predicted to be DIABETIC'
        else:
            diab_diagnosis = 'The individual is predicted to be NON-DIABETIC'
    
    st.success(diab_diagnosis)

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':

    # page title
    st.title('Heart Disease Prediction using ML (Logistic Regression)')

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.text_input('Age')
    with col2:
        sex_opt = st.radio(
            label='Sex',
            options=['Male', 'Female'] 
        )
        sex = 1 if sex_opt == 'Male' else 0
    with col3:
        cp = st.selectbox(
            label='Chest Pain types (cp)', 
            options=[i for i in range(4)]
        )
    with col1:
        trestbps = st.text_input('Resting Blood Pressure (trestbps)')
    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl (chol)')
    with col3:
        fbs_opt = st.radio(
            label='Fasting Blood Sugar > 120 mg/dl (fbs)',
            options=['Yes', 'No'] 
        )
        fbs = 1 if sex_opt == 'Yes' else 0
    with col1:
        restecg = st.selectbox(
            label='Resting Electrocardiographic results (restecg)', 
            options=[i for i in range(3)]
        )
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved (thalach)')
    with col3:
        exang_opt = st.radio(
            label='Exercise Induced Angina (exang)',
            options=['Yes', 'No'] 
        )
        exang = 1 if exang_opt == 'Yes' else 0
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise (oldpeak)')
    with col2:
        slope = st.selectbox(
            label='Slope of the peak exercise ST segment (slope)', 
            options=[i for i in range(3)]
        )
    with col3:
        ca = st.selectbox(
            label='Major vessels colored by flourosopy (ca)', 
            options=[i for i in range(5)]
        )
    with col1:
        thal_dict = {
            'Normal': 0, 
            'Fixed Defect': 1, 
            'Reversible Defect': 2,
        }
        thal_opt = st.selectbox(
            label='Thalassemia Condition (thal)', 
            options=list(thal_dict.keys())
        )
        thal = thal_dict[thal_opt]

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction
    if st.button('Heart Disease Test Prediction Result'):
        user_input = [
            age, sex, cp, trestbps, 
            chol, fbs, restecg, thalach, 
            exang, oldpeak, slope, ca, thal
        ]
        user_input = [float(x) for x in user_input]
        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The individual is predicted to HAVE heart disease'
        else:
            heart_diagnosis = 'The individual is predicted NOT TO HAVE any heart disease'
    
    st.success(heart_diagnosis)

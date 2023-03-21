# from flask import Flask,request
import pandas as pd
import numpy as np
import pickle
import streamlit as st 
# app=Flask(__name__)
pickle_in=open('classifier.pkl','rb')
classifier=pickle.load(pickle_in)


# @app.route('/')
def home_page():

    return " This is a user interface for severity classification app"

# @app.route('/predict')
def predict_severity(est_qty_released, process_type_encoded, incident_year, equival_hole_dia, duration_leak):
    
    # est_qty_released = request.args.get("est_qty_released")
    # process_type = request.args.get("process_type")
    # incident_year = request.args.get("incident_year")
    # equival_hole_dia = request.args.get("equival_hole_dia")
    # duration_leak = request.args.get('duration_leak')

    # Check if any of the parameters are missing
    if None in ([est_qty_released, process_type_encoded, incident_year, equival_hole_dia, duration_leak]):
        return 'Error: Missing one or more parameters.'

    # Convert the parameters to float/int as required
    est_qty_released = float(est_qty_released)
    # pro_type=[]
    # if process_type=='gas':
    #     pro_type.append(2)
    # elif process_type=='2-phase'
    process_type = int(process_type_encoded)
    incident_year = int(incident_year)
    equival_hole_dia = float(equival_hole_dia)
    duration_leak = float(duration_leak)

    # Call the classifier to get the prediction and probability
    pred = classifier.predict([[est_qty_released, process_type, incident_year, equival_hole_dia, duration_leak]]).item()
    pred_proba = classifier.predict_proba([[est_qty_released, process_type, incident_year, equival_hole_dia, duration_leak]])
    max_prob_index = np.argmax(pred_proba)
    max_prob = pred_proba[0, max_prob_index]

    # Return the prediction and probability as a dictionary
    # return {'prediction': str(pred), 'prediction_probability': str(max_prob)}


    # return {'pred':pred,'prob':pred_proba}

    # return " The predicted severity is {}  and it's probability is {}".format(pred,max_prob)

    if pred == 0:
        return "The predicted severity is Minor  and it's probability is {}".format(round(max_prob,4))
    
    elif pred==1:
        return "The predicted severity is Significant and it's probability is {}".format(round(max_prob,4))
    else :
        return "The predicted severity is Major  and it's probability is {}".format(round(max_prob,4))



def main():
    st.title("Severity Classifier App Developed with Streamlit")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h4 style="color:white;text-align:center;">Severity Classifier App ML App </h4>
    </div>
    """
    #options=['gas','2-phase','condesate','oil']

    st.markdown(html_temp,unsafe_allow_html=True)
    est_qty_released = st.text_input("The estimated quantity released(Kg)")
    process_type_dict={'gas' : 2, 'oil': 3,'2-phase':0,'condesate':1}
    process_type_input = st.selectbox("process_type",options=['gas','2-phase','condesate','oil'])
    process_type_encoded = process_type_dict[process_type_input]
    # process_type = st.text_input("process_type","Type Here")
    incident_year = st.text_input("incident_year")
    equival_hole_dia = st.text_input("The hole diameter(mm)")
    duration_leak = st.text_input("The duration of leak in mins")
    result=""
    if st.button("Predict"):
        result=predict_severity(est_qty_released, process_type_encoded, incident_year, equival_hole_dia, duration_leak)
    st.success(result)
    if st.button("About"):
        st.text("Lets Learn")
        st.text("Built with Streamlit")

# @app.route('/predict_file',methods=["POST"])
# def predict_csv_file():

#     df_test=pd.read_csv(request.files.get("file"))
#     print(df_test.head())
#     prediction=classifier.predict(df_test)
    
#     return str(list(prediction))


if __name__== "__main__":
    main()
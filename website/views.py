from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from flask_login import  login_required, current_user
#from . import db
from .models import Note , crop_class
import json
from sklearn.preprocessing import StandardScaler
import pickle
import numpy as np
from scipy import stats


views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():        
    return render_template("home.html", user=current_user)

@views.route("/rainfall_predictor", methods=["POST"])
def rainfall_predictor():
    return redirect(url_for("views.rainfall"))

@views.route("/crop_recommendor", methods=["GET","POST"])
def crop_recommendor():
    return redirect(url_for("views.crop"))

@views.route("/fertilizer_selector", methods=["POST"])
def fertilizer_selector():
    return redirect(url_for("views.fertilizer"))

@views.route("/rainfall")
def rainfall():
    return render_template("rainfall.html", user=current_user)



# Loading all Crop Recommendation Models
crop_xgb_pipeline = pickle.load(
    open("crop_xgb_1.pkl", "rb")
)
crop_rf_pipeline = pickle.load(
    open("crop_rf_1.pkl", "rb")
)
crop_knn_pipeline = pickle.load(
    open("crop_knn_1.pkl", "rb")
)
crop_label_dict = pickle.load(
    open("crop_label_dict1.pkl", "rb")
)

def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError

def crop_prediction(input_data):
    prediction_data = {
        "xgb_model_prediction": crop_label_dict[
            crop_xgb_pipeline.predict(input_data)[0]
        ],
        "xgb_model_probability": max(crop_xgb_pipeline.predict_proba(input_data)[0])
        * 100,
        "rf_model_prediction": crop_label_dict[crop_rf_pipeline.predict(input_data)[0]],
        "rf_model_probability": max(crop_rf_pipeline.predict_proba(input_data)[0])
        * 100,
        "knn_model_prediction": crop_label_dict[
            crop_knn_pipeline.predict(input_data)[0]
        ],
        "knn_model_probability": max(crop_knn_pipeline.predict_proba(input_data)[0])
        * 100,
    }

    all_predictions = [
            prediction_data["xgb_model_prediction"],
            prediction_data["rf_model_prediction"],
            prediction_data["knn_model_prediction"],
        ]

    all_probs = [
            prediction_data["xgb_model_probability"],
            prediction_data["rf_model_probability"],
            prediction_data["knn_model_probability"],
        ]

    if len(set(all_predictions)) == len(all_predictions):
        prediction_data["final_prediction"] = all_predictions[all_probs.index(max(all_probs))]
    else:
        prediction_data["final_prediction"] = stats.mode(all_predictions)[0][0]

    return prediction_data


@views.route("/crop", methods=["GET", "POST"])
def crop():
    if request.method == "GET":
        return render_template('crop.html', user=current_user)
    else:
            form_values = request.form.to_dict()
            column_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            input_data = np.asarray([float(form_values[i].strip()) for i in column_names]).reshape(
                1, -1
            )
            prediction_data = crop_prediction(input_data)
            
            return  render_template('crop_result.html', crop_predict=f"Recommended Crop for you : { prediction_data['final_prediction']}", user=current_user)
    


# rainfall
# Loading all rainfall Recommendation Models
rainfall_pipeline = pickle.load(
    open("rainfall_rf_1.pkl", "rb")
)
district_name_dict = pickle.load(
    open("district_rain_dict.pkl", "rb")
)

district_dict = {}
for district_value in district_name_dict:
    district_dict[district_name_dict[district_value]] = district_value



def predict_rainfall(input_data):
    return rainfall_pipeline.predict(input_data)[0]



@views.route("/rainfall", methods=["GET", "POST"])
def rainfall_prediction():
    if request.method == "GET":
        return render_template("rainfall.html")
    else:
        
        form_values = request.form.to_dict()
        column_names =["INDEX","YEAR","MN","MMAX","MMIN","LMIN","MWS","HMAX","MVP","MLO","MMD","MHG","MTC","RD","HVYRF","P1","P2"]
        for key in form_values:
                form_values[key] = form_values[key].strip()

        form_values["INDEX"] = district_dict[form_values["INDEX"]]
        input_data = np.asarray([float(str(form_values[i]).strip()) for i in column_names]).reshape(1, -1)
        '''input_data =  np.asarray([float(form_values[i].strip()) for i in column_names]).reshape(1, -1)'''
        predict_rain_data = predict_rainfall(input_data)
        return render_template("rainfall_result.html",rainfall_predict=f" Predicted rainfall : { predict_rain_data } mm", user=current_user )



#fertilizer
# Loading all Fertilizer Recommendation Models
fertilizer_xgb_pipeline = pickle.load(
    open("fert_xgb_1.pkl", "rb")
)
fertilizer_rf_pipeline = pickle.load(
    open("fert_rf_1.pkl", "rb")
)
fertilizer_svm_pipeline = pickle.load(
    open("fert_svm_1.pkl", "rb")
)
fertilizer_label_dict = pickle.load(
    open("fert_fertname_dict.pkl", "rb")
)
soiltype_label_dict = pickle.load(
    open("fert_soiltype_dict.pkl", "rb")
)
croptype_label_dict = pickle.load(
    open("fert_croptype_dict.pkl", "rb")
)

crop_label_name_dict = {}
for crop_value in croptype_label_dict:
    crop_label_name_dict[croptype_label_dict[crop_value]] = crop_value

soil_label_dict = {}
for soil_value in soiltype_label_dict:
    soil_label_dict[soiltype_label_dict[soil_value]] = soil_value

def convert(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError

def fertilizer_prediction(input_data):
    prediction_data = {
        "xgb_model_prediction": fertilizer_label_dict[
            fertilizer_xgb_pipeline.predict(input_data)[0]
        ],
        "xgb_model_probability": max(
            fertilizer_xgb_pipeline.predict_proba(input_data)[0]
        )
        * 100,
        "rf_model_prediction": fertilizer_label_dict[
            fertilizer_rf_pipeline.predict(input_data)[0]
        ],
        "rf_model_probability": max(fertilizer_rf_pipeline.predict_proba(input_data)[0])
        * 100,
        "svm_model_prediction": fertilizer_label_dict[
            fertilizer_svm_pipeline.predict(input_data)[0]
        ],
        "svm_model_probability": max(
            fertilizer_svm_pipeline.predict_proba(input_data)[0]
        )
        * 100,
    }

    all_predictions = [
            prediction_data["xgb_model_prediction"],
            prediction_data["rf_model_prediction"],
            prediction_data["svm_model_prediction"],
        ]

    all_probs = [
            prediction_data["xgb_model_probability"],
            prediction_data["rf_model_probability"],
            prediction_data["svm_model_probability"],
        ]

    if len(set(all_predictions)) == len(all_predictions):
        prediction_data["final_prediction"] = all_predictions[all_probs.index(max(all_probs))]
    else:
        prediction_data["final_prediction"] = stats.mode(all_predictions)[0][0]

    return prediction_data

@views.route("/fertilizer", methods=["GET", "POST"])
def fertilizer():
    if request.method == "GET":
        return render_template('fertilizer.html', user=current_user)
    else:
        form_values = request.form.to_dict()
        column_names = ["Temparature","Humidity","Moisture","soil_type","crop_type","Nitrogen","Potassium","Phosphorous",]

        for key in form_values:
                form_values[key] = form_values[key].strip()

        form_values["soil_type"] = soil_label_dict[form_values["soil_type"]]
        form_values["crop_type"] = crop_label_name_dict[form_values["crop_type"]]
        input_data = np.asarray([float(form_values[i]) for i in column_names]).reshape(1, -1)
        prediction_data = fertilizer_prediction(input_data)
        return render_template("fertilizer_result.html",fertilizer_predict=f" Predicted Fertilizer : { prediction_data['final_prediction'] }", user=current_user )

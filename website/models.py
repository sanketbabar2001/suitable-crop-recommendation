from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pandas as pd
import sys
import logging, pickle,os


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')



class crop_class:
    def __init__(self, N :int, P:int, K:int, temperature:int, humidity:int, ph:int, rainfall:int, label:int):
        self.N = N
        self.P = P
        self.K = K
        self.temperature = temperature
        self.humidity = humidity
        self.ph = ph
        self.rainfall = rainfall
        self.label = label
    
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "N": [self.N],
                "P": [self.P],
                "K": [self.K],
                "temperature": [self.temperature],
                "humidity": [self.humidity],
                "ph": [self.ph],
                "rainfall": [self.rainfall],
                "label": [self.label]
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)


class rainfall_class:
    def __init__(self, INDEX:int, YEAR:int, MN:int, MMAX:float, MMIN:float, LMIN:int, MWS:int, HMAX:int, MVP:float, MLO:float, MMD:float, MHG:float, MTC:float, RD:int, HVYRF:int, P1:float, P2:float, TMRF:float):
        self.INDEX = INDEX
        self.YEAR = YEAR
        self.MN = MN
        self.MMAX = MMAX
        self.MMIN = MMIN
        self.LMIN = LMIN
        self.MWS = MWS
        self.HMAX = HMAX
        self.MVP = MVP
        self.MLO = MLO
        self.MMD = MMD
        self.MHG = MHG
        self.MTC = MTC
        self.RD = RD
        self.HVYRF = HVYRF
        self.P1 = P1
        self.P2 = P2
    
    
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "INDEX": [self.INDEX],
                "YEAR": [self.YEAR],
                "MN": [self.MN],
                "MMAX": [self.MMAX],
                "MMIN": [self.MMIN],
                "LMIN": [self.LMIN],
                "MWS": [self.MWS],
                "HMAX": [self.HMAX],
                "MVP": [self.MVP],
                "MLO": [self.MLO],
                "MMD": [self.MMD],
                "MHG": [self.MHG],
                "MTC": [self.MTC],
                "RD": [self.RD],
                "HVYRF": [self.HVYRF],
                "P1": [self.P1],
                "P2": [self.P2]
            }

            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            print("An error occurred: ", str(e))



class fertilizer_class:
    def __init__(self, Temperature: float, Humidity: float, Moisture: float, soil_type: str, crop_type: str, Nitrogen: float, Potassium: float, Phosphorous: float):
        self.temperature = Temperature
        self.humidity = Humidity
        self.moisture = Moisture
        self.soil_type = soil_type
        self.crop_type = crop_type
        self.nitrogen = Nitrogen
        self.potassium = Potassium
        self.phosphorous = Phosphorous
    
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "Temparature": [self.temperature],
                "Humidity": [self.humidity],
                "Moisture": [self.moisture],
                "soil_type": [self.soil_type],
                "crop_type": [self.crop_type],
                "Nitrogen": [self.nitrogen],
                "Potassium": [self.potassium],
                "Phosphorous": [self.phosphorous]
            }

            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            print("An error occurred: ", str(e))



def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message


import pandas as pd
import os

def load_data():
    base_path = os.path.dirname(os.path.dirname(__file__))
    gen1 = pd.read_csv(os.path.join(base_path, "Data", "Plant_1_Generation_Data.csv"))
    weather1 = pd.read_csv(os.path.join(base_path, "Data", "Plant_1_Weather_Sensor_Data.csv"))

    gen2 = pd.read_csv(os.path.join(base_path,"Data", "Plant_2_Generation_Data.csv"))
    weather2 = pd.read_csv(os.path.join(base_path, "Data", "Plant_2_Weather_Sensor_Data.csv"))

    gen = pd.concat([gen1,gen2])
    weather = pd.concat([weather1,weather2])

    gen['DATE_TIME'] = pd.to_datetime(gen['DATE_TIME'], 
                                        format='mixed', 
                                        dayfirst=True, 
                                        errors='coerce')
    weather['DATE_TIME'] =pd.to_datetime(weather['DATE_TIME'], 
                                        format='mixed', 
                                        dayfirst=True, 
                                        errors='coerce')

    gen = gen.dropna(subset=['DATE_TIME'])
    weather = weather.dropna(subset=['DATE_TIME'])

    gen['DATE_TIME'] = gen['DATE_TIME'].astype('datetime64[ns]')
    weather['DATE_TIME'] = weather['DATE_TIME'].astype('datetime64[ns]')

    df = pd.merge(gen, weather, left_on=['DATE_TIME', 'PLANT_ID'],right_on=['DATE_TIME', 'PLANT_ID'], how='inner')

    return df
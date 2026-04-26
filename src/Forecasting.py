import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_model(df):
    features = [
        'hour', 'day', 'month',
        'IRRADIATION',
        'AMBIENT_TEMPERATURE',
        'MODULE_TEMPERATURE'
    ]

    X = df[features]
    y = df['AC_POWER']

    model = RandomForestRegressor(n_estimators=50)
    model.fit(X,y)

    return model

def predict_scenario(model, df, days_ahead, irr_adj, amb_temp_adj, mod_temp_adj):
    """
    Generate future synthetic weather data and predict AC_POWER under the defined scenario.
    """
    # Create baseline by averaging the values per hour to simulate a typical daily curve
    baseline = df.groupby('hour')[['IRRADIATION', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE']].mean().reset_index()
    
    # Get last date in dataframe
    last_date = df['DATE_TIME'].max().normalize()
    
    future_data = []
    
    for d in range(1, days_ahead + 1):
        target_date = last_date + pd.Timedelta(days=d)
        day_val = target_date.day
        month_val = target_date.month
        
        for index, row in baseline.iterrows():
            hour_val = row['hour']
            # Apply user multipliers/adjustments
            irr_val = max(0, row['IRRADIATION'] * (1 + irr_adj / 100.0))
            amb_temp = row['AMBIENT_TEMPERATURE'] + amb_temp_adj
            mod_temp = row['MODULE_TEMPERATURE'] + mod_temp_adj
            
            future_data.append({
                'DATE_TIME': target_date + pd.Timedelta(hours=hour_val),
                'hour': hour_val,
                'day': day_val,
                'month': month_val,
                'IRRADIATION': irr_val,
                'AMBIENT_TEMPERATURE': amb_temp,
                'MODULE_TEMPERATURE': mod_temp
            })
            
    future_df = pd.DataFrame(future_data)
    
    if future_df.empty:
        return future_df
        
    features = [
        'hour', 'day', 'month',
        'IRRADIATION',
        'AMBIENT_TEMPERATURE',
        'MODULE_TEMPERATURE'
    ]
    
    future_df['PREDICTED_AC_POWER'] = model.predict(future_df[features])
    return future_df
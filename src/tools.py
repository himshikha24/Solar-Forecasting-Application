from src.Forecasting import train_model
from src.anomaly import detect_anomalies

def run_forecast(df):
    model = train_model(df)
    return "Forecast model trained successfully"

def run_anomaly(df):
    df = detect_anomalies(df)
    return df[df['anomaly']==-1].head()
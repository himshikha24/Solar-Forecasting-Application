from src.Forecasting import train_model, predict_scenario
from src.anomaly import detect_anomalies, detect_underperforming_assets
from src.weather_api import format_weather_for_chat

def run_forecast(df):
    model = train_model(df)
    return "Forecast model trained successfully"

def run_scenario_simulation(df, days_ahead, irr_adj, amb_temp_adj, mod_temp_adj):
    model = train_model(df)
    scenario_df = predict_scenario(model, df, days_ahead, irr_adj, amb_temp_adj, mod_temp_adj)
    return scenario_df

def run_anomaly(df):
    df = detect_anomalies(df)
    return df[df['anomaly']==-1].head()

def check_asset_health(df):
    health_df = detect_underperforming_assets(df)
    if health_df.empty:
        return "Not enough data to determine asset health."
    
    issues = health_df[health_df['Status'] != 'Healthy']
    if issues.empty:
        return "All assets are operating normally and are healthy."
    
    output = "Here are the assets requiring attention:\n"
    for _, row in issues.iterrows():
        output += f"- Inverter {row['SOURCE_KEY']}: Status = {row['Status']}, Zero Power Incidents = {row['zero_power_incidents']}\n"
    return output

def get_weather():
    return format_weather_for_chat()
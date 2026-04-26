from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df):
    model = IsolationForest(contamination=0.03)
    df['anomaly'] = model.fit_predict(df[['AC_POWER']])
    return df

def detect_underperforming_assets(df):
    """
    Identifies inverters (SOURCE_KEY) that have significantly lower
    efficiency or frequent 0 AC_POWER during high irradiation.
    """
    if 'SOURCE_KEY' not in df.columns or 'IRRADIATION' not in df.columns or 'AC_POWER' not in df.columns:
        return pd.DataFrame()
        
    daylight_df = df[df['IRRADIATION'] > 0.1].copy()
    daylight_df['efficiency'] = daylight_df['AC_POWER'] / (daylight_df['IRRADIATION'] * 1000 + 1e-5)
    
    asset_health = daylight_df.groupby('SOURCE_KEY').agg(
        avg_efficiency=('efficiency', 'mean'),
        zero_power_incidents=('AC_POWER', lambda x: (x == 0).sum()),
        avg_power=('AC_POWER', 'mean')
    ).reset_index()
    
    median_eff = asset_health['avg_efficiency'].median()
    
    asset_health['Status'] = 'Healthy'
    asset_health.loc[asset_health['avg_efficiency'] < (0.7 * median_eff), 'Status'] = 'Underperforming'
    asset_health.loc[asset_health['zero_power_incidents'] > 5, 'Status'] = 'Needs Maintenance'
    
    return asset_health.sort_values(by='avg_efficiency', ascending=True)
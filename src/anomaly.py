from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.03)
    df['anomaly'] = model.fit_predict(df[['AC_POWER']])
    return df
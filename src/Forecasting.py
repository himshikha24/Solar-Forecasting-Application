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
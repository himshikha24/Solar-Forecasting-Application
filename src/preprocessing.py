def preprocess(df):

    df = df.copy()

    df['hour'] = df['DATE_TIME'].dt.hour
    df['day'] = df['DATE_TIME'].dt.day
    df['month'] = df['DATE_TIME'].dt.month

    df.ffill(inplace=True)

    return df 
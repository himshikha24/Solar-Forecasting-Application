def route_query(query):

    query = query.lower()

    if "weather" in query or "rain" in query or "temperature" in query:
        return "weather"
    elif "maintenance" in query or "damage" in query or "health" in query or "asset" in query:
        return "health"
    elif "last" in query or "between" in query or "date" in query:
        return "sql"
    elif "predict" in query or "forecast" in query:
        return "forecast"
    elif "anomaly" in query:
        return "anomaly"
    else:
        return "pandas"

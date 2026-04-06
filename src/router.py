def route_query(query):

    query = query.lower()

    if "last" in query or "between" in query or "date" in query:
        return "sql"
    elif "predict" in query or "forecast" in query:
        return "forecast"
    elif "anomaly" in query:
        return "anomaly"
    else:
        return "pandas"

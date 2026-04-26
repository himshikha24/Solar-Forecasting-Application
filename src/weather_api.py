import urllib.request
import json
from datetime import datetime

def get_weather_forecast(latitude=28.6139, longitude=77.2090):
    """
    Fetches the 7-day weather forecast from Open-Meteo API.
    Defaults to New Delhi coordinates if none provided, 
    since Plant 1 in the Kaggle dataset is typically in India.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,shortwave_radiation_sum&timezone=auto"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            precip = daily.get("precipitation_sum", [])
            rad = daily.get("shortwave_radiation_sum", [])
            
            forecasts = []
            for i in range(len(dates)):
                forecasts.append({
                    "Date": dates[i],
                    "Max Temp (°C)": max_temps[i],
                    "Min Temp (°C)": min_temps[i],
                    "Precipitation (mm)": precip[i],
                    "Radiation (MJ/m²)": rad[i] if rad[i] is not None else 0
                })
            return forecasts
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return []

def format_weather_for_chat():
    """Formats the weather data into a readable string for the LLM."""
    forecasts = get_weather_forecast()
    if not forecasts:
        return "Weather data is currently unavailable."
    
    output = "Here is the upcoming 7-day weather forecast:\n"
    for f in forecasts:
        output += f"- {f['Date']}: Max {f['Max Temp (°C)']}°C, Min {f['Min Temp (°C)']}°C, Rain {f['Precipitation (mm)']}mm, Solar Radiation {f['Radiation (MJ/m²)']} MJ/m²\n"
    
    return output

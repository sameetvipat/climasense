from django.shortcuts import render
import requests
from datetime import datetime, timedelta

# Open-Meteo API for historical weather data
HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"

def get_historical_weather(lat, lon, year, filter_type):
    """Fetch historical weather data for a specific year with a selected filter."""
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    # Determine which data to fetch based on filter
    filter_map = {
        "temperature": "temperature_2m_max",
        "humidity": "humidity_2m_max",
        "precipitation": "precipitation_sum"
    }
    selected_data = filter_map.get(filter_type, "temperature_2m_max")

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": selected_data,
        "timezone": "UTC"
    }

    response = requests.get(HISTORICAL_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("daily", {}).get(selected_data, [])  # Extract selected data list
    return None

def index(request):
    weather_data = None
    behavior = None
    historical_data = []
    year = None  # ✅ Initialize the variable to avoid UnboundLocalError
    filter_type = "temperature"  # ✅ Default filter type

    if request.method == 'POST':
        city = request.POST.get('city', '')  # ✅ Use .get() to prevent KeyError
        year = request.POST.get('year', '')  # ✅ Safely get year input
        filter_type = request.POST.get('filter', 'temperature')  # Default to temperature

        if not city or not year:  # Handle missing input fields
            return render(request, 'weather/index.html', {
                'weather': {'error': 'Please enter a city and year.'}
            })

        # Get city coordinates using Open-Meteo Geocoding API
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
        geo_response = requests.get(geo_url)

        if geo_response.status_code == 200 and geo_response.json().get("results"):
            geo_data = geo_response.json()["results"][0]
            lat, lon = geo_data["latitude"], geo_data["longitude"]

            # Fetch historical data for the selected year
            historical_data = get_historical_weather(lat, lon, year, filter_type)

            weather_data = {
                'city': city,
                'latitude': lat,
                'longitude': lon,
            }
        else:
            weather_data = {'error': 'City not found'}

    return render(request, 'weather/index.html', {
        'weather': weather_data,
        'behavior': behavior,
        'historical_data': historical_data,
        'selected_year': year,
        'selected_filter': filter_type
    })




import os
import json
import time
import requests
import streamlit as st
from datetime import datetime, timedelta
from profile_utils import get_profile_field

# Weather API constants
WEATHER_API_KEY = "f4923cb2515212f8108721ed67014dc5"  # Replace with your actual API key
WEATHER_CACHE_TTL = 3600  # Cache weather data for 1 hour (in seconds)
CACHE_DIR = "weather_data"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

def safe_get(data, keys, default=None):
    """Safely get nested dictionary values"""
    if not data:
        return default
        
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    if kelvin is None:
        return None
    return kelvin - 273.15

def get_weather_icon_url(icon_code):
    """Get URL for weather icon"""
    if not icon_code:
        return None
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def load_weather_cache():
    """Load cached weather data"""
    cache_file = os.path.join(CACHE_DIR, "weather_cache.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_weather_cache(cache):
    """Save weather data to cache"""
    cache_file = os.path.join(CACHE_DIR, "weather_cache.json")
    with open(cache_file, "w") as f:
        json.dump(cache, f)

def get_cache_key(location, endpoint="weather"):
    """Generate a cache key for a location and endpoint"""
    return f"{location.lower().strip()}_{endpoint}"

def is_cache_valid(cache_entry):
    """Check if cache entry is valid (not expired)"""
    if not cache_entry or "timestamp" not in cache_entry:
        return False
    
    # Check if cache has expired
    cache_time = cache_entry["timestamp"]
    current_time = time.time()
    return (current_time - cache_time) < WEATHER_CACHE_TTL

def fetch_weather_data(location, use_cache=True):
    """
    Fetch current weather data for a location
    
    Args:
        location (str): City name or location
        use_cache (bool): Whether to use cached data if available
        
    Returns:
        dict: Weather data or None if error
    """
    if not location:
        st.error("Location is required to fetch weather data")
        return None
    
    if not WEATHER_API_KEY:
        st.error("Weather API key not configured")
        return None
    
    # Check cache first if enabled
    cache = load_weather_cache()
    cache_key = get_cache_key(location)
    
    if use_cache and cache_key in cache and is_cache_valid(cache[cache_key]):
        return cache[cache_key]["data"]
    
    # Fetch fresh data
    try:
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        response = requests.get(f"{WEATHER_BASE_URL}/weather", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate required fields
            if not all(key in data for key in ['weather', 'main', 'wind']):
                st.error("Received incomplete weather data from API")
                return None
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"Weather API error: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def fetch_forecast_data(location, use_cache=True):
    """
    Fetch 5-day forecast data for a location
    
    Args:
        location (str): City name or location
        use_cache (bool): Whether to use cached data if available
        
    Returns:
        dict: Forecast data or None if error
    """
    if not location:
        st.error("Location is required to fetch forecast data")
        return None
    
    if not WEATHER_API_KEY:
        st.error("Weather API key not configured")
        return None
    
    # Check cache first if enabled
    cache = load_weather_cache()
    cache_key = get_cache_key(location, "forecast")
    
    if use_cache and cache_key in cache and is_cache_valid(cache[cache_key]):
        return cache[cache_key]["data"]
    
    # Fetch fresh data
    try:
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        response = requests.get(f"{WEATHER_BASE_URL}/forecast", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate required fields
            if "list" not in data or not data["list"]:
                st.error("Received incomplete forecast data from API")
                return None
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"Forecast API error: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def get_wind_direction(degrees):
    """Convert wind direction in degrees to compass direction"""
    if degrees is None:
        return "Unknown"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / (360. / len(directions))) % len(directions)
    return directions[index]

def display_current_weather(weather_data):
    """Display current weather conditions"""
    if not weather_data:
        st.error("No weather data available")
        return
    
    # Safely extract weather information with defaults
    weather_main = safe_get(weather_data, ['weather', 0, 'main'], "Unknown")
    weather_desc = safe_get(weather_data, ['weather', 0, 'description'], "Unknown").capitalize()
    weather_icon = safe_get(weather_data, ['weather', 0, 'icon'])
    temp = safe_get(weather_data, ['main', 'temp'], 0)
    feels_like = safe_get(weather_data, ['main', 'feels_like'], temp)
    humidity = safe_get(weather_data, ['main', 'humidity'], 0)
    pressure = safe_get(weather_data, ['main', 'pressure'], 0)
    wind_speed = safe_get(weather_data, ['wind', 'speed'], 0)
    wind_deg = safe_get(weather_data, ['wind', 'deg'])
    wind_dir = get_wind_direction(wind_deg)
    rain_1h = safe_get(weather_data, ['rain', '1h'], 0)
    clouds = safe_get(weather_data, ['clouds', 'all'], 0)
    
    # Display in two columns
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Display weather icon if available
        if weather_icon:
            icon_url = get_weather_icon_url(weather_icon)
            st.image(icon_url, width=100)
        else:
            st.write("No icon available")
    
    with col2:
        st.metric("Temperature", f"{temp:.1f}°C", f"Feels like {feels_like:.1f}°C")
        
        # Additional weather details
        st.write(f"""
        - **Conditions**: {weather_desc}
        - **Humidity**: {humidity}%
        - **Wind**: {wind_speed} m/s ({wind_dir})
        - **Pressure**: {pressure} hPa
        - **Rain (1h)**: {rain_1h} mm
        - **Cloud Cover**: {clouds}%
        """)

def display_weather_alerts(weather_data):
    """Display weather alerts if any"""
    alerts = get_weather_alerts(weather_data)
    
    if not alerts:
        st.success("No active weather alerts")
        return
    
    st.header("⚠️ Weather Alerts")
    
    for alert in alerts:
        alert_type = "🔴 Critical" if alert.get("type") == "danger" else "🟡 Warning"
        with st.expander(f"{alert_type}: {alert.get('title', 'Alert')}"):
            st.write(alert.get("message", "No details available"))
            if alert.get("recommendations"):
                st.markdown("**Recommendations:**")
                for rec in alert["recommendations"]:
                    st.write(f"- {rec}")

def display_agricultural_metrics(weather_data):
    """Display agricultural-specific weather metrics"""
    if not weather_data:
        return
    
    st.header("Agricultural Metrics")
    
    # Calculate metrics
    uv_index = estimate_uv_index(weather_data)
    solar_rad = estimate_solar_radiation(weather_data)
    et0 = calculate_evapotranspiration(weather_data)
    
    # Display in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("UV Index", 
                 f"{uv_index if uv_index else 'N/A'}",
                 get_uv_risk_level(uv_index))
    
    with col2:
        st.metric("Solar Radiation", 
                 f"{solar_rad} W/m²" if solar_rad else "N/A")
    
    with col3:
        st.metric("Evapotranspiration (ET₀)", 
                 f"{et0} mm/day" if et0 else "N/A")

def display_5day_forecast(forecast_data):
    """Display 5-day weather forecast"""
    if not forecast_data:
        st.error("No forecast data available")
        return
    
    daily_forecast = format_forecast_data(forecast_data)
    
    if not daily_forecast:
        st.error("Could not process forecast data")
        return
    
    st.header("5-Day Forecast")
    
    for day in daily_forecast[:5]:  # Show next 5 days
        with st.expander(f"{day['day_name']} - {day['day']}"):
            cols = st.columns([1, 3, 2])
            
            with cols[0]:
                if day.get("weather_icon"):
                    st.image(get_weather_icon_url(day["weather_icon"]), width=60)
                else:
                    st.write("No icon")
            
            with cols[1]:
                st.write(f"**{day.get('weather_description', 'Unknown conditions')}**")
                st.write(f"🌡️ {day.get('min_temp', 0):.1f}°C - {day.get('max_temp', 0):.1f}°C")
                st.write(f"💧 {day.get('avg_humidity', 0):.0f}% humidity")
                if day.get("total_rain", 0) > 0:
                    st.write(f"🌧️ {day['total_rain']:.1f} mm rain")
                st.write(f"💨 {day.get('avg_wind_speed', 0):.1f} m/s")
            
            with cols[2]:
                st.markdown("**Farming Advice**")
                st.write(generate_daily_advice(day))

def show_weather_page():
    """Display the full weather analysis page"""
    st.title("🌦️ Weather Center")
    
    # Get location from profile or user input
    location = get_profile_field(st.session_state.user_profile, "farm_location", "")

    if not location:
        location = st.text_input("Enter your location (city, country):")
        if not location:
            st.warning("Please enter a location to view weather data")
            return
    
    # Fetch data with loading indicators
    with st.spinner("Loading current weather..."):
        weather_data = fetch_weather_data(location)
    
    with st.spinner("Loading forecast data..."):
        forecast_data = fetch_forecast_data(location)
    
    if not weather_data or not forecast_data:
        st.error("Failed to load weather data. Please try again later.")
        return
    
    # Display all weather sections
    st.header("Current Conditions")
    display_current_weather(weather_data)
    
    display_weather_alerts(weather_data)
    
    display_agricultural_metrics(weather_data)
    
    display_5day_forecast(forecast_data)
    
    # Comprehensive advisory
    st.header("Agricultural Advisory")
    advisory = generate_comprehensive_advisory(weather_data, forecast_data)
    st.markdown(advisory)
    
    # Crop-specific analysis
    st.header("Crop-Specific Analysis")
    crop = st.selectbox("Select a crop for analysis:", [
        "Tomato", "Potato", "Wheat", "Rice", "Mango", 
        "Onion", "Soybean", "Cotton", "Cabbage", "Cauliflower",
        "Brinjal", "Lady Finger", "Chili", "Bottle Gourd", "Bitter Gourd",
        "Cluster Beans", "Cucumber", "Maize", "Grapes", "Carrot",
        "Radish", "Pumpkin", "Orange", "Banana", "Watermelon",
        "Guava", "Pomegranate"
    ])
    
    if crop:
        impact = get_crop_weather_impact(crop, weather_data)
        if impact:
            st.subheader(f"Analysis for {crop}")
            
            if impact.get("pros"):
                st.success("**Positive Conditions**")
                for pro in impact["pros"]:
                    st.write(f"✅ {pro}")
            
            if impact.get("cons"):
                st.error("**Potential Issues**")
                for con in impact["cons"]:
                    st.write(f"❌ {con}")
            
            if impact.get("suggestions"):
                st.info("**Recommendations**")
                for suggestion in impact["suggestions"]:
                    st.write(f"💡 {suggestion}")


def estimate_uv_index(weather_data):
    """Estimate UV index based on weather conditions"""
    if not weather_data:
        return "Unknown"
    
    # Get relevant weather parameters
    cloud_cover = weather_data.get("clouds", {}).get("all", 0)
    time_of_day = datetime.fromtimestamp(weather_data.get("dt", 0)).hour
    season = datetime.fromtimestamp(weather_data.get("dt", 0)).month
    
    # Simple estimation (in a real app, we'd use a proper UV API)
    base_uv = {
        1: 3, 2: 4, 3: 6, 4: 8, 5: 9, 6: 10,  # Summer months
        7: 9, 8: 8, 9: 6, 10: 4, 11: 3, 12: 2  # Winter months
    }.get(season, 5)
    
    # Adjust for time of day (peak at solar noon)
    time_factor = 1 - abs(12 - time_of_day) / 12
    base_uv *= time_factor
    
    # Adjust for cloud cover
    cloud_factor = 1 - (cloud_cover / 100) * 0.7  # Clouds block up to 70% of UV
    estimated_uv = max(0, min(12, base_uv * cloud_factor))
    
    return round(estimated_uv)

def get_uv_risk_level(uv_index):
    """Get UV risk level description"""
    try:
        uv_index = float(uv_index)
    except:
        return "Unknown"
    
    if uv_index < 3:
        return "Low"
    elif uv_index < 6:
        return "Moderate"
    elif uv_index < 8:
        return "High"
    elif uv_index < 11:
        return "Very High"
    else:
        return "Extreme"

def estimate_solar_radiation(weather_data):
    """Estimate solar radiation in W/m²"""
    if not weather_data:
        return "Unknown"
    
    # Get relevant weather parameters
    cloud_cover = weather_data.get("clouds", {}).get("all", 0)
    time_of_day = datetime.fromtimestamp(weather_data.get("dt", 0)).hour
    season = datetime.fromtimestamp(weather_data.get("dt", 0)).month
    
    # Simple estimation (in a real app, we'd use a proper solar API)
    max_radiation = {
        1: 500, 2: 600, 3: 700, 4: 800, 5: 900, 6: 1000,  # Summer months
        7: 950, 8: 850, 9: 750, 10: 650, 11: 550, 12: 450  # Winter months
    }.get(season, 700)
    
    # Adjust for time of day (peak at solar noon)
    time_factor = 1 - abs(12 - time_of_day) / 12
    solar_rad = max_radiation * time_factor
    
    # Adjust for cloud cover
    cloud_factor = 1 - (cloud_cover / 100) * 0.8  # Clouds block up to 80% of solar
    estimated_rad = max(0, min(1200, solar_rad * cloud_factor))
    
    return round(estimated_rad)

def calculate_evapotranspiration(weather_data):
    """Calculate reference evapotranspiration (ET₀) using simplified FAO method"""
    if not weather_data:
        return 0.0
    
    try:
        # Get required parameters
        temp = weather_data["main"]["temp"]  # °C
        humidity = weather_data["main"]["humidity"]  # %
        wind_speed = weather_data["wind"]["speed"]  # m/s
        solar_rad = estimate_solar_radiation(weather_data)  # W/m²
        
        # Convert solar radiation from W/m² to MJ/m²/day
        solar_mj = solar_rad * 0.0864  # Conversion factor
        
        # Calculate saturation vapor pressure (es)
        es = 0.6108 * (17.27 * temp) / (temp + 237.3)
        
        # Calculate actual vapor pressure (ea)
        ea = es * (humidity / 100)
        
        # Calculate slope of vapor pressure curve (Δ)
        delta = (4098 * es) / ((temp + 237.3) ** 2)
        
        # Psychrometric constant (γ)
        gamma = 0.665 * 10 ** -3 * 101.3  # Assuming constant pressure
        
        # Simplified FAO Penman-Monteith equation
        numerator = (0.408 * delta * solar_mj) + (gamma * (900 / (temp + 273)) * wind_speed * (es - ea))
        denominator = delta + (gamma * (1 + 0.34 * wind_speed))
        
        et0 = numerator / denominator
        
        return max(0, round(et0, 1))
    
    except Exception as e:
        st.error(f"Error calculating evapotranspiration: {str(e)}")
        return 0.0

def get_weather_alerts(weather_data):
    """
    Generate comprehensive weather alerts based on current conditions
    
    Args:
        weather_data (dict): Weather data from API
        
    Returns:
        list: List of alert messages with severity and recommendations
    """
    alerts = []
    
    if not weather_data:
        return alerts
    
    # Get weather parameters
    main = weather_data.get("main", {})
    temp = main.get("temp")
    humidity = main.get("humidity")
    pressure = main.get("pressure")
    wind = weather_data.get("wind", {})
    wind_speed = wind.get("speed")
    wind_gust = wind.get("gust")
    wind_dir = wind.get("deg")
    rain = weather_data.get("rain", {})
    rain_1h = rain.get("1h", 0)
    rain_3h = rain.get("3h", 0)
    snow = weather_data.get("snow", {})
    snow_1h = snow.get("1h", 0)
    clouds = weather_data.get("clouds", {}).get("all", 0)
    weather_id = weather_data.get("weather", [{}])[0].get("id") if weather_data.get("weather") else None
    
    # Temperature alerts
    if temp is not None:
        if temp > 38:
            alerts.append({
                "type": "danger",
                "title": "Extreme Heat Warning",
                "message": "Dangerously high temperatures may cause heat stress in crops and livestock.",
                "recommendations": [
                    "Increase irrigation frequency to prevent heat stress",
                    "Provide shade for sensitive crops and animals",
                    "Avoid working during peak heat hours (11AM-3PM)",
                    "Monitor for signs of wilting in crops"
                ]
            })
        elif temp > 32:
            alerts.append({
                "type": "warning",
                "title": "High Temperature Alert",
                "message": "Elevated temperatures may affect crop growth and livestock comfort.",
                "recommendations": [
                    "Adjust irrigation schedules to account for increased evaporation",
                    "Monitor water levels in ponds and reservoirs",
                    "Consider temporary shade structures for sensitive crops"
                ]
            })
        elif temp < 0:
            alerts.append({
                "type": "danger",
                "title": "Freezing Conditions",
                "message": "Freezing temperatures pose risk of frost damage to crops.",
                "recommendations": [
                    "Protect sensitive crops with frost covers or mulch",
                    "Harvest mature crops that may be damaged by frost",
                    "Consider irrigation to create protective ice layer on plants",
                    "Move potted plants to sheltered areas"
                ]
            })
        elif temp < 5:
            alerts.append({
                "type": "warning",
                "title": "Cold Temperature Alert",
                "message": "Cold conditions may slow plant growth and affect livestock.",
                "recommendations": [
                    "Delay planting of sensitive crops until temperatures rise",
                    "Provide additional bedding for livestock",
                    "Monitor for cold stress in young plants"
                ]
            })
    
    # Humidity alerts
    if humidity is not None:
        if humidity > 85:
            alerts.append({
                "type": "warning",
                "title": "High Humidity Alert",
                "message": "High humidity increases risk of fungal diseases in crops.",
                "recommendations": [
                    "Monitor crops for signs of fungal infection",
                    "Improve air circulation around plants where possible",
                    "Apply preventive fungicides if appropriate",
                    "Avoid overhead irrigation to reduce leaf wetness"
                ]
            })
        elif humidity < 30:
            alerts.append({
                "type": "warning",
                "title": "Low Humidity Alert",
                "message": "Low humidity increases water loss through transpiration.",
                "recommendations": [
                    "Increase irrigation frequency to compensate for dry conditions",
                    "Apply mulch to reduce soil moisture evaporation",
                    "Consider shade structures to reduce water loss",
                    "Monitor for signs of water stress in plants"
                ]
            })
    
    # Precipitation alerts
    if rain_1h > 10 or rain_3h > 20:
        alerts.append({
            "type": "danger",
            "title": "Heavy Rainfall Warning",
            "message": "Heavy rain may cause flooding, waterlogging, and soil erosion.",
            "recommendations": [
                "Check and clear drainage systems",
                "Monitor low-lying areas for water accumulation",
                "Postpone fertilizer applications to prevent runoff",
                "Inspect fields for signs of erosion after rain"
            ]
        })
    elif rain_1h > 5 or rain_3h > 10:
        alerts.append({
            "type": "warning",
            "title": "Moderate Rainfall Alert",
            "message": "Moderate rainfall may affect field operations and crop health.",
            "recommendations": [
                "Check field drainage systems",
                "Delay field operations until soil conditions improve",
                "Monitor for signs of disease after wet conditions"
            ]
        })
    
    if snow_1h > 2:
        alerts.append({
            "type": "danger",
            "title": "Heavy Snowfall Warning",
            "message": "Heavy snow may damage crops and structures.",
            "recommendations": [
                "Protect sensitive crops with covers or supports",
                "Clear snow from greenhouse roofs to prevent collapse",
                "Monitor livestock for cold stress",
                "Delay field operations until snow melts"
            ]
        })
    
    # Wind alerts
    if wind_speed is not None:
        if wind_speed > 15 or (wind_gust and wind_gust > 20):
            alerts.append({
                "type": "danger",
                "title": "High Wind Warning",
                "message": "Strong winds may cause physical damage to crops and structures.",
                "recommendations": [
                    "Secure greenhouse covers and structures",
                    "Stake or support tall crops and young trees",
                    "Postpone pesticide applications to prevent drift",
                    "Monitor for wind damage after event"
                ]
            })
        elif wind_speed > 10:
            alerts.append({
                "type": "warning",
                "title": "Windy Conditions",
                "message": "Moderate winds may increase water loss and affect spray applications.",
                "recommendations": [
                    "Adjust irrigation to account for increased evaporation",
                    "Avoid spraying pesticides in windy conditions",
                    "Monitor for signs of wind damage in sensitive crops"
                ]
            })
    
    # Weather condition alerts
    if weather_id:
        # Thunderstorm
        if 200 <= weather_id < 300:
            alerts.append({
                "type": "danger",
                "title": "Thunderstorm Alert",
                "message": "Thunderstorms may bring lightning, hail, and strong winds.",
                "recommendations": [
                    "Seek shelter immediately if outdoors",
                    "Unplug sensitive electrical equipment",
                    "Protect crops from potential hail damage if possible",
                    "Monitor weather updates for severe storm warnings"
                ]
            })
        # Drizzle/Rain
        elif 300 <= weather_id < 400 or 500 <= weather_id < 600:
            if 502 <= weather_id <= 504:
                alerts.append({
                    "type": "warning",
                    "title": "Heavy Rain Alert",
                    "message": "Heavy rain may affect field conditions and crop health.",
                    "recommendations": [
                        "Check field drainage systems",
                        "Monitor for signs of waterlogging in crops",
                        "Postpone field operations until conditions improve"
                    ]
                })
        # Snow
        elif 600 <= weather_id < 700:
            alerts.append({
                "type": "warning",
                "title": "Snow Alert",
                "message": "Snow may affect crop growth and field operations.",
                "recommendations": [
                    "Protect sensitive crops with covers",
                    "Delay planting until snow melts",
                    "Monitor for cold stress in livestock"
                ]
            })
        # Atmosphere (fog, haze, etc.)
        elif 700 <= weather_id < 800:
            if weather_id == 731 or weather_id == 751 or weather_id == 761:
                alerts.append({
                    "type": "warning",
                    "title": "Dust/Sand Alert",
                    "message": "Dust or sand in the air may affect crops and equipment.",
                    "recommendations": [
                        "Protect sensitive equipment from dust damage",
                        "Irrigate to settle dust on crops if possible",
                        "Consider postponing field operations until conditions improve"
                    ]
                })
            elif weather_id == 762:
                alerts.append({
                    "type": "danger",
                    "title": "Volcanic Ash Alert",
                    "message": "Volcanic ash may damage crops and pose health risks.",
                    "recommendations": [
                        "Take immediate precautions to protect yourself and livestock",
                        "Cover sensitive crops if possible",
                        "Avoid working outdoors until ash settles",
                        "Clean ash from leaves to prevent damage"
                    ]
                })
    
    # Pressure alerts
    if pressure is not None:
        if pressure < 980:
            alerts.append({
                "type": "warning",
                "title": "Low Pressure System",
                "message": "Low pressure may indicate approaching stormy weather.",
                "recommendations": [
                    "Monitor weather forecasts for storm warnings",
                    "Secure loose items around the farm",
                    "Prepare drainage systems for potential heavy rain"
                ]
            })
    
    return alerts

def format_forecast_data(forecast_data):
    """
    Format forecast data for display with agricultural insights
    
    Args:
        forecast_data (dict): Raw forecast data
        
    Returns:
        list: Formatted forecast entries with farming insights
    """
    if not forecast_data or "list" not in forecast_data:
        return []
    
    formatted_entries = []
    forecast_list = forecast_data["list"]
    
    # Group by day
    days = {}
    for entry in forecast_list:
        dt = datetime.fromtimestamp(entry["dt"])
        day = dt.strftime("%Y-%m-%d")
        
        if day not in days:
            days[day] = []
        
        days[day].append(entry)
    
    # Process each day
    for day, entries in days.items():
        dt = datetime.strptime(day, "%Y-%m-%d")
        day_name = dt.strftime("%A")  # Get day name (Monday, Tuesday, etc.)
        
        # Calculate values for the day
        temp_sum = sum(entry["main"]["temp"] for entry in entries)
        temp_min = min(entry["main"]["temp_min"] for entry in entries)
        temp_max = max(entry["main"]["temp_max"] for entry in entries)
        humidity_sum = sum(entry["main"]["humidity"] for entry in entries)
        wind_speeds = [entry["wind"]["speed"] for entry in entries if "wind" in entry]
        avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0
        wind_dirs = [entry["wind"]["deg"] for entry in entries if "wind" in entry and "deg" in entry["wind"]]
        wind_dir = wind_dirs[0] if wind_dirs else None
        
        # Get the most common weather condition
        weather_descriptions = [entry["weather"][0]["description"] for entry in entries]
        weather_icons = [entry["weather"][0]["icon"] for entry in entries]
        
        # Use the most common description and corresponding icon
        from collections import Counter
        common_desc = Counter(weather_descriptions).most_common(1)[0][0]
        common_icon = next((icon for desc, icon in zip(weather_descriptions, weather_icons) 
                         if desc == common_desc), weather_icons[0])
        
        # Calculate rain if available
        total_rain = 0
        for entry in entries:
            if "rain" in entry:
                total_rain += entry["rain"].get("3h", 0)
        
        # Calculate cloud cover
        avg_clouds = sum(entry.get("clouds", {}).get("all", 0) for entry in entries) / len(entries)
        
        # Format the entry
        formatted_entry = {
            "day": day,
            "day_name": day_name,
            "avg_temp": temp_sum / len(entries),
            "min_temp": temp_min,
            "max_temp": temp_max,
            "avg_humidity": humidity_sum / len(entries),
            "weather_description": common_desc.capitalize(),
            "weather_icon": common_icon,
            "total_rain": total_rain,
            "avg_wind_speed": avg_wind,
            "wind_direction": wind_dir,
            "avg_cloud_cover": avg_clouds,
            "hourly_data": entries  # Keep hourly data for detailed analysis
        }
        
        formatted_entries.append(formatted_entry)
    
    return formatted_entries

def generate_daily_advice(day_forecast):
    """
    Generate agricultural advice for a specific day's forecast
    
    Args:
        day_forecast (dict): Formatted forecast data for one day
        
    Returns:
        str: Markdown formatted advice
    """
    advice = []
    
    # Temperature advice
    if day_forecast["max_temp"] > 35:
        advice.append("🌡️ **Heat Advisory**: Extreme heat expected. Consider:")
        advice.append("- Increase irrigation frequency")
        advice.append("- Provide shade for sensitive crops")
        advice.append("- Avoid working during peak heat hours")
    elif day_forecast["max_temp"] > 30:
        advice.append("🌡️ **Warm Day**: Monitor for heat stress. Consider:")
        advice.append("- Adjust irrigation to account for higher evaporation")
        advice.append("- Check soil moisture levels")
    elif day_forecast["min_temp"] < 5:
        advice.append("❄️ **Cold Advisory**: Frost risk possible. Consider:")
        advice.append("- Protect sensitive crops with covers")
        advice.append("- Delay early morning irrigation")
        advice.append("- Harvest frost-sensitive produce")
    
    # Rain advice
    if day_forecast["total_rain"] > 10:
        advice.append("🌧️ **Heavy Rain Expected**: Potential impacts:")
        advice.append("- Check field drainage systems")
        advice.append("- Postpone fertilizer applications")
        advice.append("- Monitor for waterlogging")
    elif day_forecast["total_rain"] > 2:
        advice.append("🌧️ **Rain Expected**: Considerations:")
        advice.append("- Good time for planting or transplanting")
        advice.append("- Reduce irrigation accordingly")
        advice.append("- Monitor for disease after wet conditions")
    
    # Wind advice
    if day_forecast["avg_wind_speed"] > 10:
        advice.append("💨 **Windy Conditions**: Potential impacts:")
        advice.append("- Secure greenhouse covers and structures")
        advice.append("- Avoid pesticide applications")
        advice.append("- Monitor for physical damage to crops")
    
    # General farming activities
    if day_forecast["avg_cloud_cover"] < 30 and day_forecast["total_rain"] < 1:
        advice.append("☀️ **Good Day For**:")
        advice.append("- Field preparation and planting")
        advice.append("- Harvesting and drying crops")
        advice.append("- Pesticide applications (if needed)")
    elif day_forecast["avg_cloud_cover"] > 70:
        advice.append("☁️ **Overcast Conditions**: Suitable for:")
        advice.append("- Transplanting to reduce shock")
        advice.append("- Pruning operations")
    
    if not advice:
        advice.append("ℹ️ **Normal Conditions**: No special precautions needed.")
    
    return "\n".join(advice)

def generate_comprehensive_advisory(weather_data, forecast_data):
    """
    Generate comprehensive farming advisory based on current and forecasted weather
    
    Args:
        weather_data (dict): Current weather data
        forecast_data (dict): Forecast data
        
    Returns:
        str: Markdown formatted advisory
    """
    if not weather_data or not forecast_data:
        return "No weather data available to generate advisory."
    
    advisory = []
    
    # Current conditions summary
    current_temp = weather_data["main"]["temp"]
    current_humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    rain = weather_data.get("rain", {}).get("1h", 0)
    weather_desc = weather_data["weather"][0]["description"].capitalize()
    
    advisory.append(f"## Current Weather Advisory")
    advisory.append(f"- Temperature: {current_temp:.1f}°C")
    advisory.append(f"- Humidity: {current_humidity}%")
    advisory.append(f"- Wind: {wind_speed} m/s")
    advisory.append(f"- Precipitation: {rain} mm (last hour)")
    advisory.append(f"- Conditions: {weather_desc}")
    advisory.append("")
    
    # Current weather impacts
    advisory.append("### Immediate Recommendations:")
    
    # Temperature impacts
    if current_temp > 35:
        advisory.append("- **Heat Stress Management**:")
        advisory.append("  - Increase irrigation frequency to combat heat stress")
        advisory.append("  - Provide shade for sensitive crops and livestock")
        advisory.append("  - Avoid field work during peak heat hours (11AM-3PM)")
    elif current_temp < 5:
        advisory.append("- **Cold Protection**:")
        advisory.append("  - Protect sensitive crops with frost covers or mulch")
        advisory.append("  - Move potted plants to sheltered areas")
        advisory.append("  - Provide additional bedding for livestock")
    
    # Humidity impacts
    if current_humidity > 80:
        advisory.append("- **High Humidity Management**:")
        advisory.append("  - Monitor for fungal diseases (powdery mildew, rust)")
        advisory.append("  - Improve air circulation around plants")
        advisory.append("  - Consider preventive fungicide applications")
    elif current_humidity < 30:
        advisory.append("- **Low Humidity Management**:")
        advisory.append("  - Increase irrigation frequency")
        advisory.append("  - Apply mulch to conserve soil moisture")
        advisory.append("  - Monitor for signs of water stress")
    
    # Wind impacts
    if wind_speed > 10:
        advisory.append("- **Windy Conditions**:")
        advisory.append("  - Secure greenhouse covers and structures")
        advisory.append("  - Stake or support tall crops")
        advisory.append("  - Avoid pesticide applications to prevent drift")
    
    # Rain impacts
    if rain > 5:
        advisory.append("- **Heavy Rain Response**:")
        advisory.append("  - Check and clear drainage systems")
        advisory.append("  - Monitor low-lying areas for water accumulation")
        advisory.append("  - Postpone fertilizer applications to prevent runoff")
    elif rain > 0:
        advisory.append("- **Rainy Conditions**:")
        advisory.append("  - Reduce irrigation accordingly")
        advisory.append("  - Monitor for disease after wet conditions")
    
    # 5-day forecast summary
    advisory.append("")
    advisory.append("## 5-Day Forecast Outlook")
    
    daily_forecast = format_forecast_data(forecast_data)
    for day in daily_forecast[:5]:  # Show next 5 days
        advisory.append(f"### {day['day_name']} ({day['day']})")
        advisory.append(f"- **Temperature**: High {day['max_temp']:.1f}°C / Low {day['min_temp']:.1f}°C")
        advisory.append(f"- **Humidity**: {day['avg_humidity']:.0f}%")
        advisory.append(f"- **Rain**: {day['total_rain']:.1f} mm")
        advisory.append(f"- **Wind**: {day['avg_wind_speed']:.1f} m/s")
        advisory.append(f"- **Conditions**: {day['weather_description']}")
        
        # Add daily advice
        daily_advice = generate_daily_advice(day)
        advisory.append("")
        advisory.append("**Daily Farming Advice**:")
        advisory.append(daily_advice)
        advisory.append("")
    
    # Seasonal planning
    advisory.append("")
    advisory.append("## Seasonal Planning Considerations")
    
    now = datetime.now()
    month = now.month
    
    if 3 <= month <= 5:  # Spring
        advisory.append("- **Spring Planting**:")
        advisory.append("  - Prepare seedbeds for summer crops")
        advisory.append("  - Complete soil testing and amendment")
        advisory.append("  - Begin planting warm-season crops as soil warms")
    elif 6 <= month <= 8:  # Summer
        advisory.append("- **Summer Management**:")
        advisory.append("  - Monitor irrigation carefully")
        advisory.append("  - Watch for pest outbreaks in warm weather")
        advisory.append("  - Begin planning for fall crops")
    elif 9 <= month <= 11:  # Fall
        advisory.append("- **Fall Harvest**:")
        advisory.append("  - Harvest mature crops")
        advisory.append("  - Plant cover crops in harvested fields")
        advisory.append("  - Test and amend soil for next season")
    else:  # Winter
        advisory.append("- **Winter Preparation**:")
        advisory.append("  - Protect sensitive plants from frost")
        advisory.append("  - Service farm equipment during downtime")
        advisory.append("  - Plan next season's crop rotation")
    
    return "\n".join(advisory)

def display_weather_widget(location=None):
    """
    Display a compact weather widget for dashboard
    
    Args:
        location (str): Location to show weather for. If None, uses profile location.
        
    Returns:
        None: Renders the widget directly
    """
    if location is None:
        location = get_profile_field(st.session_state.user_profile, "farm_location")
        if not location:
            st.warning("Please set your location in profile settings")
            return
    
    weather_data = fetch_weather_data(location)
    if not weather_data:
        st.error("Could not fetch weather data")
        return
    
    # Extract weather info
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    weather_desc = weather_data["weather"][0]["description"].capitalize()
    icon_code = weather_data["weather"][0]["icon"]
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display weather icon
        st.image(get_weather_icon_url(icon_code), width=80)
    
    with col2:
        # Display weather info
        st.metric(label="Temperature", value=f"{temp:.1f}°C")
        st.caption(f"{weather_desc} | Humidity: {humidity}% | Wind: {wind_speed} m/s")
        
        # Show critical alerts if any
        alerts = get_weather_alerts(weather_data)
        critical_alerts = [a for a in alerts if a["type"] == "danger"]
        if critical_alerts:
            st.warning(f"⚠️ {len(critical_alerts)} active weather alerts")


def get_crop_weather_impact(crop_name, weather_data):
    """
    Analyze the impact of current weather on a specific crop
    
    Args:
        crop_name (str): Name of the crop to analyze
        weather_data (dict): Current weather data from API
        
    Returns:
        dict: Dictionary with pros, cons, and suggestions
    """
    if not weather_data or not crop_name:
        return None
    
    # Get weather parameters
    temp = weather_data.get("main", {}).get("temp")
    humidity = weather_data.get("main", {}).get("humidity")
    wind_speed = weather_data.get("wind", {}).get("speed")
    is_raining = "rain" in weather_data
    rain_amount = weather_data.get("rain", {}).get("1h", 0) if is_raining else 0
    weather_id = weather_data.get("weather", [{}])[0].get("id") if weather_data.get("weather") else None
    
    # Initialize result structure
    impact = {
        "crop": crop_name,
        "pros": [],
        "cons": [],
        "suggestions": []
    }
    
    # Define crop-specific thresholds (in Celsius) and characteristics
    crop_thresholds = {
        # Vegetables
        "Tomato": {
            "optimal_temp": (18, 28),
            "max_temp": 32,
            "min_temp": 10,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 5,
            "growth_stages": {
                "Germination": {"optimal_temp": (20, 30), "water_needs": "Moderate"},
                "Vegetative": {"optimal_temp": (18, 28), "water_needs": "High"},
                "Flowering": {"optimal_temp": (20, 28), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (20, 28), "water_needs": "Moderate"},
                "Maturity": {"optimal_temp": (18, 26), "water_needs": "Low"}
            }
        },
        "Potato": {
            "optimal_temp": (15, 20),
            "max_temp": 30,
            "min_temp": 7,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 5,
            "growth_stages": {
                "Germination": {"optimal_temp": (15, 20), "water_needs": "Moderate"},
                "Vegetative": {"optimal_temp": (15, 20), "water_needs": "High"},
                "Tuber Initiation": {"optimal_temp": (15, 20), "water_needs": "High"},
                "Tuber Bulking": {"optimal_temp": (15, 20), "water_needs": "Moderate"},
                "Maturity": {"optimal_temp": (15, 20), "water_needs": "Low"}
            }
        },
        # Cereals
        "Wheat": {
            "optimal_temp": (15, 22),
            "max_temp": 30,
            "min_temp": 5,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 8,
            "wind_tolerance": 7,
            "growth_stages": {
                "Germination": {"optimal_temp": (12, 20), "water_needs": "Moderate"},
                "Tillering": {"optimal_temp": (15, 22), "water_needs": "High"},
                "Stem Extension": {"optimal_temp": (15, 22), "water_needs": "High"},
                "Heading": {"optimal_temp": (15, 22), "water_needs": "Moderate"},
                "Maturity": {"optimal_temp": (15, 25), "water_needs": "Low"}
            }
        },
        "Rice": {
            "optimal_temp": (20, 30),
            "max_temp": 35,
            "min_temp": 15,
            "optimal_humidity": (70, 90),
            "rain_tolerance": 10,
            "wind_tolerance": 6,
            "growth_stages": {
                "Germination": {"optimal_temp": (25, 30), "water_needs": "High"},
                "Vegetative": {"optimal_temp": (20, 30), "water_needs": "High"},
                "Reproductive": {"optimal_temp": (20, 30), "water_needs": "High"},
                "Ripening": {"optimal_temp": (20, 30), "water_needs": "Moderate"}
            }
        },
        # Fruits
        "Mango": {
            "optimal_temp": (24, 30),
            "max_temp": 38,
            "min_temp": 10,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 5,
            "wind_tolerance": 6,
            "growth_stages": {
                "Dormancy": {"optimal_temp": (15, 25), "water_needs": "Low"},
                "Flowering": {"optimal_temp": (24, 30), "water_needs": "Moderate"},
                "Fruiting": {"optimal_temp": (24, 30), "water_needs": "Moderate"},
                "Ripening": {"optimal_temp": (24, 30), "water_needs": "Low"}
            }
        },
        "Onion": {
            "optimal_temp": (13, 25),
            "max_temp": 35,
            "min_temp": 10,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 5,
            "growth_stages": {
                "Bulbing": {"optimal_temp": (15, 25), "water_needs": "Moderate"},
                "Maturity": {"optimal_temp": (15, 25), "water_needs": "Low"}
            }
        },
        "Soybean": {
            "optimal_temp": (20, 30),
            "max_temp": 38,
            "min_temp": 12,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 6,
            "wind_tolerance": 6,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (20, 30), "water_needs": "High"},
                "Flowering": {"optimal_temp": (24, 30), "water_needs": "High"},
                "Pod Filling": {"optimal_temp": (20, 28), "water_needs": "Moderate"}
            }
        },
        "Cotton": {
            "optimal_temp": (21, 30),
            "max_temp": 38,
            "min_temp": 15,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 7,
            "wind_tolerance": 7,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (21, 30), "water_needs": "Moderate"},
                "Flowering": {"optimal_temp": (24, 32), "water_needs": "High"},
                "Boll Formation": {"optimal_temp": (24, 30), "water_needs": "Moderate"}
            }
        },
        "Cabbage": {
            "optimal_temp": (15, 25),
            "max_temp": 30,
            "min_temp": 5,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 6,
            "wind_tolerance": 4,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (15, 25), "water_needs": "High"},
                "Head Formation": {"optimal_temp": (15, 22), "water_needs": "Moderate"}
            }
        },
        "Cauliflower": {
            "optimal_temp": (15, 25),
            "max_temp": 30,
            "min_temp": 6,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 4,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (15, 25), "water_needs": "High"},
                "Curd Formation": {"optimal_temp": (15, 22), "water_needs": "Moderate"}
            }
        },
        "Brinjal": {
            "optimal_temp": (20, 30),
            "max_temp": 35,
            "min_temp": 15,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (20, 30), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (22, 30), "water_needs": "Moderate"}
            }
        },
        "Lady Finger": {
            "optimal_temp": (24, 32),
            "max_temp": 38,
            "min_temp": 15,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 6,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (24, 32), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (26, 32), "water_needs": "Moderate"}
            }
        },
        "Chili": {
            "optimal_temp": (20, 30),
            "max_temp": 35,
            "min_temp": 15,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (20, 30), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (22, 30), "water_needs": "Moderate"}
            }
        },
        "Bottle Gourd": {
            "optimal_temp": (24, 32),
            "max_temp": 38,
            "min_temp": 18,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 8,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (24, 32), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (25, 32), "water_needs": "Moderate"}
            }
        },
        "Bitter Gourd": {
            "optimal_temp": (24, 30),
            "max_temp": 36,
            "min_temp": 18,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 6,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (24, 30), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (26, 30), "water_needs": "Moderate"}
            }
        },
        "Cluster Beans": {
            "optimal_temp": (25, 35),
            "max_temp": 40,
            "min_temp": 15,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 5,
            "wind_tolerance": 6,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (25, 35), "water_needs": "Moderate"},
                "Fruiting": {"optimal_temp": (26, 35), "water_needs": "Moderate"}
            }
        },
        "Cucumber": {
            "optimal_temp": (22, 32),
            "max_temp": 38,
            "min_temp": 16,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 6,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (22, 32), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (24, 32), "water_needs": "Moderate"}
            }
        },
        "Maize": {
            "optimal_temp": (20, 30),
            "max_temp": 38,
            "min_temp": 10,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 8,
            "wind_tolerance": 7,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (20, 30), "water_needs": "High"},
                "Flowering": {"optimal_temp": (22, 30), "water_needs": "High"},
                "Grain Filling": {"optimal_temp": (20, 28), "water_needs": "Moderate"}
            }
        },
        "Grapes": {
            "optimal_temp": (15, 30),
            "max_temp": 38,
            "min_temp": 5,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 4,
            "wind_tolerance": 5,
            "growth_stages": {
                "Bud Break": {"optimal_temp": (15, 25), "water_needs": "Moderate"},
                "Fruit Set": {"optimal_temp": (20, 30), "water_needs": "Moderate"},
                "Ripening": {"optimal_temp": (22, 32), "water_needs": "Low"}
            }
        },
        "Carrot": {
            "optimal_temp": (15, 25),
            "max_temp": 30,
            "min_temp": 5,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 4,
            "growth_stages": {
                "Root Development": {"optimal_temp": (15, 25), "water_needs": "Moderate"},
                "Maturity": {"optimal_temp": (15, 25), "water_needs": "Low"}
            }
        },
        "Radish": {
            "optimal_temp": (15, 25),
            "max_temp": 30,
            "min_temp": 5,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 5,
            "wind_tolerance": 4,
            "growth_stages": {
                "Root Formation": {"optimal_temp": (15, 25), "water_needs": "Moderate"}
            }
        },
        "Pumpkin": {
            "optimal_temp": (22, 32),
            "max_temp": 38,
            "min_temp": 18,
            "optimal_humidity": (60, 80),
            "rain_tolerance": 8,
            "wind_tolerance": 6,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (22, 32), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (24, 32), "water_needs": "Moderate"}
            }
        },
        "Orange": {
            "optimal_temp": (15, 30),
            "max_temp": 38,
            "min_temp": 5,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 6,
            "wind_tolerance": 6,
            "growth_stages": {
                "Flowering": {"optimal_temp": (20, 30), "water_needs": "Moderate"},
                "Fruiting": {"optimal_temp": (24, 30), "water_needs": "Moderate"}
            }
        },
        "Banana": {
            "optimal_temp": (25, 35),
            "max_temp": 40,
            "min_temp": 15,
            "optimal_humidity": (70, 90),
            "rain_tolerance": 10,
            "wind_tolerance": 7,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (25, 35), "water_needs": "High"},
                "Fruiting": {"optimal_temp": (26, 35), "water_needs": "High"}
            }
        },
        "Watermelon": {
            "optimal_temp": (24, 32),
            "max_temp": 38,
            "min_temp": 18,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 6,
            "wind_tolerance": 5,
            "growth_stages": {
                "Vegetative": {"optimal_temp": (24, 32), "water_needs": "Moderate"},
                "Fruiting": {"optimal_temp": (26, 32), "water_needs": "Low"}
            }
        },
        "Guava": {
            "optimal_temp": (23, 30),
            "max_temp": 38,
            "min_temp": 10,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 5,
            "wind_tolerance": 5,
            "growth_stages": {
                "Flowering": {"optimal_temp": (23, 30), "water_needs": "Moderate"},
                "Fruiting": {"optimal_temp": (24, 30), "water_needs": "Moderate"}
            }
        },
        "Pomegranate": {
            "optimal_temp": (20, 35),
            "max_temp": 40,
            "min_temp": 10,
            "optimal_humidity": (50, 70),
            "rain_tolerance": 5,
            "wind_tolerance": 6,
            "growth_stages": {
                "Flowering": {"optimal_temp": (20, 35), "water_needs": "Moderate"},
                "Fruiting": {"optimal_temp": (22, 35), "water_needs": "Moderate"}
            }
        }
    }

    crop_info = crop_thresholds.get(crop_name)
    if not crop_info:
        impact["cons"].append("No detailed data available for this crop.")
        return impact
    
    # Temperature analysis
    opt_temp_min, opt_temp_max = crop_info["optimal_temp"]
    if temp is not None:
        if temp < opt_temp_min:
            impact["cons"].append(f"Temperature ({temp}°C) is below optimal range ({opt_temp_min}-{opt_temp_max}°C)")
            impact["suggestions"].append(f"Consider protecting {crop_name} from cold stress with covers or mulch")
        elif temp > opt_temp_max:
            impact["cons"].append(f"Temperature ({temp}°C) is above optimal range ({opt_temp_min}-{opt_temp_max}°C)")
            impact["suggestions"].append(f"Provide shade for {crop_name} to reduce heat stress")
        else:
            impact["pros"].append(f"Temperature ({temp}°C) is within optimal range for {crop_name}")
    
    # Humidity analysis
    if humidity is not None:
        opt_humidity_min, opt_humidity_max = crop_info["optimal_humidity"]
        if humidity < opt_humidity_min:
            impact["cons"].append(f"Humidity ({humidity}%) is below optimal range ({opt_humidity_min}-{opt_humidity_max}%)")
            impact["suggestions"].append(f"Increase irrigation frequency for {crop_name} to compensate for dry air")
        elif humidity > opt_humidity_max:
            impact["cons"].append(f"Humidity ({humidity}%) is above optimal range ({opt_humidity_min}-{opt_humidity_max}%)")
            impact["suggestions"].append(f"Improve air circulation around {crop_name} to prevent fungal diseases")
        else:
            impact["pros"].append(f"Humidity ({humidity}%) is within optimal range for {crop_name}")
    
    # Rain analysis
    if rain_amount > crop_info["rain_tolerance"]:
        impact["cons"].append(f"Heavy rain ({rain_amount}mm) may waterlog {crop_name} (tolerance: {crop_info['rain_tolerance']}mm)")
        impact["suggestions"].append(f"Ensure good drainage for {crop_name} fields")
    elif is_raining:
        impact["pros"].append(f"Moderate rain is beneficial for {crop_name}")
    else:
        impact["suggestions"].append(f"Monitor soil moisture for {crop_name} and irrigate if needed")
    
    # Wind analysis
    if wind_speed is not None and wind_speed > crop_info["wind_tolerance"]:
        impact["cons"].append(f"Wind speed ({wind_speed}m/s) exceeds tolerance for {crop_name} ({crop_info['wind_tolerance']}m/s)")
        impact["suggestions"].append(f"Provide wind protection for {crop_name} if possible")
    
    # Weather condition analysis
    if weather_id:
        # Thunderstorm warning
        if 200 <= weather_id < 300:
            impact["cons"].append(f"Thunderstorm may damage {crop_name}")
            impact["suggestions"].append(f"Protect {crop_name} from potential hail and strong winds")
        # Freezing conditions
        elif weather_id == 511 or (600 <= weather_id < 700 and temp < 0):
            impact["cons"].append(f"Freezing conditions may harm {crop_name}")
            impact["suggestions"].append(f"Protect {crop_name} from frost if possible")
    
    # If no specific issues found
    if not impact["cons"]:
        impact["pros"].append(f"Weather conditions are generally favorable for {crop_name}")
    
    return impact
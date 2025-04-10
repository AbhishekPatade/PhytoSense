"""
Weather service for PhytoSense application
Provides weather data and alerts for farmers
"""

import os
import json
import time
import requests
import streamlit as st
from datetime import datetime, timedelta
from profile_utils import get_profile_field

# Weather API constants
WEATHER_API_KEY = "f4923cb2515212f8108721ed67014dc5"
WEATHER_CACHE_TTL = 3600  # Cache weather data for 1 hour (in seconds)
CACHE_DIR = "weather_data"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def get_weather_icon_url(icon_code):
    """Get URL for weather icon"""
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
        return None
    
    if not WEATHER_API_KEY:
        st.warning("Weather API key not set. Weather data cannot be retrieved.")
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
        
        response = requests.get(f"{WEATHER_BASE_URL}/weather", params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"Error fetching weather data: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
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
        return None
    
    if not WEATHER_API_KEY:
        st.warning("Weather API key not set. Forecast data cannot be retrieved.")
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
        
        response = requests.get(f"{WEATHER_BASE_URL}/forecast", params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"Error fetching forecast data: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None

def get_weather_alerts(weather_data):
    """
    Generate weather alerts based on current conditions
    
    Args:
        weather_data (dict): Weather data from API
        
    Returns:
        list: List of alert messages
    """
    alerts = []
    
    if not weather_data:
        return alerts
    
    # Check temperature alerts
    temp = weather_data.get("main", {}).get("temp")
    if temp is not None:
        if temp > 35:
            alerts.append({
                "type": "danger",
                "message": "Extreme heat alert! Ensure proper irrigation and consider shade for sensitive crops."
            })
        elif temp > 30:
            alerts.append({
                "type": "warning",
                "message": "High temperature alert. Monitor water levels and irrigation needs."
            })
        elif temp < 5:
            alerts.append({
                "type": "danger",
                "message": "Frost risk alert! Protect sensitive crops from cold damage."
            })
        elif temp < 10:
            alerts.append({
                "type": "warning",
                "message": "Low temperature alert. Be prepared for potential frost conditions."
            })
    
    # Check humidity alerts
    humidity = weather_data.get("main", {}).get("humidity")
    if humidity is not None:
        if humidity > 85:
            alerts.append({
                "type": "warning",
                "message": "High humidity alert. Monitor for fungal diseases and reduce leaf wetness."
            })
        elif humidity < 30:
            alerts.append({
                "type": "warning",
                "message": "Low humidity alert. Increase irrigation to prevent crop stress."
            })
    
    # Check rain alerts
    if "rain" in weather_data:
        rain_1h = weather_data.get("rain", {}).get("1h", 0)
        rain_3h = weather_data.get("rain", {}).get("3h", 0)
        
        if rain_1h > 10 or rain_3h > 20:
            alerts.append({
                "type": "danger",
                "message": "Heavy rain alert! Be cautious of flooding and soil erosion."
            })
        elif rain_1h > 5 or rain_3h > 10:
            alerts.append({
                "type": "warning",
                "message": "Moderate rain alert. Check drainage systems and field conditions."
            })
    
    # Check wind alerts
    wind_speed = weather_data.get("wind", {}).get("speed")
    if wind_speed is not None:
        if wind_speed > 10:  # m/s = ~36 km/h
            alerts.append({
                "type": "danger",
                "message": "Strong wind alert! Secure structures and protect young plants."
            })
        elif wind_speed > 7:  # m/s = ~25 km/h
            alerts.append({
                "type": "warning",
                "message": "Moderate wind alert. Monitor for crop damage and increased water loss."
            })
    
    # Check weather conditions
    weather_id = weather_data.get("weather", [{}])[0].get("id") if weather_data.get("weather") else None
    if weather_id:
        # Thunderstorm
        if 200 <= weather_id < 300:
            alerts.append({
                "type": "danger",
                "message": "Thunderstorm alert! Seek shelter and be cautious of lightning strikes."
            })
        # Drizzle/Rain
        elif 300 <= weather_id < 400 or 500 <= weather_id < 600:
            if 502 <= weather_id <= 504:
                alerts.append({
                    "type": "warning",
                    "message": "Heavy rain alert. Check field drainage and avoid waterlogging."
                })
        # Snow
        elif 600 <= weather_id < 700:
            alerts.append({
                "type": "warning",
                "message": "Snow alert. Protect sensitive crops from cold damage."
            })
        # Atmosphere (fog, haze, etc.)
        elif 700 <= weather_id < 800:
            if weather_id == 731 or weather_id == 751 or weather_id == 761:
                alerts.append({
                    "type": "warning",
                    "message": "Dust/Sand alert. Protect sensitive equipment and crops from dust damage."
                })
            elif weather_id == 762:
                alerts.append({
                    "type": "danger",
                    "message": "Volcanic ash alert! Take immediate precautions to protect yourself and livestock."
                })
    
    return alerts

def format_forecast_data(forecast_data):
    """
    Format forecast data for display
    
    Args:
        forecast_data (dict): Raw forecast data
        
    Returns:
        list: Formatted forecast entries
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
        
        # Calculate average values for the day
        temp_sum = sum(entry["main"]["temp"] for entry in entries)
        temp_min = min(entry["main"]["temp_min"] for entry in entries)
        temp_max = max(entry["main"]["temp_max"] for entry in entries)
        humidity_sum = sum(entry["main"]["humidity"] for entry in entries)
        
        # Get the most common weather condition
        weather_descriptions = [entry["weather"][0]["description"] for entry in entries]
        weather_icons = [entry["weather"][0]["icon"] for entry in entries]
        
        # Use the most common description and corresponding icon
        from collections import Counter
        common_desc = Counter(weather_descriptions).most_common(1)[0][0]
        
        # Find an icon that matches the common description
        common_icon = next((icon for desc, icon in zip(weather_descriptions, weather_icons) 
                         if desc == common_desc), weather_icons[0])
        
        # Calculate rain if available
        total_rain = 0
        for entry in entries:
            if "rain" in entry:
                total_rain += entry["rain"].get("3h", 0)
        
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
            "total_rain": total_rain
        }
        
        formatted_entries.append(formatted_entry)
    
    return formatted_entries

def display_weather_widget(location=None):
    """
    Display weather widget in the sidebar
    
    Args:
        location (str): Location to display weather for, defaults to user's location
    """
    with st.sidebar:
        st.markdown("### Weather Information")
        
        # Get user location if not provided
        if not location and st.session_state.user_profile:
            location = get_profile_field(st.session_state.user_profile, 'farm_location')
        
        if not location:
            st.info("Farm location not set. Update your profile to see weather alerts.")
            return
        
        # Fetch weather data
        weather_data = fetch_weather_data(location)
        
        if not weather_data:
            st.warning("Unable to retrieve weather data. Please check your location or API key.")
            
            # Show API key setup prompt if needed
            if not WEATHER_API_KEY:
                st.info("To enable weather features, please add your OpenWeatherMap API key to the .env file.")
            return
        
        # Display current weather
        try:
            weather_icon = weather_data.get("weather", [{}])[0].get("icon")
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "").capitalize()
            temp = weather_data.get("main", {}).get("temp")
            feels_like = weather_data.get("main", {}).get("feels_like")
            humidity = weather_data.get("main", {}).get("humidity")
            wind_speed = weather_data.get("wind", {}).get("speed")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if weather_icon:
                    st.image(get_weather_icon_url(weather_icon), width=60)
            
            with col2:
                st.markdown(f"**{location}**")
                st.markdown(f"{weather_desc}")
                
            # Temperature and conditions
            st.markdown(f"**Temperature:** {temp:.1f}°C (Feels like: {feels_like:.1f}°C)")
            st.markdown(f"**Humidity:** {humidity}%")
            st.markdown(f"**Wind:** {wind_speed} m/s")
            
            # Check for critical alerts
            alerts = get_weather_alerts(weather_data)
            if alerts:
                st.markdown("#### Weather Alerts")
                for alert in alerts:
                    if alert["type"] == "danger":
                        st.error(alert["message"])
                    else:
                        st.warning(alert["message"])
            
            # View full forecast link
            if st.button("View Full Forecast", key="sidebar_forecast"):
                st.session_state.page = "weather"
                st.rerun()
        
        except Exception as e:
            st.error(f"Error displaying weather data: {str(e)}")

def show_weather_page():
    """Display the full weather page"""
    st.header("Weather Forecasting & Agricultural Advisories")
    
    # Get user location
    location = None
    if st.session_state.user_profile:
        location = get_profile_field(st.session_state.user_profile, 'farm_location')
    
    # Location selector with default to user's location
    location_input = st.text_input("Location", value=location if location else "")
    
    if st.button("Get Weather"):
        if location_input:
            location = location_input
        else:
            st.warning("Please enter a location.")
    
    if not location:
        st.info("Enter a location to view weather data and agricultural advisories.")
        return
    
    # Fetch current weather
    weather_data = fetch_weather_data(location, use_cache=False)
    
    if not weather_data:
        st.warning("Unable to retrieve weather data. Please check your location or API key.")
        
        # Prompt for API key if needed
        if not WEATHER_API_KEY:
            st.info("""
            To enable weather features, you need an OpenWeatherMap API key.
            1. Sign up at https://openweathermap.org/
            2. Get your API key
            3. Add it to the .env file or set the WEATHER_API_KEY environment variable
            """)
        return
    
    # Display current weather conditions
    try:
        st.markdown("## Current Weather Conditions")
        
        # Basic layout with columns
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Weather icon and basic info
        with col1:
            weather_icon = weather_data.get("weather", [{}])[0].get("icon")
            if weather_icon:
                st.image(get_weather_icon_url(weather_icon), width=100)
        
        with col2:
            weather_main = weather_data.get("weather", [{}])[0].get("main", "")
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "").capitalize()
            st.markdown(f"## {weather_main}")
            st.markdown(f"### {weather_desc}")
            
            # Temperature
            temp = weather_data.get("main", {}).get("temp")
            feels_like = weather_data.get("main", {}).get("feels_like")
            st.markdown(f"**Temperature:** {temp:.1f}°C")
            st.markdown(f"**Feels like:** {feels_like:.1f}°C")
        
        with col3:
            # Other conditions
            humidity = weather_data.get("main", {}).get("humidity")
            pressure = weather_data.get("main", {}).get("pressure")
            wind_speed = weather_data.get("wind", {}).get("speed")
            wind_deg = weather_data.get("wind", {}).get("deg", 0)
            
            st.markdown("### Conditions")
            st.markdown(f"**Humidity:** {humidity}%")
            st.markdown(f"**Pressure:** {pressure} hPa")
            st.markdown(f"**Wind:** {wind_speed} m/s at {wind_deg}°")
        
        # Display alerts if any
        alerts = get_weather_alerts(weather_data)
        if alerts:
            st.markdown("## Weather Alerts")
            for alert in alerts:
                if alert["type"] == "danger":
                    st.error(alert["message"])
                else:
                    st.warning(alert["message"])
        
        # Fetch and display forecast
        st.markdown("## 5-Day Forecast")
        forecast_data = fetch_forecast_data(location, use_cache=False)
        
        if forecast_data:
            formatted_forecast = format_forecast_data(forecast_data)
            
            # Display forecast in a tabular format
            cols = st.columns(min(5, len(formatted_forecast)))
            
            for i, forecast in enumerate(formatted_forecast[:5]):  # Display up to 5 days
                with cols[i]:
                    st.markdown(f"**{forecast['day_name']}**")
                    
                    # Weather icon
                    if forecast['weather_icon']:
                        st.image(get_weather_icon_url(forecast['weather_icon']), width=50)
                    
                    # Weather description
                    st.markdown(f"{forecast['weather_description']}")
                    
                    # Temperature range
                    st.markdown(f"**High:** {forecast['max_temp']:.1f}°C")
                    st.markdown(f"**Low:** {forecast['min_temp']:.1f}°C")
                    
                    # Humidity
                    st.markdown(f"**Humidity:** {forecast['avg_humidity']:.0f}%")
                    
                    # Rain if available
                    if forecast['total_rain'] > 0:
                        st.markdown(f"**Rain:** {forecast['total_rain']:.1f} mm")
        else:
            st.warning("Unable to retrieve forecast data.")
        
        # Agricultural recommendations based on weather
        st.markdown("## Agricultural Recommendations")
        
        # Current date
        current_date = datetime.now().strftime("%B %d, %Y")
        st.markdown(f"### Recommendations for {location} on {current_date}")
        
        # Temperature-based recommendations
        if temp > 35:
            st.markdown("""
            #### Extreme Heat Conditions
            
            1. **Irrigation Management:**
               - Increase irrigation frequency but avoid midday watering
               - Consider drip irrigation to conserve water
               - Apply water directly to the root zone
            
            2. **Plant Protection:**
               - Use shade nets for sensitive crops
               - Apply white kaolin clay spray to reflect heat
               - Mulch heavily around plants to keep soil cool
            
            3. **Crop Selection:**
               - Prioritize heat-tolerant varieties
               - Consider delaying new plantings until temperatures moderate
            """)
        elif temp < 10:
            st.markdown("""
            #### Cool Temperature Conditions
            
            1. **Frost Protection:**
               - Cover sensitive crops with row covers at night
               - Use wind machines or heaters in critical areas
               - Irrigate soil before expected frost events
            
            2. **Planting Decisions:**
               - Delay planting warm-season crops
               - Focus on cool-season vegetables and grains
               - Protect newly transplanted seedlings with cloches
            
            3. **Soil Management:**
               - Add organic matter to improve soil insulation
               - Use black plastic mulch to warm soil
               - Minimize tillage to preserve soil heat
            """)
        else:
            st.markdown("""
            #### Moderate Temperature Conditions
            
            1. **Crop Management:**
               - Ideal time for most field operations
               - Monitor pest and disease pressure
               - Maintain regular irrigation schedule
            
            2. **Field Operations:**
               - Good conditions for planting and transplanting
               - Apply fertilizers as needed
               - Perform routine maintenance tasks
            """)
        
        # Additional crops of interest section
        crop_types = ["Rice", "Wheat", "Cotton", "Sugarcane", "Onion", "Tomato"]
        selected_crop = st.selectbox("Select crop for specific recommendations", crop_types)
        
        if selected_crop:
            # Simulate crop-specific recommendations based on weather
            st.markdown(f"### {selected_crop} Management Recommendations")
            
            if selected_crop == "Rice":
                if temp > 30:
                    st.markdown("""
                    - Maintain standing water (5-10 cm) to mitigate heat stress
                    - Apply foliar spray of 2% KCl or 2% urea during extreme heat
                    - Monitor for increased pest activity, especially brown planthopper
                    - Consider additional zinc application if deficiency symptoms appear
                    """)
                else:
                    st.markdown("""
                    - Maintain optimal water level based on crop stage
                    - Follow regular pest monitoring schedule
                    - Apply nitrogen fertilizer based on leaf color chart readings
                    - Check for signs of nutrient deficiencies
                    """)
            
            elif selected_crop == "Wheat":
                if temp < 15:
                    st.markdown("""
                    - Ideal conditions for wheat development
                    - Monitor for aphid infestations which thrive in cool weather
                    - Apply light irrigation if dry conditions persist
                    - Consider foliar spray of potassium if frost is expected
                    """)
                else:
                    st.markdown("""
                    - Ensure adequate irrigation as temperature rises
                    - Apply last dose of nitrogen before flowering stage
                    - Watch for rust development in warmer temperatures
                    - Consider applying fungicide preventatively if humid conditions persist
                    """)
            
            elif selected_crop == "Cotton":
                if temp > 35:
                    st.markdown("""
                    - Increase irrigation frequency and volume
                    - Apply foliar spray of 2% MgSO₄ to mitigate heat stress
                    - Monitor for increased bollworm activity
                    - Suspend foliar fertilizer applications during peak heat
                    """)
                else:
                    st.markdown("""
                    - Maintain regular irrigation schedule
                    - Apply recommended doses of fertilizers
                    - Monitor for sucking pests like jassids and whiteflies
                    - Consider growth regulator application if vegetative growth is excessive
                    """)
            
            elif selected_crop == "Sugarcane":
                if temp > 35:
                    st.markdown("""
                    - Increase irrigation frequency to 5-7 day intervals
                    - Apply trash mulching between rows to conserve soil moisture
                    - Watch for increased pyrilla activity during hot weather
                    - Delay nutrient applications until temperatures moderate
                    """)
                else:
                    st.markdown("""
                    - Maintain irrigation at 10-15 day intervals
                    - Apply nitrogen fertilizer if crop is in formative phase
                    - Conduct propping of canes if crop is prone to lodging
                    - Monitor for early signs of red rot disease
                    """)
            
            elif selected_crop == "Onion":
                if temp > 30:
                    st.markdown("""
                    - Increase frequency of light irrigations
                    - Apply light-colored mulch to reduce soil temperature
                    - Watch for thrips which proliferate in hot, dry conditions
                    - Provide temporary shade for young transplants
                    """)
                else:
                    st.markdown("""
                    - Maintain regular irrigation schedule
                    - Apply balanced fertilizer as per crop stage
                    - Monitor for purple blotch disease in humid conditions
                    - Ensure proper drainage to prevent bulb rot
                    """)
            
            elif selected_crop == "Tomato":
                if temp > 32:
                    st.markdown("""
                    - Use shade nets to reduce direct sun exposure
                    - Apply calcium nitrate spray to prevent blossom end rot
                    - Increase irrigation frequency but avoid wetting foliage
                    - Mulch heavily to maintain soil moisture and temperature
                    """)
                else:
                    st.markdown("""
                    - Support plants with stakes or trellises
                    - Maintain regular irrigation schedule
                    - Apply recommended NPK fertilizers
                    - Monitor for early blight and leaf spot diseases
                    """)
        
        # Weather resource links
        st.markdown("## Additional Weather Resources")
        st.markdown("""
        - [Indian Meteorological Department](https://mausam.imd.gov.in/)
        - [Agriculture Weather Advisory Services](https://cropweatheroutlook.imd.gov.in/)
        - [Weather-Based Crop Advisories](https://farmer.gov.in/WeatherReport/weatherreport.aspx)
        """)
        
    except Exception as e:
        st.error(f"Error displaying weather page: {str(e)}")
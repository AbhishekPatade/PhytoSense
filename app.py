import streamlit as st
import os
import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import json
from datetime import datetime
import random

# Import custom modules
from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from recommendations import get_preventive_measures, get_fertilizer_recommendations
from utils import load_svg, get_example_images, generate_report_markdown, format_probability, save_uploaded_image
from db_adapter import create_user, verify_user, update_user_profile, save_analysis, get_user_analyses, get_user_by_id, get_user_profile
from maharashtra import get_local_recommendations
from profile_utils import get_profile_field, get_select_index
from soil_analyzer import analyze_soil, get_soil_details
from model import load_model
from plant_analysis import enhanced_analysis
from weather_service import display_weather_widget, show_weather_page, fetch_weather_data, fetch_forecast_data, get_weather_alerts
from language_support import initialize_language, show_language_selector, t

# Page configuration
st.set_page_config(
    page_title="PhytoSense - AI Plant Health Monitoring",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# Apply custom CSS
with open(".streamlit/custom.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add some interactivity with CSS animations
st.markdown("""
<style>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInFromLeft {
  from { transform: translateX(-50px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.fadeIn {
  animation: fadeIn 1.5s ease-in-out;
}

.slideIn {
  animation: slideInFromLeft 0.8s ease-out;
}

.stAlert {
  animation: fadeIn 1s ease-in;
}

/* Add a cool gradient button */
.gradient-button {
  background-image: linear-gradient(to right, #6EDB3E, #4CAF50);
  color: white;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
  display: inline-block;
  transition: all 0.3s ease;
  margin: 10px 0px;
  box-shadow: 0 4px 15px rgba(110, 219, 62, 0.3);
}

.gradient-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 7px 20px rgba(110, 219, 62, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Create data directories if they don't exist
for directory in ["data", "uploads", "assets", "assets/examples", "weather_data"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "soil_results" not in st.session_state:
        st.session_state.soil_results = None
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "soil_analysis_complete" not in st.session_state:
        st.session_state.soil_analysis_complete = False
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    if "uploaded_images" not in st.session_state:
        st.session_state.uploaded_images = []
    if "uploaded_soil_image" not in st.session_state:
        st.session_state.uploaded_soil_image = None
    if "processed_image" not in st.session_state:
        st.session_state.processed_image = None
    if "processed_images" not in st.session_state:
        st.session_state.processed_images = []
    if "plant_info" not in st.session_state:
        st.session_state.plant_info = None
    if "water_content" not in st.session_state:
        st.session_state.water_content = None
    if "diseases" not in st.session_state:
        st.session_state.diseases = None
    if "pests" not in st.session_state:
        st.session_state.pests = None
    if "preventive_measures" not in st.session_state:
        st.session_state.preventive_measures = []
    if "fertilizer_recommendations" not in st.session_state:
        st.session_state.fertilizer_recommendations = []
    if "soil_fertility" not in st.session_state:
        st.session_state.soil_fertility = None
    if "crop_suggestions" not in st.session_state:
        st.session_state.crop_suggestions = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "show_account_created" not in st.session_state:
        st.session_state.show_account_created = False
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "dashboard"
    if "plant_details" not in st.session_state:
        st.session_state.plant_details = {
            "crop_type": None,
            "plant_age": None,
            "symptoms": None,
            "planting_date": None,
            "irrigation_method": None,
            "previous_treatments": None
        }
    # Weather-related session state variables
    if "weather_location" not in st.session_state:
        st.session_state.weather_location = None
    if "weather_data" not in st.session_state:
        st.session_state.weather_data = None
    if "forecast_data" not in st.session_state:
        st.session_state.forecast_data = None
    if "weather_alerts" not in st.session_state:
        st.session_state.weather_alerts = []
    # Language support
    if "language" not in st.session_state:
        st.session_state.language = "en"

# Initialize session state
init_session_state()

# Initialize language support
initialize_language()

# Navigation functions
def go_to_login():
    st.session_state.page = "login"
    st.session_state.show_account_created = False

def go_to_signup():
    st.session_state.page = "signup"

def go_to_profile_setup():
    st.session_state.page = "profile_setup"

def go_to_dashboard():
    st.session_state.page = "dashboard"

def go_to_crop_test():
    st.session_state.page = "crop_test"
    st.session_state.analysis_complete = False
    st.session_state.uploaded_image = None
    st.session_state.processed_image = None

def go_to_soil_analysis():
    st.session_state.page = "soil_analysis"
    st.session_state.soil_analysis_complete = False
    st.session_state.uploaded_soil_image = None

def go_to_history():
    st.session_state.page = "history"

def go_to_resources():
    st.session_state.page = "resources"

def go_to_weather():
    st.session_state.page = "weather"

def logout():
    """Log out the current user and reset session state variables"""
    # Reset all session state variables
    st.session_state.current_user = None
    st.session_state.user_profile = {}
    st.session_state.page = "login"
    st.session_state.analysis_complete = False
    st.session_state.soil_analysis_complete = False
    st.session_state.uploaded_image = None
    st.session_state.uploaded_soil_image = None
    st.session_state.processed_image = None
    st.session_state.plant_info = None
    st.session_state.water_content = None
    st.session_state.diseases = None
    st.session_state.pests = None
    st.session_state.preventive_measures = []
    st.session_state.fertilizer_recommendations = []
    st.session_state.soil_fertility = None
    st.session_state.crop_suggestions = []
    st.session_state.history = []
    # Clear weather-related state
    st.session_state.weather_location = None
    st.session_state.weather_data = None
    st.session_state.forecast_data = None
    st.session_state.weather_alerts = []

# Save analysis to history
def save_to_history(analysis_type, data):
    """Save analysis results to user history"""
    # Save to database if user is authenticated
    if st.session_state.current_user:
        # Convert PIL image to path for storage
        image_path = None
        if analysis_type == "plant" and st.session_state.uploaded_image:
            image_path = save_uploaded_image(st.session_state.uploaded_image)
        elif analysis_type == "soil" and st.session_state.uploaded_soil_image:
            image_path = save_uploaded_image(st.session_state.uploaded_soil_image)
        
        # Get user_id safely, supporting both object and dict access
        user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
        
        # Save analysis to database
        success, analysis_id = save_analysis(
            user_id=user_id,
            analysis_type=analysis_type,
            image_path=image_path,
            results=data
        )
        
        if success:
            # Update the session state history
            user_analyses = get_user_analyses(user_id)
            st.session_state.history = user_analyses

# Header with navigation
def show_header():
    """Display header with logo, title and navigation"""
    # Logo and title
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        # Placeholder logo (in a real app, we'd use a proper logo file)
        svg_content = load_svg("assets/logo.svg")
        st.image(svg_content, width=80)
    
    with col2:
        st.title("PhytoSense")
        st.subheader("AI-Powered Plant Health Monitoring System")
    
    # Navigation menu for logged-in users
    if st.session_state.current_user:
        with col3:
            username = st.session_state.current_user['username'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.username
            st.write(f"Welcome, {username}")
            if st.button("Logout"):
                logout()
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Dashboard", "Test Your Crop", "Soil Analysis", "History", "Resources", "Weather"])
        
        with tab1:
            if st.button("Go to Dashboard", key="nav_dashboard"):
                go_to_dashboard()
        
        with tab2:
            if st.button("Analyze Plant Health", key="nav_crop_test"):
                go_to_crop_test()
        
        with tab3:
            if st.button("Analyze Soil", key="nav_soil_analysis"):
                go_to_soil_analysis()
        
        with tab4:
            if st.button("View History", key="nav_history"):
                go_to_history()
                
        with tab5:
            if st.button("Farming Resources", key="nav_resources"):
                go_to_resources()
                
        with tab6:
            if st.button("Weather Alerts", key="nav_weather"):
                go_to_weather()
    
    st.markdown("---")

# Login page
def show_login_page():
    """Display the login page"""
    st.markdown("<h2 class='slideIn'>Login to PhytoSense</h2>", unsafe_allow_html=True)
    
    # Check if we need to show account created message
    if st.session_state.show_account_created:
        st.success("Account created successfully! Please login.")
        st.session_state.show_account_created = False
    
    # Create two columns for the form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                user = verify_user(username, password)
                if user:
                    st.session_state.current_user = user
                    # Get user profile if it exists
                    user_id = user['id'] if isinstance(user, dict) else user.id
                    profile = get_user_profile(user_id)
                    if profile:
                        st.session_state.user_profile = profile
                    
                    # Check if user has completed their profile
                    profile_complete = user.get('profile_complete', False) if isinstance(user, dict) else user.profile_complete
                    if profile_complete:
                        go_to_dashboard()
                    else:
                        go_to_profile_setup()
                else:
                    st.error("Invalid username or password")

        if st.button("Create Account"):
            go_to_signup()
    
    with col2:
        st.markdown("""
        <div class="fadeIn">
            <h3>Welcome to PhytoSense</h3>
            <p>The AI-powered solution for monitoring and managing plant health.</p>
            <ul>
                <li>Analyze crop diseases with our AI engine</li>
                <li>Get recommendations for improving crop health</li>
                <li>Monitor soil conditions and get customized advice</li>
                <li>Track weather patterns and receive alerts</li>
                <li>Access region-specific farming insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Signup page
def show_signup_page():
    """Display the signup page"""
    st.markdown("<h2 class='slideIn'>Create a PhytoSense Account</h2>", unsafe_allow_html=True)
    
    # Create two columns for the form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        username = st.text_input("Username (required)")
        password = st.text_input("Password (required)", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        email = st.text_input("Email (optional)")
        farm_location = st.text_input("Farm Location (optional, can be set later)")
        
        if st.button("Create Account"):
            # Validate inputs
            if not username or not password:
                st.error("Username and password are required")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                # Create user
                success, message = create_user(username, password, email, farm_location)
                if success:
                    st.session_state.show_account_created = True
                    go_to_login()
                else:
                    st.error(message)
        
        if st.button("Back to Login"):
            go_to_login()
    
    with col2:
        st.markdown("""
        <div class="fadeIn">
            <h3>Join PhytoSense</h3>
            <p>Creating an account gives you access to:</p>
            <ul>
                <li>Personalized crop recommendations</li>
                <li>Analysis history and trend tracking</li>
                <li>Region-specific agricultural advice</li>
                <li>Weather alerts for your farm location</li>
                <li>Community resources and support</li>
            </ul>
            <p><small>Your data is secure and will only be used to provide you with better recommendations.</small></p>
        </div>
        """, unsafe_allow_html=True)

# Profile setup page
def show_profile_setup_page():
    """Display the profile setup page"""
    st.markdown("<h2 class='slideIn'>Complete Your Farmer Profile</h2>", unsafe_allow_html=True)
    
    # Fetch existing profile data if available
    user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
    profile_data = get_user_profile(user_id) or {}
    
    # Create form for profile setup
    with st.form("profile_form"):
        # Personal information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=get_profile_field(profile_data, 'name'))
            
        with col2:
            farm_location = st.text_input("Farm Location", 
                                         value=get_profile_field(profile_data, 'farm_location') or 
                                         (st.session_state.current_user.get('farm_location', '') if isinstance(st.session_state.current_user, dict) else getattr(st.session_state.current_user, 'farm_location', '')))
        
        # Farm details
        st.subheader("Farm Details")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            farm_size = st.text_input("Farm Size (acres)", value=get_profile_field(profile_data, 'farm_size'))
            
        with col2:
            farming_type_options = ["Conventional", "Organic", "Mixed", "Transitioning to Organic"]
            farming_type = st.selectbox(
                "Farming Type", 
                options=farming_type_options,
                index=get_select_index(get_profile_field(profile_data, 'farming_type'), farming_type_options)
            )
            
        with col3:
            irrigation_options = ["Drip", "Sprinkler", "Flood", "Rainwater Only", "Multiple Methods"]
            irrigation = st.selectbox(
                "Irrigation Method", 
                options=irrigation_options,
                index=get_select_index(get_profile_field(profile_data, 'irrigation'), irrigation_options)
            )
        
        # Crop information
        st.subheader("Crops")
        col1, col2 = st.columns(2)
        
        with col1:
            primary_crops = st.text_input("Primary Crops (comma-separated)", value=get_profile_field(profile_data, 'primary_crops'))
            
        with col2:
            secondary_crops = st.text_input("Secondary Crops (comma-separated)", value=get_profile_field(profile_data, 'secondary_crops'))
        
        # Additional preferences
        st.subheader("Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            receive_weather_alerts = st.checkbox("Receive Weather Alerts", value=get_profile_field(profile_data, 'receive_weather_alerts', True))
            
        with col2:
            language_options = ["English", "Hindi", "Marathi", "Gujarati", "Bengali"]
            preferred_language = st.selectbox(
                "Preferred Language", 
                options=language_options,
                index=get_select_index(get_profile_field(profile_data, 'preferred_language', "English"), language_options)
            )
        
        # Submit button
        submitted = st.form_submit_button("Save Profile")
        
        if submitted:
            # Prepare profile data
            profile_data = {
                'name': name,
                'farm_location': farm_location,
                'farm_size': farm_size,
                'farming_type': farming_type,
                'irrigation': irrigation,
                'primary_crops': primary_crops,
                'secondary_crops': secondary_crops,
                'receive_weather_alerts': receive_weather_alerts,
                'preferred_language': preferred_language,
                'last_updated': datetime.now().isoformat()
            }
            
            # Update profile
            success, message = update_user_profile(user_id, profile_data)
            
            if success:
                # Update session state with new profile data
                st.session_state.user_profile = profile_data
                
                # Update current_user profile_complete status
                if isinstance(st.session_state.current_user, dict):
                    st.session_state.current_user['profile_complete'] = True
                else:
                    st.session_state.current_user.profile_complete = True
                
                st.success("Profile updated successfully!")
                
                # Redirect to dashboard
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error(f"Error updating profile: {message}")
                
    # Back button
    if st.button("Skip for Now"):
        go_to_dashboard()

# Dashboard page
def show_dashboard_page():
    """Display the main dashboard page"""
    st.markdown("<h2 class='slideIn'>Farmer Dashboard</h2>", unsafe_allow_html=True)
    
    # Get user data
    user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
    profile = st.session_state.user_profile or {}
    
    # Create dashboard layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main dashboard section
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Quick Actions")
        
        # Create action buttons in a grid layout
        action1, action2, action3 = st.columns(3)
        
        with action1:
            st.markdown("""
            <div class='tile'>
                <div class='tile-icon'>🌱</div>
                <div class='tile-title'>Test Your Crop</div>
                <p>Analyze crop health and detect diseases</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze Crop", key="dashboard_crop"):
                go_to_crop_test()
                
        with action2:
            st.markdown("""
            <div class='tile'>
                <div class='tile-icon'>🌍</div>
                <div class='tile-title'>Soil Analysis</div>
                <p>Check soil quality and get recommendations</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze Soil", key="dashboard_soil"):
                go_to_soil_analysis()
                
        with action3:
            st.markdown("""
            <div class='tile'>
                <div class='tile-icon'>☁️</div>
                <div class='tile-title'>Weather Alerts</div>
                <p>Get weather forecasts and farming alerts</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Check Weather", key="dashboard_weather"):
                go_to_weather()
        
        # Second row of actions
        action4, action5, action6 = st.columns(3)
        
        with action4:
            st.markdown("""
            <div class='tile'>
                <div class='tile-icon'>📊</div>
                <div class='tile-title'>Analysis History</div>
                <p>View previous analyses and track progress</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View History", key="dashboard_history"):
                go_to_history()
                
        with action5:
            st.markdown("""
            <div class='tile'>
                <div class='tile-icon'>📚</div>
                <div class='tile-title'>Farming Resources</div>
                <p>Access guides and best practices</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Resources", key="dashboard_resources"):
                go_to_resources()
                
        with action6:
            st.markdown("""
            <div class='tile'>
                <div class='tile-icon'>👤</div>
                <div class='tile-title'>Update Profile</div>
                <p>Manage your farmer profile settings</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Edit Profile", key="dashboard_profile"):
                go_to_profile_setup()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Recent analyses
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Recent Analyses")
        
        # Get user's analysis history
        history = get_user_analyses(user_id, limit=3)
        
        if history:
            for analysis in history:
                with st.expander(f"{analysis['analysis_type'].title()} Analysis - {analysis['timestamp'][:10]}"):
                    # Display analysis details
                    st.markdown(f"**Type:** {analysis['analysis_type'].title()}")
                    st.markdown(f"**Date:** {analysis['timestamp'][:10]}")
                    
                    # Show different details based on analysis type
                    if analysis['analysis_type'] == 'plant':
                        if 'results' in analysis and 'plant_info' in analysis['results']:
                            plant_info = analysis['results']['plant_info']
                            st.markdown(f"**Plant:** {plant_info.get('name', 'Unknown')}")
                            
                            if 'diseases' in analysis['results']:
                                diseases = analysis['results']['diseases']
                                if diseases.get('detected', False):
                                    st.markdown("**Diseases Detected:** Yes")
                                    for disease in diseases.get('diseases', []):
                                        st.markdown(f"- {disease.get('name', 'Unknown')} ({disease.get('confidence', 0):.1f}%)")
                                else:
                                    st.markdown("**Diseases Detected:** No")
                    
                    elif analysis['analysis_type'] == 'soil':
                        if 'results' in analysis and 'soil_type' in analysis['results']:
                            soil_type = analysis['results']['soil_type']
                            st.markdown(f"**Soil Type:** {soil_type}")
                            
                            if 'properties' in analysis['results']:
                                properties = analysis['results']['properties']
                                st.markdown(f"**pH:** {properties.get('ph', 'Unknown')}")
                                st.markdown(f"**Organic Matter:** {properties.get('organic_matter', 'Unknown')}")
                    
                    # View full details button
                    if st.button("View Full Details", key=f"view_{analysis['id']}"):
                        # In a real app, this would navigate to a detailed view
                        st.session_state.page = "history"
        else:
            st.info("No analyses yet. Start by analyzing your crops or soil!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Sidebar/Profile summary
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Farmer Profile")
        
        # Display profile information
        st.markdown(f"**Name:** {get_profile_field(profile, 'name', 'Not set')}")
        st.markdown(f"**Location:** {get_profile_field(profile, 'farm_location', 'Not set')}")
        st.markdown(f"**Farm Size:** {get_profile_field(profile, 'farm_size', 'Not set')} acres")
        st.markdown(f"**Farming Type:** {get_profile_field(profile, 'farming_type', 'Not set')}")
        st.markdown(f"**Primary Crops:** {get_profile_field(profile, 'primary_crops', 'Not set')}")
        
        if st.button("Edit Profile", key="sidebar_edit_profile"):
            go_to_profile_setup()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Weather widget
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        display_weather_widget()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Seasonal tips
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Seasonal Farming Tips")
        
        # Determine current season (simplified)
        now = datetime.now()
        month = now.month
        
        if 3 <= month <= 5:  # Spring (March-May)
            season = "Spring"
            tips = [
                "Prepare soil with proper tillage and fertilization",
                "Start planting summer crops by end of season",
                "Monitor for early pest emergence with warming weather",
                "Apply pre-emergent herbicides for weed control",
                "Check irrigation systems before peak water needs"
            ]
        elif 6 <= month <= 8:  # Summer (June-August)
            season = "Summer"
            tips = [
                "Ensure adequate irrigation during peak heat",
                "Monitor for heat stress in sensitive crops",
                "Apply mulch to reduce water evaporation",
                "Scout regularly for pest outbreaks",
                "Prepare for early harvest of certain crops"
            ]
        elif 9 <= month <= 11:  # Fall (September-November)
            season = "Fall"
            tips = [
                "Harvest crops at optimal maturity",
                "Test soil and add amendments as needed",
                "Plant cover crops to protect soil",
                "Clean and store equipment properly",
                "Plan crop rotation for next season"
            ]
        else:  # Winter (December-February)
            season = "Winter"
            tips = [
                "Protect sensitive plants from frost",
                "Maintain proper storage conditions for harvested crops",
                "Service and repair farm equipment",
                "Order seeds and plan for spring planting",
                "Take agricultural training courses"
            ]
        
        st.markdown(f"**Current Season: {season}**")
        for tip in tips:
            st.markdown(f"• {tip}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Crop test page
def show_crop_test_page():
    """Display the crop testing page"""
    st.markdown("<h2 class='slideIn'>Plant Health Analysis</h2>", unsafe_allow_html=True)
    
    # Create tabs for different ways to add images
    tab_upload, tab_example = st.tabs(["Upload Image", "Use Example Image"])
    
    with tab_upload:
        uploaded_file = st.file_uploader("Upload an image of your crop for analysis", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Save the uploaded image to session state
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            
            # Display the uploaded image
            st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with tab_example:
        # Show example crop images
        example_images = get_example_images()
        
        if example_images:
            # Display example images in a grid
            cols = st.columns(3)
            for i, (image_path, description) in enumerate(example_images.items()):
                with cols[i % 3]:
                    st.image(image_path, caption=description, use_column_width=True)
                    if st.button(f"Use this image", key=f"example_{i}"):
                        # Load the selected example image
                        image = Image.open(image_path)
                        st.session_state.uploaded_image = image
                        st.rerun()
        else:
            st.info("No example images available.")
    
    # Form for additional plant details
    if st.session_state.uploaded_image:
        st.markdown("### Additional Information (Optional)")
        st.markdown("Providing more details helps improve analysis accuracy.")
        
        # Create a three-column layout for form inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop_type = st.selectbox(
                "Crop Type",
                options=["Unknown", "Tomato", "Potato", "Corn", "Wheat", "Rice", "Onion", "Soybean", "Cotton"],
                index=0
            )
            
            st.session_state.plant_details["crop_type"] = None if crop_type == "Unknown" else crop_type
        
        with col2:
            plant_age = st.selectbox(
                "Plant Age",
                options=["Unknown", "Seedling", "Vegetative", "Flowering", "Fruiting", "Mature"],
                index=0
            )
            
            st.session_state.plant_details["plant_age"] = None if plant_age == "Unknown" else plant_age
        
        with col3:
            planting_date = st.date_input(
                "Planting Date",
                value=None
            )
            
            st.session_state.plant_details["planting_date"] = planting_date.isoformat() if planting_date else None
        
        col1, col2 = st.columns(2)
        
        with col1:
            symptoms = st.text_area(
                "Visible Symptoms",
                placeholder="Describe any visible symptoms (e.g., yellow leaves, spots, wilting)"
            )
            
            st.session_state.plant_details["symptoms"] = symptoms if symptoms else None
        
        with col2:
            irrigation_method = st.selectbox(
                "Irrigation Method",
                options=["Unknown", "Drip", "Sprinkler", "Flood", "Rainwater Only", "None"],
                index=0
            )
            
            st.session_state.plant_details["irrigation_method"] = None if irrigation_method == "Unknown" else irrigation_method
            
            previous_treatments = st.text_area(
                "Previous Treatments",
                placeholder="List any treatments already applied"
            )
            
            st.session_state.plant_details["previous_treatments"] = previous_treatments if previous_treatments else None
        
        # Analyze button
        if st.button("Analyze Plant Health", key="analyze_plant_btn"):
            if st.session_state.uploaded_image:
                with st.spinner("Analyzing image... Please wait"):
                    # Preprocess the image
                    image = st.session_state.uploaded_image
                    processed_image = preprocess_image(image)
                    st.session_state.processed_image = processed_image
                    
                    # Perform analysis
                    if st.session_state.plant_details["crop_type"]:
                        # Use enhanced analysis for known crop types
                        results = enhanced_analysis(image, st.session_state.plant_details["crop_type"])
                    else:
                        # First identify the plant
                        plant_info = identify_plant(processed_image)
                        
                        # Then perform other analyses
                        water_content = detect_water_content(processed_image)
                        diseases = detect_diseases(processed_image, plant_info["name"])
                        pests = detect_pests(processed_image)
                        
                        # Extract features for visualization
                        features = extract_features(processed_image)
                        
                        # Get local recommendations
                        local_recommendations = get_local_recommendations(plant_info["name"])
                        
                        # Combine results
                        results = {
                            "plant_info": plant_info,
                            "water_content": water_content,
                            "diseases": diseases,
                            "pests": pests,
                            "features": features,
                            "local_recommendations": local_recommendations
                        }
                    
                    # Get preventive measures and fertilizer recommendations
                    preventive_measures = get_preventive_measures(
                        results["plant_info"]["name"], 
                        results["diseases"], 
                        results["pests"]
                    )
                    
                    fertilizer_recommendations = get_fertilizer_recommendations(
                        results["plant_info"]["name"], 
                        soil_type=None  # In a real app, this would come from soil analysis
                    )
                    
                    # Update session state with results
                    st.session_state.analysis_results = results
                    st.session_state.plant_info = results["plant_info"]
                    st.session_state.water_content = results["water_content"]
                    st.session_state.diseases = results["diseases"]
                    st.session_state.pests = results["pests"]
                    st.session_state.preventive_measures = preventive_measures
                    st.session_state.fertilizer_recommendations = fertilizer_recommendations
                    st.session_state.analysis_complete = True
                    
                    # Save results to history
                    save_to_history("plant", {
                        "plant_info": results["plant_info"],
                        "water_content": results["water_content"],
                        "diseases": results["diseases"],
                        "pests": results["pests"],
                        "preventive_measures": preventive_measures,
                        "fertilizer_recommendations": fertilizer_recommendations,
                        "plant_details": st.session_state.plant_details
                    })
                
                # Force a rerun to show results
                st.rerun()
    
    # Display analysis results
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        st.markdown("---")
        st.markdown("<h2 class='fadeIn'>Analysis Results</h2>", unsafe_allow_html=True)
        
        results = st.session_state.analysis_results
        
        # Create columns for results
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Display the processed image
            if st.session_state.processed_image is not None:
                st.image(st.session_state.processed_image, caption="Processed Image", use_column_width=True)
            else:
                st.image(st.session_state.uploaded_image, caption="Uploaded Image", use_column_width=True)
            
            # Plant identification result
            st.markdown("### Plant Identification")
            plant_info = results["plant_info"]
            st.markdown(f"**Detected Plant:** {plant_info['name']}")
            if "scientific_name" in plant_info and plant_info["scientific_name"]:
                st.markdown(f"**Scientific Name:** {plant_info['scientific_name']}")
            st.markdown(f"**Confidence:** {format_probability(plant_info['probability'])}%")
            
            # Water content
            st.markdown("### Water Content")
            water_content = results["water_content"]
            
            # Use different status classes based on water content
            if water_content["status"] == "Optimal":
                status_class = "status-healthy"
            elif water_content["status"] == "Low":
                status_class = "status-warning"
            elif water_content["status"] == "Critical":
                status_class = "status-danger"
            else:
                status_class = ""
                
            st.markdown(f"**Status:** <span class='{status_class}'>{water_content['status']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Estimated Water Content:** {water_content['percentage']}%")
            
            # Local recommendations
            if "local_recommendations" in results:
                st.markdown("### Maharashtra-Specific Advice")
                local_recommendations = results["local_recommendations"]
                
                if local_recommendations:
                    if "seasonal" in local_recommendations:
                        st.markdown(f"**Seasonal Recommendation:** {local_recommendations['seasonal']}")
                    
                    if "irrigation" in local_recommendations:
                        st.markdown(f"**Irrigation Advice:** {local_recommendations['irrigation']}")
                        
                    if "practices" in local_recommendations:
                        st.markdown("**Recommended Practices:**")
                        for practice in local_recommendations["practices"]:
                            st.markdown(f"- {practice}")
                else:
                    st.info("No region-specific recommendations available for this crop.")
        
        with col2:
            # Disease detection
            st.markdown("### Disease Detection")
            diseases = results["diseases"]
            
            if diseases["detected"]:
                for disease in diseases["diseases"]:
                    # Create a card-like container for each disease
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    
                    # Determine status class based on confidence
                    confidence = disease["confidence"]
                    if confidence > 80:
                        status_class = "status-danger"
                    elif confidence > 60:
                        status_class = "status-warning"
                    else:
                        status_class = ""
                    
                    st.markdown(f"<div class='result-header'><div class='result-icon'>🔬</div><h4 class='result-title'>{disease['name']}</h4></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-content'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Confidence:</strong> <span class='{status_class}'>{format_probability(confidence)}%</span></p>", unsafe_allow_html=True)
                    
                    if "description" in disease:
                        st.markdown(f"<p><strong>Description:</strong> {disease['description']}</p>", unsafe_allow_html=True)
                    
                    if "treatment" in disease:
                        st.markdown(f"<p><strong>Treatment:</strong> {disease['treatment']}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown("<p><span class='status-healthy'>No diseases detected.</span> The plant appears healthy.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Pest detection
            st.markdown("### Pest Detection")
            pests = results["pests"]
            
            if pests["detected"]:
                for pest in pests["pests"]:
                    # Create a card-like container for each pest
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    
                    # Determine status class based on infestation level
                    level = pest["infestation_level"]
                    if level == "High":
                        status_class = "status-danger"
                    elif level == "Medium":
                        status_class = "status-warning"
                    else:
                        status_class = ""
                    
                    st.markdown(f"<div class='result-header'><div class='result-icon'>🐞</div><h4 class='result-title'>{pest['name']}</h4></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-content'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Infestation Level:</strong> <span class='{status_class}'>{level}</span></p>", unsafe_allow_html=True)
                    
                    if "description" in pest:
                        st.markdown(f"<p><strong>Description:</strong> {pest['description']}</p>", unsafe_allow_html=True)
                    
                    if "treatment" in pest:
                        st.markdown(f"<p><strong>Treatment:</strong> {pest['treatment']}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown("<p><span class='status-healthy'>No pests detected.</span> The plant appears pest-free.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Recommendations section
        st.markdown("---")
        st.markdown("## Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Preventive measures
            st.markdown("### Preventive Measures")
            if st.session_state.preventive_measures:
                for measure in st.session_state.preventive_measures:
                    st.markdown(f"- {measure}")
            else:
                st.info("No specific preventive measures available.")
        
        with col2:
            # Fertilizer recommendations
            st.markdown("### Fertilizer Recommendations")
            if st.session_state.fertilizer_recommendations:
                for recommendation in st.session_state.fertilizer_recommendations:
                    st.markdown(f"- {recommendation}")
            else:
                st.info("No specific fertilizer recommendations available.")
        
        # Generate report button
        if st.button("Generate Detailed Report"):
            report_md = generate_report_markdown(
                plant_info=results["plant_info"],
                water_content=results["water_content"],
                diseases=results["diseases"],
                pests=results["pests"],
                preventive_measures=st.session_state.preventive_measures,
                fertilizer_recommendations=st.session_state.fertilizer_recommendations,
                local_recommendations=results.get("local_recommendations", {}),
                plant_details=st.session_state.plant_details
            )
            
            # Convert markdown to PDF (in a real app) or just display
            st.markdown("### Plant Health Report")
            st.markdown(report_md)
            
            # In a real app, we'd offer a download link here
            st.download_button(
                label="Download Report",
                data=report_md,
                file_name=f"plant_health_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

# Soil analysis page
def show_soil_analysis_page():
    """Display the soil analysis page"""
    st.markdown("<h2 class='slideIn'>Soil Analysis</h2>", unsafe_allow_html=True)
    
    # Create tabs for different ways to add images
    tab_upload, tab_example = st.tabs(["Upload Image", "Use Example Image"])
    
    with tab_upload:
        uploaded_file = st.file_uploader("Upload an image of your soil for analysis", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Save the uploaded image to session state
            image = Image.open(uploaded_file)
            st.session_state.uploaded_soil_image = image
            
            # Display the uploaded image
            st.image(image, caption="Uploaded Soil Image", use_column_width=True)
    
    with tab_example:
        # Show example soil images
        # In a real app, these would be loaded from a directory
        example_soil_images = {
            "assets/examples/soil1.jpg": "Black Soil Sample",
            "assets/examples/soil2.jpg": "Red Soil Sample",
            "assets/examples/soil3.jpg": "Sandy Soil Sample",
        }
        
        # Display example images in a grid
        cols = st.columns(3)
        for i, (image_path, description) in enumerate(example_soil_images.items()):
            with cols[i % 3]:
                # Create a placeholder for the image
                st.markdown(f"### {description}")
                st.markdown(f"<div style='background-color: #{'000000' if 'Black' in description else 'A52A2A' if 'Red' in description else 'F4A460'};height:150px;border-radius:10px;'></div>", unsafe_allow_html=True)
                if st.button(f"Use this sample", key=f"soil_example_{i}"):
                    # Create a dummy image with the right color
                    if "Black" in description:
                        color = (50, 50, 50)
                    elif "Red" in description:
                        color = (165, 42, 42)
                    else:  # Sandy
                        color = (244, 164, 96)
                    
                    # Create a solid color image
                    image = Image.new('RGB', (300, 200), color)
                    st.session_state.uploaded_soil_image = image
                    st.rerun()
    
    # Form for additional soil details
    if st.session_state.uploaded_soil_image:
        st.markdown("### Additional Information (Optional)")
        st.markdown("Providing more details helps improve analysis accuracy.")
        
        # Create a three-column layout for form inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            soil_depth = st.selectbox(
                "Soil Depth",
                options=["Surface (0-10cm)", "Subsurface (10-30cm)", "Deep (30cm+)", "Unknown"],
                index=0
            )
        
        with col2:
            recent_rainfall = st.selectbox(
                "Recent Rainfall",
                options=["None", "Light", "Moderate", "Heavy", "Unknown"],
                index=0
            )
        
        with col3:
            sampling_location = st.text_input(
                "Sampling Location",
                placeholder="Field name or coordinates"
            )
        
        # Analyze button
        if st.button("Analyze Soil", key="analyze_soil_btn"):
            if st.session_state.uploaded_soil_image:
                with st.spinner("Analyzing soil... Please wait"):
                    # Preprocess the image
                    image = st.session_state.uploaded_soil_image
                    preprocessed_soil_image = preprocess_image(image)
                    
                    # In a real app, we'd use a proper ML model here
                    # For demo, we're using the simplified soil analyzer
                    soil_model = None  # Placeholder - would be loaded from a file
                    soil_results = analyze_soil(soil_model, np.array(preprocessed_soil_image))
                    
                    # Update session state
                    st.session_state.soil_results = soil_results
                    st.session_state.soil_analysis_complete = True
                    
                    # Save to history
                    save_to_history("soil", soil_results)
                
                # Force a rerun to show results
                st.rerun()
    
    # Display soil analysis results
    if st.session_state.soil_analysis_complete and st.session_state.soil_results:
        st.markdown("---")
        st.markdown("<h2 class='fadeIn'>Soil Analysis Results</h2>", unsafe_allow_html=True)
        
        soil_results = st.session_state.soil_results
        
        # Create columns for results display
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display the soil image
            if st.session_state.uploaded_soil_image is not None:
                st.image(st.session_state.uploaded_soil_image, caption="Soil Sample", use_column_width=True)
            
            # Soil type and characteristics
            st.markdown("### Soil Classification")
            soil_type = list(soil_results.keys())[0]  # Get the soil type (key of the dict)
            st.markdown(f"**Identified Soil Type:** {soil_type}")
            
            # Display soil properties
            st.markdown("### Soil Properties")
            properties = soil_results[soil_type]["properties"]
            
            # Create a two-column layout for properties
            prop_col1, prop_col2 = st.columns(2)
            
            with prop_col1:
                st.markdown(f"**pH Value:** {properties['ph']}")
                st.markdown(f"**Organic Matter:** {properties['organic_matter']}")
            
            with prop_col2:
                st.markdown(f"**Drainage:** {properties['drainage']}")
        
        with col2:
            # Soil characteristics
            st.markdown("### Characteristics")
            characteristics = soil_results[soil_type]["characteristics"]
            st.markdown(characteristics)
            
            # Crop suitability
            st.markdown("### Crop Suitability")
            suitability = soil_results[soil_type]["suitability"]
            
            for crop, suitability_text in suitability.items():
                st.markdown(f"**{crop.title()}:** {suitability_text}")
            
            # Recommendations
            st.markdown("### Recommendations")
            recommendations = soil_results[soil_type]["recommendations"]
            st.markdown(recommendations)
        
        # Visualize soil properties
        st.markdown("---")
        st.markdown("## Soil Analysis Visualization")
        
        # Create a simple visualization of soil properties
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Parse pH value (assuming it's a string like "7.5")
        try:
            ph_value = float(properties['ph'])
        except ValueError:
            ph_value = 7.0  # Default
        
        # Create pH scale visualization
        ph_range = np.linspace(4, 10, 100)
        colors = []
        
        for ph in ph_range:
            if ph < 5.5:  # Acidic
                colors.append('#FF6B6B')  # Red
            elif ph < 6.5:  # Slightly acidic
                colors.append('#FFD166')  # Yellow
            elif ph < 7.5:  # Neutral
                colors.append('#06D6A0')  # Green
            elif ph < 8.5:  # Slightly alkaline
                colors.append('#118AB2')  # Blue
            else:  # Alkaline
                colors.append('#073B4C')  # Dark blue
        
        # Plot the pH scale
        ax.scatter(ph_range, [1] * len(ph_range), c=colors, s=100, marker='|')
        
        # Highlight the soil's pH value
        ax.scatter(ph_value, 1, c='red', s=300, marker='v', zorder=5)
        
        # Add labels
        ax.text(4.5, 1.05, "Acidic", fontsize=10, ha='center')
        ax.text(6.0, 1.05, "Slightly Acidic", fontsize=10, ha='center')
        ax.text(7.0, 1.05, "Neutral", fontsize=10, ha='center')
        ax.text(8.0, 1.05, "Slightly Alkaline", fontsize=10, ha='center')
        ax.text(9.5, 1.05, "Alkaline", fontsize=10, ha='center')
        
        # Customize the plot
        ax.set_xlim(4, 10)
        ax.set_ylim(0.9, 1.1)
        ax.set_xlabel('pH Scale')
        ax.set_title(f'Soil pH Analysis: {ph_value} ({properties["ph"]})')
        ax.get_yaxis().set_visible(False)
        
        # Show the plot
        st.pyplot(fig)
        
        # Additional information
        st.markdown("### Optimal pH Range for Common Crops")
        
        # Create a simple table for optimal pH ranges
        ph_data = {
            'Crop': ['Tomato', 'Potato', 'Wheat', 'Rice', 'Corn', 'Cotton', 'Soybean', 'Onion'],
            'Optimal pH Range': ['6.0-6.8', '5.0-6.5', '6.0-7.0', '5.5-7.0', '5.8-7.0', '5.8-8.0', '6.0-7.0', '6.0-7.0']
        }
        
        # Display as columns
        crop_cols = st.columns(4)
        for i in range(len(ph_data['Crop'])):
            with crop_cols[i % 4]:
                st.markdown(f"**{ph_data['Crop'][i]}:** {ph_data['Optimal pH Range'][i]}")
        
        # Generate report button
        if st.button("Generate Detailed Soil Report"):
            # In a real app, we'd generate a proper PDF report
            # For now, we'll just create a formatted markdown report
            
            report_md = f"""
            # Soil Analysis Report
            
            ## Soil Classification
            - **Identified Soil Type:** {soil_type}
            
            ## Soil Properties
            - **pH Value:** {properties['ph']}
            - **Organic Matter:** {properties['organic_matter']}
            - **Drainage:** {properties['drainage']}
            
            ## Characteristics
            {characteristics}
            
            ## Crop Suitability
            """
            
            for crop, suitability_text in suitability.items():
                report_md += f"- **{crop.title()}:** {suitability_text}\n"
            
            report_md += f"""
            ## Recommendations
            {recommendations}
            
            ## Date of Analysis
            {datetime.now().strftime('%Y-%m-%d %H:%M')}
            """
            
            st.markdown("### Soil Analysis Report")
            st.markdown(report_md)
            
            # Offer report download
            st.download_button(
                label="Download Report",
                data=report_md,
                file_name=f"soil_analysis_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

# History page
def show_history_page():
    """Display the user's analysis history"""
    st.markdown("<h2 class='slideIn'>Analysis History</h2>", unsafe_allow_html=True)
    
    # Get user ID
    user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
    
    # Get user's analysis history
    history = get_user_analyses(user_id, limit=50)  # Get up to 50 analyses
    
    if not history:
        st.info("No analysis history found. Start by analyzing your crops or soil!")
        return
    
    # Create filter options
    st.markdown("### Filter Results")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_types = ["All Types"] + list(set(a["analysis_type"] for a in history))
        selected_type = st.selectbox("Analysis Type", options=analysis_types)
    
    with col2:
        # Extract all dates (YYYY-MM-DD) from timestamps
        dates = ["All Dates"] + sorted(list(set(a["timestamp"][:10] for a in history)), reverse=True)
        selected_date = st.selectbox("Date", options=dates)
    
    with col3:
        # For plant analyses, get list of plants
        plant_types = ["All Plants"]
        for a in history:
            if a["analysis_type"] == "plant" and "results" in a and "plant_info" in a["results"]:
                plant_name = a["results"]["plant_info"].get("name", "Unknown")
                if plant_name not in plant_types:
                    plant_types.append(plant_name)
        
        selected_plant = st.selectbox("Plant Type", options=plant_types)
    
    # Filter history based on selections
    filtered_history = history
    
    if selected_type != "All Types":
        filtered_history = [a for a in filtered_history if a["analysis_type"] == selected_type]
    
    if selected_date != "All Dates":
        filtered_history = [a for a in filtered_history if a["timestamp"][:10] == selected_date]
    
    if selected_plant != "All Plants":
        filtered_history = [a for a in filtered_history if a["analysis_type"] == "plant" and 
                          "results" in a and 
                          "plant_info" in a["results"] and 
                          a["results"]["plant_info"].get("name") == selected_plant]
    
    # Display filtered history
    st.markdown(f"### Results ({len(filtered_history)} analyses)")
    
    if not filtered_history:
        st.info("No analyses match your filter criteria.")
        return
    
    # Create tabs for different view types
    tab1, tab2 = st.tabs(["List View", "Detail View"])
    
    with tab1:
        # Simple list view
        for i, analysis in enumerate(filtered_history):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if analysis["analysis_type"] == "plant":
                    icon = "🌱"
                    title = "Plant Health Analysis"
                    if "results" in analysis and "plant_info" in analysis["results"]:
                        subtitle = f"Plant: {analysis['results']['plant_info'].get('name', 'Unknown')}"
                    else:
                        subtitle = "Plant analysis"
                elif analysis["analysis_type"] == "soil":
                    icon = "🌍"
                    title = "Soil Analysis"
                    if "results" in analysis and "soil_type" in analysis["results"]:
                        subtitle = f"Soil: {analysis['results']['soil_type']}"
                    else:
                        subtitle = "Soil analysis"
                else:
                    icon = "📋"
                    title = f"{analysis['analysis_type'].title()} Analysis"
                    subtitle = ""
                
                st.markdown(f"**{i+1}. {icon} {title}** - {analysis['timestamp'][:10]}")
                st.markdown(f"{subtitle}")
            
            with col2:
                if st.button("View Details", key=f"view_details_{i}"):
                    # Set selected analysis for detail view
                    st.session_state.selected_analysis = analysis
                    # Switch to detail view tab
                    st.session_state.history_view_tab = "Detail View"
                    st.rerun()
    
    with tab2:
        # Detail view of selected analysis
        if "selected_analysis" in st.session_state:
            analysis = st.session_state.selected_analysis
            
            # Display analysis details based on type
            if analysis["analysis_type"] == "plant":
                st.markdown(f"## Plant Health Analysis - {analysis['timestamp'][:10]}")
                
                # Get results
                results = analysis.get("results", {})
                plant_info = results.get("plant_info", {})
                diseases = results.get("diseases", {})
                pests = results.get("pests", {})
                
                # Display image if available
                if "image_path" in analysis and analysis["image_path"]:
                    try:
                        image = Image.open(analysis["image_path"])
                        st.image(image, caption="Plant Image", width=300)
                    except Exception as e:
                        st.error(f"Could not load image: {e}")
                
                # Create columns for information display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Plant Information")
                    st.markdown(f"**Plant:** {plant_info.get('name', 'Unknown')}")
                    if "scientific_name" in plant_info and plant_info["scientific_name"]:
                        st.markdown(f"**Scientific Name:** {plant_info['scientific_name']}")
                    st.markdown(f"**Confidence:** {format_probability(plant_info.get('probability', 0))}%")
                    
                    if "water_content" in results:
                        water_content = results["water_content"]
                        st.markdown("### Water Content")
                        st.markdown(f"**Status:** {water_content.get('status', 'Unknown')}")
                        st.markdown(f"**Percentage:** {water_content.get('percentage', 'Unknown')}%")
                
                with col2:
                    st.markdown("### Disease & Pest Information")
                    
                    if diseases.get("detected", False):
                        st.markdown("**Diseases Detected:** Yes")
                        for disease in diseases.get("diseases", []):
                            st.markdown(f"- {disease.get('name', 'Unknown')} ({format_probability(disease.get('confidence', 0))}%)")
                    else:
                        st.markdown("**Diseases Detected:** No")
                    
                    if pests.get("detected", False):
                        st.markdown("**Pests Detected:** Yes")
                        for pest in pests.get("pests", []):
                            st.markdown(f"- {pest.get('name', 'Unknown')} (Level: {pest.get('infestation_level', 'Unknown')})")
                    else:
                        st.markdown("**Pests Detected:** No")
                
                # Recommendations
                st.markdown("### Recommendations")
                
                if "preventive_measures" in results:
                    st.markdown("**Preventive Measures:**")
                    for measure in results["preventive_measures"]:
                        st.markdown(f"- {measure}")
                
                if "fertilizer_recommendations" in results:
                    st.markdown("**Fertilizer Recommendations:**")
                    for recommendation in results["fertilizer_recommendations"]:
                        st.markdown(f"- {recommendation}")
            
            elif analysis["analysis_type"] == "soil":
                st.markdown(f"## Soil Analysis - {analysis['timestamp'][:10]}")
                
                # Get results
                soil_results = analysis.get("results", {})
                
                # Display image if available
                if "image_path" in analysis and analysis["image_path"]:
                    try:
                        image = Image.open(analysis["image_path"])
                        st.image(image, caption="Soil Sample", width=300)
                    except Exception as e:
                        st.error(f"Could not load image: {e}")
                
                # Soil type
                if "soil_type" in soil_results:
                    soil_type = soil_results["soil_type"]
                    st.markdown(f"### Soil Type: {soil_type}")
                    
                    # Soil properties
                    if "properties" in soil_results:
                        properties = soil_results["properties"]
                        st.markdown("### Properties")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"**pH:** {properties.get('ph', 'Unknown')}")
                        
                        with col2:
                            st.markdown(f"**Organic Matter:** {properties.get('organic_matter', 'Unknown')}")
                        
                        with col3:
                            st.markdown(f"**Drainage:** {properties.get('drainage', 'Unknown')}")
                    
                    # Soil characteristics
                    if "characteristics" in soil_results:
                        st.markdown("### Characteristics")
                        st.markdown(soil_results["characteristics"])
                    
                    # Crop suitability
                    if "suitability" in soil_results:
                        st.markdown("### Crop Suitability")
                        for crop, suitability in soil_results["suitability"].items():
                            st.markdown(f"**{crop.title()}:** {suitability}")
                    
                    # Recommendations
                    if "recommendations" in soil_results:
                        st.markdown("### Recommendations")
                        st.markdown(soil_results["recommendations"])
            
            # Generate report button
            if st.button("Generate Report"):
                # Placeholder for report generation
                if analysis["analysis_type"] == "plant":
                    report_md = generate_report_markdown(
                        plant_info=analysis.get("results", {}).get("plant_info", {}),
                        water_content=analysis.get("results", {}).get("water_content", {}),
                        diseases=analysis.get("results", {}).get("diseases", {}),
                        pests=analysis.get("results", {}).get("pests", {}),
                        preventive_measures=analysis.get("results", {}).get("preventive_measures", []),
                        fertilizer_recommendations=analysis.get("results", {}).get("fertilizer_recommendations", []),
                        local_recommendations=analysis.get("results", {}).get("local_recommendations", {}),
                        plant_details=analysis.get("results", {}).get("plant_details", {})
                    )
                    
                    st.download_button(
                        label="Download Plant Report",
                        data=report_md,
                        file_name=f"plant_report_{analysis['timestamp'][:10]}.md",
                        mime="text/markdown"
                    )
                elif analysis["analysis_type"] == "soil":
                    # Create soil report
                    soil_results = analysis.get("results", {})
                    soil_type = soil_results.get("soil_type", "Unknown")
                    
                    report_md = f"""
                    # Soil Analysis Report
                    
                    ## Analysis Date: {analysis['timestamp'][:10]}
                    
                    ## Soil Classification
                    - **Identified Soil Type:** {soil_type}
                    
                    ## Soil Properties
                    """
                    
                    if "properties" in soil_results:
                        properties = soil_results["properties"]
                        report_md += f"- **pH Value:** {properties.get('ph', 'Unknown')}\n"
                        report_md += f"- **Organic Matter:** {properties.get('organic_matter', 'Unknown')}\n"
                        report_md += f"- **Drainage:** {properties.get('drainage', 'Unknown')}\n"
                    
                    if "characteristics" in soil_results:
                        report_md += f"\n## Characteristics\n{soil_results['characteristics']}\n"
                    
                    if "suitability" in soil_results:
                        report_md += "\n## Crop Suitability\n"
                        for crop, suitability in soil_results["suitability"].items():
                            report_md += f"- **{crop.title()}:** {suitability}\n"
                    
                    if "recommendations" in soil_results:
                        report_md += f"\n## Recommendations\n{soil_results['recommendations']}\n"
                    
                    st.download_button(
                        label="Download Soil Report",
                        data=report_md,
                        file_name=f"soil_report_{analysis['timestamp'][:10]}.md",
                        mime="text/markdown"
                    )
        else:
            st.info("Select an analysis from the list view to see details.")

# Resources page (placeholder - would be implemented with actual resources)
def show_resources_page():
    """Display agricultural resources and guides"""
    st.markdown("<h2 class='slideIn'>Agricultural Resources</h2>", unsafe_allow_html=True)
    
    # Resource types tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Guides", "Best Practices", "Local Resources", "Videos"])
    
    with tab1:
        st.markdown("### Farming Guides")
        
        # Create expandable sections for different guides
        with st.expander("Crop Rotation Guide"):
            st.markdown("""
            # Crop Rotation Guide
            
            Crop rotation is the practice of growing different types of crops in the same area across a sequence of growing seasons. It reduces reliance on one set of nutrients, pest and weed pressure, and the probability of developing resistant pests and weeds.
            
            ## Benefits of Crop Rotation
            
            - **Improved soil structure** through different root structures working the soil
            - **Enhanced soil fertility** with legumes adding nitrogen
            - **Reduced pest pressure** by breaking pest cycles
            - **Improved weed control** through varying control methods
            - **Increased biodiversity** on your farm
            
            ## Simple Crop Rotation Plan (4-Year)
            
            1. **Year 1: Leafy Crops** (lettuce, spinach, cabbage)
            2. **Year 2: Fruit Crops** (tomatoes, peppers, eggplant)
            3. **Year 3: Root Crops** (carrots, onions, garlic)
            4. **Year 4: Legumes** (beans, peas, lentils)
            
            ## Maharashtra-Specific Rotations
            
            | Previous Crop | Suitable Following Crops |
            |---------------|--------------------------|
            | Cotton        | Groundnut, Pulses, Millet |
            | Rice          | Pulses, Vegetables, Oilseeds |
            | Sugarcane     | Soybean, Pulses, Vegetables |
            | Sorghum       | Legumes, Oilseeds |
            | Wheat         | Green manure, Legumes, Oilseeds |
            """)
        
        with st.expander("Integrated Pest Management (IPM) Guide"):
            st.markdown("""
            # Integrated Pest Management Guide
            
            IPM is an ecosystem-based strategy that focuses on long-term prevention of pests through a combination of techniques such as biological control, habitat manipulation, and resistant crop varieties.
            
            ## IPM Steps
            
            1. **Identify and Monitor Pests**: Know your enemy before taking action
            2. **Set Action Thresholds**: Determine at what point pest control action is necessary
            3. **Prevention**: Implement cultural practices to prevent pest problems
            4. **Control**: Use appropriate control methods starting with least risky options
            
            ## Natural Pest Control Methods
            
            | Pest Type | Natural Controls |
            |-----------|------------------|
            | Aphids    | Ladybugs, lacewings, neem oil spray |
            | Caterpillars | Bacillus thuringiensis (Bt), encourage birds |
            | Mites     | Predatory mites, sulfur dust |
            | Fungal diseases | Proper spacing, morning watering, neem oil |
            
            ## Maharashtra-Specific Pest Pressures
            
            - **Cotton**: Pink bollworm - Use pheromone traps, early plowing after harvest
            - **Rice**: Brown planthopper - Use resistant varieties, maintain water levels
            - **Sugarcane**: Pyrilla - Release Epiricania parasites, avoid excess nitrogen
            - **Vegetables**: Fruit flies - Use traps with methyl eugenol
            """)
        
        with st.expander("Water Conservation Techniques"):
            st.markdown("""
            # Water Conservation Techniques for Farmers
            
            Water conservation is especially important in regions with limited rainfall or drought conditions. Implementing efficient water management practices helps maintain crop productivity while conserving this precious resource.
            
            ## Irrigation Methods
            
            | Method | Efficiency | Best For |
            |--------|------------|----------|
            | Drip irrigation | 90% | Row crops, trees, vines |
            | Micro-sprinklers | 80-85% | Tree crops, berries |
            | Furrow irrigation | 60-80% | Row crops, heavy soils |
            | Flood irrigation | 40-50% | Rice, heavy soils |
            
            ## Conservation Practices
            
            1. **Mulching**: Apply 2-3 inches of organic mulch to reduce evaporation by 25-50%
            2. **Soil Management**: Add organic matter to increase water-holding capacity
            3. **Timing**: Irrigate early morning or evening to reduce evaporation
            4. **Weather Monitoring**: Use weather data to optimize irrigation scheduling
            5. **Rainwater Harvesting**: Capture rainwater in ponds or tanks for later use
            
            ## Maharashtra Drought Mitigation
            
            - Construction of farm ponds (5mx5mx3m) can provide critical irrigation during dry spells
            - Contour bunding on sloped lands to prevent runoff and erosion
            - Watershed development programs have shown 30-60% increase in water availability
            """)
        
        with st.expander("Soil Health Management"):
            st.markdown("""
            # Soil Health Management
            
            Healthy soil is the foundation of productive farming. Managing soil health involves maintaining soil physical, chemical, and biological properties for optimal plant growth.
            
            ## Key Soil Health Principles
            
            1. **Minimize Disturbance**: Reduce tillage to protect soil structure
            2. **Maximize Soil Cover**: Keep living plants or residue on soil
            3. **Maximize Biodiversity**: Use diverse crop rotations and cover crops
            4. **Maximize Living Roots**: Keep living roots in soil as long as possible
            
            ## Soil Amendments
            
            | Amendment | Benefits | Application Rate |
            |-----------|----------|------------------|
            | Compost | Improves structure, adds nutrients | 5-10 tons/ha |
            | Vermicompost | Rich in microbes, balanced nutrients | 2.5-5 tons/ha |
            | Green manure | Adds nitrogen, improves biology | Plant 45-60 days before main crop |
            | Biochar | Carbon sequestration, water retention | 5-10 tons/ha |
            
            ## Maharashtra Soil Types and Management
            
            - **Black cotton soil (Regur)**: Add gypsum (500 kg/ha) to improve structure
            - **Red soil**: Add organic matter and maintain neutral pH
            - **Lateritic soil**: Focus on pH correction with lime and adding organic matter
            """)
    
    with tab2:
        st.markdown("### Best Practices")
        
        # Seasonal best practices
        st.markdown("#### Seasonal Best Practices")
        
        # Determine current season (simplified)
        now = datetime.now()
        month = now.month
        
        if 3 <= month <= 5:  # Spring (March-May)
            season = "Spring"
        elif 6 <= month <= 8:  # Summer (June-August)
            season = "Summer"
        elif 9 <= month <= 11:  # Fall (September-November)
            season = "Fall"
        else:  # Winter (December-February)
            season = "Winter"
        
        # Display practices for current season
        st.markdown(f"**Current Season: {season}**")
        
        with st.expander(f"{season} Best Practices"):
            if season == "Spring":
                st.markdown("""
                ## Spring Best Practices (March-May)
                
                ### Field Preparation
                - Complete soil testing 30-45 days before planting
                - Apply recommended amendments based on soil test results
                - Perform primary and secondary tillage operations
                - Clean irrigation channels and check pumping equipment
                
                ### Planting
                - Select appropriate varieties for your region
                - Treat seeds with fungicides and bio-agents
                - Ensure proper seed rate and spacing
                - Plant when soil temperature reaches optimal level
                
                ### Irrigation
                - Pre-irrigation 10-15 days before sowing
                - Light but frequent irrigation for young seedlings
                - Monitor soil moisture regularly
                
                ### Pest & Disease Management
                - Set up monitoring systems (sticky traps, pheromone traps)
                - Scout fields weekly for early pest detection
                - Apply preventive measures before pest pressure builds up
                
                ### Other Activities
                - Prepare nurseries for transplanted crops
                - Clean and repair farm equipment and tools
                - Plan your season's crop layout and rotation
                """)
            elif season == "Summer":
                st.markdown("""
                ## Summer Best Practices (June-August)
                
                ### Crop Management
                - Apply mulch to reduce water evaporation and suppress weeds
                - Provide shade for sensitive crops during extreme heat
                - Increase irrigation frequency but maintain appropriate volume
                - Implement trellising/staking systems for vine crops
                
                ### Pest & Disease Management
                - Scout fields twice weekly during peak pest season
                - Watch for fungal diseases during humid conditions
                - Use biological controls whenever possible
                - Apply pesticides in evening hours for better efficacy
                
                ### Irrigation
                - Irrigate during early morning or evening to reduce evaporation
                - Practice deficit irrigation during critical growth stages
                - Monitor for signs of water stress even with regular irrigation
                - Consider temporary shade structures for sensitive crops
                
                ### Soil Management
                - Apply side dressing of nutrients for long-season crops
                - Protect soil from erosion during heavy monsoon rains
                - Maintain drainage channels to prevent waterlogging
                
                ### Other Activities
                - Prepare for harvest of early season crops
                - Begin planning for fall planting
                - Maintain records of all farming activities
                """)
            elif season == "Fall":
                st.markdown("""
                ## Fall Best Practices (September-November)
                
                ### Harvest Management
                - Harvest crops at optimal maturity for best quality
                - Ensure proper drying and storage of harvested crops
                - Clean and sanitize storage facilities before use
                - Grade and sort produce for better market prices
                
                ### Field Preparation
                - Collect and analyze soil samples after harvest
                - Plant cover crops in harvested fields
                - Incorporate crop residues to add organic matter
                - Apply lime if needed (based on soil test results)
                
                ### Planting (Rabi Crops)
                - Select appropriate varieties for winter growing conditions
                - Plant at recommended depth and spacing
                - Provide irrigation immediately after planting if soil is dry
                
                ### Pest & Disease Management
                - Clean up crop residues that may harbor pests
                - Apply preventive measures for winter pests
                - Monitor stored crops regularly for pest issues
                
                ### Other Activities
                - Service irrigation systems before winter
                - Review the season's records and plan improvements
                - Attend agricultural training programs during off-season
                """)
            else:  # Winter
                st.markdown("""
                ## Winter Best Practices (December-February)
                
                ### Crop Management
                - Protect sensitive crops from frost with covers or smoke
                - Provide windbreaks for vulnerable fields
                - Adjust irrigation timing to warmer parts of the day
                - Apply recommended winter fertilization
                
                ### Pest & Disease Management
                - Monitor for rodent activity in fields and storage
                - Check dormant trees for scale insects and apply dormant oil
                - Clean and sanitize greenhouse structures
                
                ### Water Management
                - Check and repair water harvesting structures
                - Maintain drainage systems to handle winter rains
                - Apply limited irrigation to prevent dehydration during dry spells
                
                ### Soil Management
                - Apply organic matter to fields for slow decomposition
                - Protect bare soil with cover crops or mulch
                - Test soil in preparation for spring planting
                
                ### Other Activities
                - Maintain and repair farm equipment and tools
                - Attend agricultural workshops and trainings
                - Review previous year's records and plan for coming season
                - Order seeds and supplies for spring planting
                """)
        
        # Crop-specific best practices
        st.markdown("#### Crop-Specific Best Practices")
        
        # Create sections for common crops
        crops = ["Tomato", "Rice", "Cotton", "Sugarcane", "Onion", "Wheat"]
        crop_selection = st.selectbox("Select Crop", options=crops)
        
        with st.expander(f"{crop_selection} Best Practices"):
            if crop_selection == "Tomato":
                st.markdown("""
                ## Tomato Best Practices
                
                ### Varieties for Maharashtra
                - **Summer**: Pusa Ruby, Punjab Chhuhara, Arka Vikas
                - **Winter**: Pusa Early Dwarf, Sioux, Punjab Kesri
                - **Hybrid Options**: Lakshmi, Naveen, Avinash-2
                
                ### Spacing & Planting
                - Row-to-row: 60-75 cm
                - Plant-to-plant: 30-45 cm
                - Transplant 4-6 week old seedlings
                - Optimum soil temperature: 18-24°C
                
                ### Nutrient Management
                - **Base Application**: FYM @ 25 tons/ha
                - **NPK Requirements**: 100:50:50 kg/ha
                - **Schedule**: 
                  - 50% N and full P & K at transplanting
                  - 25% N at flowering
                  - 25% N at fruiting
                
                ### Water Management
                - Critical stages: Flowering and fruit development
                - Drip irrigation recommended: 3-5 liters/day/plant
                - Mulching reduces water requirement by 30%
                
                ### Common Issues & Solutions
                | Problem | Symptoms | Solution |
                |---------|----------|----------|
                | Blossom end rot | Black sunken area on fruit bottom | Apply calcium nitrate, maintain even moisture |
                | Fusarium wilt | Yellowing of lower leaves, stunting | Use resistant varieties, crop rotation |
                | Tomato leaf curl virus | Curling and yellowing of leaves | Control whitefly vector, use resistant varieties |
                | Early blight | Dark concentric rings on leaves | Fungicide application, avoid overhead irrigation |
                """)
            elif crop_selection == "Rice":
                st.markdown("""
                ## Rice Best Practices
                
                ### Varieties for Maharashtra
                - **Kharif Season**: Ratna, Jaya, Indrayani, Sahyadri series
                - **Rabi Season**: Krishna, Jai Shriram, Pawana
                - **Drought Tolerant**: Phule Radha, Phule Maval
                
                ### Field Preparation & Planting
                - Thorough puddling to reduce percolation losses
                - Maintain 2-3 cm water level during puddling
                - Seed rate: 20-25 kg/ha for transplanting, 60-80 kg/ha for broadcasting
                - Spacing: 20 cm × 15 cm for transplanted rice
                
                ### Nutrient Management
                - **Base Application**: FYM @ 10 tons/ha
                - **NPK Requirements**: 100:50:50 kg/ha
                - **Application Schedule**:
                  - 50% N, 100% P & K as basal
                  - 25% N at tillering
                  - 25% N at panicle initiation
                
                ### Water Management
                - Maintain 5 cm water throughout vegetative phase
                - Practice alternate wetting and drying after panicle initiation
                - Critical stages: Tillering, panicle initiation, flowering
                
                ### Common Issues & Solutions
                | Problem | Symptoms | Solution |
                |---------|----------|----------|
                | Blast | Diamond-shaped lesions on leaves | Apply tricyclazole, maintain water level |
                | Bacterial leaf blight | Yellow to white stripes on leaves | Use resistant varieties, balanced fertilization |
                | Brown planthopper | Wilting, yellowing in patches (hopper burn) | Drain fields, use resistant varieties |
                | Stem borer | Dead heart (vegetative), white head (reproductive) | Apply carbofuran granules, monitor with pheromone traps |
                """)
            elif crop_selection == "Cotton":
                st.markdown("""
                ## Cotton Best Practices
                
                ### Varieties for Maharashtra
                - **Non-Bt Cotton**: NH 615, AKH 081, PKV Rajat
                - **Bt Cotton Hybrids**: Bollgard-II, RCH-2, JKCH-1947
                - **Early Maturing**: NH 615, PKVHY-2, AKH-9916
                
                ### Spacing & Planting
                - Row-to-row: 90-120 cm
                - Plant-to-plant: 45-60 cm
                - Seed rate: 2.5-3 kg/ha
                - Planting time: June-July with onset of monsoon
                
                ### Nutrient Management
                - **Base Application**: FYM @ 10-15 tons/ha
                - **NPK Requirements**: 100:50:50 kg/ha
                - **Application Schedule**:
                  - 50% N, 100% P & K at sowing
                  - 25% N at squaring
                  - 25% N at flowering
                - **Micronutrients**: Foliar spray of 0.5% ZnSO₄ and 0.2% Boron at flowering
                
                ### Water Management
                - Critical stages: Squaring, flowering, boll development
                - Water requirement: 500-700 mm
                - Protective irrigation during dry spells essential
                
                ### Common Issues & Solutions
                | Problem | Symptoms | Solution |
                |---------|----------|----------|
                | Pink bollworm | Rosette flowers, damaged bolls with red larvae | Use pheromone traps (5/ha), timely harvest |
                | Jassids | Yellowing of leaf margins (hopper burn) | Apply imidacloprid, use resistant varieties |
                | Bollworms | Floral bud and boll damage | Use Bt cotton, apply NPV or chemical control |
                | Bacterial blight | Angular water-soaked lesions on leaves | Use acid delinted seeds, copper fungicides |
                """)
            elif crop_selection == "Sugarcane":
                st.markdown("""
                ## Sugarcane Best Practices
                
                ### Varieties for Maharashtra
                - **Early Maturing**: Co 86032, CoM 0265
                - **Mid-Late Maturing**: Co 94012, CoM 9702
                - **Drought Tolerant**: Co 91010, CoM 88121
                
                ### Planting Methods
                - **Conventional**: 2-3 bud setts, 30,000-35,000/ha
                - **Wide row**: 150 cm paired rows, suitable for mechanization
                - **Sustainable Sugarcane Initiative (SSI)**: Single bud, wider spacing
                - **Planting Time**: October-November (Adsali), January-February (Suru)
                
                ### Nutrient Management
                - **Base Application**: FYM @ 25 tons/ha or press mud @ 10 tons/ha
                - **NPK Requirements**: 250:115:115 kg/ha
                - **Application Schedule**:
                  - 40% N, 100% P & K at planting
                  - 30% N at tillering (45-60 days)
                  - 30% N at grand growth stage (90-120 days)
                
                ### Water Management
                - Total water requirement: 1500-2500 mm
                - Critical growth stages: Germination, tillering, grand growth
                - Drip irrigation can save 30-40% water
                
                ### Common Issues & Solutions
                | Problem | Symptoms | Solution |
                |---------|----------|----------|
                | Early shoot borer | Dead heart in young shoots | Apply carbofuran granules, remove dead hearts |
                | Top borer | Bunchy top appearance | Apply fipronil or chlorantraniliprole |
                | Red rot | Internal reddening of stalk | Use disease-free setts, resistant varieties |
                | Pyrilla | Honeydew secretion, sooty mold | Release Epiricania parasites, spray buprofezin |
                """)
            elif crop_selection == "Onion":
                st.markdown("""
                ## Onion Best Practices
                
                ### Varieties for Maharashtra
                - **Kharif Season**: N-53, Baswant 780
                - **Rabi Season**: Phule Samarth, Agrifound Dark Red, Bhima Super
                - **Late Kharif**: Phule Suvarna, Baswant 780
                
                ### Nursery & Transplanting
                - Seed rate: 8-10 kg/ha
                - Nursery bed size: 3m × 1m × 15cm (raised)
                - Transplant 6-8 week old seedlings
                - Spacing: 15 cm × 10 cm
                
                ### Nutrient Management
                - **Base Application**: FYM @ 20-25 tons/ha
                - **NPK Requirements**: 100:50:50 kg/ha
                - **Application Schedule**:
                  - 50% N, 100% P & K before transplanting
                  - 25% N at 30 days after transplanting
                  - 25% N at 45 days after transplanting
                - **Micronutrients**: Foliar spray of 0.5% ZnSO₄ at 45 days
                
                ### Water Management
                - Light but frequent irrigation
                - Critical stages: Bulb formation, bulb development
                - Stop irrigation 15-20 days before harvest
                
                ### Common Issues & Solutions
                | Problem | Symptoms | Solution |
                |---------|----------|----------|
                | Purple blotch | Purple lesions on leaves | Spray mancozeb or chlorothalonil |
                | Thrips | Silvery patches, curling of leaves | Apply fipronil or spinosad |
                | Basal rot | Yellowing from leaf tips, rotting at base | Treat seed with Trichoderma, crop rotation |
                | Stemphylium blight | Small whitish spots on leaves | Apply azoxystrobin or difenoconazole |
                """)
            elif crop_selection == "Wheat":
                st.markdown("""
                ## Wheat Best Practices
                
                ### Varieties for Maharashtra
                - **Timely Sown**: MACS 6478, HD 2189, LOK-1
                - **Late Sown**: HD 2932, NIAW 34, NIAW 917
                - **Heat Tolerant**: NIAW 301, HD 3090
                
                ### Sowing & Spacing
                - Seed rate: 100 kg/ha (timely), 125 kg/ha (late)
                - Spacing: 22.5 cm between rows
                - Sowing depth: 5 cm
                - Optimum sowing time: November 1-15
                
                ### Nutrient Management
                - **Base Application**: FYM @ 10 tons/ha
                - **NPK Requirements**: 120:60:40 kg/ha
                - **Application Schedule**:
                  - 50% N, 100% P & K at sowing
                  - 25% N at first irrigation (21 days)
                  - 25% N at second irrigation (40-45 days)
                
                ### Water Management
                - Critical stages: Crown root initiation, tillering, flowering, grain filling
                - Total water requirement: 450-650 mm
                - Typical irrigation schedule:
                  - First: 21-25 days (CRI stage)
                  - Second: 40-45 days (tillering)
                  - Third: 60-65 days (late jointing)
                  - Fourth: 80-85 days (flowering)
                  - Fifth: 100-105 days (milk stage)
                
                ### Common Issues & Solutions
                | Problem | Symptoms | Solution |
                |---------|----------|----------|
                | Leaf rust | Orange-brown pustules on leaves | Use resistant varieties, apply propiconazole |
                | Powdery mildew | White powdery patches on leaves | Apply sulfur or tebuconazole |
                | Aphids | Clusters on young leaves and ears | Spray imidacloprid or thiamethoxam |
                | Termites | Wilting, drying of plants | Apply chlorpyriphos or fipronil in irrigation |
                """)
    
    with tab3:
        st.markdown("### Maharashtra Local Resources")
        
        st.markdown("""
        ## Maharashtra Agricultural Resources
        
        ### Government Institutions
        
        | Institution | Location | Services | Contact |
        |-------------|----------|----------|---------|
        | Mahatma Phule Krishi Vidyapeeth | Rahuri, Ahmednagar | Research, Training, Seed Production | mpkv.ac.in |
        | Dr. Balasaheb Sawant Konkan Krishi Vidyapeeth | Dapoli, Ratnagiri | Coastal Agriculture Research | dbskkv.org |
        | Vasantrao Naik Marathwada Agricultural University | Parbhani | Dryland Agriculture Research | vnmau.ac.in |
        | Dr. Panjabrao Deshmukh Krishi Vidyapeeth | Akola | Cotton, Pulses Research | pdkv.ac.in |
        
        ### State Government Support Schemes
        
        - **Mahatma Jyotirao Phule Debt Waiver Scheme**: Loan waiver for eligible farmers
        - **Nano Urea Subsidy Scheme**: 50% subsidy on nano urea for increasing productivity
        - **PM Kisan Samman Nidhi**: ₹6,000 annual income support in three equal installments
        - **Maharashtra Agri-Tech Infrastructure Fund**: Support for developing post-harvest infrastructure
        
        ### Farmer Producer Organizations (FPOs)
        
        | FPO Name | Region | Specialization | Contact |
        |----------|--------|----------------|---------|
        | Sahyadri Farmer Producer Company | Nashik | Grapes, Vegetables, Export | sahyadrifpo.com |
        | Devnadi Valley Farmer Producer Company | Sinnar, Nashik | Onions, Pomegranates | devnadivalley@gmail.com |
        | Ankur Farmer Producer Company | Akola | Cotton, Soybean | ankurfpc@gmail.com |
        | Maha Farmers Producer Company | Pune | Fruits, Vegetables | maha.fpc@gmail.com |
        
        ### Local Input Suppliers
        
        - **Maharashtra Agro Industries Development Corporation (MAIDC)**: Fertilizers, seeds, implements
        - **Maharashtra State Seeds Corporation (Mahabeej)**: Quality seeds of improved varieties
        - **Krishi Vigyan Kendras (KVKs)**: Technology assessment, demonstration, capacity development
        
        ### Markets & Wholesale Centers
        
        | Market | Location | Specialization | Market Day |
        |--------|----------|----------------|------------|
        | Lasalgaon APMC | Nashik | Asia's largest onion market | Daily |
        | Vashi APMC | Navi Mumbai | Vegetables, fruits, grains | Daily |
        | Kalamna Market | Nagpur | Oranges, cotton, soybeans | Daily |
        | Pune Market Yard | Pune | Vegetables, fruits | Daily |
        
        ### Weather Resources
        
        - **Indian Meteorological Department (IMD)**: mausam.imd.gov.in
        - **Maharashtra Remote Sensing Application Centre**: mrsac.gov.in
        - **District Agromet Units (DAMUs)**: Located at KVKs, provide district-level forecasts
        
        ### Mobile Apps for Maharashtra Farmers
        
        - **Kisan Suvidha**: Weather, market prices, agro-advisories
        - **Pusa Krishi**: Crop specific information from ICAR
        - **Shetkari Masik App**: Marathi agricultural magazine
        - **mKisan**: SMS portal for farmers
        """)
    
    with tab4:
        st.markdown("### Educational Videos")
        
        # In a real app, we'd embed actual videos here
        # For this demo, we'll just show placeholders with descriptions
        
        video_topics = [
            "Drip Irrigation Installation",
            "IPM for Cotton",
            "Water Conservation Techniques",
            "Soil Testing Methods",
            "Grafting Techniques for Fruit Trees"
        ]
        
        selected_topic = st.selectbox("Select Video Topic", options=video_topics)
        
        # Display placeholder for video
        st.markdown(f"### {selected_topic}")
        st.markdown(f"""
        <div style="background-color:#000; color:#fff; padding:20px; text-align:center; border-radius:5px;">
        <h3>Video: {selected_topic}</h3>
        <p>[Video would play here in the actual application]</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display video description based on selected topic
        if selected_topic == "Drip Irrigation Installation":
            st.markdown("""
            **Description:** This comprehensive tutorial shows step-by-step installation of drip irrigation systems for row crops and orchards. Learn proper component selection, layout planning, and maintenance.
            
            **Key Points:**
            - Materials selection and quantity calculation
            - System layout and design considerations
            - Installation process with common troubleshooting
            - Maintenance and seasonal care
            
            **Duration:** 32:15
            """)
        elif selected_topic == "IPM for Cotton":
            st.markdown("""
            **Description:** This video demonstrates Integrated Pest Management techniques specifically for cotton crops in Maharashtra, featuring expert advice from agricultural scientists.
            
            **Key Points:**
            - Identification of major cotton pests
            - Setting up monitoring systems including pheromone traps
            - Biological control options for bollworms
            - Chemical options as last resort with proper timing
            
            **Duration:** 28:45
            """)
        elif selected_topic == "Water Conservation Techniques":
            st.markdown("""
            **Description:** Learn practical water conservation techniques that can be implemented on farms of all sizes. This video features successful case studies from drought-prone areas of Maharashtra.
            
            **Key Points:**
            - Farm pond construction and lining
            - Rainwater harvesting structures
            - Mulching techniques for different crops
            - Efficient irrigation scheduling
            
            **Duration:** 45:10
            """)
        elif selected_topic == "Soil Testing Methods":
            st.markdown("""
            **Description:** This instructional video shows proper soil sampling and testing methods that farmers can perform themselves for basic soil health assessment.
            
            **Key Points:**
            - Proper soil sampling techniques
            - Simple pH and nutrient tests you can do on the farm
            - Interpreting laboratory soil test reports
            - Corrective measures based on test results
            
            **Duration:** 22:30
            """)
        elif selected_topic == "Grafting Techniques for Fruit Trees":
            st.markdown("""
            **Description:** Master the art of grafting fruit trees with this detailed tutorial. Focuses on mango, citrus, and guava grafting techniques appropriate for Maharashtra.
            
            **Key Points:**
            - Selection of rootstock and scion material
            - Tools and materials needed for successful grafting
            - Step-by-step demonstration of wedge, approach, and bud grafting
            - Post-grafting care and management
            
            **Duration:** 36:20
            """)
        
        # Additional resources related to the video
        st.markdown("### Related Resources")
        st.markdown("""
        - Downloadable PDF guide on this topic
        - Contact information for local experts
        - List of suppliers for related equipment
        - Upcoming workshops and training sessions
        """)

# Weather page
def show_weather_page():
    """Display detailed weather information and forecasts"""
    st.markdown("<h2 class='slideIn'>Weather Information</h2>", unsafe_allow_html=True)
    
    # Get farm location from profile
    farm_location = get_profile_field(st.session_state.user_profile, 'farm_location')
    
    # Create input for location
    location = st.text_input("Location", value=farm_location if farm_location else "")
    
    if st.button("Get Weather") or (location and not st.session_state.weather_data):
        if location:
            with st.spinner("Fetching weather data..."):
                # Fetch current weather
                weather_data = fetch_weather_data(location)
                
                # Fetch forecast
                forecast_data = fetch_forecast_data(location)
                
                # Get weather alerts
                if weather_data:
                    weather_alerts = get_weather_alerts(weather_data)
                else:
                    weather_alerts = []
                
                # Update session state
                st.session_state.weather_location = location
                st.session_state.weather_data = weather_data
                st.session_state.forecast_data = forecast_data
                st.session_state.weather_alerts = weather_alerts
                
                # Force page refresh
                st.rerun()
        else:
            st.error("Please enter a location")
    
    # Display weather information if available
    if st.session_state.weather_data:
        weather_data = st.session_state.weather_data
        forecast_data = st.session_state.forecast_data
        
        # Create columns for current weather and alerts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Current weather
            st.markdown("### Current Weather")
            
            # Get data from weather response
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            weather_desc = weather_data["weather"][0]["description"].capitalize()
            weather_icon = weather_data["weather"][0]["icon"]
            
            # Display current conditions
            st.markdown(f"""
            <div style="display: flex; align-items: center;">
                <img src="https://openweathermap.org/img/wn/{weather_icon}@2x.png" style="width: 100px; height: 100px;">
                <div>
                    <h1 style="margin: 0;">{temp:.1f}°C</h1>
                    <p>Feels like: {feels_like:.1f}°C</p>
                    <p>{weather_desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display additional details
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown(f"**Humidity:** {humidity}%")
            
            with col_b:
                st.markdown(f"**Wind:** {wind_speed} m/s")
            
            with col_c:
                if "rain" in weather_data:
                    rain_1h = weather_data["rain"].get("1h", 0)
                    st.markdown(f"**Rain (1h):** {rain_1h} mm")
                else:
                    st.markdown("**Rain:** None")
        
        with col2:
            # Weather alerts
            st.markdown("### Alerts")
            
            if st.session_state.weather_alerts:
                for alert in st.session_state.weather_alerts:
                    if alert["type"] == "danger":
                        st.error(alert["message"])
                    elif alert["type"] == "warning":
                        st.warning(alert["message"])
                    else:
                        st.info(alert["message"])
            else:
                st.info("No weather alerts at this time.")
        
        # Display forecast if available
        if forecast_data:
            st.markdown("### 5-Day Forecast")
            
            # Format forecast data for display
            from weather_service import format_forecast_data
            formatted_forecast = format_forecast_data(forecast_data)
            
            # Create columns for each day
            if formatted_forecast:
                cols = st.columns(min(5, len(formatted_forecast)))
                
                for i, day_forecast in enumerate(formatted_forecast[:5]):  # Show up to 5 days
                    with cols[i]:
                        # Format date
                        day_name = day_forecast["day_name"]
                        
                        # Get weather icon
                        icon = day_forecast["weather_icon"]
                        
                        # Display forecast for this day
                        st.markdown(f"""
                        <div style="text-align: center;">
                            <h4>{day_name}</h4>
                            <img src="https://openweathermap.org/img/wn/{icon}@2x.png" style="width: 50px; height: 50px;">
                            <p>{day_forecast["weather_description"]}</p>
                            <p><strong>{day_forecast["max_temp"]:.1f}°C</strong> / {day_forecast["min_temp"]:.1f}°C</p>
                            <p>Humidity: {day_forecast["avg_humidity"]:.0f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Forecast data not available.")
            
            # Agricultural recommendations based on weather
            st.markdown("### Agricultural Recommendations")
            
            # Get current weather conditions
            current_temp = weather_data["main"]["temp"]
            current_humidity = weather_data["main"]["humidity"]
            is_raining = "rain" in weather_data
            
            # Generate recommendations based on conditions
            recommendations = []
            
            # Temperature-based recommendations
            if current_temp > 35:
                recommendations.append("- Apply light irrigation to reduce heat stress on crops")
                recommendations.append("- Consider temporary shade for sensitive crops")
                recommendations.append("- Irrigate during early morning or evening")
            elif current_temp < 10:
                recommendations.append("- Monitor for frost damage, especially in low-lying areas")
                recommendations.append("- Cover sensitive crops if temperatures drop further")
                recommendations.append("- Delay fertilizer application until temperatures rise")
            
            # Humidity-based recommendations
            if current_humidity > 80:
                recommendations.append("- Monitor crops for fungal diseases due to high humidity")
                recommendations.append("- Avoid irrigation to prevent excess moisture")
                recommendations.append("- Consider preventative fungicide application")
            elif current_humidity < 30:
                recommendations.append("- Increase irrigation frequency to combat low humidity")
                recommendations.append("- Apply mulch to conserve soil moisture")
                recommendations.append("- Monitor for water stress in crops")
            
            # Rain-based recommendations
            if is_raining:
                rain_amount = weather_data["rain"].get("1h", 0)
                
                if rain_amount > 10:
                    recommendations.append("- Check fields for waterlogging and improve drainage if needed")
                    recommendations.append("- Postpone fertilizer application to prevent runoff")
                    recommendations.append("- Monitor for soil erosion in sloped fields")
                else:
                    recommendations.append("- Light rain can be beneficial; reduce irrigation accordingly")
                    recommendations.append("- Good time for foliar fertilizer application after rain stops")
            
            # Display recommendations
            if recommendations:
                for recommendation in recommendations:
                    st.markdown(recommendation)
            else:
                st.markdown("- Current weather conditions are favorable for most agricultural activities")
                st.markdown("- Continue with regular farm operations and monitoring")
            
            # Weather impact on crops
            st.markdown("### Potential Weather Impact on Crops")
            
            # Allow user to select crops
            crop_options = ["Tomato", "Onion", "Cotton", "Rice", "Wheat", "Sugarcane"]
            selected_crops = st.multiselect("Select your crops", options=crop_options)
            
            if selected_crops:
                # Get weather factors
                has_high_temp = current_temp > 32
                has_low_temp = current_temp < 15
                has_high_humidity = current_humidity > 75
                has_low_humidity = current_humidity < 40
                has_rain = is_raining
                
                # Display impacts for each selected crop
                for crop in selected_crops:
                    st.markdown(f"#### {crop}")
                    
                    impacts = []
                    
                    if crop == "Tomato":
                        if has_high_temp:
                            impacts.append("⚠️ High temperatures may cause flower drop and reduce fruit set")
                        if has_high_humidity:
                            impacts.append("⚠️ High humidity increases risk of late blight and leaf mold")
                        if has_rain:
                            impacts.append("⚠️ Rain may increase disease pressure; monitor for early blight")
                        if not impacts:
                            impacts.append("✅ Current conditions are favorable for tomato development")
                    
                    elif crop == "Onion":
                        if has_high_temp:
                            impacts.append("⚠️ High temperatures may reduce bulb size and quality")
                        if has_high_humidity:
                            impacts.append("⚠️ High humidity increases risk of purple blotch and downy mildew")
                        if has_rain:
                            impacts.append("⚠️ Excessive rain may lead to rot; ensure good drainage")
                        if not impacts:
                            impacts.append("✅ Current conditions are favorable for onion growth")
                    
                    elif crop == "Cotton":
                        if has_high_temp and has_low_humidity:
                            impacts.append("⚠️ Hot, dry conditions may cause square and boll shedding")
                        if has_high_humidity:
                            impacts.append("⚠️ High humidity increases risk of boll rot")
                        if has_rain:
                            impacts.append("⚠️ Rain during boll opening can reduce fiber quality")
                        if not impacts:
                            impacts.append("✅ Current conditions are favorable for cotton development")
                    
                    elif crop == "Rice":
                        if has_high_temp:
                            impacts.append("⚠️ High temperatures during flowering may reduce fertility")
                        if has_low_humidity:
                            impacts.append("⚠️ Low humidity may increase water requirements")
                        if not has_rain and has_high_temp:
                            impacts.append("⚠️ Hot, dry conditions may cause water stress; increase irrigation")
                        if not impacts:
                            impacts.append("✅ Current conditions are favorable for rice growth")
                    
                    elif crop == "Wheat":
                        if has_high_temp:
                            impacts.append("⚠️ High temperatures may accelerate maturity and reduce grain fill")
                        if has_high_humidity:
                            impacts.append("⚠️ High humidity increases risk of rust and powdery mildew")
                        if has_rain:
                            impacts.append("⚠️ Rain during grain fill may affect quality; during harvest can cause sprouting")
                        if not impacts:
                            impacts.append("✅ Current conditions are favorable for wheat development")
                    
                    elif crop == "Sugarcane":
                        if has_low_temp:
                            impacts.append("⚠️ Low temperatures may slow growth and reduce sucrose accumulation")
                        if has_low_humidity and has_high_temp:
                            impacts.append("⚠️ Hot, dry conditions increase water requirements; check irrigation")
                        if not impacts:
                            impacts.append("✅ Current conditions are favorable for sugarcane growth")
                    
                    for impact in impacts:
                        st.markdown(impact)

# Main app logic
def main():
    """Main application logic"""
    # Show header for all pages except login/signup
    if st.session_state.page not in ["login", "signup"]:
        show_header()
    
    # Language selector in sidebar (would be implemented in full app)
    if st.session_state.page not in ["login", "signup"]:
        with st.sidebar:
            show_language_selector()
    
    # Display current page
    if st.session_state.page == "login":
        show_login_page()
    elif st.session_state.page == "signup":
        show_signup_page()
    elif st.session_state.page == "profile_setup":
        show_profile_setup_page()
    elif st.session_state.page == "dashboard":
        show_dashboard_page()
    elif st.session_state.page == "crop_test":
        show_crop_test_page()
    elif st.session_state.page == "soil_analysis":
        show_soil_analysis_page()
    elif st.session_state.page == "history":
        show_history_page()
    elif st.session_state.page == "resources":
        show_resources_page()
    elif st.session_state.page == "weather":
        show_weather_page()
    else:
        st.error("Unknown page")
        go_to_login()
    
    # Footer
    if st.session_state.page not in ["login", "signup"]:
        st.markdown("---")
        st.markdown("""
        <footer>
            <p>PhytoSense v2.0 - AI-Powered Plant Health Monitoring System</p>
            <p>© 2023 PhytoSense Team. All rights reserved.</p>
        </footer>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

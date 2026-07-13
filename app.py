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

# -----------------------------
# MUST BE FIRST STREAMLIT CALL
# -----------------------------
st.set_page_config(
    page_title="PhytoSense - AI Plant Health Monitoring",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Import custom modules
# -----------------------------
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
from language_support import initialize_language, t, translate_dataframe

# -----------------------------
# Initialize language AFTER config
# -----------------------------
lang = initialize_language()

# Apply custom CSS
with open(".streamlit/custom.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Titles and text with translations
st.title(t("PhytoSense - AI Plant Health Monitoring", lang))
st.write(t("Welcome to the Smart Farming App. Get crop insights and weather forecasts.", lang))

if st.button(t("Detect Disease", lang)):
    st.success(t("Disease detection started.", lang))

# Example for translating a DataFrame
# st.dataframe(translate_dataframe(my_dataframe, lang))


lang = initialize_language()

st.title(t("PhytoSense - AI Plant Health Monitoring", lang))
st.write(t("Welcome to the Smart Farming App. Get crop insights and weather forecasts.", lang))

if st.button(t("Detect Disease", lang)):
    st.success(t("Disease detection started.", lang))

#st.dataframe(translate_dataframe(my_dataframe, lang))
import streamlit as st
from language_support import initialize_language, t

# Initialize language selector
lang = initialize_language()

# Use translation helper
st.title(t("Welcome to PhytoSense", lang))
st.write(t("This is a multi-language demo.", lang))

 

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
    /* Main container styling */
    .auth-container {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    /* Camera Input Styling */
.stCamera {
    border: 2px dashed #4CAF50;
    border-radius: 10px;
    margin-bottom: 1rem;
}
.stCamera button {
    background-color: #4CAF50 !important;
}
[data-testid="stCameraInputButton"] {
    border-radius: 20px !important;
}
            
    /* Form styling */
    .auth-form {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input, 
    .stTextInput>div>div>input:focus {
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Button styling */
    .auth-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px 0;
        cursor: pointer;
        border-radius: 25px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .auth-button:hover {
        background-color: #3e8e41;
        transform: translateY(-2px);
    }
    
    /* Secondary button styling */
    .secondary-button {
        background-color: white;
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    
    .secondary-button:hover {
        background-color: #f1f8e9;
    }
    
    /* Background styling */
    .stApp {
        background-image: linear-gradient(to bottom, #e8f5e9, #f1f8e9);
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-img {
        width: 120px;
        height: auto;
    }
    
    /* Welcome text styling */
    .welcome-text {
        color: #2e7d32;
        margin-bottom: 20px;
    }
    
    /* Feature list styling */
    .feature-list {
        padding-left: 20px;
    }
    
    .feature-list li {
        margin-bottom: 10px;
        color: #555;
    }
    
    /* Animation for the form */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-form {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
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
    if "image_source" not in st.session_state:
        st.session_state.image_source = None 
    if "image_capture_method" not in st.session_state:
        st.session_state.image_capture_method = None # Will store 'upload', 'example', or 'live'

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
    """Display the login page with enhanced design and functionality"""
    # Create a container for the entire login page
    with st.container():
        # Create two columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Login form container
            st.markdown("## Login to PhytoSense")
            
            # Logo and title
            svg_content = load_svg("assets/logo.svg")
            st.image(svg_content, width=80)

            # Show success message if account was just created
            if st.session_state.show_account_created:
                st.success("Account created successfully! Please login.")
                st.session_state.show_account_created = False

            # Login form
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me", value=True)
            
            # Login button with loading state
            if st.button("Login", key="login_button", type="primary"):
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    with st.spinner("Authenticating..."):
                        try:
                            user = verify_user(username, password)
                            if user:
                                st.session_state.current_user = user
                                st.success("Login successful!")
                                
                                # Load user profile if exists
                                user_id = user['id'] if isinstance(user, dict) else user.id
                                profile = get_user_profile(user_id)
                                if profile:
                                    st.session_state.user_profile = profile
                                
                                # Redirect based on profile completion
                                if not user.get("profile_complete", False):
                                    go_to_profile_setup()
                                else:
                                    go_to_dashboard()
                                st.rerun()
                            else:
                                st.error("Invalid username or password")
                        except Exception as e:
                            st.error(f"Login failed: {str(e)}")
            
            # Forgot password link
            st.markdown("[Forgot password?](#)")
            
            # Signup prompt
            st.markdown("Don't have an account?")
            if st.button("Create Account", key="signup_prompt_button"):
                go_to_signup()

        with col2:
            # Features section
            st.markdown("## Why Use PhytoSense?")
            
            feature_cols = st.columns([1, 3])
            with feature_cols[0]:
                st.markdown("🔍")
            with feature_cols[1]:
                st.markdown("**Disease Detection**")
                st.markdown("Identify plant issues early with AI analysis")
            
            feature_cols = st.columns([1, 3])
            with feature_cols[0]:
                st.markdown("💧")
            with feature_cols[1]:
                st.markdown("**Water Optimization**")
                st.markdown("Prevent over/under watering with precise analysis")
            
            feature_cols = st.columns([1, 3])
            with feature_cols[0]:
                st.markdown("🌱")
            with feature_cols[1]:
                st.markdown("**Smart Recommendations**")
                st.markdown("Get personalized fertilizer and care advice")
            
            feature_cols = st.columns([1, 3])
            with feature_cols[0]:
                st.markdown("📈")
            with feature_cols[1]:
                st.markdown("**Track Progress**")
                st.markdown("Monitor your farm's health over time")
            
            # Testimonial
            st.markdown("---")
            st.markdown("> *\"PhytoSense helped me reduce crop losses by 30%\"*")
            st.markdown("> **- Rajesh K., Maharashtra Farmer**")

def show_signup_page():
    """Display the signup page with enhanced design and validation"""
    # Create a container for the entire page
    with st.container():
        # Create two columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Form container
            st.markdown("## Create Your Account")
            
            # Logo and title
            svg_content = load_svg("assets/logo.svg")
            st.image(svg_content, width=80)
            
            # Signup form with validation
            with st.form("signup_form"):
                # Required fields
                username = st.text_input("Username*", help="Required. 4-20 characters, letters and numbers only")
                email = st.text_input("Email*", help="Required for account recovery")
                password = st.text_input("Password*", type="password", 
                                       help="Minimum 8 characters with at least one number and special character")
                confirm_password = st.text_input("Confirm Password*", type="password")
                
                # Optional fields
                farm_location = st.text_input("Farm Location", help="Optional - helps provide localized recommendations")
                phone = st.text_input("Phone Number", help="Optional - for SMS alerts")
                
                # Terms checkbox
                agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy*", value=False)
                
                # Marketing consent
                receive_updates = st.checkbox("I'd like to receive product updates and farming tips", value=True)
                
                # Form submission
                submitted = st.form_submit_button("Create Account", type="primary")
                
                if submitted:
                    # Validate inputs
                    errors = []
                    
                    if not username:
                        errors.append("Username is required")
                    elif len(username) < 4 or len(username) > 20:
                        errors.append("Username must be 4-20 characters")
                    elif not username.isalnum():
                        errors.append("Username can only contain letters and numbers")
                    
                    if not email:
                        errors.append("Email is required")
                    elif "@" not in email or "." not in email:
                        errors.append("Please enter a valid email address")
                    
                    if not password:
                        errors.append("Password is required")
                    elif len(password) < 8:
                        errors.append("Password must be at least 8 characters")
                    elif not any(char.isdigit() for char in password):
                        errors.append("Password must contain at least one number")
                    elif not any(not char.isalnum() for char in password):
                        errors.append("Password must contain at least one special character")
                    
                    if password != confirm_password:
                        errors.append("Passwords do not match")
                    
                    if not agree_terms:
                        errors.append("You must agree to the terms of service")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        with st.spinner("Creating your account..."):
                            try:
                                # Create user
                                success, message = create_user(
                                username=username,
                                password=password,
                                email=email
                                )
                                
                                if success:
                                    st.session_state.show_account_created = True
                                    st.success("Account created successfully!")
                                    time.sleep(1)  # Show success message briefly
                                    go_to_login()
                                    st.rerun()
                                else:
                                    st.error(message)
                            except Exception as e:
                                st.error(f"Account creation failed: {str(e)}")
            
            # Login prompt
            st.markdown("Already have an account?")
            if st.button("Back to Login", key="login_prompt_button"):
                go_to_login()
        
        with col2:
            # Benefits section
            st.markdown("## Why Join PhytoSense?")
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("🌾")
            with benefit_cols[1]:
                st.markdown("**Smart Farming**")
                st.markdown("Get AI-powered insights for your crops")
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("💧")
            with benefit_cols[1]:
                st.markdown("**Water Optimization**")
                st.markdown("Prevent over/under watering with precise analysis")
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("🔬")
            with benefit_cols[1]:
                st.markdown("**Disease Detection**")
                st.markdown("Identify plant issues before they become serious")
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("📊")
            with benefit_cols[1]:
                st.markdown("**Track Progress**")
                st.markdown("Monitor your farm's health over time")
            
            # Testimonial image placeholder
            st.markdown("---")
            st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80", 
                     caption="\"PhytoSense helped me reduce crop losses by 30%\" - Rajesh K., Maharashtra Farmer")

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
    """Display the main dashboard page with overview, quick actions, and recent activities"""
    st.markdown("<h2 class='slideIn'>Farmer Dashboard</h2>", unsafe_allow_html=True)
    
    # Get user data
    user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
    profile = st.session_state.user_profile or {}
    
    # Create dashboard layout with tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚡ Quick Actions", "🕒 Recent Activities"])
    
    with tab1:
        # Overview tab with colored heading
        st.markdown("""
        <div style='background-color:#4CAF50; padding:10px; border-radius:5px;'>
            <h3 style='color:white; margin:0;'>Farm Overview</h3>
        </div>
        <div class='tab-content'>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏡 Farm Profile")
            st.markdown(f"**Location:** {get_profile_field(profile, 'farm_location', 'Not set')}")
            st.markdown(f"**Size:** {get_profile_field(profile, 'farm_size', 'Not set')} acres")
            st.markdown(f"**Primary Crops:** {get_profile_field(profile, 'primary_crops', 'Not set')}")
            st.markdown(f"**Farming Type:** {get_profile_field(profile, 'farming_type', 'Not set')}")
            
            if st.button("✏️ Edit Profile", key="edit_profile_dash"):
                go_to_profile_setup()
        
        with col2:
            st.markdown("### 📅 Seasonal Summary")
            now = datetime.now()
            month = now.month
            
            # Determine season
            if 3 <= month <= 5:  # Spring
                season = "Spring"
                season_color = "#6EDB3E"
                season_icon = "🌱"
                season_tips = [
                    "Prepare soil for planting",
                    "Start summer crop seedlings",
                    "Apply pre-emergent herbicides",
                    "Check irrigation systems"
                ]
            elif 6 <= month <= 8:  # Summer
                season = "Summer"
                season_color = "#FF9800"
                season_icon = "☀️"
                season_tips = [
                    "Monitor for heat stress",
                    "Increase irrigation frequency",
                    "Apply mulch to retain moisture",
                    "Watch for pest outbreaks"
                ]
            elif 9 <= month <= 11:  # Fall
                season = "Fall"
                season_color = "#FF5722"
                season_icon = "🍂"
                season_tips = [
                    "Harvest mature crops",
                    "Plant cover crops",
                    "Test and amend soil",
                    "Clean and store equipment"
                ]
            else:  # Winter
                season = "Winter"
                season_color = "#2196F3"
                season_icon = "❄️"
                season_tips = [
                    "Protect sensitive plants",
                    "Service farm equipment",
                    "Plan next season's crops",
                    "Take training courses"
                ]
                
            st.markdown(f"""
            <div style='background-color:{season_color}; padding:10px; border-radius:5px; color:white; margin-bottom:15px;'>
                <span style='font-size:24px;'>{season_icon}</span> <strong>{season} Season</strong>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Seasonal Tips:**")
            for tip in season_tips:
                st.markdown(f"- {tip}")
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close tab-content
    
    with tab2:
        # Quick Actions tab with colored heading
        st.markdown("""
        <div style='background-color:#2196F3; padding:10px; border-radius:5px;'>
            <h3 style='color:white; margin:0;'>Quick Actions</h3>
        </div>
        <div class='tab-content'>
        """, unsafe_allow_html=True)
        
        # Create action buttons in a grid layout
        action_cols = st.columns(3)
        
        with action_cols[0]:
            st.markdown("""
            <div class='action-card' style='text-align:center;'>
                <h4>🌱 Test Your Crop</h4>
                <p>Analyze crop health and detect diseases</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze", key="analyze_crop_btn", type="primary"):
                go_to_crop_test()
            
        with action_cols[1]:
            st.markdown("""
            <div class='action-card' style='text-align:center;'>
                <h4>🌍 Soil Analysis</h4>
                <p>Check soil quality and get recommendations</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze", key="analyze_soil_btn", type="primary"):
                go_to_soil_analysis()
            
        with action_cols[2]:
            st.markdown("""
            <div class='action-card' style='text-align:center;'>
                <h4>☁️ Weather</h4>
                <p>Get weather forecasts and farming alerts</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Check", key="check_weather_btn", type="primary"):
                go_to_weather()
        
        # Second row of actions
        action_cols2 = st.columns(3)
        
        with action_cols2[0]:
            st.markdown("""
            <div class='action-card' style='text-align:center;'>
                <h4>📊 History</h4>
                <p>View previous analyses and reports</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View", key="view_history_btn", type="primary"):
                go_to_history()
                
        with action_cols2[1]:
            st.markdown("""
            <div class='action-card' style='text-align:center;'>
                <h4>📚 Resources</h4>
                <p>Access farming guides and materials</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Browse", key="browse_resources_btn", type="primary"):
                go_to_resources()
                
        with action_cols2[2]:
            st.markdown("""
            <div class='action-card' style='text-align:center;'>
                <h4>🛒 Marketplace</h4>
                <p>Find agricultural products</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Explore", key="explore_market_btn", type="primary"):
                st.info("Marketplace feature coming soon!")
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close tab-content
    
    with tab3:
        # Recent Activities tab with colored heading
        st.markdown("""
        <div style='background-color:#9C27B0; padding:10px; border-radius:5px;'>
            <h3 style='color:white; margin:0;'>Recent Activities</h3>
        </div>
        <div class='tab-content'>
        """, unsafe_allow_html=True)
        
        # Get user's analysis history
        history = get_user_analyses(user_id, limit=5)
        
        if history:
            for analysis in history:
                # Create a card for each analysis
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Display analysis summary
                        if analysis["analysis_type"] == "plant":
                            st.markdown(f"#### 🌱 Plant Analysis - {analysis['timestamp'][:10]}")
                            if "results" in analysis and "plant_info" in analysis["results"]:
                                plant_info = analysis["results"]["plant_info"]
                                st.markdown(f"**Plant:** {plant_info.get('name', 'Unknown')}")
                                
                                if "diseases" in analysis["results"]:
                                    diseases = analysis["results"]["diseases"]
                                    if diseases.get("detected", False):
                                        st.markdown("**Status:** <span class='status-danger'>Issues Detected</span>", unsafe_allow_html=True)
                                    else:
                                        st.markdown("**Status:** <span class='status-healthy'>Healthy</span>", unsafe_allow_html=True)
                        
                        elif analysis["analysis_type"] == "soil":
                            st.markdown(f"#### 🌍 Soil Analysis - {analysis['timestamp'][:10]}")
                            if "results" in analysis and "soil_type" in analysis["results"]:
                                soil_type = analysis["results"]["soil_type"]
                                st.markdown(f"**Soil Type:** {soil_type}")
                    
                    with col2:
                        # View details button
                        if st.button("View Details", key=f"view_{analysis['id']}"):
                            st.session_state.selected_analysis = analysis
                            st.session_state.page = "history"
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("No recent activities found. Start by analyzing your crops or soil!")
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close tab-content
    
    # Add custom CSS for the dashboard
    st.markdown("""
    <style>
        .tab-content {
            padding: 15px;
            background-color: white;
            border-radius: 0 0 10px 10px;
            border: 1px solid #e0e0e0;
            border-top: none;
        }
        
        .action-card {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .action-card h4 {
            margin: 0 0 10px 0;
        }
        
        .action-card p {
            margin: 0;
            font-size: 14px;
            color: #555;
        }
    </style>
    """, unsafe_allow_html=True)

# Crop test page
def show_crop_test_page():
    """Display the crop testing page"""
    st.markdown("<h2 class='slideIn'>Plant Health Analysis</h2>", unsafe_allow_html=True)
    
    # Create tabs for different ways to add images
    tab_upload, tab_example, tab_live = st.tabs(["📁 Upload", "🖼️ Example", "📷 Live Capture"])
    
    with tab_upload:
        uploaded_file = st.file_uploader("Upload an image of your crop for analysis", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Save the uploaded image to session state
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            st.session_state.image_source = "upload"
            
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
                        st.session_state.image_source = "example"
                        st.rerun()
        else:
            st.info("No example images available.")

    with tab_live:
        st.markdown("### Capture Plant Image Live")
        st.warning("Camera access is required. Your image will not be stored permanently.")
        
        # Add a toggle for camera visibility
        if 'show_camera' not in st.session_state:
            st.session_state.show_camera = False
        
        if not st.session_state.show_camera:
            if st.button("Open Camera", key="open_camera"):
                st.session_state.show_camera = True
                st.rerun()
        else:
            # Camera widget
            captured_image = st.camera_input(
                "Position your plant and click capture",
                key="live_camera",
                help="Ensure good lighting and focus on affected areas"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if captured_image:
                    st.session_state.uploaded_image = Image.open(captured_image)
                    st.session_state.image_capture_method = 'live'
                    st.success("Image captured! Scroll down for analysis.")
                    st.session_state.show_camera = False
                    st.rerun()
            
            with col2:
                if st.button("Close Camera", key="close_camera"):
                    st.session_state.show_camera = False
                    st.rerun()
    # Form for additional plant details
    if st.session_state.uploaded_image:
        st.markdown("### Additional Information (Optional)")
        st.markdown("Providing more details helps improve analysis accuracy.")
        
        # Create a three-column layout for form inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop_type = st.selectbox(
                "Crop Type",
                options=["Unknown", "Tomato", "Potato", "Corn", "Wheat", "Rice", "Onion", "Soybean", "Cotton", 
                         "Cabbage", "Watermelon", "Pomegranate", "Cluster Beans","Grapes","Cucumber","Bitter Gourd","Pumpkin", "Bottle Gourd", "Cauliflower", "Lady Finger"],
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
                        results["plant_info"]["name"]
                    )
                    
                    # Update session state with results
                    st.session_state.analysis_results = results
                    st.session_state.plant_info = results["plant_info"]
                    st.session_state.water_content = results["water_content"]
                    st.session_state.diseases = results["diseases"]
                    st.session_state.pests = results["pests"]
                    st.session_state.crop_details = results.get("crop_details", {})
                    st.session_state.deficiencies = results.get("deficiencies", {})
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
        st.markdown("<h2 class='fadeIn'>Plant Analysis Results</h2>", unsafe_allow_html=True)
        if hasattr(st.session_state, 'image_capture_method') and st.session_state.image_capture_method:
            if st.session_state.image_capture_method == 'live':
                st.markdown("*Image source: Live capture*")
            elif st.session_state.image_capture_method == 'upload':
                st.markdown("*Image source: File upload*")
            elif st.session_state.image_capture_method == 'example':
                st.markdown("*Image source: Example image*")
        
        results = st.session_state.analysis_results
        
        # Side-by-side layout with image and structured report
        col1, col2 = st.columns([1, 2])
        
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
            # Create a structured report following the requested format
            st.markdown("<div class='structured-report'>", unsafe_allow_html=True)
            
            # Section 1: General Information of Plant & Water Content
            st.markdown("<h3 class='section-general'>1. General Information</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            # Basic plant information
            st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Identified Plant:</strong> {plant_info['name']}</p>", unsafe_allow_html=True)
            if "scientific_name" in plant_info and plant_info["scientific_name"]:
                st.markdown(f"<p><strong>Scientific Name:</strong> <em>{plant_info['scientific_name']}</em></p>", unsafe_allow_html=True)
            
            # Water content analysis
            water_content = results["water_content"]
            status = water_content["status"]
            
            # Determine water status class for styling
            if status == "Low":
                water_status_class = "status-warning"
            elif status == "Critical":
                water_status_class = "status-danger"
            elif status == "Optimal":
                water_status_class = "status-healthy"
            else:
                water_status_class = ""
            
            st.markdown(f"<p><strong>Water Content Status:</strong> <span class='{water_status_class}'>{status}</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Estimated Water Content:</strong> {water_content['percentage']}%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)  # Close analysis-result
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close analysis-section
            
            # Section 2: Disease Detection with preventive measures
            st.markdown("<h3 class='section-disease'>2. Disease Detection</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
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
                    
                    # Display detailed database information if available
                    if "detailed_info" in disease:
                        st.markdown("<div class='detailed-info'>", unsafe_allow_html=True)
                        
                        if disease["detailed_info"]["symptoms"]:
                            st.markdown(f"<p><strong>Symptoms:</strong> {disease['detailed_info']['symptoms']}</p>", unsafe_allow_html=True)
                        
                        if disease["detailed_info"]["causes"]:
                            st.markdown(f"<p><strong>Causes:</strong> {disease['detailed_info']['causes']}</p>", unsafe_allow_html=True)
                        
                        if disease["detailed_info"]["treatment"]:
                            st.markdown(f"<p><strong>Recommended Treatment:</strong> {disease['detailed_info']['treatment']}</p>", unsafe_allow_html=True)
                            
                        if disease["detailed_info"]["prevention"]:
                            st.markdown(f"<p><strong>Prevention:</strong> {disease['detailed_info']['prevention']}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown("<p><span class='status-healthy'>No diseases detected.</span> The plant appears healthy.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)  # Close the disease analysis section
            
            # Section 3: Pest/Insect Detection with treatments
            st.markdown("<h3 class='section-pest'>3. Pest/Insect Detection</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
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
                        
                    # Display detailed database information if available
                    if "detailed_info" in pest:
                        st.markdown("<div class='detailed-info'>", unsafe_allow_html=True)
                        
                        if pest["detailed_info"]["symptoms"]:
                            st.markdown(f"<p><strong>Symptoms:</strong> {pest['detailed_info']['symptoms']}</p>", unsafe_allow_html=True)
                        
                        if pest["detailed_info"]["description"]:
                            st.markdown(f"<p><strong>About:</strong> {pest['detailed_info']['description']}</p>", unsafe_allow_html=True)
                        
                        if pest["detailed_info"]["treatment"]:
                            st.markdown(f"<p><strong>Recommended Treatment:</strong> {pest['detailed_info']['treatment']}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown("<p><span class='status-healthy'>No pests detected.</span> The plant appears pest-free.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close pest section
            
            # Section 4: Nutrient Deficiency with cures
            st.markdown("<h3 class='section-deficiency'>4. Nutrient Deficiency</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            if hasattr(st.session_state, 'deficiencies') and st.session_state.deficiencies:
                deficiencies = st.session_state.deficiencies
                for deficiency_name, deficiency_info in deficiencies.items():
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-header'><div class='result-icon'>🧪</div><h4 class='result-title'>{deficiency_name} Deficiency</h4></div>", unsafe_allow_html=True)
                    st.markdown("<div class='result-content'>", unsafe_allow_html=True)
                    
                    if "symptoms" in deficiency_info:
                        st.markdown(f"<p><strong>Symptoms:</strong> {deficiency_info['symptoms']}</p>", unsafe_allow_html=True)
                    
                    if "treatment" in deficiency_info:
                        st.markdown(f"<p><strong>Cure/Treatment:</strong> {deficiency_info['treatment']}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown("<p>No specific nutrient deficiencies identified based on the image analysis.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close nutrient deficiency section
            
            # Section 5: Overall Assessment
            st.markdown("<h3 class='section-assessment'>5. Overall Assessment</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            # Generate an overall assessment based on all findings
            has_disease = diseases["detected"]
            has_pests = pests["detected"]
            water_status = water_content["status"]
            
            overall_status = "Healthy"
            overall_class = "status-healthy"
            overall_recommendations = []
            
            if has_disease or has_pests or water_status in ["Low", "Critical"]:
                if has_disease and has_pests:
                    overall_status = "Critical Attention Needed"
                    overall_class = "status-danger"
                    overall_recommendations.append("The plant is showing signs of both disease and pest infestation which require immediate attention.")
                elif has_disease:
                    overall_status = "Attention Required"
                    overall_class = "status-warning"
                    overall_recommendations.append("The plant is showing disease symptoms that need to be addressed promptly.")
                elif has_pests:
                    overall_status = "Attention Required"
                    overall_class = "status-warning"
                    overall_recommendations.append("The plant has pest infestations that need to be controlled.")
                
                if water_status == "Low":
                    overall_recommendations.append("The plant needs more water. Increase watering frequency.")
                elif water_status == "Critical":
                    overall_status = "Critical Attention Needed"
                    overall_class = "status-danger"
                    overall_recommendations.append("The plant is severely dehydrated and needs immediate watering.")
            else:
                overall_recommendations.append("The plant appears to be in good health with no major issues detected.")
            
            st.markdown("<div class='assessment-box'>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>Overall Plant Status:</strong> <span class='{overall_class}'>{overall_status}</span></p>", unsafe_allow_html=True)
            
            st.markdown("<p><strong>Assessment Summary:</strong></p>", unsafe_allow_html=True)
            for recommendation in overall_recommendations:
                st.markdown(f"<p>• {recommendation}</p>", unsafe_allow_html=True)
            
            # Add crop-specific care advice if available
            if hasattr(st.session_state, 'crop_details') and st.session_state.crop_details:
                crop_details = st.session_state.crop_details
                if "best_season" in crop_details and crop_details["best_season"]:
                    st.markdown(f"<p><strong>Optimal Growing Season:</strong> {crop_details['best_season']}</p>", unsafe_allow_html=True)
                
                if "best_soil" in crop_details and crop_details["best_soil"]:
                    st.markdown(f"<p><strong>Ideal Soil Conditions:</strong> {crop_details['best_soil']}</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close assessment box
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close analysis section
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close structured report
        
        # Crop Information (if available)
        if hasattr(st.session_state, 'crop_details') and st.session_state.crop_details:
            st.markdown("---")
            st.markdown("<h2 class='fadeIn'>Detailed Crop Information</h2>", unsafe_allow_html=True)
            
            crop_details = st.session_state.crop_details
            
            # Create expandable sections for detailed information
            with st.expander("Crop Details", expanded=True):
                # Show varieties
                if "varieties" in crop_details and crop_details["varieties"]:
                    st.markdown("### Common Varieties")
                    varieties_html = '<div class="variety-container">'
                    for variety in crop_details["varieties"]:
                        varieties_html += f'<span class="variety-pill">{variety}</span>'
                    varieties_html += '</div>'
                    st.markdown(varieties_html, unsafe_allow_html=True)
                
                # Show growing information
                if "best_season" in crop_details and crop_details["best_season"]:
                    st.markdown(f"### Best Growing Season")
                    st.markdown(f"{crop_details['best_season']}")
                
                if "best_soil" in crop_details and crop_details["best_soil"]:
                    st.markdown(f"### Ideal Soil Type")
                    st.markdown(f"{crop_details['best_soil']}")
                
                if "time_period" in crop_details and crop_details["time_period"]:
                    st.markdown(f"### Growth Period")
                    st.markdown(f"{crop_details['time_period']}")
            
            # Show nutrient deficiencies if available
            if hasattr(st.session_state, 'deficiencies') and st.session_state.deficiencies:
                with st.expander("Common Nutrient Deficiencies", expanded=True):
                    deficiencies = st.session_state.deficiencies
                    for deficiency_name, deficiency_info in deficiencies.items():
                        st.markdown(f"<div class='deficiency-card'>", unsafe_allow_html=True)
                        st.markdown(f"<h3>{deficiency_name} Deficiency</h3>", unsafe_allow_html=True)
                        
                        if "symptoms" in deficiency_info:
                            st.markdown(f"<p><strong>Symptoms:</strong> {deficiency_info['symptoms']}</p>", unsafe_allow_html=True)
                        
                        if "treatment" in deficiency_info:
                            st.markdown(f"<p><strong>Treatment:</strong> {deficiency_info['treatment']}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
        
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
                    if isinstance(recommendation, dict):
                        # Format dictionary recommendations
                        st.markdown(f"<div class='fertilizer-rec'>", unsafe_allow_html=True)
                        st.markdown(f"<h4>{recommendation.get('name', 'Fertilizer')}</h4>", unsafe_allow_html=True)
                        if 'npk' in recommendation:
                            st.markdown(f"<p><strong>NPK Ratio:</strong> {recommendation['npk']}</p>", unsafe_allow_html=True)
                        if 'description' in recommendation:
                            st.markdown(f"<p>{recommendation['description']}</p>", unsafe_allow_html=True)
                        if 'application' in recommendation:
                            st.markdown(f"<p><strong>Application:</strong> {recommendation['application']}</p>", unsafe_allow_html=True)
                        if 'conditions' in recommendation:
                            st.markdown(f"<p><strong>Best For:</strong> {recommendation['conditions']}</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        # Handle string recommendations
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
        example_soil_images = {
            "assets/examples/soil1.jpg": "Black Soil Sample",
            "assets/examples/soil2.jpg": "Red Soil Sample",
            "assets/examples/soil3.jpg": "Sandy Soil Sample",
        }
        
        # Display example images in a grid
        cols = st.columns(3)
        for i, (image_path, description) in enumerate(example_soil_images.items()):
            with cols[i % 3]:
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
                    try:
                        # Preprocess the image
                        image = st.session_state.uploaded_soil_image
                        preprocessed_soil_image = preprocess_image(image)
                        
                        # Get soil analysis results
                        soil_results = analyze_soil(None, np.array(preprocessed_soil_image))
                        
                        # Ensure results are in proper dictionary format
                        if isinstance(soil_results, str):
                            # If it's just a string (soil type), convert to full structure
                            soil_results = {
                                "soil_type": soil_results,
                                "properties": {
                                    "ph": "Unknown",
                                    "organic_matter": "Unknown",
                                    "drainage": "Unknown"
                                },
                                "characteristics": "Basic analysis completed",
                                "suitability": {},
                                "recommendations": "Consult local agricultural expert for specific advice"
                            }
                        elif not isinstance(soil_results, dict):
                            # Fallback for unexpected formats
                            soil_results = {
                                "soil_type": "Unknown",
                                "properties": {
                                    "ph": "Unknown",
                                    "organic_matter": "Unknown",
                                    "drainage": "Unknown"
                                },
                                "characteristics": "Analysis completed",
                                "suitability": {},
                                "recommendations": "Results format unexpected"
                            }
                        
                        # Update session state
                        st.session_state.soil_results = soil_results
                        st.session_state.soil_analysis_complete = True
                        
                        # Save to history
                        save_to_history("soil", soil_results)
                    
                    except Exception as e:
                        st.error(f"Error during soil analysis: {str(e)}")
                        st.session_state.soil_analysis_complete = False
                
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
            
            # Get soil type safely
            soil_type = soil_results.get("soil_type") if isinstance(soil_results, dict) else str(soil_results)
            st.markdown(f"**Identified Soil Type:** {soil_type}")
            
            # Display soil properties
            st.markdown("### Soil Properties")
            
            properties = soil_results.get("properties", {}) if isinstance(soil_results, dict) else {
                "ph": "Unknown",
                "organic_matter": "Unknown",
                "drainage": "Unknown"
            }
            
            # Create a two-column layout for properties
            prop_col1, prop_col2 = st.columns(2)
            
            with prop_col1:
                st.markdown(f"**pH Value:** {properties.get('ph', 'Unknown')}")
                st.markdown(f"**Organic Matter:** {properties.get('organic_matter', 'Unknown')}")
            
            with prop_col2:
                st.markdown(f"**Drainage:** {properties.get('drainage', 'Unknown')}")
        
        with col2:
            # Soil characteristics
            st.markdown("### Characteristics")
            
            if isinstance(soil_results, dict):
                characteristics = soil_results.get("characteristics", "Information not available.")
            else:
                characteristics = "Basic analysis completed. Detailed characteristics not available."
            
            st.markdown(characteristics)
            
            # Crop suitability
            st.markdown("### Crop Suitability")
            
            suitability = soil_results.get("suitability", {}) if isinstance(soil_results, dict) else {}
            
            if suitability:
                for crop, suitability_text in suitability.items():
                    st.markdown(f"**{crop.title()}:** {suitability_text}")
            else:
                st.info("No specific crop suitability information available.")
            
            # Recommendations
            st.markdown("### Recommendations")
            
            if isinstance(soil_results, dict):
                recommendations = soil_results.get("recommendations", "No specific recommendations available.")
            else:
                recommendations = "Consult with local agricultural expert for specific advice."
            
            st.markdown(recommendations)
        
        # Visualize soil properties
        st.markdown("---")
        st.markdown("## Soil Analysis Visualization")
        
        # Create a simple visualization of soil properties
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Parse pH value safely
        try:
            ph_str = str(properties.get('ph', '7.0'))
            ph_value = float(ph_str) if ph_str.replace('.', '').isdigit() else 7.0
        except ValueError:
            ph_value = 7.0
        
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
        ax.set_title(f'Soil pH Analysis: {ph_value} ({properties.get("ph", "Unknown")})')
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
            # Create report content
            report_md = f"""
            # Soil Analysis Report
            
            ## Soil Classification
            - **Identified Soil Type:** {soil_type}
            
            ## Soil Properties
            - **pH Value:** {properties.get('ph', 'Unknown')}
            - **Organic Matter:** {properties.get('organic_matter', 'Unknown')}
            - **Drainage:** {properties.get('drainage', 'Unknown')}
            
            ## Characteristics
            {characteristics}
            
            ## Crop Suitability
            """
            
            if suitability:
                for crop, suitability_text in suitability.items():
                    report_md += f"- **{crop.title()}:** {suitability_text}\n"
            else:
                report_md += "No specific crop suitability information available.\n"
            
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
    
    # Check if we need to show details for a specific analysis
    if "selected_analysis_id" in st.session_state:
        selected_analysis = next((a for a in filtered_history if a["id"] == st.session_state.selected_analysis_id), None)
        if selected_analysis:
            show_analysis_details(selected_analysis)
            if st.button("Back to History"):
                del st.session_state.selected_analysis_id
                st.rerun()
            return
    
    # Create tabs for different view types
    tab1, tab2 = st.columns(2)  # Changed from tabs to columns for better layout
    
    with tab1:
        # Simple list view
        st.markdown("#### Analysis List")
        for i, analysis in enumerate(filtered_history):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
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
                    if st.button("View Details", key=f"view_details_{analysis['id']}"):
                        st.session_state.selected_analysis_id = analysis["id"]
                        st.rerun()
                
                st.markdown("---")

def show_analysis_details(analysis):
    """Display detailed view of a single analysis"""
    st.markdown(f"## Detailed Analysis - {analysis['timestamp'][:10]}")
    
    # Display analysis details based on type
    if analysis["analysis_type"] == "plant":
        st.markdown("### 🌱 Plant Health Analysis")
        
        # Get results
        results = analysis.get("results", {})
        plant_info = results.get("plant_info", {})
        diseases = results.get("diseases", {})
        pests = results.get("pests", {})
        water_content = results.get("water_content", {})
        preventive_measures = results.get("preventive_measures", [])
        fertilizer_recommendations = results.get("fertilizer_recommendations", [])
        
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
            
            st.markdown("### Water Content")
            st.markdown(f"**Status:** {water_content.get('status', 'Unknown')}")
            st.markdown(f"**Percentage:** {water_content.get('percentage', 'Unknown')}%")
        
        with col2:
            st.markdown("### Disease & Pest Information")
            
            if diseases.get("detected", False):
                st.markdown("**Diseases Detected:** Yes")
                for disease in diseases.get("diseases", []):
                    st.markdown(f"- {disease.get('name', 'Unknown')} ({format_probability(disease.get('confidence', 0))}%)")
                    if "treatment" in disease:
                        st.markdown(f"  - Treatment: {disease['treatment']}")
            else:
                st.markdown("**Diseases Detected:** No")
            
            if pests.get("detected", False):
                st.markdown("**Pests Detected:** Yes")
                for pest in pests.get("pests", []):
                    st.markdown(f"- {pest.get('name', 'Unknown')} (Level: {pest.get('infestation_level', 'Unknown')}")
                    if "treatment" in pest:
                        st.markdown(f"  - Treatment: {pest['treatment']}")
            else:
                st.markdown("**Pests Detected:** No")
        
                # Recommendations
        st.markdown("### Recommendations")
        
        if preventive_measures:
            st.markdown("**Preventive Measures:**")
            for measure in preventive_measures:
                st.markdown(f"- {measure}")
        
        if fertilizer_recommendations:
            st.markdown("### Fertilizer Recommendations")
            
            # Create tabs for different fertilizer types if they exist
            fertilizer_types = set()
            for rec in fertilizer_recommendations:
                if isinstance(rec, dict) and 'type' in rec:
                    fertilizer_types.add(rec['type'].title())
            
            if fertilizer_types:
                tabs = st.tabs([f"{ftype}" for ftype in sorted(fertilizer_types)] + ["All"])
            else:
                tabs = [st.container()]
            
            # Organize recommendations by type
            typed_recommendations = {}
            for rec in fertilizer_recommendations:
                if isinstance(rec, dict):
                    ftype = rec.get('type', 'other').title()
                    if ftype not in typed_recommendations:
                        typed_recommendations[ftype] = []
                    typed_recommendations[ftype].append(rec)
                else:
                    if 'other' not in typed_recommendations:
                        typed_recommendations['other'] = []
                    typed_recommendations['other'].append(rec)
            
            # Display in tabs
            for i, (ftype, tab) in enumerate(zip(sorted(typed_recommendations.keys()), tabs)):
                with tab:
                    for rec in typed_recommendations[ftype]:
                        if isinstance(rec, dict):
                            with st.expander(f"🔹 {rec.get('name', 'Fertilizer')}"):
                                # Create a nice card-like display
                                col1, col2 = st.columns([1, 3])
                                
                                with col1:
                                    # Display NPK ratio with colored badges
                                    if 'npk' in rec:
                                        npk = rec['npk'].split('-')
                                        if len(npk) == 3:
                                            st.markdown("""
                                            <style>
                                                .npk-badge {
                                                    display: inline-block;
                                                    padding: 2px 8px;
                                                    border-radius: 12px;
                                                    font-weight: bold;
                                                    font-size: 0.8em;
                                                    margin: 2px;
                                                }
                                                .npk-N { background-color: #4CAF50; color: white; }
                                                .npk-P { background-color: #2196F3; color: white; }
                                                .npk-K { background-color: #FF9800; color: black; }
                                            </style>
                                            """, unsafe_allow_html=True)
                                            
                                            st.markdown(f"""
                                            <div style="margin-bottom: 10px;">
                                                <span class="npk-badge npk-N">N: {npk[0]}</span>
                                                <span class="npk-badge npk-P">P: {npk[1]}</span>
                                                <span class="npk-badge npk-K">K: {npk[2]}</span>
                                            </div>
                                            """, unsafe_allow_html=True)
                                
                                with col2:
                                    st.markdown(f"**Type:** {rec.get('type', 'N/A').title()}")
                                    
                                    if 'description' in rec:
                                        st.markdown(f"**Description:** {rec['description']}")
                                    
                                    if 'application' in rec:
                                        st.markdown(f"**Application:** {rec['application']}")
                                    
                                    if 'conditions' in rec:
                                        st.markdown(f"**Best For:** {rec['conditions']}")
                                    
                                    if 'scientific_backing' in rec:
                                        st.markdown(f"*Scientific Backing:* {rec['scientific_backing']}", unsafe_allow_html=True)
                        else:
                            st.markdown(f"- {rec}")
            
            # If there's only one type, don't show tabs
            if len(fertilizer_types) <= 1:
                tabs[0].empty()  # Clear the single tab
                for rec in fertilizer_recommendations:
                    if isinstance(rec, dict):
                        with st.expander(f"🔹 {rec.get('name', 'Fertilizer')}"):
                            # Same card display as above
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                if 'npk' in rec:
                                    npk = rec['npk'].split('-')
                                    if len(npk) == 3:
                                        st.markdown(f"""
                                        <div style="margin-bottom: 10px;">
                                            <span class="npk-badge npk-N">N: {npk[0]}</span>
                                            <span class="npk-badge npk-P">P: {npk[1]}</span>
                                            <span class="npk-badge npk-K">K: {npk[2]}</span>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"**Type:** {rec.get('type', 'N/A').title()}")
                                
                                if 'description' in rec:
                                    st.markdown(f"**Description:** {rec['description']}")
                                
                                if 'application' in rec:
                                    st.markdown(f"**Application:** {rec['application']}")
                                
                                if 'conditions' in rec:
                                    st.markdown(f"**Best For:** {rec['conditions']}")
                                
                                if 'scientific_backing' in rec:
                                    st.markdown(f"*Scientific Backing:* {rec['scientific_backing']}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {rec}")

    
    # Generate report button
    if st.button("Generate Report"):
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
    """Display the full weather analysis page"""
    # Get location from profile or user input
    location = get_profile_field(st.session_state.user_profile, "location")
    if not location:
        location = st.text_input("Enter your location (city, country):")
        if not location:
            st.warning("Please enter a location to view weather data")
            return
    
    # Simply call the weather service's full page display
    from weather_service import show_weather_page as show_weather_service_page
    show_weather_service_page()

# Main app logic
def main():
    """Main application logic"""
    # Show header for all pages except login/signup
    if st.session_state.page not in ["login", "signup"]:
        show_header()
    
    # Language selector in sidebar (would be implemented in full app)
    if st.session_state.page not in ["login", "signup"]:
        with st.sidebar:
                lang = initialize_language()

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

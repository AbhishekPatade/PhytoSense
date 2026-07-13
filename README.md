# 🌿 PhytoSense – AI-Powered Smart Crop Advisory System

## Overview

PhytoSense is an AI-powered smart agriculture platform designed to help farmers identify plant diseases, analyze soil conditions, monitor weather, and receive intelligent crop recommendations. The platform combines image processing, machine learning, and agricultural datasets to provide real-time insights that improve crop health and productivity.

## Features

* 🌱 Plant disease detection using AI
* 📷 Image-based crop health analysis
* 🌍 Weather-aware crop recommendations
* 🌾 Soil analysis and suitability checking
* 📊 Crop recommendation engine
* 🌐 Multi-language support
* 👤 User profile management
* 💾 Local database support
* 📈 Detailed plant health reports

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & Machine Learning

* Custom Machine Learning Models
* Image Processing

### Database

* SQLite

### Libraries

* Streamlit
* OpenCV
* NumPy
* Pillow
* SQLite3
* Requests

## Project Structure

```text
PhytoSense/
│
├── app.py
├── model.py
├── model_handler.py
├── image_processing.py
├── plant_analysis.py
├── soil_analyzer.py
├── weather_service.py
├── recommendations.py
├── crop_database.py
├── language_support.py
├── assets/
├── translations/
├── uploads/
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/AbhishekPatade/PhytoSense.git
cd PhytoSense
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If your project uses `pyproject.toml` instead of `requirements.txt`:

```bash
pip install .
```

## Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

## Future Enhancements

* Cloud deployment on AWS
* Mobile application integration
* IoT sensor support
* Drone-based crop monitoring
* Real-time satellite data integration
* Farmer analytics dashboard
* AI chatbot for agricultural guidance

## Contributors

**Abhishek Patade**

## License

This project is intended for educational and research purposes.

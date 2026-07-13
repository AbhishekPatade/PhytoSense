# 🌿 PhytoSense – AI-Powered Smart Crop Advisory System

## 📌 Overview

PhytoSense is an AI-powered Smart Crop Advisory System designed to assist farmers in identifying plant diseases, analyzing soil conditions, monitoring weather, and receiving intelligent crop recommendations. The platform combines Artificial Intelligence, Image Processing, and Agricultural datasets to provide accurate insights for improving crop health and productivity.

---

## 🚀 Features

* 🌱 AI-based Plant Disease Detection
* 📷 Image Processing using Computer Vision
* 🌦️ Weather-based Crop Recommendations
* 🌾 Soil Analysis and Suitability Prediction
* 📊 Intelligent Crop Recommendation System
* 🌍 Multi-language Support
* 👤 Farmer Profile Management
* 💾 Local SQLite Database
* 📈 Detailed Crop Health Reports

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & Machine Learning

* Image Processing
* Machine Learning Models

### Database

* SQLite

### Libraries

* Streamlit
* OpenCV
* Pillow
* NumPy
* SQLite3

---

## 📂 Project Structure

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
├── uploads/
├── translations/
├── weather_data/
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── README.md
```

---

# 🐳 Docker Support

## Build Docker Image

```bash
docker build -t phytosense .
```

## Run Docker Container

```bash
docker run -d -p 8501:8501 --name phytosense phytosense
```

Open your browser:

```text
http://localhost:8501
```

or on AWS EC2:

```text
http://<EC2-PUBLIC-IP>:8501
```

---

## Docker Commands

### Build Image

```bash
docker build -t phytosense .
```

### View Images

```bash
docker images
```

### Run Container

```bash
docker run -d -p 8501:8501 --name phytosense phytosense
```

### Running Containers

```bash
docker ps
```

### Stop Container

```bash
docker stop phytosense
```

### Start Container

```bash
docker start phytosense
```

### Remove Container

```bash
docker rm phytosense
```

### View Logs

```bash
docker logs phytosense
```

---

# 💻 Local Installation

Clone the repository:

```bash
git clone https://github.com/AbhishekPatade/PhytoSense.git

cd PhytoSense
```

Install dependencies:

```bash
pip install .
```

Run the application:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# ☁️ Deployment

PhytoSense can be deployed on:

* Docker
* AWS EC2
* Azure Virtual Machine
* Google Cloud VM
* Render
* Railway
* Streamlit Community Cloud

---

# 👨‍💻 Author

**Abhishek Patade**

Computer Engineering Student | Full Stack Developer | Cloud & DevOps Enthusiast

GitHub: https://github.com/AbhishekPatade

---

# 📄 License

This project is developed for educational, research, and demonstration purposes.

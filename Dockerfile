
# Base Image
# -------------------------------
FROM python:3.12-slim

# Environment Variables
# -------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working Directory
# -------------------------------
WORKDIR /app

# Install System Dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Dependency Files
# -------------------------------
COPY pyproject.toml ./
COPY uv.lock ./

# Install Python Dependencies
# -------------------------------
RUN pip install --upgrade pip && \
    pip install .

# Copy Application Source
# -------------------------------
COPY . .

# Create Upload Directory
# -------------------------------
RUN mkdir -p uploads

# Expose Streamlit Port
# -------------------------------
EXPOSE 8501

# Start Streamlit
# -------------------------------
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
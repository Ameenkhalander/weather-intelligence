# 🌦️ Weather Intelligence Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/API-Open--Meteo-green" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

<p align="center">
  🌍 Explore weather conditions across the world with an interactive and data-driven dashboard.
</p>

---

## 📌 About The Project

**Weather Intelligence Dashboard** is an interactive weather analytics application built using Python and Streamlit. It provides real-time weather information, forecasts, air quality insights, and activity recommendations for cities around the world.

The application transforms weather data into meaningful visual insights through interactive charts, maps, and analytics.

## ✨ Features

- 🌍 **Global City Search** – Explore weather conditions across multiple countries and cities.
- 🌡️ **Current Weather** – View temperature, humidity, wind speed, and other weather conditions.
- ⏱️ **Hourly Forecast** – Analyze upcoming weather changes.
- 📅 **7-Day Forecast** – Plan your week with weather predictions.
- 🍃 **Air Quality Monitoring** – Explore air quality information.
- 🏃 **Activity Planner** – Discover suitable outdoor activities based on weather conditions.
- 📊 **Weather Analytics** – Visualize weather trends using interactive charts.
- ⚖️ **City Comparison** – Compare weather conditions between different locations.
- 🗺️ **Interactive Weather Map** – Explore locations visually.
- ⭐ **Favorite Cities** – Save your preferred locations.
- 🎨 **Customizable Dashboard** – Personalize the dashboard experience.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing |
| NumPy | Numerical operations |
| Plotly | Interactive visualizations |
| Requests | API communication |
| Open-Meteo API | Weather and forecast data |

## 📂 Project Structure

```text
Weather-Intelligence/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
│
└── .gitignore          # Files excluded from Git
```

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/weather-intelligence.git
```

### 2️⃣ Navigate to the Project

```bash
cd weather-intelligence
```

### 3️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🌐 API Used

This project uses the **Open-Meteo API** to retrieve weather and forecast information.

- 🌤️ Weather Forecast API: https://open-meteo.com/en/docs
- 📍 Geocoding API: https://open-meteo.com/en/docs/geocoding-api

## 🚀 Deployment

The application can be deployed using **Streamlit Community Cloud**.

1. Push your project to GitHub.
2. Visit https://share.streamlit.io/
3. Connect your GitHub account.
4. Select your repository.
5. Choose `app.py` as the main file.
6. Click **Deploy**.








<p align="center">
  ⭐ If you find this project interesting, consider giving it a star!
  <br/>
  💙 Built with Python, Streamlit, and curiosity.
</p>

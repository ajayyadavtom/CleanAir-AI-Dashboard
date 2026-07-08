import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from PIL import Image
import time
import datetime
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="CleanAir AI Municipal Dashboard", layout="wide", page_icon="🌍")

# --- MOCK DATA GENERATION ---
# Centered around North Bengaluru / Yelahanka for hyper-local testing
def generate_mock_sensor_data():
    np.random.seed(42)
    lats = np.random.uniform(13.0900, 13.1200, 15)
    lons = np.random.uniform(77.5800, 77.6200, 15)
    aqi = np.random.randint(50, 300, 15)
    types = np.random.choice(['Traffic', 'Industrial', 'Garbage Burn', 'Dust'], 15)
    return pd.DataFrame({'Lat': lats, 'Lon': lons, 'AQI': aqi, 'Source': types})

sensor_data = generate_mock_sensor_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🛠️ CleanAir AI")
st.sidebar.markdown("### Municipal Dispatch System")
nav = st.sidebar.radio("Navigation", ["🗺️ Live Pollution Map", "📸 Citizen AI Reporting", "📈 24-Hr Predictive Analytics"])

# --- PAGE 1: LIVE POLLUTION MAP ---
if nav == "🗺️ Live Pollution Map":
    st.title("Live Hyper-Local Pollution Hotspots")
    st.markdown("Fusing satellite baseline data with localized IoT sensor readings.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create map
        m = folium.Map(location=[13.1007, 77.5963], zoom_start=14, tiles="CartoDB dark_matter")
        for idx, row in sensor_data.iterrows():
            color = "green" if row['AQI'] < 100 else "orange" if row['AQI'] < 200 else "red"
            folium.CircleMarker(
                location=[row['Lat'], row['Lon']],
                radius=row['AQI']/15,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"AQI: {row['AQI']} | Source: {row['Source']}"
            ).add_to(m)
        st_folium(m, width=800, height=500)
        
    with col2:
        st.subheader("🚨 Active Alerts")
        high_risk = sensor_data[sensor_data['AQI'] > 200]
        for idx, row in high_risk.iterrows():
            st.error(f"**Critical Hotspot!**\nAQI: {row['AQI']}\nSuspected: {row['Source']}")
            if st.button(f"Dispatch Water-Mist to Loc {idx}"):
                st.success("Resource Deployed!")

# --- PAGE 2: CITIZEN AI REPORTING ---
elif nav == "📸 Citizen AI Reporting":
    st.title("Citizen Crowdsourcing & AI Triangulation")
    st.markdown("Upload photos of smoke/dust. Our CV model detects severity and coordinates.")
    
    uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Citizen Upload', use_column_width=True)
        
        if st.button("Run Computer Vision Analysis"):
            with st.spinner("Analyzing particulate density and extracting EXIF GPS data..."):
                time.sleep(2.5) # Simulate complex AI inference
                
            st.success("AI Analysis Complete!")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Detection Threat", "87% Confidence", "Garbage Fire")
            c2.metric("Extracted Latitude", "13.1054")
            c3.metric("Extracted Longitude", "77.5982")
            
            st.warning("⚠️ Triangulating with satellite data... confirmed thermal anomaly at coordinates. Generating alert for cleanup crew.")

# --- PAGE 3: PREDICTIVE ANALYTICS ---
elif nav == "📈 24-Hr Predictive Analytics":
    st.title("AI Spike Prediction Engine")
    st.markdown("Using historical localized data to predict AQI spikes before they hit city-level monitors.")
    
    # Generate fake 24 hour data
    hours = [f"{i}:00" for i in range(24)]
    base_aqi = 150
    predictions = [base_aqi + (np.sin(i/3) * 50) + np.random.randint(-10, 10) for i in range(24)]
    
    df_pred = pd.DataFrame({"Time": hours, "Predicted AQI": predictions})
    
    fig = px.line(df_pred, x="Time", y="Predicted AQI", title="24-Hour Hyper-Local AQI Forecast", markers=True)
    fig.add_hline(y=200, line_dash="dash", line_color="red", annotation_text="Hazardous Threshold")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("System recommends deploying anti-smog guns to Sector 4 at 14:00 based on predicted wind dispersion models.")


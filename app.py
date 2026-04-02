import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="DDoS Detection System",
    layout="wide",
    page_icon="🛡️"
)

# -------------------------------
# LOAD MODEL COMPONENTS
# -------------------------------
@st.cache_resource
def load_components():
    try:
        model = joblib.load("model.pkl")
        scaler = joblib.load("scaler.pkl")
        feature_names = joblib.load("features.pkl")

        # ✅ Load accuracy (new)
        try:
            accuracy = joblib.load("accuracy.pkl")
        except:
            accuracy = None

        return model, scaler, feature_names, accuracy

    except Exception as e:
        st.error(f"Error loading model files: {e}")
        return None, None, None, None


model, scaler, feature_names, accuracy = load_components()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🛡️ Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Upload Data",
    "Live Detection",
    "Model Insights",
    "About"
])

# -------------------------------
# HOME PAGE
# -------------------------------
if page == "Home":
    st.title("🚀 Network Traffic Analyser for Multi-Attack DDoS Detection and Mitigation")
    st.subheader("Detect, classify, and mitigate DDoS attacks using Machine Learning")

    st.markdown("---")

    st.write("### 🔍 Attack Types Covered")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.error("🔥 SYN Flood Attack")
        st.warning("🌊 UDP Flood Attack")

    with col2:
        st.info("📡 ICMP Flood Attack")
        st.error("🐢 Slowloris Attack")

    with col3:
        st.success("✅ Normal Traffic")

# -------------------------------
# UPLOAD DATA
# -------------------------------
elif page == "Upload Data":
    st.title("📂 Upload Network Data")

    # ✅ Show model accuracy
    st.write("### 📊 Model Accuracy")
    if accuracy is not None:
        st.metric("Accuracy", f"{accuracy:.2%}")
    else:
        st.warning("⚠️ Accuracy not available")

    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file:
        df = pd.read_csv(file)

        st.write("### 👀 Data Preview")
        st.dataframe(df.head(10))

        if st.button("🚀 Run Detection"):
            with st.spinner("Analyzing network traffic..."):
                time.sleep(2)

                if model is not None and scaler is not None and feature_names is not None:

                    try:
                        # ✅ Match training features
                        df_model = df.copy()
                        df_model = df_model.reindex(columns=feature_names, fill_value=0)

                        # ✅ Apply scaling
                        df_scaled = scaler.transform(df_model)

                        # ✅ Predict
                        predictions = model.predict(df_scaled)

                    except Exception as e:
                        st.error(f"Prediction error: {e}")
                        predictions = ["Error"] * len(df)

                else:
                    st.error("Model not loaded properly!")
                    predictions = ["No Model"] * len(df)

                df["Prediction"] = predictions

                st.success("Detection Completed!")

                st.write("### 📊 Results")
                st.dataframe(df.head(20))

                # 📊 Attack distribution
                st.write("### 📊 Attack Distribution")
                attack_counts = pd.Series(predictions).value_counts()
                st.bar_chart(attack_counts)

                # Download option
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download Results",
                    csv,
                    "results.csv",
                    "text/csv"
                )

# -------------------------------
# LIVE DETECTION (SIMULATION)
# -------------------------------
elif page == "Live Detection":
    st.title("📡 Live Traffic Simulation")
    st.warning("⚠️ This is a simulation (not real model prediction)")

    if st.button("Start Monitoring"):
        for i in range(5):
            time.sleep(1)

            attack = np.random.choice(
                ["SYN Flood", "UDP Flood", "ICMP Flood", "Slowloris", "Normal"]
            )

            if attack == "Normal":
                st.success("✅ Traffic Normal")
            else:
                st.error(f"⚠️ Attack Detected: {attack}")

# -------------------------------
# MODEL INSIGHTS
# -------------------------------
elif page == "Model Insights":
    st.title("📊 Model Insights")

    st.write("### Model Status")

    if model is not None:
        st.success("✅ Model Loaded Successfully")
    else:
        st.error("❌ Model Not Loaded")

    # ✅ Show accuracy here also
    if accuracy is not None:
        st.success(f"🎯 Model Accuracy: {accuracy:.2%}")

    st.write("### Feature Names Used")
    if feature_names is not None:
        st.write(feature_names)

    st.write("### Feature Importance")

    try:
        importance = model.feature_importances_
        idx = np.argsort(importance)[::-1]

        fig, ax = plt.subplots()
        ax.bar(range(len(feature_names)), importance[idx])
        ax.set_xticks(range(len(feature_names)))
        ax.set_xticklabels([feature_names[i] for i in idx], rotation=45)
        ax.set_title("Feature Importance")

        st.pyplot(fig)

    except:
        st.info("Feature importance not available.")

# -------------------------------
# ABOUT
# -------------------------------
elif page == "About":
    st.title("ℹ️ About This Project")

    st.write("""
    This project is a Machine Learning-based Network Traffic Analyzer designed to detect and classify
    multiple types of DDoS attacks.

    🔹 Built using:
    - Random Forest Classifier
    - Streamlit Web App
    - Real network traffic datasets

    🔹 Features:
    - Upload CSV for batch detection
    - Attack classification
    - Visualization of results

    Developed as a practical cybersecurity + ML project.
    """)

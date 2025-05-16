import streamlit as st
import os
import shutil
from main import Model

# Set up folders
TEMP_DIR = "temp"
# ARCHIVE_DIR = "arcive"
os.makedirs(TEMP_DIR, exist_ok=True)
# os.makedirs(ARCHIVE_DIR, exist_ok=True)

st.title("AI vs Human Image Detector")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save to temp folder
    temp_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(temp_path, "wb") as f:
        file_data = uploaded_file.read()
        f.write(file_data)
        print(f"Upload temp: path:{temp_path}")

    # Show uploaded image
    st.image(temp_path, caption="Uploaded Image", use_column_width=True)

    # Predict
    prediction = Model.predict(temp_path)
    print(f"app.py :- prediction value:{prediction}")
    # Display result
    if prediction < 0.5:
        st.success(f"🧠 This image is likely **Human-Generated**. \nConfodence:  {((1-prediction)*100):.2f}")
    else:
        st.warning(f"🤖 This image is likely **AI-Generated**. \nConfodence:  {(prediction*100):.2f}")


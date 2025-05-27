# import streamlit as st
# import os
# import shutil
# from server.main import Model

# # Set up folders
# TEMP_DIR = "temp"
# # ARCHIVE_DIR = "arcive"
# os.makedirs(TEMP_DIR, exist_ok=True)
# # os.makedirs(ARCHIVE_DIR, exist_ok=True)

# st.title("AI vs Human Image Detector")

# uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# if uploaded_file is not None:
#     # Save to temp folder
#     temp_path = os.path.join(TEMP_DIR, uploaded_file.name)
#     with open(temp_path, "wb") as f:
#         file_data = uploaded_file.read()
#         f.write(file_data)
#         print(f"Upload temp: path:{temp_path}")

#     # Show uploaded image
#     st.image(temp_path, caption="Uploaded Image", use_column_width=True)

#     # Predict
#     prediction = Model.predict(temp_path)
#     print(f"app.py :- prediction value:{prediction}")
#     # Display result
#     if prediction < 0.5:
#         st.success(f"🧠 This image is likely **Human-Generated**. \nConfodence:  {((1-prediction)*100):.2f}")
#     else:
#         st.warning(f"🤖 This image is likely **AI-Generated**. \nConfodence:  {(prediction*100):.2f}")

from flask import Flask, render_template, jsonify, request
from main import Model
import os

# Set base directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'client', 'pages')
STATIC_FOLDER = os.path.join(BASE_DIR, 'client', 'static')

# Create temp folder if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'server', 'temp'), exist_ok=True)

# Initialize Flask app
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

@app.route('/')
def get_index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
@app.route('/analyze', methods=['POST'])
def predict():
    if 'image' not in request.files:
        print("No image in request")
        return jsonify({'error': 'No image field in request'})

    file = request.files['image']
    if file.filename == '':
        print("Empty filename")
        return jsonify({'error': 'No file selected'})

    if file:
        try:
            temp_path = os.path.join('temp', file.filename)
            file_path = os.path.join(os.path.dirname(__file__), temp_path)
            file.save(file_path)

            print(f"Saved file to {file_path}")
            prediction = Model.predict(file_path)
            print(f"Prediction value: {prediction}")

            if prediction < 0.5:
                result = f"🧠 This image is likely **Human-Generated**. Confidence: {((1 - prediction) * 100):.2f}%"
            else:
                result = f"🤖 This image is likely **AI-Generated**. Confidence: {(prediction * 100):.2f}%"

            print(f"Final result: {result}")
            return jsonify({"result": result})
        except Exception as e:
            print(f"Prediction error: {e}")
            return jsonify({'error': f'Prediction failed: {str(e)}'})

    return jsonify({'error': 'File processing failed'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, jsonify, request
from main import Model
import os
import shutil
# Set base directory paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'client', 'pages')
STATIC_FOLDER = os.path.join(BASE_DIR, 'client', 'static')

# Create temp folder if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'server', 'temp'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'server',"archive"), exist_ok=True)
# Initialize Flask app
app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

@app.route('/')
def get_index():
    return render_template('index.html')

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
            # Move the file to the archive folder
            archived_path = os.path.join("archive", file.filename)
            shutil.move(file_path, archived_path)
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

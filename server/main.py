import tensorflow as tf
import numpy as np

from tkinter import Tk, filedialog
import cv2
import os

def get_image_from_user():
    # Create a temp directory if it doesn't exist
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Hide the root Tkinter window
    root = Tk()
    root.withdraw()

    # Ask user to select an image file
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if file_path:
        # Read image using OpenCV
        image = cv2.imread(file_path)

        if image is None:
            raise Exception("Failed to read the image.")

        # Get filename and build new path
        filename = os.path.basename(file_path)
        temp_image_path = os.path.join(temp_dir, filename)

        # Save a copy of the image to the temp folder
        cv2.imwrite(temp_image_path, image)

        return temp_image_path

    return None


class Model:
    model = None
    model_path = os.path.join(os.path.dirname(__file__), 'AI_imageDetect3.h5')

    @staticmethod
    def load_model():
        if Model.model is None:
            if not os.path.exists(Model.model_path):
                raise FileNotFoundError(f"Model file not found: {Model.model_path}")
            Model.model = tf.keras.models.load_model(Model.model_path)

    @staticmethod
    def predict(img_path):
        Model.load_model()

        try:
            # Load and preprocess image using OpenCV
            img = cv2.imread(img_path)
            if img is None:
                raise Exception("Image could not be loaded.")

            img = cv2.resize(img, (128, 128))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            img_array = np.expand_dims(img, axis=0) / 255.0

            prediction = Model.model.predict(img_array)
            return float(prediction[0][0])

        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")


# Example usage
# image_path = get_image_from_user()
# result = Model.predict(image_path)
# print("Prediction: ", result * 100)

import tensorflow as tf
import cv2 as cv
import numpy as np

from tkinter import Tk, filedialog
from PIL import Image

import os
import shutil

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
        # Load the image
        image = Image.open(file_path)

        # Get filename and build new path
        filename = os.path.basename(file_path)
        temp_image_path = os.path.join(temp_dir, filename)

        # Save a copy of the image to the temp folder
        image.save(temp_image_path)

        return temp_image_path

    return None


# Example usage:
# img = get_image_from_user()
# img.show()
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
            img = tf.keras.preprocessing.image.load_img(img_path, target_size=(128, 128))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0
            prediction = Model.model.predict(img_array)
            return float(prediction[0][0])
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
# image_path = get_image_from_user()
# # image.show()
# model = Model()
# result = model.predict(image_path)
# print("Prediction: ",result*100)
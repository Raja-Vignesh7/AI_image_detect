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
    @staticmethod
    def predict(image_path):
        model = tf.keras.models.load_model("AI_imageDetect3.h5")
        image = cv.imread(image_path)

        image = cv.resize(image, (444, 444))
        image = image.astype('float32') / 255.0
        image = np.expand_dims(image, axis=0)

        predict = model.predict(image)
        
        # ===== OPTION 1: Delete the image file after prediction =====
        # if os.path.exists(image_path):
        #     os.remove(image_path)

        # ===== OPTION 2: Move the image to an "archive" folder =====
        archive_folder = "archive"
        os.makedirs(archive_folder, exist_ok=True)
        archived_path = os.path.join(archive_folder, os.path.basename(image_path))
        shutil.move(image_path, archived_path)
        print(predict[0][1])
        return predict[0][1]
    
# image_path = get_image_from_user()
# # image.show()
# model = Model()
# result = model.predict(image_path)
# print("Prediction: ",result*100)
from tkinter import Tk, filedialog
import tensorflow as tf
import tensorflow_hub as hub
import tf_keras as keras  # Stick to this one
import numpy as np
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


# ... (get_image_from_user function remains the same)

class Model:
    model = None
    # Use absolute path to avoid "File not found" issues
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mobilenet_model_AI.keras')

    @staticmethod
    def load_model():
        if Model.model is None:
            if not os.path.exists(Model.model_path):
                raise FileNotFoundError(f"Model file not found at: {Model.model_path}")
            
            custom_objects = {"KerasLayer": hub.KerasLayer}
            
            try:
                # 1. Pass path as a POSITIONAL argument
                # 2. Use the 'keras' alias we set to 'tf_keras'
                Model.model = keras.models.load_model(
                    Model.model_path, 
                    custom_objects=custom_objects,
                    compile=False
                )
                
                # Re-compile manually to ensure compatibility
                Model.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
                print("✅ Model loaded successfully!")
            except Exception as e:
                print(f"❌ Loading failed: {e}")
    @staticmethod
    def predict(img_path):
        Model.load_model()

        try:
            # Load and preprocess image using OpenCV
            img = cv2.imread(img_path)
            if img is None:
                raise Exception("Image could not be loaded.")

            img = cv2.resize(img, (224, 224))
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            img_array = np.expand_dims(img, axis=0) / 255.0

            prediction = Model.model.predict(img_array)
            print("Raw prediction output: ", prediction)
            return float(prediction[0][1])

        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
# class Model:
#     model = None
#     model_path = os.path.join(os.path.dirname(__file__), 'mobilenet_model_AI.keras')

#     @staticmethod
#     def load_model():
#         if Model.model is None:
#             if not os.path.exists(Model.model_path):
#                 raise FileNotFoundError(f"Model file not found: {Model.model_path}")
#             # Model.model = tf.keras.models.load_model(Model.model_path)
#             custom_objects = {
#                 "KerasLayer": hub.KerasLayer
#             }
#             # Model.model = tf.keras.models.load_model(Model.model_path, custom_objects={'KerasLayer': hub.KerasLayer})
#             try:
#                 # Use keras.models instead of tf.keras.models if you're on Keras 3
#                 Model.model = keras.models.load_model(
#                     model_path=Model.model_path, 
#                     custom_objects=custom_objects,
#                     compile=False # Loading without compiling helps bypass optimizer errors
#                 )
#                 Model.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#                 print("Model loaded successfully!")
#             except Exception as e:
#                 print(f"Loading failed: {e}")

#     @staticmethod
#     def predict(img_path):
#         Model.load_model()

#         try:
#             # Load and preprocess image using OpenCV
#             img = cv2.imread(img_path)
#             if img is None:
#                 raise Exception("Image could not be loaded.")

#             img = cv2.resize(img, (224, 224))
#             # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
#             img_array = np.expand_dims(img, axis=0) / 255.0

#             prediction = Model.model.predict(img_array)
#             print("Raw prediction output: ", prediction)
#             return float(prediction[0][1])

#         except Exception as e:
#             raise Exception(f"Prediction failed: {str(e)}")


# Example usage
# image_path = get_image_from_user()
# result = Model.predict(image_path)
# print("Prediction: ", result * 100)

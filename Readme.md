#  AI vs Natural Detector

In this day and age, it is hard to identify which human photo or nature image is real and natural vs AI generated, I had participated in a kaggle competition, [Detect AI vs. Human-Generated Images](https://www.kaggle.com/competitions/detect-ai-vs-human-generated-images).The competition satament is simple, design a model that accuartly classifies the given image is natural or AI generated image.


---
##  Project Overview

-  Upload an image through a **Streamlit web interface**
-  Model analyzes and predicts the origin (AI or Human)
-  Uploaded images are saved temporarily, then archived post-analysis
-  Powered by TensorFlow with lightweight, efficient architecture

---

##  Model Details

The model was developed using **TensorFlow Keras** with a focus on computational efficiency. The architecture uses `DepthwiseConv2D` and `SeparableConv2D` layers to reduce the number of parameters while maintaining performance.

Model accuracy : 90%

---

## Dataset
The Model is trained from a kaggle competition dataset [Detect AI vs. Human-Generated Images](https://www.kaggle.com/competitions/detect-ai-vs-human-generated-images)



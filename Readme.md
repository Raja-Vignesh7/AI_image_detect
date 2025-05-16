# 🧠🤖 AI vs Human Image Detector

This project aims to classify whether a given image is **AI-generated** or **Human-generated** using a custom-built deep learning model. The idea emerged from a Kaggle competition in which participants had to design an effective model for this binary classification task.

---
## 📌 Project Overview

- 📁 Upload an image through a **Streamlit web interface**
- 🧠 Model analyzes and predicts the origin (AI or Human)
- 🗂️ Uploaded images are saved temporarily, then archived post-analysis
- ⚙️ Powered by TensorFlow with lightweight, efficient architecture

---

## 🧠 Model Details

The model was developed using **TensorFlow Keras** with a focus on computational efficiency. The architecture uses `DepthwiseConv2D` and `SeparableConv2D` layers to reduce the number of parameters while maintaining performance.

Model accuracy : 90%

---

## Dataset
The Model is trained from a kaggle competition [Detect AI vs. Human-Generated Images](https://www.kaggle.com/competitions/detect-ai-vs-human-generated-images)



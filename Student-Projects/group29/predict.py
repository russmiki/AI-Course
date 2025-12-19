"""
Prediction script for Cat vs Dog.
- Load a saved model
- Predict a single external image
- Print label and confidence
Usage:
    python predict.py sample.jpg
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import sys

# Check for input
if len(sys.argv) < 2:
    print("Usage: python predict.py <image_path>")
    sys.exit()

image_path = sys.argv[1]

# Load model
model = tf.keras.models.load_model("model.h5")

IMG_SIZE = 64

# Load and preprocess image
image = Image.open(image_path).convert("RGB")
image = image.resize((IMG_SIZE, IMG_SIZE))
image = np.array(image) / 255.0
image = np.expand_dims(image, axis=0)  # Add batch dimension

# Predict
prediction = model.predict(image)[0][0]
label = "Dog" if prediction > 0.5 else "Cat"
confidence = prediction if label == "Dog" else 1 - prediction

print(f"Prediction: {label}")
print(f"Confidence: {confidence:.2f}")

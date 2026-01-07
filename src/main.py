import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import requests
import os
import sys

# TFLite Import
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

# Load Model
MODEL_PATH = "plants.tflite"
if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: {MODEL_PATH} not found. Please run convert_model.py first.")
    sys.exit(1)

print("⏳ Loading model...")
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("✅ Model loaded")

# Load Labels (Same logic as before)
labelmap_path = "labelmap.txt"
if not os.path.exists(labelmap_path):
    try:
        url = "https://storage.googleapis.com/aiy/vision/classifier/plants/labelmap.txt"
        r = requests.get(url)
        with open(labelmap_path, 'w') as f: f.write(r.text)
    except: pass

def load_labels(path):
    labels = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2: labels[int(parts[0])] = parts[1].lower()
    return labels

plant_labels = load_labels(labelmap_path)

def get_pretty_name(label):
    enhancements = {'sunflower': 'Sunflower', 'rose': 'Rose', 'tulip': 'Tulip',
                   'daisy': 'Daisy', 'dandelion': 'Dandelion', 'lily': 'Lily', 'orchid': 'Orchid'}
    for k, v in enhancements.items():
        if k in label.lower(): return v
    return label.capitalize()

def predict_flower(image_path):
    try:
        # Preprocess
        img = Image.open(image_path).resize((224, 224)).convert('RGB')
        img_array = np.array(img, dtype=np.float32)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Predict
        interpreter.set_tensor(input_details[0]['index'], img_array)
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])

        # Results
        predicted_class = np.argmax(predictions[0])
        confidence = np.max(predictions[0]) * 100
        flower_name = get_pretty_name(plant_labels.get(predicted_class, f"Plant {predicted_class}"))

        # Visualization
        plt.figure(figsize=(6, 6))
        plt.imshow(img)
        plt.title(f"{flower_name} ({confidence:.1f}%)")
        plt.axis('off')
        plt.show()
        
    except Exception as e:
        print(f"❌ Error: {e}")

# ... (Keep your existing input loop logic here) ...
# Minimal Main Loop
if __name__ == "__main__":
    while True:
        path = input("\nEnter image path (or 'q' to quit): ").strip().strip('"')
        if path.lower() == 'q': break
        if os.path.exists(path):
            predict_flower(path)
        else:
            print("❌ File not found")
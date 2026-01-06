from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import io
import os
import requests

app = FastAPI()

# Enable CORS for React Client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model (Global)
print("⏳ Loading model...")
model_url = "https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1"
model = tf.keras.Sequential([
    hub.KerasLayer(model_url, input_shape=(224, 224, 3))
])
model.build([None, 224, 224, 3])
print("✅ Model loaded!")

# Load Label Map
labelmap_path = "labelmap.txt"
if not os.path.exists(labelmap_path):
    # Quick fallback if file missing
    labelmap_url = "https://storage.googleapis.com/aiy/vision/classifier/plants/labelmap.txt"
    try:
        response = requests.get(labelmap_url)
        with open(labelmap_path, 'w') as f:
            f.write(response.text)
    except:
        pass 

def load_labels(path):
    labels = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    labels[int(parts[0])] = parts[1].lower()
    return labels

plant_labels = load_labels(labelmap_path)

def get_pretty_name(label):
    enhancements = {
        'sunflower': 'Sunflower', 'rose': 'Rose', 'tulip': 'Tulip',
        'daisy': 'Daisy', 'dandelion': 'Dandelion', 'lily': 'Lily', 'orchid': 'Orchid'
    }
    for k, v in enhancements.items():
        if k in label.lower():
            return v
    return label.capitalize()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read Image
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    img = img.resize((224, 224))
    
    # Preprocess
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # Predict
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]) * 100)
    
    raw_name = plant_labels.get(predicted_class, f"Plant {predicted_class}")
    pretty_name = get_pretty_name(raw_name)

    return {
        "name": pretty_name,
        "scientificName": raw_name.title(),
        "confidence": round(confidence, 1),
        "description": f"This appears to be a healthy {pretty_name}. Identified with {round(confidence, 1)}% confidence.",
        "raw_label": raw_name
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

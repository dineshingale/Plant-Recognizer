from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from PIL import Image
import io
import os
import requests

# --- TFLite Import Logic ---
# Try to import the lightweight runtime first, fallback to full TF if needed
try:
    import tflite_runtime.interpreter as tflite
    print("✅ Using TFLite Runtime")
except ImportError:
    import tensorflow.lite as tflite
    print("⚠️  TFLite Runtime not found, using full TensorFlow (this is fine)")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load Model (Lightweight) ---
MODEL_PATH = "plants.tflite"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"❌ {MODEL_PATH} not found! Did you run convert_model.py?")

print(f"⏳ Loading {MODEL_PATH}...")
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print("✅ Model loaded successfully!")

# --- Load Label Map ---
labelmap_path = "labelmap.txt"
if not os.path.exists(labelmap_path):
    print("⏳ Downloading label map...")
    url = "https://storage.googleapis.com/aiy/vision/classifier/plants/labelmap.txt"
    try:
        r = requests.get(url)
        with open(labelmap_path, 'w') as f:
            f.write(r.text)
    except Exception as e:
        print(f"Warning: Could not download labels: {e}")

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
    # 1. Read and Process Image
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    img = img.resize((224, 224))
    
    # Convert to numpy array and normalize [0, 1]
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    # 2. Run Inference (TFLite style)
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])

    # 3. Process Results
    predicted_class = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]) * 100)
    
    raw_name = plant_labels.get(predicted_class, f"Plant {predicted_class}")
    pretty_name = get_pretty_name(raw_name)

    return {
        "name": pretty_name,
        "scientificName": raw_name.title(),
        "confidence": round(confidence, 1),
        "description": f"This appears to be a healthy {pretty_name}.",
        "raw_label": raw_name
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
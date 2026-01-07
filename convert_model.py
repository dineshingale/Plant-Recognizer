import tensorflow as tf
import tensorflow_hub as hub

print("⏳ Downloading model from TF Hub... (This happens only once)")
# Load the original heavy model
model_url = "https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1"
model = tf.keras.Sequential([
    hub.KerasLayer(model_url, input_shape=(224, 224, 3))
])

# Convert it to TFLite
print("⚙️  Converting to TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the file
with open('plants.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ Success! 'plants.tflite' created. Upload this file to your project.")
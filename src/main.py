# Import libraries
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import requests
import os
import sys

# Check TensorFlow version
print("TensorFlow version:", tf.__version__)
print("TensorFlow Hub version:", hub.__version__)

# Load the pretrained model from TF Hub
print("⏳ Loading model... (this may take a moment)")
model_url = "https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1"
model = tf.keras.Sequential([
    hub.KerasLayer(model_url, input_shape=(224, 224, 3))
])
model.build([None, 224, 224, 3])
model.summary()

# Download label map with error handling
labelmap_url = "https://storage.googleapis.com/aiy/vision/classifier/plants/labelmap.txt"
labelmap_path = "labelmap.txt"

if not os.path.exists(labelmap_path):
    try:
        response = requests.get(labelmap_url)
        response.raise_for_status()
        with open(labelmap_path, 'w') as f:
            f.write(response.text)
        print("✅ Label map downloaded successfully")
    except Exception as e:
        print(f"⚠️  Couldn't download label map ({e}), creating basic flower mapping")
        # Create basic fallback mapping
        basic_labels = {
            1680: "Sunflower",
            1220: "Rose",
            1993: "Tulip",
            1896: "Daisy",
            652: "Dandelion",
            945: "Lily",
            812: "Orchid"
        }
        with open(labelmap_path, 'w') as f:
            for k, v in basic_labels.items():
                f.write(f"{k} {v}\n")

# Load label map
def load_label_map(file_path):
    label_map = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    label_map[int(parts[0])] = parts[1].lower()
        print(f"Loaded {len(label_map)} plant labels")
    except Exception as e:
        print(f"Error loading label map: {e}")
        label_map = {
            1680: "sunflower",
            1220: "rose",
            1993: "tulip",
            1945:"daisy",
            410:"rose",
            1752: "daisy",
            652: "dandelion",
            945: "lily",
            812: "orchid"
        }
    return label_map

plant_labels = load_label_map(labelmap_path)

# Enhance flower names for display
flower_name_enhancements = {
    'sunflower': 'Sunflower',
    'rose': 'Rose',
    'tulip': 'Tulip',
    'daisy': 'Daisy',
    'dandelion': 'Dandelion',
    'lily': 'Lily',
    'orchid': 'Orchid'
}

def get_pretty_flower_name(label):
    """Convert raw label to prettier flower name"""
    label_lower = label.lower()
    for key, pretty_name in flower_name_enhancements.items():
        if key in label_lower:
            return pretty_name
    return label.capitalize()

# Function to get image path from user
def get_image_path():
    """Get image path from user input"""
    while True:
        print("\n📸 Image Input Options:")
        print("1. Provide image file path")
        print("2. Use sample image from directory")
        print("3. Exit Program")
        
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == '1':
            # .strip('"') removes quotes if you specifically "Copy as path" in Windows
            image_path = input("Enter the full path to your image file: ").strip().strip('"')
            
            if not os.path.exists(image_path):
                print(f"❌ Error: File not found at: {image_path}")
                print("   Please check the path and try again.")
                continue # Loops back to the menu
            return image_path
            
        elif choice == '2':
            # Look for images in current directory
            image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
            images = [f for f in os.listdir('.') if f.lower().endswith(image_extensions)]
            
            if not images:
                print("❌ No image files found in current directory")
                continue # Loops back to menu
            
            print("\nAvailable images:")
            for i, img in enumerate(images, 1):
                print(f"{i}. {img}")
            
            try:
                img_choice_input = input("Select image number (or '0' to go back): ")
                img_choice = int(img_choice_input) - 1
                
                if img_choice == -1: # User entered 0
                    continue

                if 0 <= img_choice < len(images):
                    return images[img_choice]
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")
        
        elif choice == '3':
            print("👋 Exiting...")
            sys.exit(0)
            
        else:
            print("❌ Invalid choice, please try again.")

# Function to preprocess and predict
def predict_flower(image_path):
    # Load and preprocess image
    try:
        img = Image.open(image_path).resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = img_array / 255.0  # Normalize to [0,1]

        # Make prediction
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = np.max(predictions[0]) * 100

        # Get human-readable names
        flower_name = get_pretty_flower_name(plant_labels.get(predicted_class, f"plant {predicted_class}"))

        # Get top 5 predictions
        top_k = 5
        top_indices = predictions[0].argsort()[-top_k:][::-1]
        top_flowers = [(get_pretty_flower_name(plant_labels.get(i, f"plant {i}")),
                    predictions[0][i]) for i in top_indices]

        # Display results
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.imshow(img)
        plt.title('Captured Image')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.barh([name for name, _ in top_flowers],
                [conf*100 for _, conf in top_flowers],
                color='skyblue')
        plt.xlabel('Confidence (%)')
        plt.title(f'Top Predictions\nBest Match: {flower_name} ({confidence:.1f}%)')

        # Add confidence percentages to bars
        for i, (name, conf) in enumerate(top_flowers):
            plt.text(conf*100 + 1, i, f'{conf*100:.1f}%', va='center')

        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"❌ Error processing image: {e}")

# Main execution
print("\n🌼 Flower Recognition System 🌸")
print("=" * 60)

# This While True loop ensures the program keeps running until you explicitly exit
while True:
    try:
        image_path = get_image_path()
        
        if image_path:
            print(f"\n📷 Analyzing {os.path.basename(image_path)}...")
            predict_flower(image_path)
            
            # Ask if user wants to continue immediately
            cont = input("\nWould you like to identify another flower? (y/n): ").lower()
            if cont != 'y':
                print("👋 Goodbye!")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        break
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        # We continue the loop here instead of crashing
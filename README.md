# 🌼 Plant Recognizer

A Python-based flower recognition system using TensorFlow and TensorFlow Hub. This application identifies various plant species from images using the pre-trained MobileNet-based AIY Plants model.

## 🚀 Features

- **Plant Identification**: Uses a pre-trained deep learning model to classify plant images.
- **Top-5 Predictions**: display the top 5 most likely plant matches with confidence percentages.
- **Visual Feedback**: Shows the input image alongside a prediction confidence chart.
- **Input Flexibility**: 
    - Provide a full file path.
    - Select from available images in the current directory.
- **Automatic Setup**: Automatically downloads the required label map on first run.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dineshingale/Plant-Recognizer.git
    cd Plant-Recognizer
    ```

2.  **Set up a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    
    # Windows
    .\venv\Scripts\activate
    
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 📖 Usage

1.  **Run the main script:**
    ```bash
    python src/main.py
    ```

2.  **Follow the on-screen prompts:**
    - **Option 1**: Paste the full path to an image file on your computer.
    - **Option 2**: Automatically detect and choose from images in the project folder.
    - **Option 3**: Exit the application.

## 📦 Dependencies

- **TensorFlow** (2.12.0)
- **TensorFlow Hub** (0.13.0)
- **Pillow** (Image processing)
- **Matplotlib** (Visualization)
- **NumPy**

## 🤖 Model Information

This project uses the **Google AIY Plants V1** model from TensorFlow Hub:
- **Model Handle**: `https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1`
- **Input Shape**: 224x224x3

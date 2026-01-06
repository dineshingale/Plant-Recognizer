# � Plant Recognizer

A full-stack AI application for identifying plant species. It features a modern **React + Vite** frontend with a beautiful UI and a **FastAPI + TensorFlow** backend for real-time inference using the MobileNet-based AIY Plants model.

![Plant Recognizer UI](./Screenshots/Dashboard.jpeg)

## 🚀 Features

*   **Real-time Recognition**: Upload any plant image and get instant identification.
*   **Deep Learning**: Utilizing Google's pre-trained AIY Plants V1 model via TensorFlow Hub.
*   **Interactive UI**: Drag-and-drop uploads, live previews, and detailed results card.
*   **Result Insights**:
    *   Scientific Name & Common Name
    *   Confidence Score
    *   Health Status Check
    *   Detailed Description

## 🛠️ Technology Stack

*   **Frontend**: React, Vite, Tailwind CSS, Lucide React
*   **Backend**: FastAPI, Python 3.9+, Uvicorn
*   **AI/ML**: TensorFlow, TensorFlow Hub, Pillow, NumPy

## � Installation & Setup

### Prerequisites
*   Node.js (v18+)
*   Python (v3.9+)

### 1. Clone the Repository
```bash
git clone https://github.com/dineshingale/Plant-Recognizer.git
cd Plant-Recognizer
```

### 2. Backend Setup
Set up the Python server to handle predictions.

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Install dependencies (FastAPI, TensorFlow, etc.)
pip install -r requirements.txt

# Run the API Server
python server.py
```
> The server will start at `http://localhost:8000`

### 3. Frontend Setup
Launch the React Client interface.

```bash
# Open a new terminal and navigate to Client
cd Client

# Install dependencies
npm install

# Run Development Server
npm run dev
```
> The app will open at `http://localhost:5173`

## 📖 Usage Guide

1.  Ensure both **Server** (port 8000) and **Client** (port 5173) are running.
2.  Open `http://localhost:5173`.
3.  **To Identify a Plant:**
    *   Drag & drop an image onto the upload zone.
    *   Or click to browse your files.
    *   Click the **Recognize Plant** button.
4.  View the detailed results including confidence score and species info.

## � Project Structure

```
Plant-Recognizer/
├── Client/                 # React Frontend
│   ├── src/
│   │   ├── components/     # UI Components (Navbar, ImageUpload, ResultSection)
│   │   ├── App.jsx         # Main Logic
│   │   └── main.jsx        # Entry Point
│   └── package.json
├── src/                    # Legacy CLI Script (optional)
├── server.py               # FastAPI Backend Server
├── requirements.txt        # Python Dependencies
└── run.py                  # Helper Script
```

## 🤖 Model Details

This project uses the **Google AIY Plants V1** model:
*   **Source**: [TensorFlow Hub](https://tfhub.dev/google/aiy/vision/classifier/plants_V1/1)
*   **Architecture**: MobileNet-based (optimized for speed/mobile)
*   **Input**: 224x224 RGB Images

---
*Built with 💚 using React & Python*

import { useState } from 'react';
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import ResultSection from './components/ResultSection';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [image, setImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleImageSelect = (file) => {
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      setImage(e.target.result);
      setResult(null);
      setError(null);
    };
    reader.readAsDataURL(file);
  };

  const handleClear = () => {
    setImage(null);
    setSelectedFile(null);
    setResult(null);
    setError(null);
  };

  const handleRecognize = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError('Failed to connect to the recognition server. Please ensure it is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar
        onRecognize={handleRecognize}
        isAnalyzing={isAnalyzing}
        hasImage={!!image}
      />
      <main className="container mx-auto p-4 max-w-6xl">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6 text-center animate-in fade-in slide-in-from-top-2">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 my-8 items-start">
          <div className="w-full">
            <ImageUpload
              image={image}
              onImageSelect={handleImageSelect}
              onClear={handleClear}
            />
          </div>
          <div className="w-full">
            <ResultSection result={result} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;

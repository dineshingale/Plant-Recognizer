import { useState } from 'react';
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import ResultSection from './components/ResultSection';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [image, setImage] = useState(null);

  const handleImageSelect = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => setImage(e.target.result);
    reader.readAsDataURL(file);
  };

  const handleRecognize = () => {
    setIsAnalyzing(true);
    // Simulate API call
    setTimeout(() => {
      setIsAnalyzing(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar
        onRecognize={handleRecognize}
        isAnalyzing={isAnalyzing}
        hasImage={!!image}
      />
      <main className="container mx-auto p-4 max-w-2xl">
        <div className="my-8">
          <ImageUpload
            image={image}
            onImageSelect={handleImageSelect}
            onClear={() => setImage(null)}
          />
        </div>
        <ResultSection />
      </main>
    </div>
  );
}

export default App;

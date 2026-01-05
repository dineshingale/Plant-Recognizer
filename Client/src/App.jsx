import { useState } from 'react';
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import ResultSection from './components/ResultSection';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [hasImage, setHasImage] = useState(true); // Default true for demo

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
        hasImage={hasImage}
      />
      <main className="container mx-auto p-4 max-w-2xl">
        <div className="my-8">
          <ImageUpload />
        </div>
        <ResultSection />
      </main>
    </div>
  );
}

export default App;

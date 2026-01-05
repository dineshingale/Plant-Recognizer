import { useState } from 'react';
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import ResultSection from './components/ResultSection';

function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleImageSelect = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setImage(e.target.result);
      setResult(null); // Clear previous result on new image
    };
    reader.readAsDataURL(file);
  };

  const handleClear = () => {
    setImage(null);
    setResult(null);
  };

  const handleRecognize = () => {
    setIsAnalyzing(true);
    // Simulate API call
    setTimeout(() => {
      setIsAnalyzing(false);
      setResult({
        name: 'Monstera Deliciosa',
        scientificName: 'Monstera deliciosa',
        confidence: 98,
        description: 'Monstera deliciosa, also known as the Swiss Cheese Plant, is a species of flowering plant native to tropical forests of southern Mexico, south to Panama. It has become a mildly invasive species in many tropical areas and has become a very popular houseplant in temperate zones.',
      });
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
            onClear={handleClear}
          />
        </div>
        <ResultSection result={result} />
      </main>
    </div>
  );
}

export default App;

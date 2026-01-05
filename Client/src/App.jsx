import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import ResultSection from './components/ResultSection';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
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

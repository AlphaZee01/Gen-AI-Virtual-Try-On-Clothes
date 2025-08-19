import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { 
  SunIcon, 
  MoonIcon, 
  PhotoIcon,
  ArrowUpTrayIcon,
  SparklesIcon,
  ClockIcon
} from "@heroicons/react/24/outline";

import ImageUpload from "./components/ImageUpload";
import Footer from './components/Footer';

// Configure axios base URL for production
const API_BASE_URL = import.meta.env.PROD ? '' : 'http://localhost:8000';
axios.defaults.baseURL = API_BASE_URL;

function App() {
  const [personImage, setPersonImage] = useState(null);
  const [clothImage, setClothImage] = useState(null);
  const [instructions, setInstructions] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedMode = localStorage.getItem("darkMode");
    return savedMode ? JSON.parse(savedMode) : false;
  });

  const [modelType, setModelType] = useState("");
  const [gender, setGender] = useState("");
  const [garmentType, setGarmentType] = useState("");
  const [style, setStyle] = useState("");

  const resultRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("darkMode", JSON.stringify(isDarkMode));
  }, [isDarkMode]);

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [result]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!personImage || !clothImage) {
      toast.error("Please upload both person and cloth images");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("person_image", personImage);
    formData.append("cloth_image", clothImage);
    formData.append("instructions", instructions);
    
    // Add dropdown values to form data
    formData.append("model_type", modelType || "");
    formData.append("gender", gender || "");
    formData.append("garment_type", garmentType || "");
    formData.append("style", style || "");

    try {
      const response = await axios.post("/api/try-on", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 120000, // 2 minutes timeout
      });

      const newResult = {
        id: Date.now(),
        resultImage: response.data.image,
        text: response.data.text,
        timestamp: new Date().toLocaleString(),
      };

      setResult(newResult);
      setHistory((prev) => [newResult, ...prev]);
      toast.success("Virtual try-on completed successfully!");
    } catch (error) {
      console.error("API Error:", error);
      if (error.code === 'ECONNABORTED') {
        toast.error("Request timed out. Please try again.");
      } else if (error.response?.status === 500) {
        toast.error("Server error. Please check if the API key is configured.");
      } else if (error.response?.data?.detail) {
        toast.error(error.response.data.detail);
      } else {
        toast.error("An error occurred during processing. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      {/* Header */}
      <header className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} shadow-sm border-b ${isDarkMode ? 'border-gray-700' : 'border-gray-200'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <h1 className="text-2xl font-bold flex items-center">
              <SparklesIcon className="w-8 h-8 mr-2 text-blue-500" />
              Virtual Try-On
            </h1>
            <button
              onClick={() => setIsDarkMode(!isDarkMode)}
              className={`p-2 rounded-lg transition-colors ${
                isDarkMode 
                  ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400' 
                  : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
              }`}
            >
              {isDarkMode ? (
                <SunIcon className="w-5 h-5" />
              ) : (
                <MoonIcon className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">
            Try-On Clothes in Seconds
          </h2>
          <p className={`text-lg ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
            Upload your photo and garment to see how it looks on you
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Model Section */}
            <div className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <PhotoIcon className="w-6 h-6 mr-2 text-blue-500" />
                Model Image
              </h3>

              <ImageUpload
                label="Upload Model Image"
                onImageChange={setPersonImage}
                isDarkMode={isDarkMode}
              />

              <div className="mt-6 space-y-4">
                {/* Model Type */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    Model Type
                  </label>
                  <select
                    value={modelType}
                    onChange={(e) => setModelType(e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      isDarkMode 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  >
                    <option value="">Select model type</option>
                    <option value="top">Top Half</option>
                    <option value="bottom">Bottom Half</option>
                    <option value="full">Full Body</option>
                  </select>
                </div>

                {/* Gender */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    Gender
                  </label>
                  <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      isDarkMode 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  >
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="unisex">Unisex</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Garment Section */}
            <div className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
              <h3 className="text-xl font-semibold mb-6 flex items-center">
                <ArrowUpTrayIcon className="w-6 h-6 mr-2 text-green-500" />
                Garment Image
              </h3>

              <ImageUpload
                label="Upload Cloth Image"
                onImageChange={setClothImage}
                isDarkMode={isDarkMode}
              />

              <div className="mt-6 space-y-4">
                {/* Garment Type */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    Garment Type
                  </label>
                  <select
                    value={garmentType}
                    onChange={(e) => setGarmentType(e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      isDarkMode 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  >
                    <option value="">Select garment type</option>
                    <option value="shirt">Shirt</option>
                    <option value="pants">Pants</option>
                    <option value="jacket">Jacket</option>
                    <option value="dress">Dress</option>
                    <option value="tshirt">T-shirt</option>
                  </select>
                </div>

                {/* Style */}
                <div>
                  <label className={`block text-sm font-medium mb-2 ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    Style
                  </label>
                  <select
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                      isDarkMode 
                        ? 'bg-gray-700 border-gray-600 text-white' 
                        : 'bg-white border-gray-300 text-gray-900'
                    }`}
                  >
                    <option value="">Select style</option>
                    <option value="casual">Casual</option>
                    <option value="formal">Formal</option>
                    <option value="streetwear">Streetwear</option>
                    <option value="traditional">Traditional</option>
                    <option value="sports">Sportswear</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          {/* Instructions */}
          <div className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-6`}>
            <h3 className="text-lg font-semibold mb-4">Special Instructions</h3>
            <textarea
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              rows={4}
              placeholder="e.g. Fit for walking pose, crop top, side view preferred..."
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                isDarkMode 
                  ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
                  : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
              }`}
            />
          </div>

          {/* Submit Button */}
          <div className="flex justify-center">
            <button
              type="submit"
              disabled={loading}
              className={`px-8 py-3 rounded-lg font-semibold text-lg transition-all duration-200 flex items-center ${
                loading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 transform hover:scale-105'
              } text-white shadow-lg`}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Processing...
                </>
              ) : (
                <>
                  <SparklesIcon className="w-5 h-5 mr-2" />
                  Try On
                </>
              )}
            </button>
          </div>
        </form>

        {/* Results */}
        {result && (
          <div ref={resultRef} className="mt-16">
            <div className="border-t border-gray-200 dark:border-gray-700 pt-12">
              <h3 className="text-3xl font-bold text-center mb-8">Your Try-On Result</h3>
              <div className="flex justify-center">
                <img
                  src={result.resultImage}
                  alt="Try-On Result"
                  className="rounded-2xl shadow-2xl max-h-96"
                />
              </div>
              <p className="text-center mt-6 text-xl font-semibold">
                {result.text}
              </p>
            </div>
          </div>
        )}

        {/* History */}
        {history.length > 0 && (
          <div className="mt-16">
            <div className="border-t border-gray-200 dark:border-gray-700 pt-12">
              <h3 className="text-3xl font-bold mb-8 flex items-center justify-center">
                <ClockIcon className="w-8 h-8 mr-2 text-blue-500" />
                Previous Results
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {history.map((item) => (
                  <div
                    key={item.id}
                    className={`${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-lg p-4`}
                  >
                    <img
                      src={item.resultImage}
                      alt="Previous"
                      className="w-full rounded-lg mb-4"
                    />
                    <p className="font-semibold text-lg mb-2">
                      {item.text}
                    </p>
                    <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                      {item.timestamp}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer isDarkMode={isDarkMode} />

      <ToastContainer theme={isDarkMode ? "dark" : "light"} />
    </div>
  );
}

export default App;

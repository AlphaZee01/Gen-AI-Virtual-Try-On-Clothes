import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Moon, Sun, Upload, X } from "lucide-react";

import { Button } from "./components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";

import ImageUpload from "./components/ImageUpload";
import Footer from './components/Footer';

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
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
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
      const response = await axios.post("http://localhost:8000/api/try-on", formData, {
        headers: { "Content-Type": "multipart/form-data" },
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
      toast.error(
        error.response?.data?.message || "An error occurred during processing"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
                         <div className="flex items-center space-x-2">
               <img 
                 src="/uwear transparent logo.PNG"
                 alt="Uwear Logo"
                 className="h-14"
               />
                                            <div>
                 <h1 className="text-2xl font-bold text-foreground">
                   Virtual Try-On
                 </h1>
                 <p className="text-sm text-muted-foreground">
                   Powered by Uwear
                 </p>
               </div>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="rounded-full"
          >
            {isDarkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-foreground mb-4">
              Try-On Clothes in Seconds
            </h1>
            <p className="text-muted-foreground text-lg">
              Upload your photo and garment to see how it looks on you with your original background preserved
            </p>
            <div className="mt-4 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
              <p className="text-sm text-green-700 dark:text-green-300">
                ✨ Enhanced Experience: Your original background and lighting are preserved. Only the clothing is applied to your image for the most realistic try-on experience.
              </p>
              <p className="text-sm text-green-700 dark:text-green-300 mt-2">
                🎨 Advanced Texture Preservation: Clothing textures, patterns, and design details are maintained with high fidelity for authentic results.
              </p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Upload Sections */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Model Section */}
              <Card className="border-2 border-dashed border-muted-foreground/20 hover:border-uwear-orange/50 transition-colors">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Upload className="h-5 w-5 text-uwear-orange" />
                    Model Image
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <ImageUpload
                    label="Upload Person Image"
                    onImageChange={setPersonImage}
                    isDarkMode={isDarkMode}
                  />

                  <div className="space-y-4">
                    {/* Model Type */}
                    <div>
                      <label className="text-sm font-medium text-muted-foreground mb-2 block">
                        Model Type
                      </label>
                      <Select value={modelType} onValueChange={setModelType}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select model type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="professional">Professional</SelectItem>
                          <SelectItem value="casual">Casual</SelectItem>
                          <SelectItem value="fashion">Fashion</SelectItem>
                          <SelectItem value="street">Street Style</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Gender */}
                    <div>
                      <label className="text-sm font-medium text-muted-foreground mb-2 block">
                        Gender
                      </label>
                      <Select value={gender} onValueChange={setGender}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select gender" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="male">Male</SelectItem>
                          <SelectItem value="female">Female</SelectItem>
                          <SelectItem value="unisex">Unisex</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Garment Section */}
              <Card className="border-2 border-dashed border-muted-foreground/20 hover:border-uwear-orange/50 transition-colors">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Upload className="h-5 w-5 text-uwear-orange" />
                    Garment Image
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <ImageUpload
                    label="Upload Cloth Image"
                    onImageChange={setClothImage}
                    isDarkMode={isDarkMode}
                  />

                  <div className="space-y-4">
                    {/* Garment Type */}
                    <div>
                      <label className="text-sm font-medium text-muted-foreground mb-2 block">
                        Garment Type
                      </label>
                      <Select value={garmentType} onValueChange={setGarmentType}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select garment type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="shirt">Shirt</SelectItem>
                          <SelectItem value="pants">Pants</SelectItem>
                          <SelectItem value="jacket">Jacket</SelectItem>
                          <SelectItem value="dress">Dress</SelectItem>
                          <SelectItem value="tshirt">T-shirt</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    {/* Style */}
                    <div>
                      <label className="text-sm font-medium text-muted-foreground mb-2 block">
                        Style
                      </label>
                      <Select value={style} onValueChange={setStyle}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select style" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="casual">Casual</SelectItem>
                          <SelectItem value="formal">Formal</SelectItem>
                          <SelectItem value="streetwear">Streetwear</SelectItem>
                          <SelectItem value="traditional">Traditional</SelectItem>
                          <SelectItem value="sports">Sportswear</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Instructions */}
            <Card>
              <CardHeader>
                <CardTitle>Special Instructions</CardTitle>
              </CardHeader>
              <CardContent>
                <textarea
                  value={instructions}
                  onChange={(e) => setInstructions(e.target.value)}
                  placeholder="e.g. Fit for walking pose, crop top, side view preferred..."
                  className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none"
                />
              </CardContent>
            </Card>

            {/* Submit Button */}
            <div className="flex justify-center">
              <Button
                type="submit"
                variant="uwear"
                size="lg"
                disabled={loading}
                className="px-8 py-3 text-lg font-semibold"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Processing...
                  </div>
                ) : (
                  "Generate Virtual Try-On"
                )}
              </Button>
            </div>
          </form>

          {/* Results Section */}
          {result && (
            <div ref={resultRef} className="mt-12">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    ✨ Try-On Result
                    <span className="text-sm font-normal text-muted-foreground">
                      {result.timestamp}
                    </span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="flex justify-center">
                    <img
                      src={result.resultImage}
                      alt="Try-on result"
                      className="max-w-full h-auto rounded-lg shadow-lg border"
                    />
                  </div>
                  {result.text && (
                    <div className="bg-muted/50 p-4 rounded-lg">
                      <p className="text-sm text-muted-foreground">{result.text}</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}

          {/* History Section */}
          {history.length > 0 && (
            <div className="mt-12">
              <h2 className="text-2xl font-bold text-foreground mb-6">Previous Results</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {history.slice(1).map((item) => (
                  <Card key={item.id} className="overflow-hidden">
                    <CardContent className="p-0">
                      <img
                        src={item.resultImage}
                        alt="Previous result"
                        className="w-full h-48 object-cover"
                      />
                      <div className="p-4">
                        <p className="text-sm text-muted-foreground">{item.timestamp}</p>
                        {item.text && (
                          <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                            {item.text}
                          </p>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <Footer />

      {/* Toast Container */}
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme={isDarkMode ? "dark" : "light"}
      />
    </div>
  );
}

export default App;

import { useState, useRef } from "react";
import { PhotoIcon, XMarkIcon } from "@heroicons/react/24/outline";

const ImageUpload = ({ label, onImageChange, isDarkMode = false }) => {
  const [preview, setPreview] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFileSelect = (file) => {
    setError(""); // Clear previous errors
    
    const isImage = file.type.startsWith("image/");
    if (!isImage) {
      setError("You can only upload image files!");
      return;
    }

    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isLt10M) {
      setError("Image must be smaller than 10MB!");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
      onImageChange(file);
    };
    reader.onerror = () => {
      setError("Failed to read the image file. Please try again.");
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleRemove = () => {
    setPreview(null);
    setError("");
    onImageChange(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="w-full transition-all duration-300 flex flex-col items-center">
      {label && (
        <h4 className="text-lg font-semibold mb-4 text-center">
          {label}
        </h4>
      )}

      {error && (
        <div className="w-full mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {preview ? (
        <div className="relative w-full flex justify-center items-center mt-4">
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="h-48 w-48 object-contain rounded-lg shadow-md"
            />
            <button
              onClick={handleRemove}
              type="button"
              className={`absolute -top-2 -right-2 p-1 rounded-full shadow-lg transition-colors ${
                isDarkMode 
                  ? 'bg-gray-800 hover:bg-gray-700 text-red-400' 
                  : 'bg-white hover:bg-gray-50 text-red-500'
              }`}
              aria-label="Remove image"
            >
              <XMarkIcon className="w-5 h-5" aria-hidden="true" />
            </button>
          </div>
        </div>
      ) : (
        <div
          className={`w-full max-w-xs p-8 border-2 border-dashed rounded-xl transition-all duration-200 cursor-pointer ${
            isDragOver
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : isDarkMode
              ? 'border-gray-600 bg-gray-800 hover:border-gray-500'
              : 'border-gray-300 bg-gray-50 hover:border-gray-400'
          }`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => fileInputRef.current?.click()}
          role="button"
          tabIndex={0}
          onKeyPress={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              fileInputRef.current?.click();
            }
          }}
          aria-label="Upload image"
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) handleFileSelect(file);
            }}
            className="hidden"
            aria-describedby="file-upload-help"
          />
          
          <div className="text-center">
            <PhotoIcon 
              className={`w-12 h-12 mx-auto mb-4 ${
                isDarkMode ? 'text-blue-400' : 'text-blue-500'
              }`}
              aria-hidden="true"
            />
            <p className={`font-medium mb-2 ${
              isDarkMode ? 'text-gray-200' : 'text-gray-700'
            }`}>
              Click or drag an image here to upload
            </p>
            <p id="file-upload-help" className={`text-sm ${
              isDarkMode ? 'text-gray-400' : 'text-gray-500'
            }`}>
              Image only • Max size: 10MB
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;

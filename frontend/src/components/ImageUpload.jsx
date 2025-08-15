import { useState } from "react";
import { Upload, X } from "lucide-react";
import { Button } from "./ui/button";
import { cn } from "../lib/utils";

const ImageUpload = ({ label, onImageChange, isDarkMode = false }) => {
  const [preview, setPreview] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const isImage = file.type.startsWith("image/");
    if (!isImage) {
      alert("You can only upload image files!");
      return;
    }

    const isLt10M = file.size / 1024 / 1024 < 10;
    if (!isLt10M) {
      alert("Image must be smaller than 10MB!");
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
      onImageChange(file);
    };
    reader.readAsDataURL(file);
  };

  const handleRemove = () => {
    setPreview(null);
    onImageChange(null);
  };

  return (
    <div className="w-full transition-all duration-300 flex flex-col items-center">
      {label && (
        <h3 className="text-lg font-semibold mb-4 text-center text-foreground">
          {label}
        </h3>
      )}

      {preview ? (
        <div className="relative w-full flex justify-center items-center">
          <div className="relative group">
            <img
              src={preview}
              alt="Preview"
              className="h-48 w-48 object-cover rounded-lg shadow-md border-2 border-uwear-orange/20"
            />
            <Button
              variant="destructive"
              size="icon"
              onClick={handleRemove}
              className="absolute -top-2 -right-2 h-8 w-8 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ) : (
        <div className="w-full">
          <label
            htmlFor={`file-upload-${label}`}
            className={cn(
              "flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer transition-colors",
              "border-muted-foreground/30 hover:border-uwear-orange/50",
              "bg-muted/20 hover:bg-muted/30"
            )}
          >
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <Upload className="w-10 h-10 mb-3 text-muted-foreground" />
              <p className="mb-2 text-sm text-muted-foreground">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-muted-foreground">
                PNG, JPG, GIF up to 10MB
              </p>
            </div>
            <input
              id={`file-upload-${label}`}
              type="file"
              className="hidden"
              accept="image/*"
              onChange={handleFileChange}
            />
          </label>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;

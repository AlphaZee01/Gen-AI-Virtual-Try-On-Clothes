# Deployment Guide

## Python Version Compatibility

### ✅ Recommended: Python 3.11.9 (Enhanced Features with MediaPipe)
- **Use:** `requirements.txt` (MediaPipe included)
- **Features:** Full virtual try-on with MediaPipe pose detection
- **Deployment:** Works on Render.com with enhanced accuracy
- **Installation:** `pip install -r requirements.txt`

### Fallback: Python 3.13+ (Basic Features)
- **Use:** `requirements.txt` (MediaPipe excluded)
- **Features:** Full virtual try-on with fallback pose detection
- **Deployment:** Works on all platforms with basic functionality

## Render.com Configuration

### ✅ Automatic Deployment with MediaPipe
The system is configured to use Python 3.11.9 with MediaPipe for enhanced features.

### Configuration Files
- `render.yaml` - Specifies Python 3.11.9 and MediaPipe installation
- `.python-version` - Ensures correct Python version
- `requirements.txt` - Includes MediaPipe for enhanced pose detection

## Local Development

### ✅ Recommended: With MediaPipe (Python 3.11.9)
```bash
pip install -r requirements.txt
```

### Fallback: Without MediaPipe (Python 3.13+)
```bash
# Remove mediapipe line from requirements.txt first
pip install -r requirements.txt
```

## Features Available

### Always Available (Fallback)
- ✅ Person segmentation (color-based)
- ✅ Body detection (heuristic-based)
- ✅ Background removal
- ✅ Texture preservation
- ✅ Pattern detection
- ✅ Virtual try-on processing

### Enhanced Features (with MediaPipe)
- ✅ Advanced pose detection
- ✅ Precise body landmarks
- ✅ Improved segmentation accuracy

## Troubleshooting

### MediaPipe Import Error
- **Solution:** The system automatically falls back to alternative methods
- **No action required:** Virtual try-on will work without MediaPipe

### Python Version Issues
- **Render.com:** Use Python 3.13+ (automatic fallback)
- **Other platforms:** Use Python 3.11.9 for MediaPipe support

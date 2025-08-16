# Deployment Guide

## Python Version Compatibility

### Option 1: Python 3.13+ (Recommended for Render.com)
- **Use:** `requirements.txt` (MediaPipe excluded)
- **Features:** Full virtual try-on with fallback pose detection
- **Deployment:** Works on all platforms including Render.com

### Option 2: Python 3.8-3.12 (Enhanced Features)
- **Use:** `requirements.txt` + `requirements-mediapipe.txt`
- **Features:** Full virtual try-on with MediaPipe pose detection
- **Installation:** `pip install -r requirements.txt -r requirements-mediapipe.txt`

## Render.com Configuration

### Automatic Deployment
The system will automatically use fallback methods when MediaPipe is not available.

### Manual Configuration (if needed)
1. Set Python version to 3.11.9 in Render.com dashboard
2. Or use the `render.yaml` configuration file

## Local Development

### With MediaPipe (Python 3.8-3.12)
```bash
pip install -r requirements.txt -r requirements-mediapipe.txt
```

### Without MediaPipe (Python 3.13+)
```bash
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

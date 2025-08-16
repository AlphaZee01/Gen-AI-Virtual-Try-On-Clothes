# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Fixed
- Resolved import error for cv2 (OpenCV) in enhanced_tryon.py
- Fixed missing dependencies in pyproject.toml file
- Added onnxruntime dependency for rembg background removal
- Implemented fallback background removal method when rembg is unavailable
- Updated requirements.txt with all necessary computer vision dependencies

### Added
- Enhanced virtual try-on system with advanced texture preservation
- MediaPipe integration for precise body detection and segmentation
- Advanced pattern detection and preservation algorithms
- Texture-aware blending for realistic clothing application
- High-quality image interpolation (Lanczos4) for better detail preservation
- Conservative lighting adjustment to maintain texture details
- Enhanced sharpness and contrast preservation for clothing patterns

### Changed
- Replaced Gemini image generation with specialized virtual try-on processing
- Updated backend to preserve original background instead of generating new ones
- Enhanced clothing extraction with texture and pattern preservation
- Improved person segmentation using MediaPipe SelfieSegmentation
- Better body landmark detection for precise clothing placement

### Technical Improvements
- Added OpenCV, MediaPipe, scikit-image, and scipy dependencies
- Implemented texture-aware blending algorithms
- Enhanced image preprocessing pipeline
- Added pattern detection using Canny edge detection
- Improved alpha compositing with texture preservation

## [Previous Versions]
- Initial virtual try-on implementation with Gemini AI
- Basic frontend interface with image upload
- Simple background replacement system

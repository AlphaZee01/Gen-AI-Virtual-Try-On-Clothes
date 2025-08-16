from setuptools import setup, find_packages

setup(
    name="uwear-virtual-try-on",
    version="1.0.0",
    description="AI-powered virtual try-on application",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.12,<0.116.0",
        "uvicorn>=0.34.1,<0.35.0",
        "python-multipart>=0.0.20,<0.0.21",
        "python-dotenv>=1.1.0,<2.0.0",
        "google-genai>=1.11.0,<2.0.0",
        "opencv-python>=4.8.0",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "rembg>=2.0.0",
        "scikit-image>=0.21.0",
        "scipy>=1.11.0",
        "onnxruntime>=1.22.0",
        "mediapipe>=0.10.0,<0.11.0",
    ],
    python_requires=">=3.11",
)

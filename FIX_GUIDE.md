# Fix Guide - Frontend and Backend Issues

## ✅ Issues Identified and Fixed

### 1. Frontend Issue: ✅ FIXED
- **Problem**: npm dependencies not installed properly
- **Solution**: Used `npm install --legacy-peer-deps` to install dependencies
- **Status**: Frontend server should now be running on http://localhost:3000

### 2. Backend Issue: ⚠️ NEEDS YOUR ACTION
- **Problem**: Invalid API key - still using placeholder value
- **Solution**: You need to add your actual Google Gemini API key

## 🔧 How to Fix the API Key Issue

### Step 1: Get a Google Gemini API Key

1. **Visit Google AI Studio**: https://aistudio.google.com/
2. **Sign in** with your Google account
3. **Click "Get API key"** or go to "API keys" section
4. **Create a new API key**
5. **Copy the key** (it will look like: `AIzaSyC...`)

### Step 2: Update the Environment File

1. **Open the .env file** in the backend directory:
   ```cmd
   cd C:\Users\Kingsman007\Desktop\Gen-AI-Virtual-Try-On-Clothes\Gen-AI-Virtual-Try-On-Clothes\backend
   notepad .env
   ```

2. **Replace this line**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **With your actual API key**:
   ```
   GEMINI_API_KEY=AIzaSyC...your_actual_key_here
   ```

3. **Save the file**

### Step 3: Restart the Backend Server

1. **Stop the current backend server** (if running):
   - Press `Ctrl+C` in the backend terminal window

2. **Restart the backend server**:
   ```cmd
   cd C:\Users\Kingsman007\Desktop\Gen-AI-Virtual-Try-On-Clothes\Gen-AI-Virtual-Try-On-Clothes\backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 🧪 Testing the Fix

### 1. Test Backend Health
Visit: http://localhost:8000/health
- Should return: `{"status": "healthy", "environment": "development"}`

### 2. Test Frontend
Visit: http://localhost:3000
- Should load the Virtual Try-On application

### 3. Test API Documentation
Visit: http://localhost:8000/docs
- Should show interactive API documentation

### 4. Test Try-On Feature
1. Upload a person image and a garment image
2. Fill in the options (model type, gender, etc.)
3. Click "Try On"
4. Should generate a result (if API key is valid)

## 🚨 Common Issues and Solutions

### If Frontend Still Won't Start:
```cmd
cd frontend
npm cache clean --force
npm install --legacy-peer-deps
npm run dev
```

### If Backend Won't Start:
```cmd
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### If API Key Still Invalid:
1. Double-check the API key format (should start with `AIzaSy`)
2. Make sure there are no extra spaces in the .env file
3. Restart the backend server after changing the key
4. Verify the key has proper permissions in Google AI Studio

## 🎯 Success Indicators

- ✅ Frontend loads at http://localhost:3000
- ✅ Backend responds at http://localhost:8000/health
- ✅ API docs available at http://localhost:8000/docs
- ✅ Try-on feature works without API errors

## 📞 Need Help?

If you're still having issues:
1. Check that both servers are running
2. Verify your API key is correct
3. Check the browser console for any JavaScript errors
4. Check the backend terminal for any Python errors

Your application should now be fully functional once you add the correct API key!

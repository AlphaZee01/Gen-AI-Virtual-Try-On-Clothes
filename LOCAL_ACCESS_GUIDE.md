# Local Access Guide - Frontend to Backend Connection

## ✅ Current Status

Both servers are now running:
- **Backend**: http://localhost:8000 (FastAPI server)
- **Frontend**: http://localhost:3000 (React development server)

## 🌐 How to Access Your Application

### 1. Open Your Web Browser
Navigate to: **http://localhost:3000**

### 2. How the Connection Works

The frontend is already configured to communicate with your local backend through:

- **Vite Proxy Configuration**: The frontend automatically forwards all `/api/*` requests to `http://localhost:8000`
- **API Calls**: When you use the try-on feature, requests go to `/api/try-on` which gets proxied to your backend

## 🔧 Configuration Details

### Frontend Configuration (`frontend/vite.config.js`)
```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

### API Call in Frontend (`frontend/src/App.jsx`)
```javascript
const response = await axios.post("/api/try-on", formData, {
  headers: { "Content-Type": "multipart/form-data" },
});
```

## 🧪 Testing the Connection

### 1. Health Check
Visit: http://localhost:8000/health
- Should return: `{"status": "healthy", "environment": "development"}`

### 2. API Documentation
Visit: http://localhost:8000/docs
- Interactive API documentation with Swagger UI

### 3. Frontend Application
Visit: http://localhost:3000
- Upload images and test the try-on functionality

## 🚨 Important Requirements

### 1. Google Gemini API Key
Before the try-on feature works, you need to:

1. **Get an API Key**: Visit [Google AI Studio](https://aistudio.google.com/)
2. **Add to Environment**: Edit `backend\.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. **Restart Backend**: Stop and restart the backend server after adding the key

### 2. Both Servers Must Be Running
- Backend on port 8000
- Frontend on port 3000

## 🔍 Troubleshooting

### If Frontend Can't Connect to Backend:

1. **Check Backend Status**:
   ```cmd
   curl http://localhost:8000/health
   ```

2. **Check Ports**:
   ```cmd
   netstat -an | findstr :8000
   netstat -an | findstr :3000
   ```

3. **Restart Servers**:
   - Backend: `Ctrl+C` then `uvicorn main:app --reload --host 0.0.0.0 --port 8000`
   - Frontend: `Ctrl+C` then `npm run dev`

### Common Issues:

1. **Port Already in Use**:
   - Change backend port: `--port 8001`
   - Update frontend proxy: `target: 'http://localhost:8001'`

2. **CORS Errors**:
   - Backend already has CORS configured for localhost:3000

3. **API Key Missing**:
   - Add your Google Gemini API key to `backend\.env`

## 📱 Using the Application

1. **Upload Images**:
   - Person/Model Image: Upload a photo of the person
   - Garment Image: Upload the clothing item

2. **Select Options**:
   - Model Type (top/bottom/full body)
   - Gender (male/female/unisex)
   - Garment Type (shirt/pants/jacket/dress/tshirt)
   - Style (casual/formal/streetwear/traditional/sportswear)

3. **Add Instructions** (optional):
   - Special requirements or preferences

4. **Generate Try-On**:
   - Click "Try On" button
   - Wait for AI processing
   - View the generated result

## 🎯 Success Indicators

- ✅ Frontend loads at http://localhost:3000
- ✅ Backend responds at http://localhost:8000/health
- ✅ API docs available at http://localhost:8000/docs
- ✅ Try-on feature works (after adding API key)

Your local setup is now complete and ready to use!

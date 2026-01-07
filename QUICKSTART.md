# 🚀 Quick Start Guide - EXIF Demo App

## 5-Minute Setup

### 1️⃣ Open Command Prompt

Navigate to the project directory:

```cmd
cd "Image Metadata EXIF Leakage\exif_demo_app"
```

### 2️⃣ Create Virtual Environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```cmd
pip install -r requirements.txt
```

### 4️⃣ Run Application

```cmd
python app.py
```

### 5️⃣ Access Application

Open your browser and go to:

```
http://localhost:5000/
```

---

## 📋 Test Credentials

**Username**: `demo`  
**Password**: `demo123`

---

## 🎯 Quick Test

### 1. Home Page
- Overview of vulnerabilities
- Recent uploads
- Getting started guide

### 2. Login
- Click Login button
- Use demo/demo123
- Click Login

### 3. Dashboard (Vulnerability #1)
- Upload any image file
- Click "Upload Profile Picture"
- View in gallery

### 4. Profile (Vulnerability #2)
- Upload any image file
- Click "Upload Avatar"
- View in gallery

### 5. Settings (Vulnerability #3)
- Upload any image file
- Click "Upload Background"
- View in gallery

### 6. Gallery
- View all uploaded images
- Click "Download (with EXIF)"
- Check EXIF metadata with ExifTool

---

## 🔍 Extract EXIF Metadata

### Using ExifTool (if installed)

```cmd
exiftool downloaded_image.jpg
```

### Using Python

```python
from PIL import Image

img = Image.open("downloaded_image.jpg")
exif = img.getexif()
for key, value in exif.items():
    print(f"{key}: {value}")
```

---

## 📊 Expected Results

✅ 3 upload endpoints discovered  
✅ All EXIF metadata preserved  
✅ GPS coordinates leaked (if in test image)  
✅ Device info exposed  
✅ Author PII retained  

---

## 🛑 Stop Server

Press `Ctrl + C` in the terminal

---

## ❌ If Something Goes Wrong

### Port Already in Use
Change port in `app.py` (line near end):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Module Not Found
Ensure virtual environment is activated:
```cmd
venv\Scripts\activate
```

### Permission Error
Delete `uploads/` folder and let app recreate it

---

## 📚 For Scanner Testing

Point your EXIF scanner at: `http://localhost:5000/`

It will discover:
1. `/upload` - Profile picture upload
2. `/profile` - Avatar upload
3. `/settings` - Background image upload

All 3 endpoints are intentionally vulnerable!

---

## 🔐 Security Warning

**⚠️ THIS IS INTENTIONALLY VULNERABLE**

For testing and educational purposes ONLY. Do not use in production!

---

Enjoy testing! 🧪

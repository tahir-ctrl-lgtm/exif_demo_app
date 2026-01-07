# 📦 Complete Project Setup & Documentation

## 🎯 Project Overview

This is a **fully vulnerable Flask web application** designed to demonstrate EXIF metadata leakage vulnerabilities. It includes:

- ✅ **3 Intentional EXIF Leakage Vulnerabilities** across different endpoints
- ✅ **Public & Authenticated Pages** with proper routing
- ✅ **Responsive Design** with modern CSS styling
- ✅ **API Endpoints** for programmatic access
- ✅ **Comprehensive Documentation** and guides

---

## 📁 Project Structure

```
exif_demo_app/
├── app.py                               # Main Flask application (333 lines)
├── requirements.txt                     # Dependencies (Pillow, Flask, Werkzeug)
├── README.md                            # Comprehensive documentation
├── QUICKSTART.md                        # 5-minute setup guide
├── SETUP.md                             # This file
├── uploads/                             # Uploaded images directory (auto-created)
├── static/
│   └── css/
│       └── style.css                   # Complete responsive styling (1000+ lines)
└── templates/
    ├── home.html                        # Homepage with vulnerability overview
    ├── login.html                       # User authentication
    ├── dashboard.html                   # Vulnerability #1: Profile picture upload
    ├── profile.html                     # Vulnerability #2: Avatar upload
    ├── settings.html                    # Vulnerability #3: Background image upload
    ├── gallery.html                     # Public gallery with downloads
    ├── 404.html                         # 404 error page
    └── 500.html                         # 500 error page
```

---

## ⚡ Key Features

### 1. **Three Intentional EXIF Leakage Vulnerabilities**

#### Vulnerability #1: Dashboard `/upload`
- **Field**: `profile_picture`
- **Authentication**: Required
- **EXIF Stripping**: ❌ NONE
- **Metadata Preserved**: ✅ ALL

#### Vulnerability #2: Profile `/profile`
- **Field**: `avatar`
- **Authentication**: Required
- **EXIF Stripping**: ❌ NONE
- **Metadata Preserved**: ✅ ALL

#### Vulnerability #3: Settings `/settings`
- **Field**: `background_image`
- **Authentication**: Required
- **EXIF Stripping**: ❌ NONE
- **Metadata Preserved**: ✅ ALL

### 2. **Comprehensive Application Pages**

| Page | Route | Auth | Purpose |
|------|-------|------|---------|
| Home | `/` | No | Overview & vulnerability info |
| Login | `/login` | No | User authentication |
| Dashboard | `/dashboard` | Yes | Upload profile picture |
| Profile | `/profile` | Yes | Upload avatar |
| Settings | `/settings` | Yes | Upload background |
| Gallery | `/gallery` | No | View/download all images |

### 3. **Advanced Features**

- 🔐 Session-based authentication
- 📸 File upload handling with validation
- 🖼️ Image display and download endpoints
- 📊 JSON API for metadata access
- 🎨 Responsive CSS with modern design
- 📱 Mobile-friendly interface
- 🔍 Vulnerability indicators and warnings
- 📚 Comprehensive documentation

---

## 🛠️ Installation Guide

### Step 1: Prerequisites

- Python 3.8 or higher
- pip package manager
- Windows/macOS/Linux

Verify Python:
```bash
python --version
```

### Step 2: Create Virtual Environment

```bash
# Navigate to project
cd "Image Metadata EXIF Leakage\exif_demo_app"

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `Flask==3.0.0` - Web framework
- `Werkzeug==3.0.1` - WSGI utilities
- `Pillow==10.1.0` - Image handling (optional but recommended)

### Step 4: Verify Installation

```bash
pip list
```

Should show:
- Flask
- Werkzeug
- Pillow (optional)

---

## 🚀 Running the Application

### Start Server

```bash
python app.py
```

### Expected Console Output

```
====================================================================================================
                    EXIF METADATA LEAKAGE - DEMO APPLICATION
====================================================================================================

⚠️  INTENTIONALLY VULNERABLE - FOR TESTING ONLY

📋 Test Credentials:
   Username: demo          | Password: demo123
   Username: testuser      | Password: password
   Username: admin         | Password: admin123

📍 Upload Endpoints:
   • /upload (profile_picture)        [Vulnerability #1]
   • /profile (avatar)                [Vulnerability #2]
   • /settings (background_image)     [Vulnerability #3]

📊 Scanner will discover 3 upload fields across authenticated endpoints

🌐 Access Points:
   Homepage:   http://localhost:5000/
   Login:      http://localhost:5000/login
   Dashboard:  http://localhost:5000/dashboard (after login)
   Gallery:    http://localhost:5000/gallery
   API:        http://localhost:5000/api/images

====================================================================================================
```

### Access Application

Open browser: **http://localhost:5000/**

---

## 📖 Usage Workflow

### 1. Home Page (Public)

```
http://localhost:5000/
```

- View vulnerability overview
- See recent uploads
- Learn about EXIF metadata risks
- Read about real-world attack scenarios

### 2. Login Page (Public)

```
http://localhost:5000/login
```

Enter credentials:
- Username: `demo`
- Password: `demo123`

### 3. Dashboard (Authenticated)

```
http://localhost:5000/dashboard
```

- **Vulnerability #1**: Profile picture upload
- Upload any image file
- View your uploaded images

### 4. Profile Page (Authenticated)

```
http://localhost:5000/profile
```

- **Vulnerability #2**: Avatar upload
- Upload any image file
- View your avatars

### 5. Settings Page (Authenticated)

```
http://localhost:5000/settings
```

- **Vulnerability #3**: Background image upload
- Upload any image file
- Complete testing workflow
- EXIF categories reference

### 6. Gallery (Public)

```
http://localhost:5000/gallery
```

- View all uploaded images
- Download with full EXIF metadata
- See API documentation
- Testing instructions for researchers

---

## 🧪 Testing with EXIF Scanner

### 1. Generate Test Images

Create images with EXIF metadata:

```bash
# Using exiftool
exiftool -GPSLatitude=40.7128 -GPSLongitude=-74.0060 \
         -Artist="Test User" -Copyright="© Test" \
         test.jpg
```

### 2. Start Application

```bash
python app.py
```

### 3. Run Your Scanner

Point your EXIF scanner at: `http://localhost:5000/`

### 4. Expected Discoveries

Scanner should find:
- ✅ 3 upload endpoints
- ✅ 3 file input fields
- ✅ All require authentication
- ✅ No EXIF stripping
- ✅ All metadata preserved

---

## 🔌 API Endpoints

### 1. List All Images (Public)

```
GET /api/images
```

Returns JSON with all uploaded images and metadata.

### 2. User Statistics (Authenticated)

```
GET /api/user-stats
```

Returns upload statistics for logged-in user.

### Example API Response

```json
[
  {
    "filename": "demo_profile_20231111_120000_photo.jpg",
    "uploader": "demo",
    "upload_time": "2023-11-11 12:00:00",
    "original_name": "photo.jpg",
    "endpoint": "/upload",
    "field_name": "profile_picture",
    "download_url": "http://localhost:5000/download/demo_profile_20231111_120000_photo.jpg"
  }
]
```

---

## 📊 Vulnerabilities Summary

### EXIF Categories Leaked

1. **🔴 GPS/Location Metadata** (CRITICAL)
   - Exact coordinates
   - Home address exposure
   - Daily routine tracking

2. **🔴 Device Serial Numbers** (CRITICAL)
   - Device identification
   - Cross-platform tracking
   - Persistent user ID

3. **🟠 Author/PII Data** (HIGH)
   - Real name
   - Email address
   - Copyright information

4. **🟠 Device Information** (HIGH)
   - Camera model
   - Firmware version
   - Fingerprinting data

5. **🟡 Timestamps** (MEDIUM)
   - Capture date/time
   - Routine analysis
   - Location correlation

6. **🟡 Software Information** (MEDIUM)
   - Editing tools used
   - Application versions
   - Firmware versions

7. **🟢 Image Comments** (LOW)
   - User notes
   - Descriptions
   - Metadata tags

8. **🟢 Geometry Information** (LOW)
   - Pixel dimensions
   - Resolution
   - Image size

9. **🟢 Lens Information** (LOW)
   - Lens model
   - Focal length
   - Aperture

10. **🟢 Copyright/Rights** (LOW)
    - Ownership info
    - License terms
    - Usage rights

---

## 🔧 Troubleshooting

### Issue: Port 5000 Already in Use

**Solution**: Modify port in `app.py`:

```python
# At the end of app.py, change:
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

Then access at `http://localhost:5001/`

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution**: Activate virtual environment and reinstall:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### Issue: Permission Denied When Saving Uploads

**Solution**: Delete `uploads/` folder - app will recreate it:

```bash
# Windows
rmdir /s uploads

# macOS/Linux
rm -rf uploads
```

### Issue: "OSError: [Errno 48] Address already in use"

**Solution**: Kill existing process or use different port:

```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

---

## 📚 Testing Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed via pip
- [ ] Application starts without errors
- [ ] Homepage accessible and loads correctly
- [ ] Login page works with demo credentials
- [ ] Dashboard accessible after login
- [ ] Can upload images to dashboard
- [ ] Can upload avatars to profile
- [ ] Can upload backgrounds to settings
- [ ] Gallery displays all uploaded images
- [ ] Images downloadable with full EXIF
- [ ] API endpoint `/api/images` returns JSON
- [ ] Mobile view responsive on small screens
- [ ] Error pages (404/500) display correctly

---

## 🎯 What to Test

### 1. Image Upload Functionality

- Upload images to all 3 endpoints
- Verify file is saved
- Check different file types (PNG, JPG, GIF)
- Test max file size (16MB)

### 2. EXIF Preservation

- Upload image with embedded EXIF
- Download the image
- Extract EXIF using exiftool
- Verify all metadata preserved

### 3. Gallery Access

- View uploaded images in gallery
- Download images without authentication
- Verify EXIF intact in downloaded files

### 4. API Access

- Access `/api/images` without auth
- Verify JSON response
- Check image metadata in response

### 5. Authentication

- Login with valid credentials
- Access protected pages
- Attempt access without login (should redirect)
- Logout and verify session cleared

---

## 🔐 Security Notes

### This Application Is Intentionally Vulnerable

- ❌ No EXIF metadata stripping
- ❌ No input validation beyond file type
- ❌ Minimal security measures
- ❌ Debug mode enabled
- ❌ No HTTPS/SSL
- ❌ Session-based only

**DO NOT USE IN PRODUCTION!**

---

## 📞 Support Resources

### Tools for Testing

- **ExifTool**: Extract EXIF data from images
  ```bash
  exiftool image.jpg
  ```

- **Python PIL**: Image metadata extraction
  ```python
  from PIL import Image
  img = Image.open("test.jpg")
  print(img.info)
  ```

- **Online EXIF Viewers**:
  - https://exif.regex.info/
  - https://www.verexif.com/

### Learning Resources

- [OWASP Information Exposure](https://owasp.org/www-community/Information_Exposure)
- [CWE-359 Definition](https://cwe.mitre.org/data/definitions/359.html)
- [GDPR Article 9](https://gdpr-info.eu/art-9-gdpr/)
- [ExifTool Documentation](https://exiftool.org/)

---

## 📝 Additional Notes

- Application stores uploads in `uploads/` directory
- Session data stored in memory (lost on restart)
- No database required (in-memory storage)
- All vulnerabilities are intentional and documented
- Perfect for demonstrating EXIF scanner capabilities

---

## ✅ Verification

To verify everything is working:

1. **App Running**: Should see output starting with "EXIF METADATA LEAKAGE"
2. **Homepage**: `http://localhost:5000/` should load with vulnerability info
3. **Login**: Credentials demo/demo123 should work
4. **Upload**: Should be able to upload images
5. **Gallery**: Should display uploaded images
6. **EXIF**: Downloaded images should have metadata intact

---

## 🎓 What You'll Learn

- How EXIF metadata can leak privacy information
- Why image upload endpoints are security risks
- How to identify vulnerable file handling
- Real-world privacy attack scenarios
- Proper image sanitization techniques
- Importance of metadata stripping

---

## 🚀 Next Steps

1. ✅ Complete setup (you are here)
2. 📖 Read README.md for detailed documentation
3. 🧪 Use QUICKSTART.md for quick testing
4. 🔍 Run your EXIF scanner against this app
5. 📊 Analyze and report vulnerabilities

---

**Created for security research and educational purposes**

⚠️ **FOR TESTING ONLY - DO NOT USE IN PRODUCTION**

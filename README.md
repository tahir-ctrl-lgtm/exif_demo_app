# 📸 EXIF Metadata Leakage Demo Application

A vulnerable Flask web application intentionally designed for testing and demonstrating EXIF metadata leakage vulnerabilities.

## ⚠️ WARNING

**THIS APPLICATION IS INTENTIONALLY VULNERABLE**

**DO NOT USE IN PRODUCTION!** This app is designed for security testing and educational purposes only.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Vulnerabilities](#vulnerabilities)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Application Structure](#application-structure)
- [Testing the Vulnerabilities](#testing-the-vulnerabilities)
- [API Endpoints](#api-endpoints)
- [Test Credentials](#test-credentials)
- [Expected Scanner Results](#expected-scanner-results)
- [Privacy Impact](#privacy-impact)
- [Remediation Tips](#remediation-tips)

---

## 🎯 Overview

This application demonstrates a critical privacy vulnerability where uploaded images retain their EXIF (Exchangeable Image File Format) metadata. This metadata can leak sensitive information including:

- **GPS coordinates** → Home address exposure
- **Device information** → Camera model/serial for device tracking
- **Author/PII** → Identity disclosure
- **Timestamps** → Routine analysis and location tracking
- **Copyright info** → Ownership information
- **Lens information** → Photography equipment details

### Vulnerability Type
- **CWE-359**: Exposure of Private Personal Information to an Unauthorized Actor
- **CWE-200**: Exposure of Sensitive Information to an Unauthorized Actor
- **OWASP A01:2021**: Broken Access Control (Information Disclosure)

### Regulatory Impact
- **GDPR Article 9**: GPS coordinates are special category personal data
- **CCPA**: Location data classified as sensitive personal information
- **HIPAA**: Facility location in medical facility photos

---

## 🔴 Vulnerabilities

### Vulnerability #1: Profile Picture Upload (Dashboard)
- **Endpoint**: `/upload`
- **Field**: `profile_picture`
- **Location**: Dashboard page (requires authentication)
- **Issue**: No EXIF stripping on upload
- **Leakage**: All EXIF metadata preserved

### Vulnerability #2: Avatar Upload (Profile)
- **Endpoint**: `/profile`
- **Field**: `avatar`
- **Location**: Profile page (requires authentication)
- **Issue**: No EXIF stripping on upload
- **Leakage**: All EXIF metadata preserved

### Vulnerability #3: Background Image Upload (Settings)
- **Endpoint**: `/settings`
- **Field**: `background_image`
- **Location**: Settings page (requires authentication)
- **Issue**: No EXIF stripping on upload
- **Leakage**: All EXIF metadata preserved

### Additional Vulnerabilities

#### Public Gallery Download
- **Endpoint**: `/download/<filename>`
- **Issue**: Images downloadable with full EXIF metadata intact
- **Impact**: No authentication required - anyone can download with metadata

#### API Exposure
- **Endpoint**: `/api/images`
- **Issue**: No authentication on image list endpoint
- **Impact**: Metadata accessible via API without login

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

#### 1. Navigate to the Project Directory
```bash
cd "Image Metadata EXIF Leakage/exif_demo_app"
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
pip list
```

---

## 🏃 Running the Application

### Start the Flask Server
```bash
python app.py
```

### Expected Output
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

---

## 📁 Application Structure

```
exif_demo_app/
├── app.py                           # Main Flask application
├── requirements.txt                 # Python dependencies
├── uploads/                         # Uploaded images directory
├── static/
│   └── css/
│       └── style.css               # Application styling
└── templates/
    ├── home.html                   # Homepage
    ├── login.html                  # Login page
    ├── dashboard.html              # Dashboard (Vulnerability #1)
    ├── profile.html                # Profile page (Vulnerability #2)
    ├── settings.html               # Settings page (Vulnerability #3)
    ├── gallery.html                # Public gallery
    ├── 404.html                    # 404 error page
    └── 500.html                    # 500 error page
```

---

## 🧪 Testing the Vulnerabilities

### Step 1: Generate Test Images with EXIF Metadata

Create test images with embedded EXIF data. You can use tools like:

```bash
# Using exiftool (install: apt-get install exiftool)
exiftool -GPSLatitude=40.7128 -GPSLongitude=-74.0060 \
         -Artist="John Doe" -Copyright="© John Doe" \
         -Make="Canon" -Model="Canon EOS 5D Mark IV" \
         test_image.jpg

# Using Python with piexif
python -c "
import piexif
import piexif.helper

# Create GPS IFD
gps_ifd = {
    piexif.GPSIFD.GPSLatitude: ((40,), (42,), (44.52,)),
    piexif.GPSIFD.GPSLatitudeRef: b'N',
    piexif.GPSIFD.GPSLongitude: ((74,), (0,), (47.37,)),
    piexif.GPSIFD.GPSLongitudeRef: b'W',
}

# Add to image
exif_dict = {'GPS': gps_ifd}
# ... save with metadata
"
```

### Step 2: Access the Application

Open browser: `http://localhost:5000/`

### Step 3: Authenticate

1. Click **Login**
2. Enter credentials:
   - Username: `demo`
   - Password: `demo123`
3. Click **Login**

### Step 4: Upload Test Images

Navigate to each endpoint and upload test images:

#### Dashboard (Vulnerability #1)
1. Go to **Dashboard** → **Upload Profile Picture**
2. Select test image
3. Click **Upload Profile Picture**

#### Profile (Vulnerability #2)
1. Go to **Profile** → **Upload Avatar**
2. Select test image
3. Click **Upload Avatar**

#### Settings (Vulnerability #3)
1. Go to **Settings** → **Upload Background Image**
2. Select test image
3. Click **Upload Background**

### Step 5: Download and Extract Metadata

1. Go to **Gallery**
2. Click **Download (with EXIF)** on uploaded image
3. Extract EXIF data:

```bash
# Using exiftool
exiftool downloaded_image.jpg

# Or use Python
python -c "
from PIL import Image
from PIL.ExifTags import TAGS

with Image.open('downloaded_image.jpg') as img:
    exif = img.getexif()
    for k, v in exif.items():
        print(f'{TAGS.get(k)}: {v}')
"
```

### Step 6: Verify Metadata Preservation

Compare original and downloaded EXIF data:

```bash
# Original image
exiftool original_image.jpg > original_exif.txt

# Downloaded image
exiftool downloaded_image.jpg > downloaded_exif.txt

# Compare
diff original_exif.txt downloaded_exif.txt
```

---

## 🌐 Access Points

| Page | URL | Authentication | Purpose |
|------|-----|-----------------|---------|
| Homepage | `http://localhost:5000/` | None | Overview of vulnerabilities |
| Login | `http://localhost:5000/login` | None | User authentication |
| Dashboard | `http://localhost:5000/dashboard` | Required | Profile picture upload (Vuln #1) |
| Profile | `http://localhost:5000/profile` | Required | Avatar upload (Vuln #2) |
| Settings | `http://localhost:5000/settings` | Required | Background upload (Vuln #3) |
| Gallery | `http://localhost:5000/gallery` | None | View/download uploaded images |
| API | `http://localhost:5000/api/images` | None | JSON list of images |

---

## 🔑 Test Credentials

### Demo Users

| Username | Password | Purpose |
|----------|----------|---------|
| demo | demo123 | Primary test user |
| testuser | password | Alternative test user |
| admin | admin123 | Admin test account |

---

## 📊 Expected Scanner Results

When testing this application with an EXIF scanner, expect:

### Discovered Endpoints
- ✅ 3 upload endpoints found
- ✅ 3 file input fields detected
- ✅ All endpoints require authentication

### Vulnerability Detection
- ✅ No EXIF stripping detected
- ✅ Original metadata preserved
- ✅ GPS coordinates retained
- ✅ Device serial numbers exposed
- ✅ Author/PII data leaked
- ✅ Timestamps preserved

### EXIF Categories Tested
- GPS Location Metadata (CRITICAL)
- Device Information (HIGH)
- Serial Numbers (CRITICAL)
- Author/Artist PII (HIGH)
- Timestamps (MEDIUM)
- Software/Firmware (MEDIUM)
- Image Comments (MEDIUM)
- Geometry/Size (LOW)
- Lens Information (LOW)
- Copyright/Rights (LOW)

### Expected Severity
- 🔴 **CRITICAL**: Multiple privacy exposure risks
- 🟠 **HIGH**: Device tracking via serials
- 🟡 **MEDIUM**: Timestamp analysis
- 🟢 **LOW**: General metadata exposure

---

## 🔌 API Endpoints

### GET /api/images
Returns JSON list of all uploaded images

```bash
curl http://localhost:5000/api/images
```

**Response:**
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

### GET /api/user-stats
Returns user upload statistics (requires authentication)

```bash
curl -b "session_cookie" http://localhost:5000/api/user-stats
```

---

## 🎯 Privacy Impact Assessment

### GPS/Location Coordinates
- **Risk Level**: 🔴 CRITICAL
- **Impact**: Home address exposure → Stalking/burglary
- **GDPR**: Article 9 (special category data)
- **Attack Scenario**: Photo with GPS → Maps to residence → Burglar targets

### Device Serial Numbers
- **Risk Level**: 🔴 CRITICAL
- **Impact**: Cross-platform tracking
- **Attack Scenario**: Serial number → Track across multiple platforms → Persistent user ID

### Author/PII Data
- **Risk Level**: 🟠 HIGH
- **Impact**: Identity disclosure
- **Attack Scenario**: Real name in EXIF → Identity revealed → Targeted harassment

### Device Information
- **Risk Level**: 🟠 HIGH
- **Impact**: Device fingerprinting
- **Attack Scenario**: Camera model + serial → Unique fingerprint → Tracking

### Timestamps
- **Risk Level**: 🟡 MEDIUM
- **Impact**: Routine analysis
- **Attack Scenario**: Timestamps + GPS → Daily patterns → Predictable location

---

## 🛠️ Remediation

### Proper Image Handling

#### Python/Django
```python
from PIL import Image
from io import BytesIO

def strip_exif(image_file):
    """Remove EXIF metadata from uploaded image"""
    img = Image.open(image_file)
    
    # Remove EXIF data
    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    
    return image_without_exif
```

#### PHP/Laravel
```php
use Image;

Route::post('/upload', function(Request $request) {
    $image = $request->file('image');
    $img = Image::make($image)
        ->orientate()
        ->resize(800, 600)
        ->save(); // Automatically strips EXIF
    
    $img->save(storage_path('uploads/' . $image->hashName()));
});
```

#### Node.js/Express
```javascript
const sharp = require('sharp');

app.post('/upload', async (req, res) => {
  const image = await sharp(req.file.buffer)
    .withMetadata(false)  // Remove EXIF
    .toBuffer();
    
  fs.writeFileSync(`uploads/${req.file.filename}`, image);
});
```

### Best Practices

1. **Always strip EXIF** before serving user-uploaded images
2. **Validate file type** - Check MIME type, not just extension
3. **Limit file size** - Prevent DOS attacks
4. **Store separately** - Keep uploads outside web root
5. **Rename files** - Don't preserve original filenames
6. **Log uploads** - Track who uploaded what when
7. **Monitor metadata** - Audit for compliance
8. **User education** - Warn users about metadata

---

## 📚 Tools for Testing

### EXIF Extraction
```bash
# ExifTool
exiftool image.jpg

# ImageMagick
identify -verbose image.jpg

# Python PIL
python -c "from PIL import Image; print(Image.open('image.jpg').info)"

# Online tools
https://exif.regex.info/
https://www.verexif.com/
```

### EXIF Creation (Testing)
```bash
# Create test image with EXIF
exiftool -GPSLatitude=40.7128 -GPSLongitude=-74.0060 \
         -Artist="Test User" -Copyright="© Test" \
         -Make="TestCamera" test.jpg

# Using Python piexif
pip install piexif
```

---

## 📖 Learning Resources

- [OWASP - Information Exposure](https://owasp.org/www-community/Information_Exposure)
- [CWE-359: Information Exposure](https://cwe.mitre.org/data/definitions/359.html)
- [GDPR Article 9 - Special Categories](https://gdpr-info.eu/art-9-gdpr/)
- [CCPA - Sensitive Personal Information](https://oag.ca.gov/privacy/ccpa)
- [ExifTool Documentation](https://exiftool.org/)

---

## 🐛 Troubleshooting

### Issue: Port 5000 Already in Use
```bash
# Change port
python app.py  # Edit port in app.py
# Or kill process on port 5000
netstat -ano | findstr :5000  # Windows
```

### Issue: Module Not Found
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Permission Denied on uploads/
```bash
# Fix permissions
chmod 755 uploads/  # macOS/Linux
```

---

## ✅ Verification Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Flask server running (`python app.py`)
- [ ] Homepage accessible at `http://localhost:5000/`
- [ ] Login works with demo/demo123
- [ ] Can upload images to all 3 endpoints
- [ ] Gallery displays uploaded images
- [ ] Can download images with EXIF intact
- [ ] API endpoint `/api/images` returns JSON

---

## 📝 Notes

- All uploads are stored in the `uploads/` directory
- Session data is stored in memory (resets on restart)
- EXIF metadata is intentionally preserved
- No authentication tokens/API keys are used
- Application runs in debug mode by default

---

## 📄 License

Educational purpose only. Not for production use.

---

## 👨‍💻 Author

Created for demonstrating EXIF metadata leakage vulnerabilities in web applications.

**Version**: 1.0.0  
**Last Updated**: November 2024

---

## ⚠️ Disclaimer

This application is provided for security research and educational purposes. Unauthorized testing on systems you do not own or have permission to test is illegal. Always obtain proper authorization before security testing.

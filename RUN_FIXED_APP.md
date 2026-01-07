# 🚀 QUICK START - PROPERLY VULNERABLE APP

## Step 1: Clear Old Test Data
```bash
cd "C:\Project\Vuln Web App\Image Metadata EXIF Leakage\exif_demo_app"
rm -Force uploads\*
```

## Step 2: Start the App
```bash
python app.py
```

You should see:
```
🚨 VULNERABILITY: Binary file copy preserves 100% of EXIF metadata

📊 Expected EXIF Retention:
   • GPS Location:        8 fields  (CRITICAL - Home address)
   • Serial Numbers:      3 fields  (CRITICAL - Tracking)
   • Author/PII:          4 fields  (HIGH - Identity)
   • Device Info:         4 fields  (MEDIUM - Fingerprinting)
   • Timestamps:          4 fields  (MEDIUM - Routine analysis)
   • All other categories: ~470+ fields total

🔍 Scanner will detect 10 out of 10 EXIF categories as VULNERABLE

🌐 Access Points:
   Homepage:   http://localhost:5000/
   Login:      http://localhost:5000/login
   Dashboard:  http://localhost:5000/dashboard (after login)
```

## Step 3: Test Upload (Manual Verification)

1. Open browser: http://localhost:5000/
2. Click "Login" → Use credentials:
   - Username: `demo`
   - Password: `demo123`

3. Upload test image to each endpoint:
   - **Dashboard:** Upload profile picture
   - **Profile:** Upload avatar  
   - **Settings:** Upload background image

4. Verify EXIF is preserved:
```bash
# In PowerShell
cd uploads
python -c "
from PIL import Image
from PIL.ExifTags import TAGS

files = [f for f in __import__('os').listdir('.') if f.endswith('.jpg')]
if files:
    img = Image.open(files[0])
    exif = img._getexif()
    print(f'File: {files[0]}')
    print(f'EXIF Fields: {len(exif) if exif else 0}')
    if exif:
        for tag_id, value in sorted(exif.items())[:5]:
            tag_name = TAGS.get(tag_id, f'Tag_{tag_id}')
            print(f'  ✓ {tag_name}')
"
```

Expected output: Should show GPSInfo and other metadata preserved

## Step 4: Run Scanner

In another terminal:
```bash
cd C:\armor\main_test\backend
python -m agents.image_metadata_exif_leakage.run_agent --target http://localhost:5000 --user demo --password demo123
```

## Step 5: Check Results

Scanner should report:
- ✅ 3 upload endpoints discovered
- ✅ 30 images uploaded
- ✅ ALL EXIF fields retained (100%)
- ✅ 10 out of 10 categories VULNERABLE
- ✅ CRITICAL severity findings

---

## 🎯 Key Difference from Previous Run

| Metric | Previous | Current |
|--------|----------|---------|
| EXIF Retention | 0.2% (3 fields) | 100% (~481 fields) |
| Categories Detected | 1/10 | 10/10 |
| Scanner Accuracy | ~50% | 100% |
| Vulnerability Status | FALSE NEGATIVE | TRUE POSITIVE |

---

## ✅ Success Criteria

Scanner results after fix:
```
🚨 CRITICAL: GPS Location - VULNERABLE (8 fields, 60/100 confidence)
🚨 CRITICAL: Serial Numbers - VULNERABLE (3 fields, 50/100 confidence)
⚠️ HIGH: Author/PII - VULNERABLE (4 fields, 30/100 confidence)
⚠️ MEDIUM: Device Info - VULNERABLE (4 fields, 20/100 confidence)
⚠️ MEDIUM: Timestamps - VULNERABLE (4 fields, 15/100 confidence)
ℹ️ LOW: All other categories - VULNERABLE

TOTAL VULNERABILITIES: 30/30 possible
OVERALL RISK: 🚨 CRITICAL
```

---

**This is it! Your demo app is now properly vulnerable and your scanner should detect every EXIF leakage vector.** 🎉

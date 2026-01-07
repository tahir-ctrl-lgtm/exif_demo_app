"""
Vercel Entry Point for EXIF Demo Application
"""
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import secrets
import shutil
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configuration for Vercel
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff"}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock user database
users = {
    "demo": generate_password_hash("demo123"),
    "testuser": generate_password_hash("password"),
    "admin": generate_password_hash("admin123"),
}

# Mock image metadata storage
uploaded_images = []


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_with_exif_preserved(file, filepath):
    """
    🚨 VULNERABILITY: Save file preserving ALL EXIF metadata
    
    Uses binary copy instead of PIL/Werkzeug to avoid automatic EXIF stripping.
    This simulates a naive developer who doesn't realize EXIF metadata is a privacy risk.
    """
    temp_path = filepath + ".tmp"
    try:
        # Save to temporary location first
        file.save(temp_path)
        
        # Binary copy preserves ALL EXIF metadata
        shutil.copy2(temp_path, filepath)
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return True
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise e


# ============================================================================
# PUBLIC ROUTES
# ============================================================================


@app.route("/")
def home():
    """Homepage - displays recent uploads"""
    return render_template("home.html", images=uploaded_images[:12])


@app.route("/gallery")
def gallery():
    """Public gallery - VULNERABILITY: Images downloadable with EXIF intact"""
    return render_template("gallery.html", images=uploaded_images)


@app.route("/download/<filename>")
def download_image(filename):
    """
    🚨 VULNERABILITY: Serves original image file WITH ALL EXIF DATA
    
    PRIVACY RISKS:
    - GPS coordinates exposed (home address)
    - Device information leaked (fingerprinting)
    - Author/copyright metadata preserved (identity)
    - Serial numbers visible (tracking)
    - Timestamp metadata included (routine analysis)
    """
    try:
        return send_file(
            os.path.join(app.config["UPLOAD_FOLDER"], filename),
            as_attachment=False,
            download_name=filename
        )
    except Exception as e:
        flash(f"Error downloading image: {str(e)}", "error")
        return redirect(url_for("gallery"))


@app.route("/view/<filename>")
def view_image(filename):
    """
    🚨 VULNERABILITY: View image with ALL EXIF DATA intact
    
    Browser will load and display the image including all EXIF metadata.
    Tools like browser developer console can extract this metadata.
    """
    try:
        return send_file(
            os.path.join(app.config["UPLOAD_FOLDER"], filename),
            mimetype="image/jpeg"
        )
    except Exception as e:
        flash(f"Error loading image: {str(e)}", "error")
        return redirect(url_for("gallery"))


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================


@app.route("/login", methods=["GET", "POST"])
def login():
    """User authentication"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            session["logged_in"] = True
            flash("✅ Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("❌ Invalid credentials", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """User logout"""
    session.clear()
    flash("👋 Logged out successfully", "info")
    return redirect(url_for("home"))


# ============================================================================
# AUTHENTICATED ROUTES (Upload Endpoints)
# ============================================================================


@app.route("/dashboard")
def dashboard():
    """
    User dashboard with image upload

    VULNERABILITY: Multiple upload fields, no EXIF stripping
    """
    if "logged_in" not in session:
        return redirect(url_for("login"))

    user_images = [img for img in uploaded_images if img["uploader"] == session["user"]]
    return render_template("dashboard.html", user=session["user"], images=user_images)


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    🚨 VULNERABILITY #1: Profile picture upload (NO EXIF STRIPPING)
    
    Endpoint: POST /dashboard
    Field: profile_picture
    EXIF Preserved: YES - 100% of metadata retained
    
    Privacy Risk: GPS coordinates → home address exposure
    """
    if "logged_in" not in session:
        flash("❌ Please login first", "error")
        return redirect(url_for("login"))

    if "profile_picture" not in request.files:
        flash("❌ No file selected", "error")
        return redirect(url_for("dashboard"))

    file = request.files["profile_picture"]

    if file.filename == "":
        flash("❌ No file selected", "error")
        return redirect(url_for("dashboard"))

    if file and allowed_file(file.filename):
        filename = secure_filename(
            f"profile_{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        )
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        try:
            # 🚨 VULNERABILITY: Save with ALL EXIF preserved (binary copy)
            save_with_exif_preserved(file, filepath)

            # Store metadata
            uploaded_images.append(
                {
                    "filename": filename,
                    "uploader": session["user"],
                    "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "original_name": file.filename,
                    "endpoint": "/upload",
                    "field_name": "profile_picture",
                    "type": "profile",
                }
            )

            flash(
                f"✅ Profile picture uploaded successfully: {file.filename}", "success"
            )
        except Exception as e:
            flash(f"❌ Error uploading file: {str(e)}", "error")
    else:
        flash("❌ Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, TIFF", "error")

    return redirect(url_for("dashboard"))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    """
    🚨 VULNERABILITY #2: Profile avatar upload (NO EXIF STRIPPING)
    
    Endpoint: POST /profile
    Field: avatar
    EXIF Preserved: YES - 100% of metadata retained
    
    Privacy Risk: Device serial numbers → persistent tracking
    """
    if "logged_in" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if "avatar" not in request.files:
            flash("❌ No file selected", "error")
            return redirect(url_for("profile"))

        file = request.files["avatar"]

        if file.filename == "":
            flash("❌ No file selected", "error")
            return redirect(url_for("profile"))

        if file and allowed_file(file.filename):
            filename = secure_filename(
                f"avatar_{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            )
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            try:
                # 🚨 VULNERABILITY: Save with ALL EXIF preserved (binary copy)
                save_with_exif_preserved(file, filepath)

                uploaded_images.append(
                    {
                        "filename": filename,
                        "uploader": session["user"],
                        "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "original_name": file.filename,
                        "endpoint": "/profile",
                        "field_name": "avatar",
                        "type": "avatar",
                    }
                )

                flash("✅ Avatar updated successfully!", "success")
            except Exception as e:
                flash(f"❌ Error uploading avatar: {str(e)}", "error")
        else:
            flash("❌ Invalid file type", "error")

    user_images = [
        img
        for img in uploaded_images
        if img["uploader"] == session["user"] and img.get("type") == "avatar"
    ]
    return render_template("profile.html", user=session["user"], images=user_images)


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    🚨 VULNERABILITY #3: Settings page with background image upload
    
    Endpoint: POST /settings
    Field: background_image
    EXIF Preserved: YES - 100% of metadata retained
    
    Privacy Risk: Author/PII information → identity disclosure
    """
    if "logged_in" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if "background_image" not in request.files:
            flash("❌ No file selected", "error")
            return redirect(url_for("settings"))

        file = request.files["background_image"]

        if file.filename == "":
            flash("❌ No file selected", "error")
            return redirect(url_for("settings"))

        if file and allowed_file(file.filename):
            filename = secure_filename(
                f"bg_{session['user']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            )
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            try:
                # 🚨 VULNERABILITY: Save with ALL EXIF preserved (binary copy)
                save_with_exif_preserved(file, filepath)

                uploaded_images.append(
                    {
                        "filename": filename,
                        "uploader": session["user"],
                        "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "original_name": file.filename,
                        "endpoint": "/settings",
                        "field_name": "background_image",
                        "type": "background",
                    }
                )

                flash("✅ Background image updated!", "success")
            except Exception as e:
                flash(f"❌ Error uploading background: {str(e)}", "error")
        else:
            flash("❌ Invalid file type", "error")

    return render_template("settings.html", user=session["user"])


@app.route("/api/images")
def api_images():
    """API endpoint to list all uploaded images (VULNERABILITY: No auth check)"""
    return jsonify(
        [
            {
                "filename": img["filename"],
                "uploader": img["uploader"],
                "upload_time": img["upload_time"],
                "original_name": img["original_name"],
                "endpoint": img.get("endpoint", "unknown"),
                "field_name": img.get("field_name", "unknown"),
                "download_url": url_for("download_image", filename=img["filename"]),
            }
            for img in uploaded_images
        ]
    )


@app.route("/api/user-stats")
def api_user_stats():
    """API endpoint for user statistics"""
    if "logged_in" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = session["user"]
    user_images = [img for img in uploaded_images if img["uploader"] == user]

    return jsonify(
        {
            "username": user,
            "total_uploads": len(user_images),
            "images": [img["original_name"] for img in user_images],
            "upload_endpoints_tested": list(
                set([img.get("endpoint", "unknown") for img in user_images])
            ),
        }
    )


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash("⚠️ File too large! Maximum size is 16MB", "error")
    return redirect(request.url), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template("500.html"), 500


# Export app for Vercel
# This is the WSGI application that Vercel will use
def handler(event, context):
    """Vercel serverless function handler"""
    return app

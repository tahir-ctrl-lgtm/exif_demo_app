# Vercel Deployment Guide

This Flask application is now configured for deployment on Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): Install with `npm i -g vercel`
3. **Git Repository**: Push your code to GitHub, GitLab, or Bitbucket

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Login to Vercel**
   - Go to [vercel.com](https://vercel.com) and sign in

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your Git repository
   - Select the root directory: `exif_demo_app`

3. **Configure Project**
   - Framework Preset: `Other`
   - Root Directory: `./` (or the path to exif_demo_app)
   - Build Command: Leave empty
   - Output Directory: Leave empty

4. **Environment Variables** (Optional)
   - Add `SECRET_KEY` with a secure random value
   - Example: `SECRET_KEY=your-secret-key-here`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live at: `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from project directory**
   ```bash
   cd exif_demo_app
   vercel
   ```

4. **Follow the prompts**
   - Set up and deploy: `Y`
   - Scope: Select your account
   - Link to existing project: `N`
   - Project name: Enter a name
   - Directory: `./`
   - Override settings: `N`

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Important Notes

### File Storage Limitations

⚠️ **Vercel uses ephemeral storage** - uploaded files are stored in `/tmp/` and will be **deleted after the function execution completes**. This means:

- Uploaded images will NOT persist between requests
- Files will disappear after serverless function timeout
- This is suitable for demo/testing purposes only

### For Production Use

If you need persistent file storage, consider:

1. **Vercel Blob Storage**
   - Add `@vercel/blob` to your dependencies
   - Store files in Vercel's blob storage
   - [Vercel Blob Documentation](https://vercel.com/docs/storage/vercel-blob)

2. **External Storage Services**
   - AWS S3
   - Google Cloud Storage
   - Azure Blob Storage
   - Cloudinary

3. **Database Storage**
   - Store small images in a database (not recommended for large files)
   - Use services like Supabase, PlanetScale, or MongoDB Atlas

### Configuration Files

The following files have been created/configured for Vercel:

- **`vercel.json`**: Vercel configuration
  - Defines build settings
  - Routes static files and API requests
  - Sets environment variables

- **`api/index.py`**: Vercel entry point
  - Flask application configured for serverless
  - Uses `/tmp/` for temporary file storage
  - Templates and static files properly referenced

- **`.vercelignore`**: Files to exclude from deployment
  - Excludes Python cache, virtual environments
  - Prevents uploading unnecessary files

## Testing Locally

To test the Vercel configuration locally:

```bash
# Install Vercel CLI
npm i -g vercel

# Run development server
vercel dev
```

This will start a local server that simulates Vercel's environment.

## Access Your Deployed App

After deployment, your app will be available at:
```
https://your-project-name.vercel.app
```

### Default Login Credentials

- Username: `demo` | Password: `demo123`
- Username: `testuser` | Password: `password`
- Username: `admin` | Password: `admin123`

## Troubleshooting

### Build Errors

If you encounter build errors:
1. Check that all dependencies are in `requirements.txt`
2. Verify Python version compatibility
3. Check Vercel build logs

### Runtime Errors

1. **500 Internal Server Error**: Check Vercel function logs
2. **File upload issues**: Remember files are ephemeral in `/tmp/`
3. **Template not found**: Verify template paths in `api/index.py`

### View Logs

```bash
vercel logs your-deployment-url
```

Or view logs in Vercel Dashboard under "Deployments" → Select deployment → "Function Logs"

## Security Notes

⚠️ This application is intentionally vulnerable for testing purposes:
- EXIF metadata is preserved (security vulnerability demo)
- Do NOT use in production
- For educational/testing purposes only

## Custom Domain (Optional)

1. Go to your project in Vercel Dashboard
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Continuous Deployment

Once connected to Git:
- Every push to `main` branch triggers a production deployment
- Pull requests create preview deployments
- Automatic rollbacks available

## Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- [Vercel CLI Reference](https://vercel.com/docs/cli)
- [Vercel Storage Options](https://vercel.com/docs/storage)

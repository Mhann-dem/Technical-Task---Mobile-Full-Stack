# Setup Instructions

Quick setup guide to get the Image Analysis API running.

## Prerequisites

- **Python 3.9+** (Tested with Python 3.13)
- **pip** (Python package manager)
- **Git** (for version control)

## Installation Steps

### 1. Navigate to Project Directory

```powershell
cd "Technical Task – Mobile Full-Stack"
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` appear in your prompt like:
```
(venv) PS C:\Users\...\Technical Task – Mobile Full-Stack>
```

**On Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Running the Server

### Option 1: Using the Provided Script (Recommended)

**On Windows (PowerShell):**
```powershell
.\run_server.ps1
```

**On Windows (Command Prompt):**
```cmd
run_server.bat
```

### Option 2: Manual Command

After activating the virtual environment:
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

## Server Status

Once the server starts, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

## Testing the API

1. **Open Swagger UI Documentation:**
   - Navigate to: http://localhost:8000/docs

2. **API Endpoints Available:**
   - `GET /` - Health check
   - `GET /health` - Health status
   - `POST /api/upload` - Upload image
   - `POST /api/analyze` - Analyze image

3. **Try the API:**
   - Click "Try it out" on any endpoint
   - Add the API key header (default: `test-api-key-12345`)
   - Test upload and analysis workflows

## Environment Configuration

Create a `.env` file for custom settings:

```powershell
cp .env.example .env
```

Edit `.env` to customize:
- `API_KEY` - Custom API key
- `MAX_FILE_SIZE` - Maximum upload size
- `ENABLE_API_KEY` - Enable/disable authentication

## Virtual Environment Management

### Deactivate Virtual Environment

```powershell
deactivate
```

### Delete Virtual Environment (if needed)

```powershell
Remove-Item -Recurse -Force venv
```

## Troubleshooting

### "Module not found" errors
- Ensure virtual environment is **activated** (check for `(venv)` in prompt)
- Reinstall dependencies: `pip install -r requirements.txt`

### Port 8000 already in use
- Use different port: `python -m uvicorn app.main:app --port 8001`

### File upload issues
- Ensure `uploads/` directory exists (created automatically)
- Check file size is under 5MB
- Verify file format is JPEG or PNG

## Next Steps

1. ✅ Server is running
2. ✅ Test API endpoints
3. ✅ Verify image upload/analysis functionality
4. 📝 Initialize Git and push to repository

See `README.md` for detailed API documentation.

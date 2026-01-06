# Technical Task Submission - Mobile Full-Stack Developer (Backend-Driven)

## Project Overview

This is a complete **FastAPI REST backend service** for a mobile image analysis application. The service demonstrates production-ready code patterns, including proper authentication, error handling, logging, and Docker support.

## ✅ Requirements Met

### Core Functionality
- ✅ **Image Upload Endpoint** (`POST /api/upload`)
  - Accepts JPEG and PNG files
  - Validates file type and size (max 5MB)
  - Returns unique image_id
  - Stores files locally in `uploads/` directory

- ✅ **Image Analysis Endpoint** (`POST /api/analyze`)
  - Accepts image_id
  - Performs mock analysis (no ML required)
  - Returns structured JSON with:
    - Skin type
    - Detected issues
    - Confidence score (0.65-0.99)

### Technical Requirements
- ✅ **Language:** Python
- ✅ **Framework:** FastAPI
- ✅ **API Type:** REST
- ✅ **Storage:** Local file system

### Code Quality
- ✅ Clean folder structure with separation of concerns
- ✅ Clear separation between routes, services, and utilities
- ✅ Readable, maintainable code
- ✅ Comprehensive error handling
- ✅ Input validation for all endpoints

### Bonus Features (All Implemented)
- ✅ **API Key Authentication** - `X-API-Key` header validation
- ✅ **Comprehensive Logging** - Console and rotating file logs
- ✅ **Docker Support** - Production-ready Dockerfile with multi-stage build
- ✅ **Health Checks** - Monitoring endpoints
- ✅ **Error Handling** - Proper HTTP status codes and messages

## Project Structure

```
Technical Task – Mobile Full-Stack/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py           # Image upload endpoint
│   │   └── analyze.py          # Image analysis endpoint
│   └── utils/
│       ├── __init__.py
│       ├── auth.py             # API key authentication
│       ├── validators.py       # File/image validation
│       ├── analysis.py         # Mock analysis logic
│       └── logger.py           # Logging configuration
├── uploads/                    # Uploaded images storage
├── logs/                       # Application logs
├── venv/                       # Virtual environment
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
├── .env.example                # Example .env file
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Container configuration
├── README.md                   # Detailed documentation
├── SETUP.md                    # Setup instructions
├── run_server.ps1              # PowerShell startup script
├── run_server.bat              # Batch startup script
└── SUBMISSION.md               # This file
```

## Quick Start

### 1. Prerequisites
- Python 3.9 or higher
- Virtual environment support

### 2. Installation

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Server

**Option A - Using startup script (Recommended):**
```powershell
.\run_server.ps1
```

**Option B - Manual command:**
```powershell
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Test API

Visit: http://localhost:8000/docs

## API Endpoints

### 1. Upload Image
**Endpoint:** `POST /api/upload`

**Headers:**
```
X-API-Key: test-api-key-12345
Content-Type: multipart/form-data
```

**Request:**
- File upload (JPEG or PNG, max 5MB)

**Success Response (200):**
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "photo.jpg",
  "size": 1024000,
  "message": "Image uploaded successfully"
}
```

### 2. Analyze Image
**Endpoint:** `POST /api/analyze`

**Headers:**
```
X-API-Key: test-api-key-12345
Content-Type: application/json
```

**Request Body:**
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Success Response (200):**
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "skin_type": "Oily",
  "detected_issues": ["Acne", "Texture Issues"],
  "confidence": 0.87
}
```

## Configuration

Create `.env` file (or copy from `.env.example`):

```env
API_KEY=test-api-key-12345
MAX_FILE_SIZE=5242880
ENABLE_API_KEY=true
```

## Testing Workflow

1. **Upload Image:**
   - Go to http://localhost:8000/docs
   - Try `/api/upload` endpoint
   - Upload a JPEG or PNG file
   - Copy the returned `image_id`

2. **Analyze Image:**
   - Try `/api/analyze` endpoint
   - Paste the `image_id`
   - Get mock analysis results

3. **Test Error Cases:**
   - Upload non-image file (should get 400)
   - Upload file > 5MB (should get 413)
   - Analyze non-existent image_id (should get 404)
   - Request without API key (should get 401)

## File Size Limits

- **Maximum upload:** 5MB
- **Supported formats:** JPEG (.jpg, .jpeg), PNG (.png)

## Authentication

All endpoints require `X-API-Key` header:
- **Default key:** `test-api-key-12345`
- **Can be customized** via `.env` file
- **Can be disabled** by setting `ENABLE_API_KEY=false`

## Logging

Application logs are written to:
- **Console:** Real-time output during execution
- **File:** `logs/app.log` (with automatic rotation)

Log levels: DEBUG, INFO, WARNING, ERROR

## Docker Deployment

### Build Image
```bash
docker build -t image-analysis-api:1.0 .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e API_KEY=your-api-key \
  -v $(pwd)/uploads:/app/uploads \
  image-analysis-api:1.0
```

## Assumptions Made

1. **Mock Analysis:** Analysis logic is mocked and returns randomized but realistic results
2. **Local Storage:** Images stored in local file system, not cloud storage
3. **Single Instance:** Designed for single-server deployment
4. **Stateless API:** No session management; each request is independent
5. **File Format:** Images stored in original format (JPEG/PNG)
6. **No Database:** Image metadata not persisted (IDs generated per upload session)

## Production Recommendations

For production deployment, consider:

1. **Database Integration** - Persist image metadata (PostgreSQL, MongoDB)
2. **Real ML Models** - Integrate actual image analysis models
3. **Cloud Storage** - Use S3, Azure Blob Storage, or Google Cloud Storage
4. **Caching** - Implement Redis for frequently analyzed images
5. **Rate Limiting** - Prevent API abuse
6. **HTTPS/TLS** - Enable secure communication
7. **Image Processing** - Add resizing, compression, optimization
8. **Async Processing** - Use Celery for long-running analysis tasks
9. **Monitoring** - Integrate Prometheus/Grafana for metrics
10. **Testing** - Add comprehensive unit and integration tests

## Key Features

- 🔐 **Secure:** API key authentication on all endpoints
- 📝 **Logged:** Comprehensive application logging
- 🐳 **Containerized:** Docker support for easy deployment
- ✅ **Validated:** File type and size validation
- 🔄 **Auto-reload:** Development server with hot reload
- 📊 **Documented:** Swagger UI with interactive API docs
- 🎯 **Clean:** Organized code structure with clear separation
- 🚀 **Production-ready:** Error handling and health checks

## Submission Contents

This submission includes:

1. ✅ Complete FastAPI backend application
2. ✅ All source code with proper structure
3. ✅ Virtual environment setup files
4. ✅ Configuration files (.env, requirements.txt)
5. ✅ Docker configuration
6. ✅ Comprehensive documentation (README, SETUP, this file)
7. ✅ Startup scripts for easy execution
8. ✅ Git initialization ready

## Running Locally

```powershell
# Clone/navigate to project
cd "Technical Task – Mobile Full-Stack"

# Activate venv
.\venv\Scripts\Activate.ps1

# Run server
python -m uvicorn app.main:app --reload

# Test at http://localhost:8000/docs
```

## Support & Troubleshooting

See `SETUP.md` for detailed troubleshooting guide.

---

**Status:** ✅ Complete and tested
**Last Updated:** January 6, 2026
**Python Version:** 3.9+
**Framework:** FastAPI 0.104.1

# Image Analysis API - Backend Service

A FastAPI-based REST backend service that allows mobile applications to upload images and receive mock analysis results.

## 🎯 Overview

This backend service provides two main endpoints:
1. **Image Upload** - Accept and store image files (JPEG/PNG)
2. **Image Analysis** - Perform mock analysis on uploaded images

The service demonstrates:
- Clean architecture with separation of concerns
- Proper error handling and validation
- API key authentication
- Comprehensive logging
- Production-ready patterns

## 📋 Requirements

- **Language**: Python 3.9+
- **Framework**: FastAPI
- **API Type**: REST
- **Storage**: Local file system

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### 2. Installation

```bash
# Clone or navigate to the project directory
cd "Technical Task – Mobile Full-Stack"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Service

```bash
# Run the server
python -m uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

### 4. Verify Installation

Open your browser and visit:
- **Health Check**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

## 📡 API Endpoints

### 1. Image Upload Endpoint

**Endpoint**: `POST /api/upload`

**Description**: Upload an image file for storage and processing

**Headers**:
```
X-API-Key: test-api-key-12345
Content-Type: multipart/form-data
```

**Request**:
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "X-API-Key: test-api-key-12345" \
  -F "file=@/path/to/image.jpg"
```

**Success Response** (200):
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "photo.jpg",
  "size": 1024000,
  "message": "Image uploaded successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid file type
- `401 Unauthorized`: Missing API key
- `403 Forbidden`: Invalid API key
- `413 Payload Too Large`: File exceeds 5MB limit
- `500 Internal Server Error`: Server error during upload

### 2. Image Analysis Endpoint

**Endpoint**: `POST /api/analyze`

**Description**: Analyze a previously uploaded image

**Headers**:
```
X-API-Key: test-api-key-12345
Content-Type: application/json
```

**Request Body**:
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Request Example**:
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "X-API-Key: test-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Success Response** (200):
```json
{
  "image_id": "550e8400-e29b-41d4-a716-446655440000",
  "skin_type": "Oily",
  "detected_issues": ["Acne", "Texture Issues"],
  "confidence": 0.87
}
```

**Error Responses**:
- `401 Unauthorized`: Missing API key
- `403 Forbidden`: Invalid API key
- `404 Not Found`: Image ID not found
- `500 Internal Server Error`: Server error during analysis

## 📁 Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and settings
├── routes/
│   ├── __init__.py
│   ├── upload.py        # Image upload endpoint
│   └── analyze.py       # Image analysis endpoint
└── utils/
    ├── __init__.py
    ├── auth.py          # API key authentication
    ├── validators.py    # File and image validation
    ├── analysis.py      # Mock analysis logic
    └── logger.py        # Logging configuration

uploads/                 # Directory for stored images
logs/                    # Application logs
requirements.txt         # Python dependencies
README.md               # This file
Dockerfile              # Container image definition
.env.example            # Example environment variables
.gitignore              # Git ignore rules
```

## 🔐 Authentication

The API uses API key authentication via the `X-API-Key` header.

**Default API Key**: `test-api-key-12345`

To use a custom API key:

1. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

2. Edit `.env` and set your API key:
```
API_KEY=your-custom-api-key-12345
```

3. Restart the server

To disable API key authentication (not recommended for production):
```
ENABLE_API_KEY=false
```

## 📝 File Validation

### Accepted Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)

### Size Limits
- Maximum file size: **5MB**

## 🧪 Testing the API

### Using Swagger UI (Interactive)

1. Start the server
2. Open http://localhost:8000/docs
3. Use the interactive interface to test endpoints

### Using curl (Command Line)

**Upload Image**:
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "X-API-Key: test-api-key-12345" \
  -F "file=@test-image.jpg"
```

**Analyze Image**:
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "X-API-Key: test-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "your-image-id-here"}'
```

## 🔍 Logging

Application logs are written to:
- **Console**: Real-time output during execution
- **File**: `logs/app.log` - Persistent logs with rotation (max 10MB per file)

Log levels:
- `DEBUG`: Detailed diagnostic information
- `INFO`: General informational messages
- `WARNING`: Warning messages for suspicious events
- `ERROR`: Error messages for serious problems

## 🐳 Docker Deployment

### Build Docker Image

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

## 📊 Mock Analysis Logic

The analysis endpoint returns mock results with:
- **Skin Type**: One of [Oily, Dry, Combination, Sensitive, Normal]
- **Detected Issues**: List of detected skin issues
- **Confidence Score**: Confidence level (0.65 - 0.99)

**Note**: This is a mock implementation. In production, integrate with actual ML/AI models.

## 💡 Assumptions Made

1. **Mock Analysis**: Analysis logic is mocked and returns randomized but realistic results
2. **Local Storage**: Images are stored in the local file system, not cloud storage
3. **Single Server**: Designed for single-instance deployment
4. **Stateless API**: No session management; each request is independent
5. **Image Format**: Images are stored in their original format (JPEG/PNG)
6. **No Database**: Image metadata is not persisted (IDs are generated per upload)

## 🎁 Bonus Features Implemented

✅ **API Key Authentication**: Secure access control via API key header
✅ **Comprehensive Logging**: Detailed logging to console and file
✅ **Docker Support**: Production-ready Dockerfile with multi-stage build
✅ **Error Handling**: Proper HTTP error codes and messages
✅ **Input Validation**: File type and size validation
✅ **Health Checks**: Health check endpoints for monitoring

## 🚀 Production Improvements

If this were a production service, the following improvements would be recommended:

1. **Database Integration**: Store image metadata in a database (PostgreSQL, MongoDB)
2. **Real ML/AI Models**: Integrate with actual image analysis models
3. **Cloud Storage**: Use S3, Azure Blob Storage, or Google Cloud Storage
4. **Caching**: Implement Redis caching for frequently analyzed images
5. **Rate Limiting**: Add rate limiting to prevent abuse
6. **HTTPS**: Enable SSL/TLS for secure communication
7. **Image Processing**: Add image resizing, compression, and optimization
8. **Async Processing**: Use Celery or similar for long-running analysis tasks
9. **Monitoring**: Integrate with Prometheus/Grafana for metrics
10. **Testing**: Add comprehensive unit and integration tests

## 📞 Support & Questions

For issues or questions:
1. Check the error message and HTTP status code
2. Review the logs in `logs/app.log`
3. Verify file format is JPEG or PNG
4. Ensure file size is under 5MB
5. Check that API key is correct

## 📄 License

This project is provided as-is for technical assessment purposes.

---

**Built with**: Python 3.11, FastAPI, Uvicorn
**Last Updated**: January 2026

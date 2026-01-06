@echo off
REM Test script for Image Analysis API
REM This script tests all API endpoints

setlocal enabledelayedexpansion
set API_URL=http://localhost:8000
set API_KEY=test-api-key-12345

echo.
echo ========================================
echo Image Analysis API - Test Suite
echo ========================================
echo.

REM Test 1: Health Check
echo [TEST 1] Health Check - GET /
echo Testing server health...
powershell -Command "Invoke-WebRequest -Uri '%API_URL%/' -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json"
echo.

REM Test 2: Health Endpoint
echo [TEST 2] Health Status - GET /health
powershell -Command "Invoke-WebRequest -Uri '%API_URL%/health' -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json | ConvertTo-Json"
echo.

REM Test 3: Upload without API key (should fail)
echo [TEST 3] Upload without API Key (Expected: 401 Unauthorized)
powershell -Command "try { Invoke-WebRequest -Uri '%API_URL%/api/upload' -Method Post -UseBasicParsing } catch { Write-Host $_.Exception.Message }"
echo.

REM Test 4: Test with missing Authorization
echo [TEST 4] Test API Key Validation
powershell -Command "try { Invoke-WebRequest -Uri '%API_URL%/api/upload' -Method Post -ContentType 'application/json' -UseBasicParsing } catch { Write-Host Status: $_.Exception.Response.StatusCode }"
echo.

echo ========================================
echo To test file upload:
echo 1. Go to http://localhost:8000/docs
echo 2. Click 'Try it out' on /api/upload
echo 3. Upload a JPEG or PNG file
echo 4. Copy the image_id
echo 5. Use image_id in /api/analyze
echo ========================================
echo.
echo Tests complete!
pause

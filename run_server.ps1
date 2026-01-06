# Run the FastAPI server from the virtual environment
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Activate virtual environment and keep the shell interactive
Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# The (venv) prompt will now appear in the current shell
# Run the server
Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "Virtual environment is active. Server running at http://localhost:8000" -ForegroundColor Cyan
python -m uvicorn app.main:app --reload --port 8000

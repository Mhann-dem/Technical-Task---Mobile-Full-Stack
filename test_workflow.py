"""
Complete workflow test for Image Upload and Analysis
Tests the full workflow: Upload -> Analyze
"""

import requests
import json
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000"
API_KEY = "test-api-key-12345"
HEADERS = {"X-API-Key": API_KEY}

def print_header(title):
    """Print section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def upload_image(image_path):
    """Upload an image file via API"""
    print_header(f"UPLOADING IMAGE: {Path(image_path).name}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/api/upload", headers=HEADERS, files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload Successful!")
            print(f"   Image ID: {data['image_id']}")
            print(f"   Filename: {data['filename']}")
            print(f"   Size: {data['size']} bytes")
            print(f"   Message: {data['message']}")
            return data['image_id']
        else:
            print(f"❌ Upload Failed!")
            print(f"   Error: {response.json().get('detail', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def analyze_image(image_id):
    """Analyze an uploaded image"""
    print_header(f"ANALYZING IMAGE: {image_id}")
    
    try:
        payload = {"image_id": image_id}
        response = requests.post(f"{API_URL}/api/analyze", headers=HEADERS, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analysis Successful!")
            print(f"   Image ID: {data['image_id']}")
            print(f"   Skin Type: {data['skin_type']}")
            print(f"   Detected Issues: {', '.join(data['detected_issues']) if data['detected_issues'] else 'None'}")
            print(f"   Confidence: {data['confidence']:.2%}")
            return True
        else:
            print(f"❌ Analysis Failed!")
            print(f"   Error: {response.json().get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def find_image_files():
    """Find all image files in uploads directory"""
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        print("❌ uploads directory not found")
        return []
    
    image_extensions = {'.jpg', '.jpeg', '.png'}
    images = [f for f in uploads_dir.iterdir() if f.suffix.lower() in image_extensions]
    return sorted(images)

def main():
    """Main test workflow"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  Image Analysis API - Upload & Analyze Workflow Test".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Find image files
    print_header("FINDING IMAGES TO UPLOAD")
    image_files = find_image_files()
    
    if not image_files:
        print("No image files found in uploads directory")
        print("\nPlace JPEG or PNG images in the 'uploads' folder and run this script again")
        return
    
    print(f"Found {len(image_files)} image(s):")
    for i, img in enumerate(image_files, 1):
        print(f"  {i}. {img.name} ({img.stat().st_size / 1024:.1f} KB)")
    
    # Test upload and analyze workflow
    print_header("TESTING UPLOAD & ANALYZE WORKFLOW")
    
    results = []
    
    for image_path in image_files:
        print(f"\n📝 Processing: {image_path.name}")
        
        # Upload
        image_id = upload_image(str(image_path))
        if not image_id:
            results.append((image_path.name, False))
            continue
        
        # Analyze
        success = analyze_image(image_id)
        results.append((image_path.name, success))
    
    # Summary
    print_header("TEST SUMMARY")
    
    for filename, success in results:
        symbol = "✅" if success else "❌"
        print(f"{symbol} {filename}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print()
    print(f"Results: {passed}/{total} images processed successfully")
    print(f"Success Rate: {(passed/total)*100:.1f}%" if total > 0 else "N/A")
    
    # Instructions
    print_header("TESTING VIA SWAGGER UI")
    print("""
You can also test the API interactively:

1. Open: http://localhost:8000/docs
2. Upload an image:
   - Click on POST /api/upload
   - Click "Try it out"
   - Select a JPEG or PNG file from your computer
   - Click "Execute"
   - Copy the "image_id" from the response

3. Analyze the image:
   - Click on POST /api/analyze
   - Click "Try it out"
   - Paste the "image_id" in the request body
   - Click "Execute"
   - View the analysis results with:
     * skin_type: The detected skin type
     * detected_issues: List of detected issues
     * confidence: Confidence score (0-1)

API Key:
- All requests require: X-API-Key: test-api-key-12345
- Swagger UI handles this automatically in the header
    """)
    
    print("="*70)
    print("Workflow test complete!\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to http://localhost:8000")
        print("   Make sure the server is running with: .\\run_server.ps1")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

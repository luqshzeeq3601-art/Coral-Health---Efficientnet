
import requests
import numpy as np
import cv2
import io

# Create a dummy image
img = np.zeros((224, 224, 3), dtype=np.uint8)
cv2.rectangle(img, (50, 50), (150, 150), (255, 255, 255), -1)
_, buffer = cv2.imencode('.png', img)
img_bytes = io.BytesIO(buffer)

url = 'http://localhost:5000/api/predict'
files = {'file': ('test.png', img_bytes, 'image/png')}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response received.")
        if 'gradcam' in data and 'heatmap' in data['gradcam']:
            print("Grad-CAM present in response.")
        elif 'gradcam' in data and 'error' in data['gradcam']:
            print(f"Grad-CAM error in response: {data['gradcam']['error']}")
        else:
            print("Grad-CAM missing from response key structure.")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")

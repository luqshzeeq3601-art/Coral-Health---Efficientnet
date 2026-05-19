@echo off
REM Start the Flask app
start "Coral App" cmd /k "cd /d C:\Users\ZeeqRyz\Desktop\BASEPROJECT\04_Web_Application && python app.py"

REM Start the Cloudflare tunnel
start "Coral Tunnel" cmd /k ""C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --protocol http2 --url http://localhost:5000 run coralapp"

echo Started app and tunnel windows.

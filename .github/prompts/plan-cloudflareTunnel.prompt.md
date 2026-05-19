## Plan: Cloudflare Tunnel for Local Flask App

Expose the local Flask application running on Windows port 5000 to the internet using a Cloudflare Tunnel linked to a domain managed by name.com.

**Steps**
1. **Install Cloudflared CLI**: Download and install the Cloudflare daemon (`cloudflared`) for Windows using Winget (`winget install --id Cloudflare.cloudflared`) or via the direct download from Cloudflare.
2. **Authenticate Cloudflared**: Run `cloudflared tunnel login`. This will open a browser to authorize the daemon with the Cloudflare account associated with the domain.
3. **Create the Tunnel**: Run `cloudflared tunnel create flask-app-tunnel` to register the new tunnel.
4. **Configure DNS Routing**: Bind the tunnel to the desired domain/subdomain by running `cloudflared tunnel route dns flask-app-tunnel <your-domain.com>`.
5. **Start Local App**: Run the Flask application (04_Web_Application/app.py) so it listens on port 5000.
6. **Start the Tunnel**: Run the tunnel to connect incoming domain traffic to the local Flask application using `cloudflared tunnel run --url http://localhost:5000 flask-app-tunnel`.

**Relevant files**
- `04_Web_Application/app.py` — Runs the local Flask web server on port 5000. No code changes are required here since it already binds to `0.0.0.0` or `127.0.0.1` locally.

**Verification**
1. Open a web browser and visit `https://<your-domain.com>`. Ensure the application loads correctly and functions identically to `http://localhost:5000`.
2. Check the terminal running `cloudflared` for incoming HTTP traffic logs to verify routing is successful.

**Decisions**
- The domain is already managed by Cloudflare.
- The built-in Flask development server will be used instead of a production WSGI server, per user preference.

**Further Considerations**
1. Do you want to run `cloudflared` as a background Windows Service so the tunnel starts automatically on system boot?
2. Ensure no local firewall rules on your Windows machine are blocking outgoing connections from `cloudflared.exe`.
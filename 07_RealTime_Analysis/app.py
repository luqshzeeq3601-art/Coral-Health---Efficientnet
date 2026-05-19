from __future__ import annotations

from pathlib import Path
from typing import Optional

from flask import Flask, jsonify, make_response, render_template, request, send_file
from flask_cors import CORS

from src.model_runtime import RealTimeModelRuntime, decode_frame_from_request
from src.stream_runtime import StreamWorker


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True
CORS(app)

runtime = RealTimeModelRuntime(MODELS_DIR)
stream_worker = StreamWorker(runtime)
latest_frame_bgr = None


@app.route("/")
def home():
    response = make_response(render_template("realtime.html"))
    response.headers["X-Template-Source"] = "realtime.html"
    return response


@app.after_request
def disable_html_cache(response):
    if response.content_type and response.content_type.startswith("text/html"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.route("/assets/coral-preview-bg.png")
def coral_preview_bg():
    bg_path = BASE_DIR.parent / "04_Web_Application" / "static" / "img" / "coral_hero_bg.png"
    return send_file(bg_path)


@app.route("/api/health", methods=["GET"])
def health():
    mode = request.args.get("mode", "fast")
    return jsonify(
        {
            "status": "running",
            "app": "Safe Real-Time Coral Analysis",
            "port": 5050,
            "runtime": runtime.status(mode),
            "stream": stream_worker.status(),
        }
    )


@app.route("/api/frame", methods=["POST"])
def analyze_frame():
    global latest_frame_bgr
    try:
        payload = request.get_json(silent=True)
        mode = request.form.get("mode") or request.args.get("mode") or (payload or {}).get("mode") or "fast"
        frame = decode_frame_from_request(request.files, payload)
        latest_frame_bgr = frame.copy()
        result = runtime.predict_frame(frame, mode=str(mode))
        return jsonify({"ok": True, "result": result})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.route("/api/explain", methods=["POST"])
def explain_frame():
    global latest_frame_bgr
    try:
        payload = request.get_json(silent=True) or {}
        mode = request.form.get("mode") or request.args.get("mode") or payload.get("mode") or "fast"
        class_name = request.form.get("class") or request.args.get("class") or payload.get("class")

        frame = None
        if request.files or "image" in payload:
            frame = decode_frame_from_request(request.files, payload)
        elif latest_frame_bgr is not None:
            frame = latest_frame_bgr
        else:
            frame = stream_worker.latest_frame()

        if frame is None:
            return jsonify({"ok": False, "error": "No frame available to explain"}), 400

        latest_frame_bgr = frame.copy()
        result = runtime.explain_frame(frame, class_name=class_name, mode=str(mode))
        return jsonify({"ok": True, "result": result})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.route("/api/video/start", methods=["POST"])
def start_video():
    payload = request.get_json(silent=True) or {}
    source_type = str(payload.get("source_type", "webcam")).lower()
    mode = str(payload.get("mode", "fast"))
    analyze_every = int(payload.get("analyze_every", 5) or 5)

    if source_type == "video":
        video_path = payload.get("video_path")
        if not video_path:
            return jsonify({"ok": False, "error": "video_path is required for video source"}), 400
        status = stream_worker.start(str(video_path), f"video:{video_path}", mode=mode, analyze_every=analyze_every)
    else:
        camera_index = int(payload.get("camera_index", 0) or 0)
        status = stream_worker.start(camera_index, f"webcam:{camera_index}", mode=mode, analyze_every=analyze_every)

    return jsonify({"ok": True, "stream": status})


@app.route("/api/video/stop", methods=["POST"])
def stop_video():
    return jsonify({"ok": True, "stream": stream_worker.stop()})


@app.route("/api/video/status", methods=["GET"])
def video_status():
    return jsonify({"ok": True, "stream": stream_worker.status()})


if __name__ == "__main__":
    runtime.load_models("fast")
    app.run(host="127.0.0.1", port=5050, debug=False, threaded=True)

from __future__ import annotations

import base64
import threading
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Union

import cv2
import numpy as np

from .model_runtime import RealTimeModelRuntime


@dataclass
class StreamState:
    running: bool = False
    source: str = "idle"
    mode: str = "fast"
    analyze_every: int = 5
    frames_seen: int = 0
    frames_analyzed: int = 0
    fps: float = 0.0
    latest_prediction: Optional[Dict[str, object]] = None
    latest_frame_jpeg: Optional[str] = None
    error: Optional[str] = None
    started_at: float = field(default_factory=time.time)


class StreamWorker:
    """Background OpenCV capture loop for local webcam or video paths."""

    def __init__(self, runtime: RealTimeModelRuntime):
        self.runtime = runtime
        self._state = StreamState()
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._latest_bgr: Optional[np.ndarray] = None

    def start(self, source: Union[int, str], source_label: str, mode: str = "fast", analyze_every: int = 5) -> Dict[str, object]:
        self.stop()
        analyze_every = max(1, int(analyze_every or 1))
        self._stop_event.clear()
        with self._lock:
            self._state = StreamState(running=True, source=source_label, mode=mode, analyze_every=analyze_every)
            self._latest_bgr = None

        self._thread = threading.Thread(
            target=self._run_capture,
            args=(source, source_label, mode, analyze_every),
            daemon=True,
        )
        self._thread.start()
        return self.status()

    def stop(self) -> Dict[str, object]:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        with self._lock:
            self._state.running = False
        return self.status()

    def status(self) -> Dict[str, object]:
        with self._lock:
            return dict(self._state.__dict__)

    def latest_frame(self) -> Optional[np.ndarray]:
        with self._lock:
            return None if self._latest_bgr is None else self._latest_bgr.copy()

    def _run_capture(self, source: Union[int, str], source_label: str, mode: str, analyze_every: int) -> None:
        capture = cv2.VideoCapture(source)
        if not capture.isOpened():
            with self._lock:
                self._state.running = False
                self._state.error = f"Could not open {source_label}"
            return

        last_tick = time.perf_counter()
        fps_window_start = last_tick
        fps_frames = 0

        try:
            while not self._stop_event.is_set():
                ok, frame = capture.read()
                if not ok:
                    break

                fps_frames += 1
                now = time.perf_counter()
                elapsed = now - fps_window_start
                fps = fps_frames / elapsed if elapsed > 0 else 0.0

                with self._lock:
                    self._state.frames_seen += 1
                    frame_index = self._state.frames_seen
                    self._state.fps = fps
                    self._latest_bgr = frame.copy()

                if frame_index % analyze_every == 0:
                    try:
                        prediction = self.runtime.predict_frame(frame, mode=mode)
                        jpeg = self._encode_frame(frame)
                        with self._lock:
                            self._state.frames_analyzed += 1
                            self._state.latest_prediction = prediction
                            self._state.latest_frame_jpeg = jpeg
                            self._state.error = None
                    except Exception as exc:
                        with self._lock:
                            self._state.error = str(exc)

                if now - last_tick < 0.001:
                    time.sleep(0.001)
                last_tick = now
        finally:
            capture.release()
            with self._lock:
                self._state.running = False

    def _encode_frame(self, frame_bgr: np.ndarray) -> str:
        ok, buffer = cv2.imencode(".jpg", frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            return ""
        encoded = base64.b64encode(buffer).decode("ascii")
        return f"data:image/jpeg;base64,{encoded}"

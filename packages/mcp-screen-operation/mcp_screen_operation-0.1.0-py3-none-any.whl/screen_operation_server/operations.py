"""Screen and window operations using platform-agnostic implementations."""

import base64
import io
from typing import Any, Dict, List

import mss
from PIL import Image

from .window_manager import get_window_manager


def _capture_to_base64(sct: mss.mss, monitor: Dict) -> Dict[str, str]:
    """Captures a region and returns it as a base64 encoded PNG."""
    sct_img = sct.grab(monitor)
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return {"content": img_str, "mime_type": "image/png"}


def get_screen_info() -> Dict[str, Any]:
    """Gets information about all connected displays."""
    with mss.mss() as sct:
        # sct.monitors[0] is a virtual monitor of all screens combined
        monitors = sct.monitors
        return {
            "monitor_count": len(monitors) - 1 if len(monitors) > 1 else 1,
            "monitors": [
                {
                    "id": i,
                    "width": m["width"],
                    "height": m["height"],
                    "top": m["top"],
                    "left": m["left"],
                }
                for i, m in enumerate(monitors)
            ],
        }


def capture_screen_by_number(monitor_number: int) -> Dict[str, str]:
    """Captures a screenshot of a specific monitor."""
    with mss.mss() as sct:
        try:
            monitor = sct.monitors[monitor_number]
            return _capture_to_base64(sct, monitor)
        except IndexError:
            raise ValueError(f"Monitor {monitor_number} not found.")


def capture_all_screens() -> Dict[str, str]:
    """Captures all screens and stitches them into a single image."""
    with mss.mss() as sct:
        # Skip the first monitor which is the combined view of all monitors
        monitors_to_capture = sct.monitors[1:]

        # If only one monitor, capture it
        if not monitors_to_capture:
            return _capture_to_base64(sct, sct.monitors[0])

        images = [Image.frombytes("RGB", sct.grab(m).size, sct.grab(m).bgra, "raw", "BGRX") for m in monitors_to_capture]

        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)

        stitched_image = Image.new("RGB", (total_width, max_height))

        x_offset = 0
        for img in images:
            stitched_image.paste(img, (x_offset, 0))
            x_offset += img.width

        buffer = io.BytesIO()
        stitched_image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return {"content": img_str, "mime_type": "image/png"}


def get_window_list() -> List[Dict[str, Any]]:
    """Gets a list of all visible windows using platform-specific manager."""
    window_manager = get_window_manager()
    return window_manager.get_window_list()


def capture_window(window_id: int) -> Dict[str, str]:
    """Captures a screenshot of a specific window by its ID."""
    window_manager = get_window_manager()
    bounds = window_manager.get_window_bounds(window_id)

    # Convert bounds to mss monitor format
    monitor = {"top": bounds["top"], "left": bounds["left"], "width": bounds["width"], "height": bounds["height"]}

    with mss.mss() as sct:
        return _capture_to_base64(sct, monitor)

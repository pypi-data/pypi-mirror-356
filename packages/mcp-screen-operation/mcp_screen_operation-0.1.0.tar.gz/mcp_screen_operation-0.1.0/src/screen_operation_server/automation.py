"""Automation operations using pyautogui."""

from typing import Any, Dict, Tuple, Optional

import pyautogui

# セーフティ機能を無効化（ローカル用なので）
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1  # デフォルトの動作間隔


def mouse_move(x: int, y: int, duration: float = 0.0) -> Dict[str, Any]:
    """
    Moves the mouse cursor to the specified coordinates.

    Args:
        x: The x-coordinate to move to
        y: The y-coordinate to move to
        duration: Time in seconds for the movement (0 = instant)

    Returns:
        Dictionary with the new mouse position
    """
    pyautogui.moveTo(x, y, duration=duration)
    new_x, new_y = pyautogui.position()
    return {"x": new_x, "y": new_y, "message": f"Mouse moved to ({new_x}, {new_y})"}


def mouse_click(x: int, y: int, button: str = "left", clicks: int = 1) -> Dict[str, Any]:
    """
    Clicks the mouse at the specified coordinates.

    Args:
        x: The x-coordinate to click at
        y: The y-coordinate to click at
        button: Mouse button to click ('left', 'right', 'middle')
        clicks: Number of clicks (1 for single, 2 for double)

    Returns:
        Dictionary with click information
    """
    pyautogui.click(x, y, button=button, clicks=clicks)
    return {"x": x, "y": y, "button": button, "clicks": clicks, "message": f"Clicked {button} button {clicks} time(s) at ({x}, {y})"}


def mouse_drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5) -> Dict[str, Any]:
    """
    Drags the mouse from start coordinates to end coordinates.

    Args:
        start_x: Starting x-coordinate
        start_y: Starting y-coordinate
        end_x: Ending x-coordinate
        end_y: Ending y-coordinate
        duration: Time in seconds for the drag operation

    Returns:
        Dictionary with drag information
    """
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(end_x, end_y, duration=duration)
    return {
        "start": {"x": start_x, "y": start_y},
        "end": {"x": end_x, "y": end_y},
        "duration": duration,
        "message": f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})",
    }


def mouse_scroll(clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> Dict[str, Any]:
    """
    Scrolls the mouse wheel.

    Args:
        clicks: Number of scroll clicks (positive = up, negative = down)
        x: Optional x-coordinate to scroll at (None = current position)
        y: Optional y-coordinate to scroll at (None = current position)

    Returns:
        Dictionary with scroll information
    """
    if x is not None and y is not None:
        pyautogui.moveTo(x, y)

    pyautogui.scroll(clicks)
    current_x, current_y = pyautogui.position()

    return {
        "clicks": clicks,
        "position": {"x": current_x, "y": current_y},
        "direction": "up" if clicks > 0 else "down",
        "message": f"Scrolled {abs(clicks)} clicks {'up' if clicks > 0 else 'down'}",
    }


def keyboard_type(text: str, interval: float = 0.0) -> Dict[str, Any]:
    """
    Types the specified text.

    Args:
        text: Text to type
        interval: Interval between keystrokes in seconds

    Returns:
        Dictionary with typing information
    """
    pyautogui.typewrite(text, interval=interval)
    return {"text": text, "length": len(text), "interval": interval, "message": f"Typed {len(text)} characters"}


def keyboard_press(key: str) -> Dict[str, Any]:
    """
    Presses a single key.

    Args:
        key: Key to press (e.g., 'enter', 'tab', 'space', 'a', '1')

    Returns:
        Dictionary with key press information
    """
    pyautogui.press(key)
    return {"key": key, "message": f"Pressed key: {key}"}


def keyboard_hotkey(*keys: str) -> Dict[str, Any]:
    """
    Presses a keyboard hotkey combination.

    Args:
        *keys: Keys to press together (e.g., 'ctrl', 'c' for Ctrl+C)

    Returns:
        Dictionary with hotkey information
    """
    pyautogui.hotkey(*keys)
    return {"keys": list(keys), "combination": "+".join(keys), "message": f"Pressed hotkey: {'+'.join(keys)}"}


def keyboard_hotkey_from_list(keys: list) -> Dict[str, Any]:
    """
    Presses a keyboard hotkey combination from a list of keys.

    Args:
        keys: List of keys to press together (e.g., ['ctrl', 'c'] for Ctrl+C)

    Returns:
        Dictionary with hotkey information
    """
    pyautogui.hotkey(*keys)
    return {"keys": keys, "combination": "+".join(keys), "message": f"Pressed hotkey: {'+'.join(keys)}"}


def get_mouse_position() -> Dict[str, Any]:
    """
    Gets the current mouse position.

    Returns:
        Dictionary with current mouse coordinates
    """
    x, y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()

    return {"x": x, "y": y, "screen_size": {"width": screen_width, "height": screen_height}, "message": f"Mouse is at ({x}, {y})"}

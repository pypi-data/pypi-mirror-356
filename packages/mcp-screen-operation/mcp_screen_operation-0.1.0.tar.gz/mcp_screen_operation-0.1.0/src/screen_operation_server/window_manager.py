"""Platform-specific window management implementations with dependency checking."""

import platform
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class WindowManager(ABC):
    """Abstract base class for platform-specific window operations."""

    @abstractmethod
    def get_window_list(self) -> List[Dict[str, Any]]:
        """Get a list of all visible windows."""
        pass  # pylint: disable=unnecessary-pass

    @abstractmethod
    def get_window_bounds(self, window_id: int) -> Dict[str, int]:
        """Get window bounds (top, left, width, height) for the given window ID."""
        pass  # pylint: disable=unnecessary-pass

    @classmethod
    @abstractmethod
    def check_dependencies(cls) -> bool:
        """Check if platform-specific dependencies are available."""
        pass  # pylint: disable=unnecessary-pass

    @classmethod
    @abstractmethod
    def get_error_message(cls) -> str:
        """Get platform-specific error message for missing dependencies."""
        pass  # pylint: disable=unnecessary-pass


class LinuxWindowManager(WindowManager):
    """Linux-specific window manager using Xlib."""

    def __init__(self):
        if not self.check_dependencies():
            raise ImportError(self.get_error_message())

        from Xlib import X, display  # type: ignore  # pylint: disable=import-error

        self.X = X
        self.display = display

    @classmethod
    def check_dependencies(cls) -> bool:
        """Check Linux-specific dependencies."""
        try:
            from Xlib import display  # type: ignore  # pylint: disable=unused-import

            return True
        except ImportError:
            return False

    @classmethod
    def get_error_message(cls) -> str:
        """Get Linux-specific error message."""
        return "Error: python-xlib is not installed. Please run 'pip install \"mcp-screen-operation[linux]\"'"

    def get_window_list(self) -> List[Dict[str, Any]]:
        """Get a list of all visible windows on Linux."""
        d = self.display.Display()
        root = d.screen().root
        window_ids = root.get_full_property(d.intern_atom("_NET_CLIENT_LIST"), self.X.AnyPropertyType).value
        windows = []

        for window_id in window_ids:
            try:
                window = d.create_resource_object("window", window_id)
                attrs = window.get_attributes()
                if attrs.map_state != self.X.IsViewable:
                    continue

                title_prop = window.get_full_property(d.intern_atom("_NET_WM_NAME"), d.intern_atom("UTF8_STRING"))
                title = title_prop.value.decode("utf-8") if title_prop else ""
                if not title:
                    title_prop = window.get_full_property(self.X.WM_NAME, self.X.AnyPropertyType)
                    title = title_prop.value.decode("latin-1") if title_prop else ""

                if title:
                    geom = window.get_geometry()
                    coords = root.translate_coords(window, 0, 0)
                    windows.append({"id": window_id, "title": title, "x": coords.x, "y": coords.y, "width": geom.width, "height": geom.height})
            except Exception:  # pylint: disable=broad-exception-caught
                continue

        return windows

    def get_window_bounds(self, window_id: int) -> Dict[str, int]:
        """Get window bounds for Linux."""
        try:
            d = self.display.Display()
            root = d.screen().root
            window = d.create_resource_object("window", window_id)
            geom = window.get_geometry()
            coords = root.translate_coords(window, 0, 0)

            return {"top": coords.y, "left": coords.x, "width": geom.width, "height": geom.height}
        except Exception:  # pylint: disable=broad-exception-caught
            raise ValueError(f"Window with ID {window_id} not found.")  # pylint: disable=raise-missing-from


class WindowsWindowManager(WindowManager):
    """Windows-specific window manager using win32gui."""

    def __init__(self):
        if not self.check_dependencies():
            raise ImportError(self.get_error_message())

        import win32gui  # pylint: disable=import-error

        self.win32gui = win32gui

    @classmethod
    def check_dependencies(cls) -> bool:
        """Check Windows-specific dependencies."""
        try:
            import win32gui  # pylint: disable=unused-import

            return True
        except ImportError:
            return False

    @classmethod
    def get_error_message(cls) -> str:
        """Get Windows-specific error message."""
        return "Error: pywin32 is not installed. Please run 'pip install \"mcp-screen-operation[windows]\"'"

    def get_window_list(self) -> List[Dict[str, Any]]:
        """Get a list of all visible windows on Windows."""
        windows = []

        def callback(hwnd, _):
            if self.win32gui.IsWindowVisible(hwnd) and self.win32gui.GetWindowText(hwnd):
                rect = self.win32gui.GetWindowRect(hwnd)
                x, y, w, h = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
                if w > 0 and h > 0:
                    windows.append({"id": hwnd, "title": self.win32gui.GetWindowText(hwnd), "x": x, "y": y, "width": w, "height": h})

        self.win32gui.EnumWindows(callback, None)
        return windows

    def get_window_bounds(self, window_id: int) -> Dict[str, int]:
        """Get window bounds for Windows."""
        try:
            rect = self.win32gui.GetWindowRect(window_id)
            return {"top": rect[1], "left": rect[0], "width": rect[2] - rect[0], "height": rect[3] - rect[1]}
        except Exception:  # pylint: disable=broad-exception-caught
            raise ValueError(f"Window with ID {window_id} not found.")  # pylint: disable=raise-missing-from


class MacOSWindowManager(WindowManager):
    """macOS-specific window manager using Quartz."""

    def __init__(self):
        if not self.check_dependencies():
            raise ImportError(self.get_error_message())

        from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly, kCGWindowListOptionIncludingWindow  # type: ignore  # pylint: disable=import-error

        self.CGWindowListCopyWindowInfo = CGWindowListCopyWindowInfo
        self.kCGNullWindowID = kCGNullWindowID
        self.kCGWindowListOptionOnScreenOnly = kCGWindowListOptionOnScreenOnly
        self.kCGWindowListOptionIncludingWindow = kCGWindowListOptionIncludingWindow

    @classmethod
    def check_dependencies(cls) -> bool:
        """Check macOS-specific dependencies."""
        try:
            from Quartz import CGWindowListCopyWindowInfo  # type: ignore  # pylint: disable=unused-import

            return True
        except ImportError:
            return False

    @classmethod
    def get_error_message(cls) -> str:
        """Get macOS-specific error message."""
        return "Error: PyObjC is not installed. Please run 'pip install \"mcp-screen-operation[macos]\"'"

    def get_window_list(self) -> List[Dict[str, Any]]:
        """Get a list of all visible windows on macOS."""
        options = self.kCGWindowListOptionOnScreenOnly
        window_list = self.CGWindowListCopyWindowInfo(options, self.kCGNullWindowID)
        windows = []

        for window in window_list:
            if window.get("kCGWindowLayer") == 0 and window.get("kCGWindowOwnerName"):
                bounds = window.get("kCGWindowBounds", {})
                windows.append(
                    {
                        "id": window.get("kCGWindowNumber"),
                        "title": f'{window.get("kCGWindowOwnerName")} - {window.get("kCGWindowName", "")}',
                        "x": int(bounds.get("X", 0)),
                        "y": int(bounds.get("Y", 0)),
                        "width": int(bounds.get("Width", 0)),
                        "height": int(bounds.get("Height", 0)),
                    }
                )

        return windows

    def get_window_bounds(self, window_id: int) -> Dict[str, int]:
        """Get window bounds for macOS."""
        options = self.kCGWindowListOptionIncludingWindow
        window_list = self.CGWindowListCopyWindowInfo(options, window_id)

        if not window_list:
            raise ValueError(f"Window with ID {window_id} not found.")

        bounds = window_list[0].get("kCGWindowBounds", {})
        return {
            "left": int(bounds.get("X", 0)),
            "top": int(bounds.get("Y", 0)),
            "width": int(bounds.get("Width", 0)),
            "height": int(bounds.get("Height", 0)),
        }


class WindowManagerFactory:
    """Factory class for creating platform-specific window managers."""

    @staticmethod
    def create_manager() -> Optional[WindowManager]:
        """Create appropriate window manager based on current system."""
        system = platform.system()

        if system == "Linux":
            return LinuxWindowManager()
        elif system == "Windows":
            return WindowsWindowManager()
        elif system == "Darwin":
            return MacOSWindowManager()
        else:
            return None

    @staticmethod
    def check_platform_dependencies() -> None:
        """Check platform-specific dependencies and exit if missing."""
        system = platform.system()

        if system == "Linux":
            manager_class = LinuxWindowManager
        elif system == "Windows":
            manager_class = WindowsWindowManager
        elif system == "Darwin":
            manager_class = MacOSWindowManager
        else:
            print(f"Error: Unsupported platform: {system}")
            sys.exit(1)

        if not manager_class.check_dependencies():
            print(manager_class.get_error_message())
            sys.exit(1)


def get_window_manager() -> WindowManager:
    """Get the appropriate window manager for the current platform."""
    manager = WindowManagerFactory.create_manager()
    if manager is None:
        raise NotImplementedError(f"Window management is not supported on {platform.system()}")
    return manager

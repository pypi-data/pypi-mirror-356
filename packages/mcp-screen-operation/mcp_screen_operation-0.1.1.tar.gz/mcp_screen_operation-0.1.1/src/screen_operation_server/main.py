import argparse
from typing import Any, Dict, List
from importlib.metadata import version, PackageNotFoundError

from fastmcp import FastMCP, Context

from . import operations, automation
from .window_manager import WindowManagerFactory

# バージョン情報を取得
try:
    __version__ = version("mcp-screen-operation")
except PackageNotFoundError:
    __version__ = "0.0.0+dev"

# FastMCPインスタンスを作成
mcp = FastMCP("screen-operation-server")


@mcp.tool()
async def get_screen_info(ctx: Context) -> Dict[str, Any]:
    """
    Retrieves information about connected displays.

    Returns:
        A dictionary containing the number of monitors and details for each monitor.
    """
    try:
        return operations.get_screen_info()
    except Exception as e:
        await ctx.error(f"Error in get_screen_info: {e}")
        raise


@mcp.tool()
async def capture_screen_by_number(monitor_number: int, ctx: Context) -> Dict[str, Any]:
    """
    Captures a screenshot of the specified monitor.

    Args:
        monitor_number: The number of the monitor to capture.

    Returns:
        A dictionary containing the base64-encoded image and its mime type.
    """
    try:
        return operations.capture_screen_by_number(monitor_number)
    except Exception as e:
        await ctx.error(f"Error in capture_screen_by_number: {e}")
        raise


@mcp.tool()
async def capture_all_screens(ctx: Context) -> Dict[str, Any]:
    """
    Captures all connected monitors and stitches them into a single image.

    Returns:
        A dictionary containing the base64-encoded stitched image and its mime type.
    """
    try:
        return operations.capture_all_screens()
    except Exception as e:
        await ctx.error(f"Error in capture_all_screens: {e}")
        raise


@mcp.tool()
async def get_window_list(ctx: Context) -> List[Dict[str, Any]]:
    """
    Retrieves a list of currently open windows.

    Returns:
        A list of dictionaries, each containing details about a window (id, title, size, position).
    """
    try:
        return operations.get_window_list()
    except Exception as e:
        await ctx.error(f"Error in get_window_list: {e}")
        raise


@mcp.tool()
async def capture_window(window_id: int, ctx: Context) -> Dict[str, Any]:
    """
    Captures a screenshot of the specified window.

    Args:
        window_id: The ID of the window to capture.

    Returns:
        A dictionary containing the base64-encoded image and its mime type.
    """
    try:
        return operations.capture_window(window_id)
    except Exception as e:
        await ctx.error(f"Error in capture_window: {e}")
        raise


# Mouse automation tools
@mcp.tool()
async def mouse_move(x: int, y: int, duration: float, ctx: Context) -> Dict[str, Any]:
    """
    Moves the mouse cursor to the specified coordinates.

    Args:
        x: The x-coordinate to move to.
        y: The y-coordinate to move to.
        duration: Time in seconds for the movement (0 = instant).

    Returns:
        A dictionary with the new mouse position.
    """
    try:
        return automation.mouse_move(x, y, duration)
    except Exception as e:
        await ctx.error(f"Error in mouse_move: {e}")
        raise


@mcp.tool()
async def mouse_click(x: int, y: int, button: str, clicks: int, ctx: Context) -> Dict[str, Any]:
    """
    Clicks the mouse at the specified coordinates.

    Args:
        x: The x-coordinate to click at.
        y: The y-coordinate to click at.
        button: Mouse button to click ('left', 'right', 'middle').
        clicks: Number of clicks (1 for single, 2 for double).

    Returns:
        A dictionary with click information.
    """
    try:
        return automation.mouse_click(x, y, button, clicks)
    except Exception as e:
        await ctx.error(f"Error in mouse_click: {e}")
        raise


@mcp.tool()
async def mouse_drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float, ctx: Context) -> Dict[str, Any]:
    """
    Drags the mouse from start coordinates to end coordinates.

    Args:
        start_x: Starting x-coordinate.
        start_y: Starting y-coordinate.
        end_x: Ending x-coordinate.
        end_y: Ending y-coordinate.
        duration: Time in seconds for the drag operation.

    Returns:
        A dictionary with drag information.
    """
    try:
        return automation.mouse_drag(start_x, start_y, end_x, end_y, duration)
    except Exception as e:
        await ctx.error(f"Error in mouse_drag: {e}")
        raise


@mcp.tool()
async def mouse_scroll(clicks: int, x: int, y: int, ctx: Context) -> Dict[str, Any]:
    """
    Scrolls the mouse wheel.

    Args:
        clicks: Number of scroll clicks (positive = up, negative = down).
        x: Optional x-coordinate to scroll at (None = current position).
        y: Optional y-coordinate to scroll at (None = current position).

    Returns:
        A dictionary with scroll information.
    """
    try:
        return automation.mouse_scroll(clicks, x, y)
    except Exception as e:
        await ctx.error(f"Error in mouse_scroll: {e}")
        raise


# Keyboard automation tools
@mcp.tool()
async def keyboard_type(text: str, interval: float, ctx: Context) -> Dict[str, Any]:
    """
    Types the specified text.

    Args:
        text: Text to type.
        interval: Interval between keystrokes in seconds.

    Returns:
        A dictionary with typing information.
    """
    try:
        return automation.keyboard_type(text, interval)
    except Exception as e:
        await ctx.error(f"Error in keyboard_type: {e}")
        raise


@mcp.tool()
async def keyboard_press(key: str, ctx: Context) -> Dict[str, Any]:
    """
    Presses a single key.

    Args:
        key: Key to press (e.g., 'enter', 'tab', 'space', 'a', '1').

    Returns:
        A dictionary with key press information.
    """
    try:
        return automation.keyboard_press(key)
    except Exception as e:
        await ctx.error(f"Error in keyboard_press: {e}")
        raise


@mcp.tool()
async def keyboard_hotkey(keys: str, ctx: Context) -> Dict[str, Any]:
    """
    Presses a keyboard hotkey combination.

    Args:
        keys: Keys to press together, separated by '+' (e.g., 'ctrl+c' for Ctrl+C).

    Returns:
        A dictionary with hotkey information.
    """
    try:
        key_list = [key.strip() for key in keys.split("+")]
        return automation.keyboard_hotkey_from_list(key_list)
    except Exception as e:
        await ctx.error(f"Error in keyboard_hotkey: {e}")
        raise


@mcp.tool()
async def get_mouse_position(ctx: Context) -> Dict[str, Any]:
    """
    Gets the current mouse position.

    Returns:
        A dictionary with current mouse coordinates and screen size.
    """
    try:
        return automation.get_mouse_position()
    except Exception as e:
        await ctx.error(f"Error in get_mouse_position: {e}")
        raise


def main():
    """
    Main entry point that supports multiple transport protocols.
    """
    # プラットフォーム依存関係をチェック
    WindowManagerFactory.check_platform_dependencies()

    # コマンドライン引数を解析
    parser = argparse.ArgumentParser(description="MCP Screen Operation Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"], default="stdio", help="Transport protocol to use (default: stdio)")
    parser.add_argument("--port", type=int, default=8205, help="Port for HTTP-based transports (default: 8205)")
    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP-based transports (default: 127.0.0.1)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    print(f"Starting {mcp.name} v{__version__} with {args.transport} transport...")

    try:
        if args.transport == "stdio":
            # STDIOトランスポート（デフォルト）
            mcp.run(transport="stdio")
        elif args.transport == "sse":
            # SSEトランスポート
            print(f"SSE endpoint: http://{args.host}:{args.port}/sse")
            mcp.run(transport="sse", host=args.host, port=args.port)
        elif args.transport == "streamable-http":
            # Streamable HTTPトランスポート（推奨）
            print(f"Streamable HTTP endpoint: http://{args.host}:{args.port}/mcp")
            mcp.run(transport="streamable-http", host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("Server stopped.")


if __name__ == "__main__":
    main()

# MCP スクリーン操作サーバー

FastMCPで構築され、複数のトランスポートプロトコルをサポートする、クロスプラットフォーム対応のスクリーンおよびウィンドウ操作用のモダンなModel Context Protocol (MCP) サーバーです。

## 機能

### スクリーン操作
- 接続されたディスプレイの情報取得
- 特定のモニターのスクリーンショット撮影
- 全モニターを結合したスクリーンショット撮影

### ウィンドウ操作
- 開いているすべてのウィンドウのリスト取得
- 特定のウィンドウのスクリーンショット撮影

### 自動操作機能
- マウスの移動、クリック、ドラッグ、スクロール操作
- キーボードによる文字入力、キー押下、ホットキー組み合わせ
- 現在のマウス位置とスクリーン情報の取得

### トランスポートプロトコル
- **STDIO** (デフォルト) - ローカルツールとClaude Desktopの統合用
- **SSE** (Server-Sent Events) - Webベースのデプロイメント用
- **Streamable HTTP** (推奨) - モダンなHTTPベースプロトコル

### プラットフォームサポート
- **Linux** (python-xlibによるX11)
- **Windows** (pywin32によるWin32 API)
- **macOS** (PyObjCによるQuartz)

## アーキテクチャ

サーバーはクリーンでプラットフォーム非依存のアーキテクチャを使用しています：

- **FastMCP統合**: マルチトランスポートサポートを持つモダンなMCPサーバーフレームワーク
- **プラットフォーム抽象化**: プラットフォーム固有の実装を持つ`WindowManager`インターフェース
- **依存関係管理**: プラットフォーム固有の依存関係の自動チェック
- **クリーンな分離**: プラットフォーム詳細から独立した操作レイヤー

## インストール

### PyPIからのクイックインストール

PyPIに公開された後は、簡単にインストールして実行できます：

```bash
# uv を使用（推奨）
uvx mcp-screen-operation  # インストールせずに直接実行

# または pip を使用
pip install mcp-screen-operation[windows]  # 'windows' をあなたのプラットフォームに置き換え
```

### ソースからのインストール

#### 前提条件

仮想環境を作成して有効化します：

```bash
python -m venv venv

# Windows の場合
.\venv\Scripts\Activate.ps1

# Linux/macOS の場合
source venv/bin/activate
```

### 基本インストール

プラットフォーム固有の依存関係を含む編集可能モードでプロジェクトをインストールします：

#### 本番利用の場合

```bash
# Linux
pip install -e ".[linux]"

# Windows
pip install -e ".[windows]"

# macOS
pip install -e ".[macos]"
```

#### 開発用の場合

開発ツールを含めてインストールします：

```bash
# Linux 開発環境
pip install -e ".[dev,linux]"

# Windows 開発環境
pip install -e ".[dev,windows]"

# macOS 開発環境
pip install -e ".[dev,macos]"
```

### 依存関係

**コア依存関係** (自動インストール):
- `fastmcp>=2.3.0` - モダンなMCPサーバーフレームワーク
- `mcp>=1.9.4` - Model Context Protocolライブラリ
- `mss` - クロスプラットフォームスクリーンショットライブラリ
- `Pillow` - 画像処理
- `pyautogui` - クロスプラットフォーム自動操作ライブラリ

**プラットフォーム固有の依存関係**:
- **Linux**: `python-xlib` - X11ウィンドウ管理
- **Windows**: `pywin32` - Windows APIアクセス
- **macOS**: `pyobjc-framework-Quartz`, `pyobjc-framework-Cocoa` - macOSウィンドウ管理

**開発依存関係** (`[dev]`でインストール):
- `pylint` - コードリンティング
- `pylint-plugin-utils` - Pylintユーティリティ
- `pylint-mcp` - MCP固有のリンティングルール
- `black` - コードフォーマッティング

### インストール例

#### クイックスタート (本番環境)
```bash
# プラットフォーム用にクローンしてインストール
git clone <repository-url>
cd mcp-screen-operation
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -e ".[windows]"
```

#### 開発者セットアップ
```bash
# 開発環境をクローンしてセットアップ
git clone <repository-url>
cd mcp-screen-operation
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
pip install -e ".[dev,windows]"

# 開発ツールを実行
black src/
pylint src/
```

## 使用方法

### コマンドラインオプション

```bash
screen-operation-server --help
```

```
usage: screen-operation-server [-h] [--transport {stdio,sse,streamable-http}]
                               [--port PORT] [--host HOST]

MCP Screen Operation Server

options:
  -h, --help            show this help message and exit
  --transport {stdio,sse,streamable-http}
                        Transport protocol to use (default: stdio)
  --port PORT           Port for HTTP-based transports (default: 8205)
  --host HOST           Host for HTTP-based transports (default: 127.0.0.1)
```

### コマンド例

```bash
# バージョンを確認
screen-operation-server --version
```

### 異なるトランスポートでの実行

#### STDIO (デフォルト)
ローカルツールとClaude Desktop統合に最適：
```bash
screen-operation-server
# または明示的に
screen-operation-server --transport stdio
```

#### Streamable HTTP (Web用推奨)
Webデプロイメント用のモダンなHTTPベースプロトコル：
```bash
screen-operation-server --transport streamable-http --port 8205
```
アクセス先: `http://localhost:8205/mcp`

#### SSE (レガシーWebサポート)
レガシーWebデプロイメント用のServer-Sent Events：
```bash
screen-operation-server --transport sse --port 8205
```
アクセス先: `http://localhost:8205/sse`

### 開発モード

FastMCPの開発モードをインスペクターと共に使用：
```bash
# pip install -e ".[dev,windows]" でインストール後
fastmcp dev src/screen_operation_server/main.py
```

### MCP Inspector

MCP Inspectorを使用してMCPサーバーをインタラクティブにテストおよびデバッグできます：

```bash
# MCP Inspectorをインストールして実行
npx @modelcontextprotocol/inspector
```

MCP Inspectorは以下の機能を提供するWebベースのインターフェースです：
- すべての利用可能なツールのテスト
- ツールスキーマとドキュメントの表示
- サーバーレスポンスのデバッグ
- サーバーログの監視

## 利用可能なツール

### スクリーン情報
- **`get_screen_info()`**: 接続されたディスプレイの情報を取得
  - 戻り値: モニター数と各ディスプレイの詳細（解像度、位置）

### スクリーンキャプチャ
- **`capture_screen_by_number(monitor_number: int)`**: 指定されたモニターのスクリーンショットを撮影
  - 引数: `monitor_number` - キャプチャするモニター（0ベースのインデックス）
  - 戻り値: Base64エンコードされたPNG画像

- **`capture_all_screens()`**: 接続されたすべてのモニターをキャプチャして単一の画像に結合
  - 戻り値: すべてのスクリーンを結合したBase64エンコードされたPNG画像

### ウィンドウ管理
- **`get_window_list()`**: 現在開いているウィンドウのリストを取得
  - 戻り値: ID、タイトル、位置、寸法を含むウィンドウのリスト

- **`capture_window(window_id: int)`**: 指定されたウィンドウのスクリーンショットを撮影
  - 引数: `window_id` - キャプチャするウィンドウID
  - 戻り値: ウィンドウのBase64エンコードされたPNG画像

### マウス自動操作
- **`mouse_move(x: int, y: int, duration: float = 0.0)`**: マウスカーソルを移動
  - 引数: `x`, `y` - 移動先の座標; `duration` - 移動時間（秒）
  - 戻り値: 新しいマウス位置

- **`mouse_click(x: int, y: int, button: str = "left", clicks: int = 1)`**: マウスをクリック
  - 引数: `x`, `y` - クリック座標; `button` - マウスボタン（'left', 'right', 'middle'）; `clicks` - クリック回数
  - 戻り値: クリック情報

- **`mouse_drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5)`**: マウスをドラッグ
  - 引数: 開始位置と終了位置の座標; `duration` - ドラッグ時間
  - 戻り値: ドラッグ操作の詳細

- **`mouse_scroll(clicks: int, x: int = None, y: int = None)`**: マウスホイールをスクロール
  - 引数: `clicks` - スクロール量（正の値=上、負の値=下）; オプションの座標
  - 戻り値: スクロール情報

- **`get_mouse_position()`**: 現在のマウス位置を取得
  - 戻り値: 現在の座標とスクリーンサイズ

### キーボード自動操作
- **`keyboard_type(text: str, interval: float = 0.0)`**: テキストを入力
  - 引数: `text` - 入力するテキスト; `interval` - キーストローク間の遅延
  - 戻り値: 入力情報

- **`keyboard_press(key: str)`**: 単一のキーを押下
  - 引数: `key` - キー名（例: 'enter', 'tab', 'space', 'a'）
  - 戻り値: キー押下情報

- **`keyboard_hotkey(keys: str)`**: ホットキーの組み合わせを押下
  - 引数: `keys` - '+' で区切られた同時に押すキー（例: 'ctrl+c'）
  - 戻り値: ホットキー情報

## 統合例

### Claude Desktop統合

Claude DesktopのMCP設定に追加：

```json
{
  "mcpServers": {
    "screen-operation": {
      "command": "screen-operation-server",
      "args": []
    }
  }
}
```

または、PyPI公開後は自動インストール用にuvxを使用：

```json
{
  "mcpServers": {
    "screen-operation": {
      "command": "uvx",
      "args": ["mcp-screen-operation"]
    }
  }
}
```

### Webアプリケーション統合

Streamable HTTPの場合：
```javascript
// MCPサーバーに接続
const response = await fetch('http://localhost:8205/mcp', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'tools/call',
    params: {
      name: 'get_screen_info',
      arguments: {}
    }
  })
});
```

### FastMCPクライアント統合

```python
import asyncio
from fastmcp import FastMCP

async def main():
    # HTTPサーバーに接続
    client = FastMCP.create_client('http://localhost:8205/mcp')

    # スクリーン情報を取得
    result = await client.call_tool('get_screen_info', {})
    print(result)

asyncio.run(main())
```

## エラーハンドリング

サーバーは起動時にプラットフォーム固有の依存関係を自動的にチェックします：

- **Linux**: `python-xlib`の可用性を検証
- **Windows**: `pywin32`の可用性を検証
- **macOS**: `PyObjC`の可用性を検証

依存関係が不足している場合、サーバーはインストール手順を表示して終了します。

## 開発

### 開発環境セットアップ

1. **環境をクローンしてセットアップ:**
```bash
git clone <repository-url>
cd mcp-screen-operation
python -m venv venv

# 仮想環境を有効化
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

# 開発モードでインストール
pip install -e ".[dev,windows]"  # 'windows'をあなたのプラットフォームに置き換え
```

2. **コードフォーマッティングとリンティング:**
```bash
# コードをフォーマット
black src/

# リンターを実行
pylint src/
```

3. **開発中のテスト:**
```bash
# サーバーをテスト
screen-operation-server --help

# 異なるトランスポートでテスト
screen-operation-server --transport stdio
screen-operation-server --transport sse --port 8205
screen-operation-server --transport streamable-http --port 8205
```

### 利用可能なエクストラ

- `linux`: Linuxプラットフォーム依存関係（`python-xlib`）
- `windows`: Windowsプラットフォーム依存関係（`pywin32`）
- `macos`: macOSプラットフォーム依存関係（`PyObjC`フレームワーク）
- `dev`: 開発ツール（`pylint`, `black`）

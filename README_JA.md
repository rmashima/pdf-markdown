# PDF to Markdown Converter

PyMuPDF4LLMを使用してPDFをMarkdownに変換するシンプルなGUIアプリケーションです。

## 概要

このアプリケーションは、PDFファイルをMarkdown形式に変換するためのグラフィカルユーザーインターフェース（GUI）を提供します。PyMuPDF4LLMライブラリを使用して高品質な変換を実現しています。

## 機能

- PDFファイルをMarkdown形式に変換
- 直感的なGUIインターフェース
- ドラッグ&ドロップでのファイル選択
- リアルタイムでの変換進捗表示
- カスタマイズ可能な変換オプション

## 必要な環境

- Python 3.12以上
- Windows 10/11（他のプラットフォームでも動作可能）

## インストール方法

### 開発環境でのインストール

1. リポジトリをクローンします：
```bash
git clone https://github.com/rmashima/pdf-markdown.git
cd pdf-markdown
```

2. uvを使用して依存関係をインストールします：
```bash
uv sync
```

3. アプリケーションを実行します：
```bash
uv run python main.py
```

## ビルド方法

PyInstallerを使用してスタンドアロンの実行ファイルを作成できます。

### 前提条件

- uvがインストールされていること
- `icon.ico`ファイルがプロジェクトルートに配置されていること

### ビルド手順

1. PyInstallerを依存関係に追加：
```bash
uv add pyinstaller
```

2. EXEファイルをビルド：
```bash
uv run pyinstaller --onefile --windowed --icon=icon.ico --name="PDF-to-Markdown-Converter" main.py
```

3. 不要なファイルを削除：
```bash
Remove-Item -Recurse -Force build
Remove-Item "PDF-to-Markdown-Converter.spec"
```

ビルドされたEXEファイルは`dist`フォルダに生成されます。

### ビルドオプションの説明

- `--onefile`: 単一の実行ファイルとして作成
- `--windowed`: コンソールウィンドウを表示しない（GUIアプリケーション用）
- `--icon=icon.ico`: アプリケーションアイコンを指定
- `--name="PDF-to-Markdown-Converter"`: 出力ファイル名を指定

## 使用方法

### GUI版の使用方法

1. アプリケーションを起動します
2. 「参照」ボタンをクリックしてPDFファイルを選択するか、ファイルをドラッグ&ドロップします
3. 必要に応じて変換オプションを設定します
4. 「変換開始」ボタンをクリックして変換を実行します
5. 変換が完了すると、Markdownファイルが同じディレクトリに保存されます

### 対応ファイル形式

- **入力**: PDF（.pdf）
- **出力**: Markdown（.md）

## 依存関係

このプロジェクトは以下のライブラリを使用しています：

| ライブラリ | バージョン | ライセンス | 説明 |
|-----------|-----------|-----------|------|
| PyMuPDF4LLM | >=0.0.10 | AGPL-3.0 | PDF解析とMarkdown変換のためのライブラリ |
| tkinterdnd2 | >=0.4.3 | MIT | Tkinterへのドラッグ&ドロップ機能を追加 |
| PyInstaller | >=6.13.0 | GPL-2.0 | Pythonアプリケーションの実行ファイル化 |

### ライセンス詳細

#### PyMuPDF / PyMuPDF4LLM
- **ライセンス**: AGPL-3.0 License
- **概要**: PyMuPDFはArtifex Softwareによって開発されたPDF処理ライブラリです
- **商用利用**: AGPLライセンスの条件下で使用可能。商用ライセンスも利用可能
- **詳細**: [PyMuPDF License](https://pymupdf.readthedocs.io/en/latest/about.html#license)

#### tkinterdnd2
- **ライセンス**: MIT License
- **概要**: Tkinterにドラッグアンドドロップ機能を追加するライブラリ
- **商用利用**: 制限なく使用可能

#### PyInstaller
- **ライセンス**: GPL-2.0 License
- **概要**: Pythonスクリプトを実行ファイルに変換するツール
- **商用利用**: GPLライセンスの条件下で使用可能

## 開発

### プロジェクト構造
```
pdf-markdown/
├── main.py              # メインアプリケーションファイル
├── pyproject.toml       # プロジェクト設定とメタデータ
├── icon.ico            # アプリケーションアイコン
├── README.md           # このファイル
├── uv.lock            # 依存関係のロックファイル
└── dist/              # ビルドされた実行ファイル
    └── PDF-to-Markdown-Converter.exe
```

### 開発環境のセットアップ

1. uvを使用して開発環境を構築：
```bash
uv sync
```

2. 開発モードでアプリケーションを実行：
```bash
uv run python main.py
```

## トラブルシューティング

### よくある問題

1. **PyMuPDF4LLMのインポートエラー**
   - 解決方法: `uv sync`を実行して依存関係を再インストール

2. **アイコンファイルが見つからない**
   - 解決方法: `icon.ico`ファイルがプロジェクトルートに存在することを確認

3. **EXEファイルが起動しない**
   - 解決方法: Windows Defenderやウイルス対策ソフトウェアによってブロックされている可能性があります

## ライセンス

このプロジェクトは AGPL-3.0 の下で公開されています。ただし、使用している依存関係のライセンスにも注意してください：

- PyMuPDF/PyMuPDF4LLM: AGPL-3.0 (商用利用時には注意)
- tkinterdnd2: MIT
- PyInstaller: GPL-2.0 (EXEビルド時のみ使用)

## 貢献

プロジェクトへの貢献を歓迎します。バグ報告や機能要求は、GitHubのIssuesで管理しています。

## サポート

問題や質問がある場合は、以下の方法でサポートを受けることができます：

1. GitHubのIssuesページで問題を報告
2. プロジェクトのDiscussionsページで質問

---

**注意**: このソフトウェアは無保証で提供されており、明示または黙示を問わず、いかなる保証もありません。使用している依存関係のライセンス条項を確認し、適切に遵守してください。
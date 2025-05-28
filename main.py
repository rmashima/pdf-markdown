"""
PDF to Markdown Converter GUI / PDFからMarkdownへの変換GUI
Simple GUI application using PyMuPDF4LLM to convert PDF to Markdown
PyMuPDF4LLMを使用してPDFをMarkdownに変換するシンプルなGUIアプリケーション
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import pathlib
import time
import sys
import json
import locale

# Try to import required libraries / 必要なライブラリのインポートを試行
try:
    import pymupdf4llm
    import pymupdf
except ImportError:
    # Language detection for error messages / エラーメッセージのための言語検出
    lang = "en"
    try:
        default_locale = locale.getdefaultlocale()[0]
        if default_locale and default_locale.startswith('en'):
            lang = "en"
        else:
            lang = "ja"
    except:
        lang = "ja"
    
    if lang == "ja":
        print("PyMuPDF4LLMまたはPyMuPDFがインストールされていません。")
        print("pip install pymupdf4llm でインストールしてください。")
    else:
        print("PyMuPDF4LLM or PyMuPDF is not installed.")
        print("Please install with: pip install pymupdf4llm")
    sys.exit(1)

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    # Set flag for drag and drop availability / ドラッグ&ドロップ利用可否フラグを設定
    DRAG_DROP_AVAILABLE = False
    # Create fallback class / フォールバッククラスを作成
    class TkinterDnD:
        @staticmethod
        def Tk():
            return tk.Tk()
    
    DND_FILES = None


class LanguageManager:
    """Language management class / 言語管理クラス"""
    
    def __init__(self):
        self.config_file = "config.json"  # Configuration file / 設定ファイル
        self.current_language = self.load_language_setting()  # Load saved language / 保存された言語を読み込み
        self.translations = {
            "ja": {
                "title": "PDF to Markdown Converter",
                "file_selection": "PDFファイル選択",
                "browse": "参照",
                "drag_drop_hint": "または、PDFファイルをこのウィンドウにドラッグ＆ドロップしてください",
                "conversion_options": "変換オプション",                "add_page_headers": "ページ番号を見出しとして追加",
                "page_range": "ページ範囲",
                "page_range_hint": "変換するページ範囲を指定 (例: 1-5, 3,7,10, または空白で全ページ)",
                "language_selection": "言語選択",
                "start_conversion": "変換開始",
                "ready": "準備完了",
                "log": "ログ",
                "converting": "変換中...",
                "error": "エラー",
                "warning": "警告",
                "completed": "完了",
                "file_selected": "ファイルが選択されました",
                "file_dropped": "ファイルがドロップされました",
                "select_pdf_file": "PDFファイルを選択してください。",
                "file_not_found": "選択されたファイルが存在しません。",
                "not_pdf_file": "PDFファイルを選択してください。",
                "conversion_in_progress": "変換が既に実行中です。",
                "conversion_starting": "変換を開始します...",
                "total_pages": "総ページ数",
                "page_completed": "完了",
                "conversion_completed": "変換完了",
                "conversion_success": "変換が完了しました。\n保存先:",
                "no_content": "変換できるコンテンツがありませんでした。",
                "conversion_failed": "変換失敗",
                "drop_pdf_only": "PDFファイルをドロップしてください。",
                "drag_drop_unavailable": "ドラッグアンドドロップ機能が利用できません",
                "drop_error": "ドロップエラー",
                "no_pages": "PDFにページが含まれていません。",
                "page_conversion_error": "の変換でエラー",
                "pdf_read_error": "PDFファイルの読み込みエラー",
                "conversion_error": "変換エラー",                "file_save_error": "ファイル保存エラー",
                "invalid_page_range": "無効なページ範囲です",
                "page_range_error": "ページ範囲の指定に誤りがあります",
                "page_out_of_range": "指定されたページが範囲外です",
                "pymupdf_not_installed": "PyMuPDF4LLMまたはPyMuPDFがインストールされていません。",
                "install_pymupdf": "pip install pymupdf4llm でインストールしてください。",
                "tkinterdnd2_not_installed": "tkinterdnd2がインストールされていません。",
                "install_tkinterdnd2": "pip install tkinterdnd2 でインストールしてください。"
            },
            "en": {
                "title": "PDF to Markdown Converter",
                "file_selection": "PDF File Selection",
                "browse": "Browse",
                "drag_drop_hint": "Or drag and drop a PDF file into this window",
                "conversion_options": "Conversion Options",                "add_page_headers": "Add page numbers as headers",
                "page_range": "Page Range",
                "page_range_hint": "Specify page range to convert (e.g., 1-5, 3,7,10, or leave empty for all pages)",
                "language_selection": "Language",
                "start_conversion": "Start Conversion",
                "ready": "Ready",
                "log": "Log",
                "converting": "Converting...",
                "error": "Error",
                "warning": "Warning",
                "completed": "Completed",
                "file_selected": "File selected",
                "file_dropped": "File dropped",
                "select_pdf_file": "Please select a PDF file.",
                "file_not_found": "Selected file does not exist.",
                "not_pdf_file": "Please select a PDF file.",
                "conversion_in_progress": "Conversion is already in progress.",
                "conversion_starting": "Starting conversion...",
                "total_pages": "Total pages",
                "page_completed": "completed",
                "conversion_completed": "Conversion completed",
                "conversion_success": "Conversion completed successfully.\nSaved to:",
                "no_content": "No content could be converted.",
                "conversion_failed": "Conversion failed",
                "drop_pdf_only": "Please drop a PDF file.",
                "drag_drop_unavailable": "Drag and drop feature is not available",
                "drop_error": "Drop error",
                "no_pages": "The PDF contains no pages.",
                "page_conversion_error": "Error converting page",
                "pdf_read_error": "PDF file reading error",
                "conversion_error": "Conversion error",                "file_save_error": "File save error",
                "invalid_page_range": "Invalid page range",
                "page_range_error": "Error in page range specification", 
                "page_out_of_range": "Specified page is out of range",
                "pymupdf_not_installed": "PyMuPDF4LLM or PyMuPDF is not installed.",
                "install_pymupdf": "Please install with: pip install pymupdf4llm",
                "tkinterdnd2_not_installed": "tkinterdnd2 is not installed.",
                "install_tkinterdnd2": "Please install with: pip install tkinterdnd2"
            }
        }
    
    def load_language_setting(self):
        """Load language setting from config file / 設定ファイルから言語設定を読み込み"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('language', 'ja')
        except Exception:
            pass
        return 'ja'  # Default to Japanese / デフォルトは日本語
    
    def save_language_setting(self):
        """Save language setting to config file / 言語設定を設定ファイルに保存"""
        try:
            config = {'language': self.current_language}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # Ignore errors / エラーは無視
    
    def get_text(self, key):
        """Get translation text for specified key / 指定されたキーの翻訳テキストを取得"""
        return self.translations.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language):
        """Set language / 言語を設定"""
        if language in self.translations:
            self.current_language = language
            self.save_language_setting()  # Save immediately / 即座に保存
    
    def get_available_languages(self):
        """Get list of available languages / 利用可能な言語のリストを取得"""
        return list(self.translations.keys())
    
    def get_language_display_name(self, lang_code):
        """Get display name for language code / 言語コードの表示名を取得"""
        display_names = {"ja": "日本語", "en": "English"}
        return display_names.get(lang_code, lang_code)


class PDFToMarkdownConverter:
    def __init__(self, root):
        self.root = root
        
        # Language management / 言語管理
        self.lang_manager = LanguageManager()
        
        self.root.title(self.lang_manager.get_text("title"))
        self.root.geometry("800x600")
        
        # Conversion state management / 変換状態管理
        self.is_converting = False
        
        # Create UI / UI作成
        self.create_widgets()
        
        # Setup drag and drop / ドラッグアンドドロップの設定
        self.setup_drag_and_drop()
    
    def create_widgets(self):
        # Main frame / メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Language selection frame / 言語選択フレーム
        lang_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.get_text("language_selection"), padding="10")
        lang_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Language selection combobox / 言語選択コンボボックス
        self.language_var = tk.StringVar(value=self.lang_manager.current_language)
        language_display_options = [
            (lang_code, self.lang_manager.get_language_display_name(lang_code)) 
            for lang_code in self.lang_manager.get_available_languages()
        ]
        
        self.language_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, 
                                         values=[lang[1] for lang in language_display_options],
                                         state="readonly", width=15)
        self.language_combo.grid(row=0, column=0, sticky=tk.W)
        
        # Set initial display value / 初期表示値を設定
        current_display = self.lang_manager.get_language_display_name(self.lang_manager.current_language)
        self.language_combo.set(current_display)
        
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_changed)
        
        # File selection frame / ファイル選択フレーム
        self.file_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.get_text("file_selection"), padding="10")
        self.file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # File path display / ファイルパス表示
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_path_var, width=60)
        self.file_entry.grid(row=0, column=0, padx=(0, 10))
        
        # File selection button / ファイル選択ボタン
        self.browse_button = ttk.Button(self.file_frame, text=self.lang_manager.get_text("browse"), command=self.select_file)
        self.browse_button.grid(row=0, column=1)
        
        # Drag and drop explanation / ドラッグアンドドロップの説明
        self.drag_drop_label = ttk.Label(self.file_frame, text=self.lang_manager.get_text("drag_drop_hint"), 
                                       foreground="gray")
        self.drag_drop_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
        # Options frame / オプションフレーム
        self.options_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.get_text("conversion_options"), padding="10")
        self.options_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
          # Page number header addition option / ページ番号見出し追加オプション
        self.add_page_headers_var = tk.BooleanVar(value=True)
        self.page_headers_checkbox = ttk.Checkbutton(self.options_frame, text=self.lang_manager.get_text("add_page_headers"), 
                       variable=self.add_page_headers_var)
        self.page_headers_checkbox.grid(row=0, column=0, sticky=tk.W)
        
        # Page range specification / ページ範囲指定
        page_range_label = ttk.Label(self.options_frame, text=self.lang_manager.get_text("page_range"))
        page_range_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        self.page_range_var = tk.StringVar()
        self.page_range_entry = ttk.Entry(self.options_frame, textvariable=self.page_range_var, width=30)
        self.page_range_entry.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        
        page_range_hint = ttk.Label(self.options_frame, text=self.lang_manager.get_text("page_range_hint"), 
                                  foreground="gray", font=("TkDefaultFont", 8))
        page_range_hint.grid(row=3, column=0, sticky=tk.W, pady=(2, 0))
        
        # Conversion button frame / 変換ボタンフレーム
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))        
        # Conversion button / 変換ボタン
        self.convert_button = ttk.Button(button_frame, text=self.lang_manager.get_text("start_conversion"), command=self.start_conversion)
        self.convert_button.grid(row=0, column=0)
        
        # Progress bar / プログレスバー
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label / ステータスラベル
        self.status_var = tk.StringVar(value=self.lang_manager.get_text("ready"))
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))
        
        # Log area / ログエリア
        self.log_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.get_text("log"), padding="10")
        self.log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid weight settings / グリッドの重み設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
    
    def on_language_changed(self, event=None):
        """Processing when language is changed / 言語が変更された時の処理"""
        selected_display = self.language_combo.get()
        # Find language code from display name / 表示名から言語コードを探す
        for lang_code in self.lang_manager.get_available_languages():
            if self.lang_manager.get_language_display_name(lang_code) == selected_display:
                self.lang_manager.set_language(lang_code)
                break
        
        # Update UI texts / UIテキストを更新
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Update UI texts to current language / UIのテキストを現在の言語に更新"""
        self.root.title(self.lang_manager.get_text("title"))
        self.file_frame.config(text=self.lang_manager.get_text("file_selection"))
        self.browse_button.config(text=self.lang_manager.get_text("browse"))
        self.drag_drop_label.config(text=self.lang_manager.get_text("drag_drop_hint"))
        self.options_frame.config(text=self.lang_manager.get_text("conversion_options"))
        self.page_headers_checkbox.config(text=self.lang_manager.get_text("add_page_headers"))
        
        # Update page range related labels / ページ範囲関連のラベルを更新
        try:
            page_range_label = self.options_frame.grid_slaves(row=1, column=0)[0]
            page_range_label.config(text=self.lang_manager.get_text("page_range"))
            page_range_hint = self.options_frame.grid_slaves(row=3, column=0)[0]
            page_range_hint.config(text=self.lang_manager.get_text("page_range_hint"))
        except IndexError:
            pass  # UI not fully initialized yet / UIがまだ完全に初期化されていない
        
        self.convert_button.config(text=self.lang_manager.get_text("start_conversion"))
        self.log_frame.config(text=self.lang_manager.get_text("log"))
        
        # Update status if it's "Ready" / ステータスが"準備完了"の場合は更新
        if self.status_var.get() in ["準備完了", "Ready"]:
            self.status_var.set(self.lang_manager.get_text("ready"))
    
    def select_file(self):
        """File selection dialog / ファイル選択ダイアログ"""
        title_text = "PDFファイルを選択" if self.lang_manager.current_language == "ja" else "Select PDF File"
        file_path = filedialog.askopenfilename(
            title=title_text,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            message = f"{self.lang_manager.get_text('file_selected')}: {os.path.basename(file_path)}"
            self.log_message(message)
    
    def log_message(self, message):
        """Add log message / ログメッセージの追加"""
        timestamp = time.strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_line)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    def setup_drag_and_drop(self):
        """Setup drag and drop functionality / ドラッグアンドドロップ機能の設定"""
        if not DRAG_DROP_AVAILABLE:
            self.log_message(self.lang_manager.get_text("drag_drop_unavailable"))
            return
            
        try:
            # Set drag and drop for entire window / ウィンドウ全体にドラッグアンドドロップを設定
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<DropEnter>>', self.on_drop_enter)
            self.root.dnd_bind('<<DropPosition>>', self.on_drop_position)
            self.root.dnd_bind('<<DropLeave>>', self.on_drop_leave)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        except Exception as e:
            # Fallback when tkinterdnd2 is not available / tkinterdnd2が利用できない場合のフォールバック
            self.log_message(f"{self.lang_manager.get_text('drag_drop_unavailable')}: {str(e)}")
    
    def on_drop_enter(self, event):
        """When drag and drop starts / ドラッグアンドドロップ開始時"""
        return event.action
    
    def on_drop_position(self, event):
        """When position changes during drag / ドラッグ中の位置変更時"""
        return event.action
    
    def on_drop_leave(self, event):
        """When drag and drop ends / ドラッグアンドドロップ終了時"""
        return event.action
    
    def on_drop(self, event):
        """Processing when file is dropped / ファイルがドロップされた時の処理"""
        try:
            # Get path of dropped file / ドロップされたファイルのパスを取得
            files = event.data.split()
            if files:
                file_path = files[0].strip('{}')  # Remove braces / 波括弧を除去
                
                # Check if it's a PDF file / PDFファイルかチェック
                if file_path.lower().endswith('.pdf'):
                    self.file_path_var.set(file_path)
                    message = f"{self.lang_manager.get_text('file_dropped')}: {os.path.basename(file_path)}"
                    self.log_message(message)
                else:
                    messagebox.showerror(self.lang_manager.get_text("error"), 
                                       self.lang_manager.get_text("drop_pdf_only"))
                    
        except Exception as e:
            error_msg = f"{self.lang_manager.get_text('drop_error')}: {str(e)}"
            self.log_message(error_msg)
        
        return event.action
    def convert_pages(self, pdf_path):
        """Convert all pages sequentially / 全ページを順次変換"""
        doc = None
        try:
            # Open document / ドキュメントを開く
            doc = pymupdf.open(pdf_path)
            total_pages = len(doc)
            
            if total_pages == 0:
                return {'error': self.lang_manager.get_text("no_pages")}
            
            # For better performance with large PDFs, convert entire document at once
            # 大きなPDFでのパフォーマンス向上のため、ドキュメント全体を一度に変換
            try:
                # Convert entire document with PyMuPDF4LLM / PyMuPDF4LLMでドキュメント全体を変換
                md_text = pymupdf4llm.to_markdown(doc)
                
                # If page headers are requested, we'll process page by page / ページヘッダーが要求された場合はページ毎に処理
                if self.add_page_headers_var.get():
                    return self._convert_pages_with_headers(doc, total_pages)
                else:
                    # Return as single result / 単一結果として返す
                    self.progress_var.set(100)
                    self.log_message(f"{self.lang_manager.get_text('page_completed')} {total_pages}/{total_pages}")
                    self.root.update()
                    
                    return [{
                        'page_num': 1,
                        'content': md_text
                    }]
                    
            except Exception as e:
                # Fall back to page-by-page conversion / ページ毎の変換にフォールバック
                self.log_message(f"Falling back to page-by-page conversion: {str(e)}")
                return self._convert_pages_with_headers(doc, total_pages)
            
        except Exception as e:
            return {'error': f"{self.lang_manager.get_text('pdf_read_error')}: {str(e)}"}
        
        finally:
            if doc:
                doc.close()
    
    def _convert_pages_with_headers(self, doc, total_pages):
        """Convert pages individually with headers / ヘッダー付きでページを個別変換"""
        all_results = []
        
        for page_num in range(total_pages):
            single_page_doc = None
            try:
                # Add page number as header / ページ番号を見出しとして追加
                if self.add_page_headers_var.get():
                    header = f"\n\n# Page {page_num + 1}\n\n"
                else:
                    header = "\n\n"
                
                # Convert single page to Markdown / 単一ページをMarkdownに変換
                single_page_doc = pymupdf.open()
                single_page_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                
                # Convert with PyMuPDF4LLM / PyMuPDF4LLMで変換
                md_text = pymupdf4llm.to_markdown(single_page_doc)
                
                all_results.append({
                    'page_num': page_num + 1,
                    'content': header + md_text
                })
                
                # Update progress / プログレス更新
                progress = ((page_num + 1) / total_pages) * 100
                self.progress_var.set(progress)
                message = f"{self.lang_manager.get_text('page_completed')} {page_num + 1}/{total_pages}"
                self.log_message(message)
                self.root.update()  # Update UI / UI更新
                
            except Exception as e:
                error_msg = f"{self.lang_manager.get_text('page_conversion_error')} {page_num + 1}: {str(e)}"
                self.log_message(error_msg)
                # Continue on individual page errors / 個別ページのエラーは継続する
                
            finally:
                if single_page_doc:
                    single_page_doc.close()
        
        return all_results
    
    def convert_specific_pages(self, pdf_path, page_numbers):
        """Convert specific pages only / 指定したページのみを変換"""
        doc = None
        try:
            # Open document / ドキュメントを開く
            doc = pymupdf.open(pdf_path)
            total_pages = len(doc)
            
            if total_pages == 0:
                return {'error': self.lang_manager.get_text("no_pages")}
            
            all_results = []
            
            for i, page_num in enumerate(page_numbers):
                single_page_doc = None
                try:
                    # Add page number as header / ページ番号を見出しとして追加
                    if self.add_page_headers_var.get():
                        header = f"\n\n# Page {page_num}\n\n"
                    else:
                        header = "\n\n"
                    
                    # Convert single page to Markdown / 単一ページをMarkdownに変換
                    single_page_doc = pymupdf.open()
                    single_page_doc.insert_pdf(doc, from_page=page_num-1, to_page=page_num-1)
                    
                    # Convert with PyMuPDF4LLM / PyMuPDF4LLMで変換
                    md_text = pymupdf4llm.to_markdown(single_page_doc)
                    
                    all_results.append({
                        'page_num': page_num,
                        'content': header + md_text
                    })
                    
                    # Update progress / プログレス更新
                    progress = ((i + 1) / len(page_numbers)) * 100
                    self.progress_var.set(progress)
                    message = f"{self.lang_manager.get_text('page_completed')} {page_num} ({i + 1}/{len(page_numbers)})"
                    self.log_message(message)
                    self.root.update()  # Update UI / UI更新
                    
                except Exception as e:
                    error_msg = f"{self.lang_manager.get_text('page_conversion_error')} {page_num}: {str(e)}"
                    self.log_message(error_msg)
                    # Continue on individual page errors / 個別ページのエラーは継続する
                    
                finally:
                    if single_page_doc:
                        single_page_doc.close()
            
            return all_results
            
        except Exception as e:
            return {'error': f"{self.lang_manager.get_text('pdf_read_error')}: {str(e)}"}
        
        finally:
            if doc:
                doc.close()

    def start_conversion(self):
        """Start conversion / 変換開始"""
        pdf_path = self.file_path_var.get().strip()
        
        if not pdf_path:
            messagebox.showerror(self.lang_manager.get_text("error"), 
                               self.lang_manager.get_text("select_pdf_file"))
            return
            
        if not os.path.exists(pdf_path):
            messagebox.showerror(self.lang_manager.get_text("error"), 
                               self.lang_manager.get_text("file_not_found"))
            return
        
        if not pdf_path.lower().endswith('.pdf'):
            messagebox.showerror(self.lang_manager.get_text("error"), 
                               self.lang_manager.get_text("not_pdf_file"))
            return
        
        if self.is_converting:
            messagebox.showwarning(self.lang_manager.get_text("warning"), 
                                 self.lang_manager.get_text("conversion_in_progress"))
            return
        
        # Update UI state / UI状態の更新
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set(self.lang_manager.get_text("converting"))
        
        # Clear log / ログクリア
        self.log_text.delete(1.0, tk.END)
        self.log_message(self.lang_manager.get_text("conversion_starting"))
          # Execute conversion / 変換実行
        self.run_conversion(pdf_path)
    
    def run_conversion(self, pdf_path):
        """Execute conversion / 変換実行"""
        try:
            # Get total pages of PDF / PDFの総ページ数を取得
            with pymupdf.open(pdf_path) as doc:
                total_pages = len(doc)
            
            message = f"{self.lang_manager.get_text('total_pages')}: {total_pages}"
            self.log_message(message)
            
            # Parse page range / ページ範囲を解析
            try:
                page_range_str = self.page_range_var.get().strip()
                page_numbers = self.parse_page_range(page_range_str, total_pages)
                
                if page_numbers != list(range(1, total_pages + 1)):
                    # Convert specific pages / 指定ページを変換
                    self.log_message(f"Converting pages: {', '.join(map(str, page_numbers))}")
                    all_results = self.convert_specific_pages(pdf_path, page_numbers)
                else:
                    # Convert all pages / 全ページを変換
                    all_results = self.convert_pages(pdf_path)
                
            except Exception as e:
                # Show error for invalid page range / 無効なページ範囲のエラーを表示
                error_msg = str(e)
                self.log_message(error_msg)
                messagebox.showerror(self.lang_manager.get_text("error"), error_msg)
                self.reset_ui_state()
                return
            
            # Process results / 結果処理
            self.handle_conversion_result(pdf_path, all_results)
        
        except Exception as e:
            error_msg = f"{self.lang_manager.get_text('conversion_error')}: {str(e)}"
            self.handle_conversion_error(error_msg)
    
    def handle_conversion_result(self, pdf_path, all_results):
        """Process conversion results / 変換結果の処理"""
        try:
            if isinstance(all_results, dict) and 'error' in all_results:
                self.log_message(all_results['error'])
                self.status_var.set(self.lang_manager.get_text("error"))
                messagebox.showerror(self.lang_manager.get_text("error"), all_results['error'])
            elif all_results:
                output_path = self.save_markdown(pdf_path, all_results)
                message = f"{self.lang_manager.get_text('conversion_completed')}: {output_path}"
                self.log_message(message)
                self.status_var.set(self.lang_manager.get_text("conversion_completed"))
                success_msg = f"{self.lang_manager.get_text('conversion_success')} {output_path}"
                messagebox.showinfo(self.lang_manager.get_text("completed"), success_msg)
            else:
                self.log_message(self.lang_manager.get_text("no_content"))
                self.status_var.set(self.lang_manager.get_text("conversion_failed"))
                messagebox.showwarning(self.lang_manager.get_text("warning"), 
                                     self.lang_manager.get_text("no_content"))
        
        finally:
            self.reset_ui_state()
    
    def handle_conversion_error(self, error_msg):
        """Process conversion errors / 変換エラーの処理"""
        self.log_message(error_msg)
        self.status_var.set(self.lang_manager.get_text("error"))
        messagebox.showerror(self.lang_manager.get_text("error"), error_msg)
        self.reset_ui_state()
    
    def save_markdown(self, pdf_path, results):
        """Save as Markdown file / Markdownファイルとして保存"""
        try:
            # Determine output filename (safe filename generation) / 出力ファイル名を決定（安全なファイル名生成）
            pdf_name = pathlib.Path(pdf_path).stem
            parent_dir = pathlib.Path(pdf_path).parent
            
            # Add page range info to filename if specific pages were converted / 特定ページが変換された場合はページ範囲情報をファイル名に追加
            page_range_str = self.page_range_var.get().strip()
            if page_range_str:
                # Sanitize page range string for filename / ファイル名用にページ範囲文字列をサニタイズ
                safe_range = page_range_str.replace(',', '_').replace('-', 'to').replace(' ', '')
                output_path = parent_dir / f"{pdf_name}_pages_{safe_range}.md"
            else:
                output_path = parent_dir / f"{pdf_name}.md"
            
            # Add number if existing file exists / 既存ファイルがある場合は番号を付ける
            counter = 1
            original_output_path = output_path
            while output_path.exists():
                if page_range_str:
                    safe_range = page_range_str.replace(',', '_').replace('-', 'to').replace(' ', '')
                    output_path = parent_dir / f"{pdf_name}_pages_{safe_range}_{counter}.md"
                else:
                    output_path = parent_dir / f"{pdf_name}_{counter}.md"
                counter += 1
            
            # Combine content and save / 内容を結合して保存
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {pdf_name}\n\n")
                f.write(f"*PDF to Markdown converted file*\n\n")
                if page_range_str:
                    f.write(f"*Converted pages: {page_range_str}*\n\n")
                f.write("---\n\n")
                
                for result in results:
                    f.write(result['content'])
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"{self.lang_manager.get_text('file_save_error')}: {str(e)}")
    
    def reset_ui_state(self):
        """Reset UI state / UI状態のリセット"""
        self.is_converting = False
        self.convert_button.config(state=tk.NORMAL)
        self.progress_var.set(0)
    
    def parse_page_range(self, page_range_str, total_pages):
        """Parse page range string and return list of page numbers / ページ範囲文字列を解析してページ番号のリストを返す"""
        if not page_range_str.strip():
            # Return all pages if empty / 空の場合は全ページを返す
            return list(range(1, total_pages + 1))
        
        pages = []
        try:
            # Split by comma / カンマで分割
            parts = page_range_str.split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range specification like "1-5" / "1-5"のような範囲指定
                    start, end = part.split('-', 1)
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    if start < 1 or end > total_pages or start > end:
                        raise ValueError(f"Invalid range: {part}")
                    
                    pages.extend(range(start, end + 1))
                else:
                    # Single page number / 単一ページ番号
                    page_num = int(part)
                    if page_num < 1 or page_num > total_pages:
                        raise ValueError(f"Page {page_num} out of range")
                    pages.append(page_num)
            
            # Remove duplicates and sort / 重複を削除してソート
            pages = sorted(list(set(pages)))
            return pages
            
        except ValueError as e:
            raise Exception(f"{self.lang_manager.get_text('page_range_error')}: {str(e)}")
        except Exception as e:
            raise Exception(f"{self.lang_manager.get_text('invalid_page_range')}: {str(e)}")


def main():
    """Main function / メイン関数"""
    try:
        if DRAG_DROP_AVAILABLE:
            root = TkinterDnD.Tk()
        else:
            root = tk.Tk()
    except Exception:
        # Final fallback / 最終フォールバック
        root = tk.Tk()
    
    app = PDFToMarkdownConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()

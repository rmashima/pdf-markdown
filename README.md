# PDF to Markdown Converter

A simple GUI application for converting PDF files to Markdown format using PyMuPDF4LLM.

## Overview

This application provides a graphical user interface (GUI) for converting PDF files to Markdown format. It achieves high-quality conversion using the PyMuPDF4LLM library.

## Features

- Convert PDF files to Markdown format
- Intuitive GUI interface
- Drag & drop file selection
- Real-time conversion progress display
- Customizable conversion options

## Requirements

- Python 3.12 or higher
- Windows 10/11 (compatible with other platforms)

## Installation

### Development Environment Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pdf-markdown
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Run the application:
```bash
uv run python main.py
```

## Build Method

You can create a standalone executable file using PyInstaller.

### Prerequisites

- uv must be installed
- `icon.ico` file must be placed in the project root

### Build Steps

1. Add PyInstaller to dependencies:
```bash
uv add pyinstaller
```

2. Build the EXE file:
```bash
uv run pyinstaller --onefile --windowed --icon=icon.ico --name="PDF-to-Markdown-Converter" main.py
```

3. Remove unnecessary files:
```bash
Remove-Item -Recurse -Force build
Remove-Item "PDF-to-Markdown-Converter.spec"
```

The built EXE file will be generated in the `dist` folder.

### Build Options Explanation

- `--onefile`: Create as a single executable file
- `--windowed`: Don't display console window (for GUI applications)
- `--icon=icon.ico`: Specify application icon
- `--name="PDF-to-Markdown-Converter"`: Specify output filename

## Usage

### GUI Application Usage

1. Launch the application
2. Click the "Browse" button to select a PDF file or drag & drop files
3. Configure conversion options as needed
4. Click the "Start Conversion" button to execute conversion
5. When conversion is complete, the Markdown file will be saved in the same directory

### Supported File Formats

- **Input**: PDF (.pdf)
- **Output**: Markdown (.md)

## Dependencies

This project uses the following libraries:

| Library | Version | License | Description |
|---------|---------|---------|-------------|
| PyMuPDF4LLM | >=0.0.10 | AGPL-3.0 | Library for PDF analysis and Markdown conversion |
| tkinterdnd2 | >=0.4.3 | MIT | Adds drag & drop functionality to Tkinter |
| PyInstaller | >=6.13.0 | GPL-2.0 | Tool for converting Python applications to executables |

### License Details

#### PyMuPDF / PyMuPDF4LLM
- **License**: AGPL-3.0 License
- **Overview**: PyMuPDF is a PDF processing library developed by Artifex Software
- **Commercial Use**: Available under AGPL license conditions. Commercial licenses are also available
- **Details**: [PyMuPDF License](https://pymupdf.readthedocs.io/en/latest/about.html#license)

#### tkinterdnd2
- **License**: MIT License
- **Overview**: Library that adds drag and drop functionality to Tkinter
- **Commercial Use**: Can be used without restrictions

#### PyInstaller
- **License**: GPL-2.0 License
- **Overview**: Tool for converting Python scripts to executable files
- **Commercial Use**: Available under GPL license conditions

## Development

### Project Structure
```
pdf-markdown/
├── main.py              # Main application file
├── pyproject.toml       # Project configuration and metadata
├── icon.ico            # Application icon
├── README.md           # This file
├── uv.lock            # Dependency lock file
└── dist/              # Built executable files
    └── PDF-to-Markdown-Converter.exe
```

### Development Environment Setup

1. Build development environment using uv:
```bash
uv sync
```

2. Run application in development mode:
```bash
uv run python main.py
```

## Troubleshooting

### Common Issues

1. **PyMuPDF4LLM Import Error**
   - Solution: Run `uv sync` to reinstall dependencies

2. **Icon File Not Found**
   - Solution: Ensure `icon.ico` file exists in the project root

3. **EXE File Won't Start**
   - Solution: May be blocked by Windows Defender or antivirus software

## License

This project is published under the AGPL-3.0 license. Please also note the licenses of the dependencies used:
- PyMuPDF/PyMuPDF4LLM: AGPL-3.0 (Note for commercial use)
- tkinterdnd2: MIT
- PyInstaller: GPL-2.0 (Used only for EXE building)

## Contributing

Contributions to the project are welcome. Bug reports and feature requests are managed through GitHub Issues.

## Support

If you have any problems or questions, you can get support through the following methods:

1. Report issues on the GitHub Issues page
2. Ask questions on the project's Discussions page

---

**Notice**: This software is provided without warranty, either express or implied. Please check and properly comply with the license terms of the dependencies used.
# Quick Notepad

Quick Notepad is a lightweight Windows desktop text editor built with Python and wxPython. It provides a straightforward interface for creating and editing plain-text documents.

## Features

- Create, open, and save text files
- Undo and redo, clipboard actions, and select all
- Automatic word wrapping
- Light and dark editor themes, plus font selection
- Text analysis for non-whitespace characters, words, and lines
- An asterisk in the window title when there are unsaved changes
- Keyboard shortcuts for common file and editing actions

## Requirements

- Windows
- Python 3
- wxPython (installed from `requirements.txt`)

## Installation

1. Install Python 3 for Windows if it is not already installed.
2. Download or clone this repository.
3. In the project folder, install the dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Usage

Run the app from the project folder:

```powershell
python quick_notepad.py
```

Use the **File** menu to create, open, or save a document. The **Edit** menu provides standard editing actions, **Tools** opens text analysis, and **Settings** provides theme and font selection. The app asks before discarding unsaved changes.

Common shortcuts:

| Action | Shortcut |
| --- | --- |
| New | Ctrl+N |
| Open | Ctrl+O |
| Save | Ctrl+S |
| Save as | Ctrl+Shift+S |
| Close | Ctrl+W |
| Undo / Redo | Ctrl+Z / Ctrl+Y |
| Cut / Copy / Paste | Ctrl+X / Ctrl+C / Ctrl+V |
| Select all | Ctrl+A |

## Offline use

Quick Notepad does not require an internet connection to run or edit local files. An internet connection may be needed to download Python or install wxPython.

## Windows executable

A prebuilt Windows executable is provided through the project's GitHub **Releases**. Download the executable from a release to run the app without installing Python or wxPython.

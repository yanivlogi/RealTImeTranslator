**[עברית](README.md)** | **[English]**
___

# Translate Screen

Description
- A Python script that performs real-time OCR on a defined screen region and displays the translation in Hebrew in an overlay window.
- Uses `easyocr` for text recognition and `deep_translator` (GoogleTranslator) for translation.

Files
- Main script: `translate.py`

Dependencies
- Python 3.8+
- pip packages:
  - `easyocr`
  - `opencv-python`
  - `numpy`
  - `Pillow`
  - `deep-translator`
- `tkinter` (usually included with Python on Windows)
- Note: `easyocr` requires `torch` — install PyTorch appropriate for your system if you want GPU support.

Installation
```bash
python -m pip install easyocr opencv-python numpy Pillow deep-translator
# Install torch according to your OS/CUDA version if you want GPU acceleration
```

Usage
1. Adjust the capture region by editing the `bbox` variable at the top of `translate.py`.
   - Format: `[x1, y1, x2, y2]` (pixels, top-left then bottom-right).
2. Run:
```bash
python translate.py
```
3. Three windows will open:
   - A red framed window (border-only) that marks the capture area.
   - A black translation window that shows the translated text.
   - A control window to move the capture box and translation window or toggle the frame.

Control Window
- "Show/Hide Red Frame": toggles the visibility of the red capture frame.
- Arrow buttons: move the capture region or the translation window by 10 pixels per click.

Common adjustments
- OCR languages: change `reader = easyocr.Reader(['en'], gpu=False)` to the desired language code(s).
- Enable GPU for `easyocr`: set `gpu=True` and install a compatible `torch` build.
- The script filters and cleans detected text before sending it to translation — adjust the heuristics as needed.

Known issues and notes
- The code swallows exceptions (`except: pass`) — failures may be silent; consider adding logging for debugging.
- `ImageGrab` may require screen-capture permissions on some Windows setups.
- OCR performance depends on the clarity and contrast of text in the capture region.

Possible improvements
- Replace broad exception handlers with explicit error logging.
- Support multiple OCR languages or automatic language detection.
- Add history, copy-to-clipboard, or hotkey-based capture features.

Next steps I can help with
- Add a `requirements.txt` file and update the repo.
- Add verbose logging and error handling to `translate.py`.
- Add a simple installer or a packaged executable for Windows.

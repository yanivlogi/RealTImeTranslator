import easyocr
import tkinter as tk
import threading
import time
import numpy as np
import cv2
import re
from PIL import ImageGrab
from deep_translator import GoogleTranslator
import queue

# הגדרות התחלתיות
bbox = [400, 750, 1500, 950]
reader = easyocr.Reader(['en'], gpu=False)
translation_queue = queue.Queue()

# --- חלון 1: מסגרת אדומה (דיבאג) ---
root_frame = tk.Tk()
root_frame.overrideredirect(True)
root_frame.attributes('-topmost', True)
root_frame.attributes('-transparentcolor', 'white')
canvas = tk.Canvas(root_frame, bg='white', highlightthickness=0)
canvas.pack(fill='both', expand=True)
rect = canvas.create_rectangle(0, 0, 1100, 100, outline='red', width=4)

# --- חלון 2: טקסט תרגום (כחול) ---
root_trans = tk.Toplevel()
root_trans.overrideredirect(True)
root_trans.attributes('-topmost', True)
root_trans.configure(bg='black')
label = tk.Label(root_trans, text="ממתין...", fg="#00FFCC", bg="black", 
                 font=("Arial", 18, "bold"), justify="right", wraplength=800)
label.pack(padx=10, pady=10)

# --- שלט בקרה ---
ctrl = tk.Toplevel()
ctrl.title("מרכז שליטה")
ctrl.attributes('-topmost', True)
ctrl.geometry("300x450+500+200")

def toggle_frame():
    curr = canvas.itemcget(rect, "state")
    canvas.itemconfig(rect, state='hidden' if curr == 'normal' else 'normal')

def move_bbox(dx, dy):
    bbox[0] += dx; bbox[2] += dx
    bbox[1] += dy; bbox[3] += dy
    root_frame.geometry(f"{bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}+{bbox[0]}+{bbox[1]}")

def move_window(dx, dy):
    root_trans.geometry(f"+{root_trans.winfo_x() + dx}+{root_trans.winfo_y() + dy}")

# כפתורים
tk.Button(ctrl, text="הצג/הסתר מסגרת אדומה", command=toggle_frame).pack(fill='x')
tk.Label(ctrl, text="--- הזזת סריקה (אדום) ---").pack()
f1 = tk.Frame(ctrl); f1.pack()
tk.Button(f1, text="⬆️", command=lambda: move_bbox(0, -10)).grid(row=0, column=1)
tk.Button(f1, text="⬅️", command=lambda: move_bbox(-10, 0)).grid(row=1, column=0)
tk.Button(f1, text="➡️", command=lambda: move_bbox(10, 0)).grid(row=1, column=2)
tk.Button(f1, text="⬇️", command=lambda: move_bbox(0, 10)).grid(row=2, column=1)

tk.Label(ctrl, text="--- הזזת תרגום (כחול) ---").pack()
f2 = tk.Frame(ctrl); f2.pack()
tk.Button(f2, text="⬆️", command=lambda: move_window(0, -10)).grid(row=0, column=1)
tk.Button(f2, text="⬅️", command=lambda: move_window(-10, 0)).grid(row=1, column=0)
tk.Button(f2, text="➡️", command=lambda: move_window(10, 0)).grid(row=1, column=2)
tk.Button(f2, text="⬇️", command=lambda: move_window(0, 10)).grid(row=2, column=1)

# --- לוגיקה ---
def monitor_screen():
    last_text = ""
    while True:
        try:
            img = np.array(ImageGrab.grab(tuple(bbox)))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # זיהוי טקסט עם פרטים כדי לסנן לפי מיקום
            results = reader.readtext(gray, detail=1)
            width, height = img.shape[1], img.shape[0]
            
            clean_list = []
            for (coords, text, prob) in results:
                # חישוב מרכז התיבה וסינון טקסט מחוץ למסגרת
                x_center = (coords[0][0] + coords[2][0]) / 2
                y_center = (coords[0][1] + coords[2][1]) / 2
                if 0 < x_center < width and 0 < y_center < height:
                    if len(text) > 3 and not any(c.isdigit() for c in text):
                        clean_list.append(text)
            
            txt = " ".join(clean_list)
            clean = re.sub(r'[^\w\s\:]', '', txt)
            if len(clean) > 3 and clean != last_text:
                last_text = clean
                translation_queue.put(clean)
        except: pass
        time.sleep(0.5)

def translator_worker():
    while True:
        text = translation_queue.get()
        try:
            prefix = ""
            if "Bond:" in text:
                prefix = "בונד: "
                text = text.replace("Bond:", "").strip()
            translated = GoogleTranslator(source='en', target='iw').translate(text)
            root_trans.after(0, lambda: label.config(text=prefix + translated))
        except: pass

threading.Thread(target=monitor_screen, daemon=True).start()
threading.Thread(target=translator_worker, daemon=True).start()
root_frame.geometry(f"{bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}+{bbox[0]}+{bbox[1]}")
root_trans.mainloop()
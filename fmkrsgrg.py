import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
import subprocess

# Новый стиль и цвета
BG_COLOR = "#121212"
CARD_COLOR = "#1f1f1f"
ACCENT_COLOR = "#00ffff"
HIGHLIGHT_COLOR = "#33cccc"
TEXT_COLOR = "#eeeeee"
ACTIVE_COLOR = "#00ffff"

FONT_TITLE = ("Arial", 14, "bold")
FONT_TEXT = ("Arial", 11)
FONT_BUTTON = ("Arial", 12, "bold")

led_state = False
crt_active = False
scan_y = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
vault_path = os.path.join(BASE_DIR, "vaultboy.png")
power_on_path = os.path.join(BASE_DIR, "power on.wav")
power_off_path = os.path.join(BASE_DIR, "power off.wav")

def play_sound(file):
    if os.path.exists(file):
        subprocess.run(["afplay", file])
    else:
        print("Файл не найден:", file)

def toggle_led():
    global led_state, crt_active
    led_state = not led_state

    if led_state:
        play_sound(power_on_path)
        status_label.config(text="STATUS: ONLINE")
        power_btn.config(text="ON", bg=ACCENT_COLOR)
        indicator.itemconfig(ind_light, fill=ACCENT_COLOR)
        crt_active = True
        scanline()
        crt_flicker()
    else:
        play_sound(power_off_path)
        status_label.config(text="STATUS: OFFLINE")
        power_btn.config(text="OFF", bg="#444")
        indicator.itemconfig(ind_light, fill="#222")
        crt_active = False
        canvas.delete("scan")

def scanline():
    global scan_y
    if not crt_active:
        return
    canvas.delete("scan")
    canvas.create_rectangle(0, scan_y, 320, scan_y + 3, fill=HIGHLIGHT_COLOR, outline="", tags="scan")
    scan_y = (scan_y + 5) % 240
    win.after(35, scanline)

def crt_flicker():
    if not crt_active:
        return
    alpha = random.randint(235, 255)
    win.attributes("-alpha", alpha / 255)
    win.after(80, crt_flicker)

def aboutMsg():
    messagebox.showinfo("About", "Vault-Tec Power Interface\nModern styled interface\n2026")

def exit_app(event=None):
    win.quit()

# Главное окно
win = tk.Tk()
win.title("Vault-Tec Interface")
win.geometry("400x300")
win.configure(bg=BG_COLOR)
win.resizable(False, False)

# Основная рамка
frame = tk.Frame(win, bg=CARD_COLOR, bd=2, relief="raised")
frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=280)

# Заголовок
title_label = tk.Label(frame, text="Vault-Tec Power", font=FONT_TITLE, fg=ACCENT_COLOR, bg=CARD_COLOR)
title_label.pack(pady=10)

# Статус
status_label = tk.Label(frame, text="STATUS: OFFLINE", fg=TEXT_COLOR, bg=CARD_COLOR, font=FONT_TEXT)
status_label.pack()

# ИК-ограник (индикатор)
indicator = tk.Canvas(frame, width=20, height=20, bg=CARD_COLOR, highlightthickness=0)
indicator.pack(pady=5)
ind_light = indicator.create_oval(2, 2, 18, 18, fill="#222", outline="#555")

# Межстрочный разделитель
separator = tk.Frame(frame, height=2, bg=HIGHLIGHT_COLOR)
separator.pack(fill='x', padx=10, pady=10)

# Vault Boy изображение или рисованный блок
try:
    pil_img = Image.open(vault_path)
    pil_img = pil_img.resize((80, 80))
    tk_img = ImageTk.PhotoImage(pil_img)
    vault_img_label = tk.Label(frame, image=tk_img, bg=CARD_COLOR)
    vault_img_label.image = tk_img
except Exception as e:
    print("Ошибка загрузки vaultboy.png:", e)
    vault_img_label = tk.Label(frame, text="Vault Boy", fg=TEXT_COLOR, bg=CARD_COLOR, font=FONT_TEXT)

vault_img_label.pack(pady=10)

# Кнопка питания
power_btn = tk.Button(frame, text="OFF", font=FONT_BUTTON, bg="#444", fg=TEXT_COLOR, width=10, command=toggle_led)
power_btn.pack(pady=10)

# ABOUT кнопка
about_btn = tk.Button(frame, text="ABOUT", font=FONT_TEXT, width=8, bg=HIGHLIGHT_COLOR, fg=BG_COLOR, command=aboutMsg)
about_btn.pack(side="bottom", pady=10)

# Обработка клавиш
win.bind("<Escape>", exit_app)
win.bind("<Control-q>", exit_app)

# Создаем холст для сканлайна
canvas = tk.Canvas(frame, width=320, height=240, bg="black", highlightthickness=0)
canvas.place(relx=0.5, rely=0.55, anchor="n")
canvas.create_rectangle(5, 5, 315, 235, outline=ACCENT_COLOR, width=2)

win.mainloop()
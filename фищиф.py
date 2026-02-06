import tkinter as tk
from tkinter import messagebox
from pyfirmata import Arduino, PWM
import threading

# Инициализация Arduino (раскомментируйте и укажите свой порт)
try:
    board = Arduino("COM3")  # Замените на ваш порт
    board.digital[3].mode = PWM
    board.digital[5].mode = PWM
except Exception as e:
    messagebox.showerror("Ошибка соединения", f"Не удалось подключиться к Arduino: {e}")
    board = None

def set_led(pin_number, brightness):
    """Обновляем яркость LED на пине, если Arduino подключен."""
    if board:
        # brightness — число от 0 до 1
        board.digital[pin_number].write(brightness)

def run_led(pin_number, delay, brightness):
    """Запускаем управление светодиодом в отдельном потоке."""
    def task():
        # Включение LED
        set_led(pin_number, brightness)
        # Задержка
        sleep_time = delay * 1000  # ms для after
        root.after(int(sleep_time), lambda: set_led(pin_number, 0))
        # Фокусируем кнопку обратно
        if pin_number == 3:
            blueBtn.config(state=tk.NORMAL)
        elif pin_number == 5:
            redBtn.config(state=tk.NORMAL)
    # Отключаем кнопку во время работы
    if pin_number == 3:
        blueBtn.config(state=tk.DISABLED)
    elif pin_number == 5:
        redBtn.config(state=tk.DISABLED)
    threading.Thread(target=task, daemon=True).start()

def blueLED():
    try:
        delay = float(LEDtime.get())
        brightness_percent = float(LEDbright.get())
        brightness = brightness_percent / 100.0
        run_led(3, delay, brightness)
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте введённые данные!")

def redLED():
    try:
        delay = float(LEDtime.get())
        brightness_percent = float(LEDbright.get())
        brightness = brightness_percent / 100.0
        run_led(5, delay, brightness)
    except ValueError:
        messagebox.showerror("Ошибка", "Проверьте введённые данные!")

def aboutMsg():
    messagebox.showinfo(
        "О программе",
        "LED Контроллер v1.0\nJanuary 2026\n\nРабота с хорошим Arduino через Python"
    )

# Создаем почти то же окно
win = tk.Tk()
win.title("Dimmer LED")
win.geometry("400x250")
win.resizable(False, False)
win.configure(bg="#1e1e2f")

# Шрифты
font_title = ("Gabriola", 26, "bold")
font_text = ("Segoe Script", 12, "bold")
font_btn = ("Segoe Script", 11, "bold")

# Заголовок
tk.Label(win, text="LED CONTROLLER", font=font_title, fg="white", bg="#1e1e2f").grid(column=1, row=0, columnspan=2, pady=10)

# Ввод времени
tk.Label(win, text="Время (сек)", font=font_text, fg="white", bg="#1e1e2f").grid(column=1, row=1, sticky="w")
LEDtime = tk.Entry(win, width=10, font=font_text, bg="#2a2a40", fg="white")
LEDtime.grid(column=2, row=1)

# Яркость
tk.Label(win, text="Яркость", font=font_text, fg="white", bg="#1e1e2f").grid(column=1, row=2, sticky="w")
LEDbright = tk.Scale(win, from_=0, to=100, orient=tk.HORIZONTAL, bg="#1e1e2f", fg="white", troughcolor="#2a2a40")
LEDbright.grid(column=2, row=2)

# Кнопки
blueBtn = tk.Button(win, text="BLUE LED", font=font_btn, bg="#3b82f6", fg="white", relief="flat", width=12, command=blueLED)
blueBtn.grid(column=1, row=3, pady=10)
redBtn = tk.Button(win, text="RED LED", font=font_btn, bg="#ef4444", fg="white", relief="flat", width=12, command=redLED)
redBtn.grid(column=2, row=3)
aboutBtn = tk.Button(win, text="Справка", font=font_btn, bg="#22c55e", fg="white", relief="flat", width=12, command=aboutMsg)
aboutBtn.grid(column=1, row=4, pady=5)
quitBtn = tk.Button(win, text="Закрыть", font=font_btn, bg="#6b7280", fg="white", relief="flat", width=12, command=win.quit)
quitBtn.grid(column=2, row=4)

win.mainloop()
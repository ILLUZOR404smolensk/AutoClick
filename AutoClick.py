import tkinter as tk
from tkinter import ttk
import threading
import keyboard
import mouse
import time


work = False

def autoclicker_logic():
    """Логика кликера, которая будет работать в фоне"""
    global work
    while True:
        if work:
            mouse.click(button='left')
            time.sleep(0.1)
        else:
            time.sleep(0.1)

def toggle_work():
    """Функция для переключения состояния"""
    global work
    work = not work
    status_label.config(text=f"Статус: {'РАБОТАЕТ' if work else 'СТОП'}", 
                        foreground="green" if work else "red")


keyboard.add_hotkey('=', toggle_work)


root = tk.Tk()
root.title("My AutoClicker")
root.geometry("250x150")

status_label = ttk.Label(root, text="Статус: СТОП", font=("Arial", 12), foreground="red")
status_label.pack(pady=20)

btn = ttk.Button(root, text="Вкл/Выкл (=)", command=toggle_work)
btn.pack(pady=10)


threading.Thread(target=autoclicker_logic, daemon=True).start()

root.mainloop()


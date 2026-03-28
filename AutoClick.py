import keyboard
import mouse
import time

print("Нажмите '=' для запуска/остановки")

work = False

def change():
    global work
    work = not work
    state = "ЗАПУЩЕН" if work else "ОСТАНОВЛЕН"
    print(f"Статус: {state}")

keyboard.add_hotkey('=', change)

while True:
    if work:
        mouse.click(button='left')
        time.sleep(0.1) 
    else:
        time.sleep(0.1)  

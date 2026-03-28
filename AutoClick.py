import tkinter as tk
from tkinter import ttk
import threading
import keyboard
import mouse
import time

class UltraClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultra Clicker v3.3")
        self.root.geometry("400x550")
        self.root.attributes("-topmost", True)
        self.root.configure(background="#121212")

       
        self.work = False
        self.recorded_actions = []
        self.is_recording = False
        self.is_playing = False
        self.start_rec_time = 0
        
        
        self.hotkeys = ['1', '2', '3', '4', '=']

        self.setup_ui()
        self.setup_hotkeys()
        
        
        threading.Thread(target=self.clicker_loop, daemon=True).start()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#121212")
        style.configure("TLabelframe", background="#121212", foreground="#00d4ff", bordercolor="#333")
        style.configure("TLabelframe.Label", background="#121212", foreground="#00d4ff", font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background="#121212", foreground="#bbbbbb", font=("Segoe UI", 9))

        
        f1 = ttk.LabelFrame(self.root, text=" АВТОКЛИКЕР ", padding=15)
        f1.pack(fill="x", padx=20, pady=10)
        
        row1 = ttk.Frame(f1)
        row1.pack(fill="x")
        ttk.Label(row1, text="Старт/Стоп: [ = ]").pack(side="left")
        self.lbl_c = ttk.Label(row1, text="ВЫКЛ", foreground="#ff4444", font=("Segoe UI", 11, "bold"))
        self.lbl_c.pack(side="right")

        row2 = ttk.Frame(f1)
        row2.pack(fill="x", pady=(10, 0))
        ttk.Label(row2, text="Интервал (сек):").pack(side="left")
        self.click_speed = tk.DoubleVar(value=0.1)
        
        self.ent_speed = ttk.Entry(row2, textvariable=self.click_speed, width=8, justify="center")
        self.ent_speed.pack(side="right")

        
        f2 = ttk.LabelFrame(self.root, text=" ЗАПИСЬ ДЕЙСТВИЙ ", padding=15)
        f2.pack(fill="x", padx=20, pady=10)
        info = "1 - Старт | 2 - Стоп | 3 - Повтор | 4 - СТОП"
        ttk.Label(f2, text=info, justify="center").pack(pady=5)
        self.lbl_m = ttk.Label(f2, text="ГОТОВ", foreground="#00ff88", font=("Segoe UI", 11, "bold"))
        self.lbl_m.pack(pady=5)

        
        f3 = ttk.LabelFrame(self.root, text=" ПОВТОРЫ МАКРОСА ", padding=15)
        f3.pack(fill="x", padx=20, pady=10)
        ttk.Label(f3, text="Кол-во циклов:").pack(side="left")
        self.rep_var = tk.IntVar(value=1)
        self.ent_rep = ttk.Entry(f3, textvariable=self.rep_var, width=8, justify="center")
        self.ent_rep.pack(side="right")

    def setup_hotkeys(self):
        keyboard.unhook_all()
       
        keyboard.add_hotkey('=', self.toggle_clicker)
        keyboard.add_hotkey('1', self.start_full_record)
        keyboard.add_hotkey('2', self.stop_full_record)
        keyboard.add_hotkey('3', self.play_threaded)
        keyboard.add_hotkey('4', self.emergency_stop)

    def is_focus_on_input(self):
        """Проверка: если курсор в поле ввода, игнорируем команды 1,2,3,"=" """
        focus = self.root.focus_get()
        return focus in [self.ent_speed, self.ent_rep]

    def toggle_clicker(self):
        if self.is_focus_on_input(): return
        self.work = not self.work
        self.lbl_c.config(text="ВКЛ" if self.work else "ВЫКЛ", foreground="#00ff88" if self.work else "#ff4444")

    def clicker_loop(self):
        while True:
            if self.work:
                try:
                    val = self.click_speed.get()
                    
                    delay = max(0.001, float(val))
                    mouse.click()
                    time.sleep(delay)
                except:
                    time.sleep(0.1)
            else:
                time.sleep(0.05)



    def start_full_record(self):
        if self.is_focus_on_input() or self.is_recording: return
        self.recorded_actions = []
        self.is_recording = True
        self.start_rec_time = time.perf_counter()
        self.lbl_m.config(text="ИДЕТ ЗАПИСЬ...", foreground="#ffaa00")
        
        mouse.hook(self._record_mouse)
        keyboard.hook(self._record_kb)

    def _record_mouse(self, event):
        if self.is_recording:
            self.recorded_actions.append(('mouse', event, time.perf_counter() - self.start_rec_time))

    def _record_kb(self, event):
        
        if self.is_recording and event.name not in self.hotkeys:
            self.recorded_actions.append(('kb', event, time.perf_counter() - self.start_rec_time))

    def stop_full_record(self):
        if self.is_focus_on_input(): return
        if self.is_recording:
            self.is_recording = False
            mouse.unhook(self._record_mouse)
            keyboard.unhook(self._record_kb)
            self.setup_hotkeys() 
            self.lbl_m.config(text="ЗАПИСАНО", foreground="#00aaff")

    def play_threaded(self):
        if self.is_focus_on_input(): return
        if not self.is_playing and self.recorded_actions:
            threading.Thread(target=self.play_logic, daemon=True).start()

    def play_logic(self):
        self.is_playing = True
        self.lbl_m.config(text="ВОСПРОИЗВЕДЕНИЕ", foreground="#00ff88")
        try:
            cycles = int(self.rep_var.get())
            for _ in range(cycles):
                if not self.is_playing: break
                start_p = time.perf_counter()
                for act_type, event, ts in self.recorded_actions:
                    if not self.is_playing: break
                   
                    while (time.perf_counter() - start_p) < ts:
                        if not self.is_playing: break
                        time.sleep(0.001)
                    
                    if act_type == 'kb':
                        if event.event_type == 'down': keyboard.press(event.name)
                        else: keyboard.release(event.name)
                    elif act_type == 'mouse':
                        if isinstance(event, mouse.ButtonEvent):
                            if event.event_type == 'down': mouse.press(event.button)
                            else: mouse.release(event.button)
                        elif isinstance(event, mouse.MoveEvent):
                            mouse.move(event.x, event.y, absolute=True)
        except: pass
        self.is_playing = False
        self.lbl_m.config(text="ГОТОВ", foreground="#00aaff")

    def emergency_stop(self):
        self.is_playing = False
        self.work = False
        self.is_recording = False
        try:
            mouse.unhook(self._record_mouse)
            keyboard.unhook(self._record_kb)
        except: pass
        self.setup_hotkeys()
        self.lbl_c.config(text="ВЫКЛ", foreground="#ff4444")
        self.lbl_m.config(text="СТОП", foreground="#ff4444")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraClickerApp(root)
    root.mainloop()
#Это исходный код приложения

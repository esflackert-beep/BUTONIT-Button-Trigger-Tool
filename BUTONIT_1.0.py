from pynput import keyboard, mouse
import tkinter as tk
import threading
import time
import random
import atexit
import logging

# Logging-Konfiguration (Punkt 7)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

FLICK_INTERVAL_MS = 150
COMBO_RECORD_TIME = 3.0

class AutoFireGUI:
    def __init__(self):
        self.firing = False
        self.hold_mode = False
        self.fire_thread = None
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.running = True
        self.combo_actions = []
        self.listening = False
        self.fire_rate = 5
        self.rate_mode = "cps"
        self.delay_threshold = 0.0
        self.key_listener = None
        self.mouse_listener = None
        
        # Threading-Lock für combo_actions (Punkt 8)
        self.combo_lock = threading.Lock()
        
        # Cleanup registrieren (JCA Vorteil)
        atexit.register(self.cleanup)

        self.root = tk.Tk()
        self.root.title("BUTOON IT! 1.0")
        self.root.geometry("280x340")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#0d0d0d")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        main = tk.Frame(self.root, bg="#0d0d0d", padx=6, pady=3)
        main.pack(fill=tk.BOTH, expand=True)

        # Status mit Flicker-Hintergrund (oben)
        status_frame = tk.Frame(main, bg="#0d0d0d")
        status_frame.pack(pady=2)

        self.flicker_top = tk.Canvas(status_frame, width=120, height=20, bg="#000000", highlightthickness=0)
        self.flicker_top.pack()
        
        self.status_label = tk.Label(status_frame, text="BUTTOON IT! 1.0", font=("Consolas", 10, "bold"), 
                                     fg="#00ff41", bg="#000000")
        self.status_label.place(in_=self.flicker_top, relx=0.5, rely=0.5, anchor="center")

        # Button mit Flicker-Hintergrund
        button_frame = tk.Frame(main, bg="#0d0d0d")
        button_frame.pack(pady=2)

        self.flicker_button = tk.Canvas(button_frame, width=140, height=28, bg="#000000", highlightthickness=0)
        self.flicker_button.pack()

        self.select_btn = tk.Button(button_frame, text="Button it!", command=self.start_key_selection,
                                    font=("Consolas", 9, "bold"), fg="#00ff41", bg="#1a1a1a",
                                    relief='flat', cursor='hand2', padx=8, pady=3)
        self.select_btn.place(in_=self.flicker_button, relx=0.5, rely=0.5, anchor="center")

        self.key_label = tk.Label(main, text="[ NO COMBO ]", font=("Consolas", 9, "bold"), fg="#00cc33", bg="#0d0d0d")
        self.key_label.pack(pady=2)

        # Rate Mode Wahl
        mode_frame = tk.Frame(main, bg="#0d0d0d")
        mode_frame.pack(pady=2, fill=tk.X)

        self.mode_var = tk.StringVar(value="cps")
        
        cps_radio = tk.Radiobutton(mode_frame, text="Klicks/s", variable=self.mode_var, value="cps",
                                   command=self.switch_rate_mode,
                                   font=("Consolas", 8, "bold"), fg="#00ff41", bg="#0d0d0d",
                                   activeforeground="#00ff41", activebackground="#0d0d0d",
                                   selectcolor="#1a1a1a")
        cps_radio.pack(side=tk.LEFT, padx=5)
        
        interval_radio = tk.Radiobutton(mode_frame, text="Intervall (s)", variable=self.mode_var, value="interval",
                                        command=self.switch_rate_mode,
                                        font=("Consolas", 8, "bold"), fg="#00ff41", bg="#0d0d0d",
                                        activeforeground="#00ff41", activebackground="#0d0d0d",
                                        selectcolor="#1a1a1a")
        interval_radio.pack(side=tk.LEFT, padx=5)

        # Container für beide Regler
        self.slider_container = tk.Frame(main, bg="#0d0d0d", height=50)
        self.slider_container.pack(pady=2, fill=tk.X)
        self.slider_container.pack_propagate(False)

        # CPS Regler
        self.cps_frame = tk.Frame(self.slider_container, bg="#0d0d0d")
        self.cps_frame.place(x=0, y=0, relwidth=1.0)

        cps_lbl = tk.Label(self.cps_frame, text="Klicks/s:", font=("Consolas", 8, "bold"), fg="#00cc33", bg="#0d0d0d")
        cps_lbl.pack(side=tk.LEFT, padx=(0,4))

        self.cps_var = tk.DoubleVar(value=5.0)
        self.cps_scale = tk.Scale(self.cps_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                                  variable=self.cps_var, resolution=0.5,
                                  font=("Consolas", 7), fg="#00ff41", bg="#0d0d0d",
                                  troughcolor="#1a1a1a", highlightthickness=0,
                                  command=self.update_rate)
        self.cps_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        self.cps_value = tk.Label(self.cps_frame, text="5.0", font=("Consolas", 8, "bold"), fg="#00ff41", bg="#0d0d0d", width=4)
        self.cps_value.pack(side=tk.LEFT, padx=(4,0))

        # Intervall Regler
        self.interval_frame = tk.Frame(self.slider_container, bg="#0d0d0d")

        int_lbl = tk.Label(self.interval_frame, text="Alle X s:", font=("Consolas", 8, "bold"), fg="#00cc33", bg="#0d0d0d")
        int_lbl.pack(side=tk.LEFT, padx=(0,4))

        self.interval_var = tk.DoubleVar(value=1.0)
        self.interval_scale = tk.Scale(self.interval_frame, from_=0.05, to=5.0, orient=tk.HORIZONTAL,
                                       variable=self.interval_var, resolution=0.05,
                                       font=("Consolas", 7), fg="#00ff41", bg="#0d0d0d",
                                       troughcolor="#1a1a1a", highlightthickness=0,
                                       command=self.update_rate)
        self.interval_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        self.interval_value = tk.Label(self.interval_frame, text="1.0", font=("Consolas", 8, "bold"), fg="#00ff41", bg="#0d0d0d", width=4)
        self.interval_value.pack(side=tk.LEFT, padx=(4,0))

        # Delay Threshold
        delay_frame = tk.Frame(main, bg="#0d0d0d")
        delay_frame.pack(pady=2, fill=tk.X)

        delay_lbl = tk.Label(delay_frame, text="Verzögerung (s):", font=("Consolas", 8, "bold"), fg="#00cc33", bg="#0d0d0d")
        delay_lbl.pack(side=tk.LEFT, padx=(0,4))

        self.delay_var = tk.DoubleVar(value=0.0)
        self.delay_scale = tk.Scale(delay_frame, from_=0.0, to=3.0, orient=tk.HORIZONTAL,
                                    variable=self.delay_var, resolution=0.1,
                                    font=("Consolas", 7), fg="#00ff41", bg="#0d0d0d",
                                    troughcolor="#1a1a1a", highlightthickness=0,
                                    command=self.update_delay)
        self.delay_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        self.delay_value = tk.Label(delay_frame, text="0.0", font=("Consolas", 8, "bold"), fg="#00ff41", bg="#0d0d0d", width=4)
        self.delay_value.pack(side=tk.LEFT, padx=(4,0))

        # Hold Mode
        self.hold_btn = tk.Checkbutton(main, text="GEDRÜCKT HALTEN",
                                       command=self.toggle_hold_mode,
                                       font=("Consolas", 8, "bold"), fg="#00ff41", bg="#0d0d0d",
                                       activeforeground="#00ff41", activebackground="#0d0d0d",
                                       selectcolor="#1a1a1a")
        self.hold_btn.pack(pady=2)

        # Flicker Pixels für beide Canvas (JCA: optimierte List-Comprehension)
        self.flicker_pixels_top = [
            self.flicker_top.create_rectangle((i % 30) * 4, (i // 30) * 10, 
                                             (i % 30) * 4 + 4, (i // 30) * 10 + 10, 
                                             fill="#000000", width=0)
            for i in range(60)
        ]

        self.flicker_pixels_button = [
            self.flicker_button.create_rectangle((i % 35) * 4, (i // 35) * 10,
                                                (i % 35) * 4 + 4, (i // 35) * 10 + 10,
                                                fill="#000000", width=0)
            for i in range(98)
        ]

        self.root.deiconify()
        logger.info("BUTONIT 1.0 gestartet")

    def on_close(self):
        """Sauberes Beenden aller Threads und Listener"""
        logger.info("Beende Anwendung...")
        self.running = False
        self.firing = False
        self.listening = False
        self.stop_listeners()
        self.root.quit()
        self.root.destroy()
    
    def cleanup(self):
        """Wird von atexit aufgerufen - letzte Rettung"""
        logger.info("Cleanup wird durchgeführt...")
        self.running = False
        self.firing = False
        self.stop_listeners()

    def switch_rate_mode(self):
        self.rate_mode = self.mode_var.get()
        if self.rate_mode == "cps":
            self.interval_frame.place_forget()
            self.cps_frame.place(x=0, y=0, relwidth=1.0)
        else:
            self.cps_frame.place_forget()
            self.interval_frame.place(x=0, y=0, relwidth=1.0)
        self.update_rate()

    def update_rate(self, event=None):
        if self.rate_mode == "cps":
            rate = self.cps_var.get()
            self.fire_rate = rate
            self.cps_value.config(text=f"{rate:.1f}")
        else:
            interval = self.interval_var.get()
            self.fire_rate = 1.0 / interval if interval > 0 else 20.0
            self.interval_value.config(text=f"{interval:.2f}")

    def update_delay(self, event=None):
        self.delay_threshold = self.delay_var.get()
        self.delay_value.config(text=f"{self.delay_threshold:.1f}")

    def start_flicker(self):
        tones = ["#001100", "#003300", "#005500", "#007700"]
        def flick():
            if not self.firing:
                return
            for px in self.flicker_pixels_top:
                self.flicker_top.itemconfig(px, fill=random.choice(tones))
            for px in self.flicker_pixels_button:
                self.flicker_button.itemconfig(px, fill=random.choice(tones))
            self.root.after(FLICK_INTERVAL_MS, flick)  # JCA: Verwendet Konstante
        flick()

    def stop_flicker(self):
        for px in self.flicker_pixels_top:
            self.flicker_top.itemconfig(px, fill="#000000")
        for px in self.flicker_pixels_button:
            self.flicker_button.itemconfig(px, fill="#000000")
    
    def start_key_selection(self):
        if self.listening:
            return
        
        self.listening = True
        with self.combo_lock:  # Thread-safe (Punkt 8)
            self.combo_actions = []
        
        self.select_btn.config(text="RECORDING...", bg="#00ff41", fg="#0d0d0d", state='disabled')
        self.key_label.config(text="3 SEK RECORDING...", fg="#00ff41")
        
        start_time = time.time()
        recorded_keys = []
        recording_active = True
        
        def on_key_press(key):
            if recording_active:
                timestamp = time.time() - start_time
                try:
                    key_name = key.char if hasattr(key, 'char') and key.char else str(key).replace('Key.', '')
                except:
                    key_name = str(key).replace('Key.', '')
                
                with self.combo_lock:  # Thread-safe (Punkt 8)
                    self.combo_actions.append(('key', key, timestamp))
                recorded_keys.append(key_name.upper())
            return True
        
        def on_mouse_click(x, y, button, pressed):
            if recording_active and pressed:
                timestamp = time.time() - start_time
                btn_name = "LEFT" if button == mouse.Button.left else ("RIGHT" if button == mouse.Button.right else "MIDDLE")
                
                with self.combo_lock:  # Thread-safe (Punkt 8)
                    self.combo_actions.append(('mouse', button, timestamp))
                recorded_keys.append(f"M-{btn_name}")
            return True
        
        def finish_recording():
            nonlocal recording_active
            recording_active = False
            self.listening = False
            
            self.stop_listeners()
            
            # FINAL: Entferne letzten Mausklick, falls sehr kurz vorher
            with self.combo_lock:  # Thread-safe (Punkt 8)
                if self.combo_actions:
                    last_action = self.combo_actions[-1]
                    if last_action[0] == 'mouse' and (time.time() - start_time - last_action[2]) < 0.3:
                        self.combo_actions.pop()
                        if recorded_keys:
                            recorded_keys.pop()
                        logger.info("Letzter Mausklick entfernt (zu kurz)")
                
                has_combo = len(self.combo_actions) > 0
            
            # Punkt 3 & 9: Thread-sichere GUI-Updates via self.root.after()
            if has_combo:
                combo_str = " + ".join(recorded_keys[:5])
                if len(recorded_keys) > 5:
                    combo_str += "..."
                self.root.after(0, lambda: self.key_label.config(text=f"COMBO: {combo_str}", fg="#00ff41"))
                self.root.after(0, lambda: self.status_label.config(text="COMBOONED!", fg="#00ff41"))
                logger.info(f"Combo aufgenommen: {combo_str}")
            else:
                self.root.after(0, lambda: self.key_label.config(text="[ NO COMBO ]", fg="#ff0000"))
                logger.warning("Keine Combo aufgenommen")
            
            self.root.after(0, lambda: self.select_btn.config(text="Button it!", bg="#1a1a1a", fg="#00ff41", state='normal'))
        
        self.key_listener = keyboard.Listener(on_press=on_key_press)
        self.mouse_listener = mouse.Listener(on_click=on_mouse_click)
        self.key_listener.start()
        self.mouse_listener.start()
        
        threading.Timer(COMBO_RECORD_TIME, finish_recording).start()
    
    def toggle_hold_mode(self):
        self.hold_mode = not self.hold_mode
        logger.info(f"Hold-Mode: {'AN' if self.hold_mode else 'AUS'}")
    
    def hide_window(self):
        self.root.withdraw()
    
    def stop_listeners(self):
        """Zentrale Methode zum Stoppen aller Listener (JCA Vorteil)"""
        if self.key_listener:
            try:
                self.key_listener.stop()
                logger.debug("Key-Listener gestoppt")
            except Exception as e:
                logger.error(f"Fehler beim Stoppen des Key-Listeners: {e}")
            self.key_listener = None
        
        if self.mouse_listener:
            try:
                self.mouse_listener.stop()
                logger.debug("Mouse-Listener gestoppt")
            except Exception as e:
                logger.error(f"Fehler beim Stoppen des Mouse-Listeners: {e}")
            self.mouse_listener = None
    
    def handle_hotkey(self):
        if self.firing:
            self.stop_firing()
        else:
            self.start_firing()
    
    def start_firing(self):
        with self.combo_lock:  # Thread-safe (Punkt 8)
            has_combo = len(self.combo_actions) > 0
        
        if not has_combo:
            self.root.after(0, lambda: self.status_label.config(text="KEINE COMBO!", fg="#ff0000"))
            logger.warning("Start-Firing fehlgeschlagen: Keine Combo vorhanden")
            return
        
        if self.delay_threshold > 0:
            self.root.after(0, lambda: self.status_label.config(text=f"WARTE {self.delay_threshold}s...", fg="#ffaa00"))
            logger.info(f"Warte {self.delay_threshold}s vor Start...")
            time.sleep(self.delay_threshold)
        
        self.firing = True
        self.root.after(0, lambda: self.status_label.config(text="COMBOONING!!!", fg="#00ff41"))
        self.start_flicker()
        logger.info("Firing gestartet")
        
        self.fire_thread = threading.Thread(target=self.fire_loop, daemon=True)
        self.fire_thread.start()
    
    def stop_firing(self):
        self.firing = False
        self.root.after(0, lambda: self.status_label.config(text="STOPPOONED", fg="#00ff41"))
        self.stop_flicker()
        logger.info("Firing gestoppt")
    
    def fire_loop(self):
        if self.hold_mode:
            # JCA: HOLD MODE - Drücke alle Tasten EINMAL und halte sie gedrückt
            pressed_keys = []
            try:
                with self.combo_lock:  # Thread-safe (Punkt 8)
                    actions_copy = list(self.combo_actions)
                
                for action_type, key, _ in actions_copy:
                    if not self.firing:
                        break
                    
                    try:
                        if action_type == 'mouse':
                            self.mouse_controller.press(key)
                        else:
                            self.keyboard_controller.press(key)
                        pressed_keys.append((action_type, key))
                    except Exception as e:
                        logger.error(f"Fehler beim Drücken von {action_type}/{key}: {e}")
                
                logger.info(f"Hold-Mode: {len(pressed_keys)} Tasten gedrückt")
                
                # Warte bis firing gestoppt wird
                while self.firing and self.running:
                    time.sleep(0.1)
                
            finally:
                # Garantiert alle Tasten loslassen
                for action_type, key in pressed_keys:
                    try:
                        if action_type == 'mouse':
                            self.mouse_controller.release(key)
                        else:
                            self.keyboard_controller.release(key)
                    except Exception as e:
                        logger.error(f"Fehler beim Loslassen von {action_type}/{key}: {e}")
                logger.info("Hold-Mode: Alle Tasten losgelassen")
        else:
            # NORMAL MODE: Wiederhole die Combo mit Dauerfeuer
            interval = 1.0 / self.fire_rate  # JCA: Klares Timing
            while self.firing and self.running:
                try:
                    with self.combo_lock:  # Thread-safe (Punkt 8)
                        actions_copy = list(self.combo_actions)
                    
                    for action_type, key, _ in actions_copy:
                        if not self.firing:
                            break
                        
                        try:
                            if action_type == 'mouse':
                                self.mouse_controller.click(key)
                            else:
                                self.keyboard_controller.press(key)
                                self.keyboard_controller.release(key)
                        except Exception as e:
                            logger.error(f"Fehler beim Ausführen von {action_type}/{key}: {e}")
                    
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Fehler in fire_loop: {e}")
                    self.firing = False
    
    def stop(self):
        self.running = False
        self.firing = False
        self.stop_listeners()
        self.root.quit()

app = AutoFireGUI()

def on_activate():
    if app.running:
        app.handle_hotkey()

hotkey_listener = None

def start_listener():
    global hotkey_listener
    hotkey_listener = keyboard.GlobalHotKeys({"<alt>+^": on_activate, "<alt_gr>+^": on_activate})
    with hotkey_listener:
        hotkey_listener.join()

hotkey_thread = threading.Thread(target=start_listener, daemon=True)
hotkey_thread.start()

try:
    app.root.mainloop()
except KeyboardInterrupt:
    app.on_close()
finally:
    if hotkey_listener:
        try:
            hotkey_listener.stop()
            logger.info("Hotkey-Listener gestoppt")
        except Exception as e:
            logger.error(f"Fehler beim Stoppen des Hotkey-Listeners: {e}")

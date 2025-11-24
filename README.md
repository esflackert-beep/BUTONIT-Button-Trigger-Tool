# BUTONIT! 🎮⚡

**Tastenkombinationen automatisieren mit Dauerfeuer**

BUTONIT ist ein Desktop-Tool für Windows, das es ermöglicht, Tastenkombinationen und Mausklicks zu automatisieren und mit einstellbarem Dauerfeuer zu versehen. Ideal für Roguelite-Games und repetitive Tasks.

---

## 📦 Versionen

### BUTONIT 1.0 (Vollversion)
**Datei:** `BUTONIT_1.0.py`

**Features:**
- ✨ **Multi-Key-Combo Recording:** Nimmt 3 Sekunden lang alle gedrückten Tasten und Mausklicks auf
- 🎯 Kombinationen aus Tastatur + Maus möglich
- 🔥 Automatisches Dauerfeuer mit einstellbarer Rate
- ⚙️ Zwei Modi: Klicks/Sekunde oder Intervall-Modus
- ⏱️ Einstellbare Verzögerung vor Start
- 🔒 "Gedrückt Halten"-Modus für dauerhafte Tastenaktivierung
- 🎨 Retro-GUI mit Matrix-Style Flicker-Effekten
- 🔑 Hotkey: `Alt+^` oder `AltGr+^` zum Start/Stop

### BUTONIT MINI
**Datei:** `BUTONIT_MINI.py`

**Features:**
- 🎯 **Single-Key Recording:** Einfache Aufnahme einer einzelnen Taste oder eines Mausklicks
- 🔥 Dauerfeuer mit einstellbarer Rate (1-20 Klicks/s)
- ⏱️ Verzögerungsfunktion
- 🔒 "Gedrückt Halten"-Modus
- 🎨 Kompakte GUI
- 🔑 Hotkey: `Alt+^` oder `AltGr+^` zum Start/Stop

---

## 📥 Download

### Fertige .exe Dateien (kein Python nötig!)
- **[BUTONIT_1.0.exe](https://github.com/esflackert-beep/BUTONIT-Button-Trigger-Tool/raw/main/BUTONIT_1.0.exe)** - Vollversion mit Multi-Key-Combos
- **[BUTONIT_MINI.exe](https://github.com/esflackert-beep/BUTONIT-Button-Trigger-Tool/raw/main/BUTONIT_MINI.exe)** - Einfache Single-Key-Version

Einfach herunterladen und starten - keine Installation nötig! ✨

---

## 🚀 Installation (für Python-Version)

### Voraussetzungen
```bash
pip install pynput
```

### Verwendung
```bash
python BUTONIT_1.0.py
# oder
python BUTONIT_MINI.py
```

---

## 🎮 Bedienung

### BUTONIT 1.0 (Multi-Combo)
1. **"Button it!" klicken** - Startet 3-Sekunden-Recording
2. **Während der Aufnahme:** Alle gewünschten Tasten/Mausklicks drücken
3. **Wartezeit einstellen** (optional): 0-3 Sekunden Verzögerung vor Start
4. **Rate anpassen:**
   - **Klicks/s-Modus:** 1-20 Klicks pro Sekunde
   - **Intervall-Modus:** Ausführung alle X Sekunden (0.05-5s)
5. **"Gedrückt Halten"** aktivieren (optional): Hält Tasten dauerhaft gedrückt
6. **`Alt+^` drücken:** Startet/Stoppt das Dauerfeuer

### BUTONIT MINI (Single-Key)
1. **"[ BUTTON ]" klicken** - Aktiviert Aufnahme
2. **Eine Taste oder Maustaste drücken**
3. **Parameter wie oben einstellen**
4. **`Alt+^` drücken:** Startet/Stoppt das Dauerfeuer

---

## 🛠️ Technische Details

### Features
- **Thread-sichere Implementierung** mit Locks
- **Automatisches Cleanup** bei Beenden (atexit)
- **Logging-System** für Debugging
- **GUI bleibt immer im Vordergrund** (topmost)
- **Minimierbar** statt schließbar (läuft weiter im Hintergrund)

### Tastenkürzel
| Tastenkombination | Funktion |
|-------------------|----------|
| `Alt + ^` | Dauerfeuer Start/Stop |
| `AltGr + ^` | Alternative zum Start/Stop |

### Modi

#### Klicks/Sekunde (CPS)
- Direkte Angabe der Ausführungsrate
- 1-20 Klicks pro Sekunde
- Ideal für schnelle Wiederholungen

#### Intervall-Modus
- Ausführung in festen Zeitabständen
- 0.05-5 Sekunden Intervall
- Präziser für langsame Wiederholungen

#### Gedrückt Halten-Modus
- Drückt Tasten/Mausbuttons dauerhaft
- Ideal für Fähigkeiten mit "Gedrückt halten"-Mechanik
- Garantiertes Loslassen beim Stop

---

## 💡 Anwendungsbeispiele

### Gaming
- **Roguelites:** Auto-Fire für Schusswaffen
- **RPGs:** Automatisches Sammeln/Looten
- **MMOs:** Crafting-Makros
- **Idle Games:** Auto-Click

### Produktivität
- **Repetitive Tasks:** Automatisierte Klicksequenzen
- **Testing:** Automatisierte UI-Tests
- **Data Entry:** Schnelleres Ausfüllen von Formularen

---

## ⚠️ Wichtige Hinweise

- **Online-Games:** Prüfen Sie die Nutzungsbedingungen - Automatisierung kann gegen die AGB verstoßen!
- **Anti-Cheat:** Einige Spiele erkennen und blockieren Automatisierungs-Tools
- **Verantwortung:** Nutzen Sie das Tool nur in erlaubten Kontexten

---

## 🔧 Systemanforderungen

- **OS:** Windows (getestet auf Windows 10/11)
- **Python:** 3.7+
- **Dependencies:** pynput, tkinter (meist vorinstalliert)

---

## 📝 Lizenz

Dieses Projekt ist Open Source. Nutzen Sie es auf eigene Verantwortung.

---

## 🐛 Bekannte Probleme / ToDo

- [ ] Linux/macOS Support
- [ ] Speichern/Laden von Combos
- [ ] Profile für verschiedene Spiele
- [ ] Einstellbare Hotkeys

---

## 👨‍💻 Entwickler

Entwickelt mit ❤️ für die Gaming-Community

---

## 🙏 Credits

- **pynput** - Für Keyboard/Mouse-Control
- **tkinter** - Für die GUI

---

**BUTONIT - Button It Like You Mean It!** 🚀

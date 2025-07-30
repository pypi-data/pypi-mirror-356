# Dikshant - Windows Voice Assistant

**Dikshant** is a lightweight background voice assistant for Windows that activates on the phrase **"hey friend"**. It performs system-level tasks like opening applications, adjusting volume, creating files/folders, and browsing the internet — all using voice commands.

---

## 🔥 Features

- 🎙️ Wake-word activation with **"hey friend"**
- 🖥️ Opens apps like Notepad, Calculator, Chrome, etc.
- 🌐 Opens websites or performs **Google searches**
- 🔊 Adjusts volume (mute/increase/decrease)
- 🗃️ Creates folders or files on Desktop
- 💻 Shuts down your system on command
- 🔁 Runs continuously in the background
- 📦 Easy to install via `pip`

---

## 🗣️ Supported Example Commands

All commands must begin with `hey friend`

| Command | Action |
|--------|--------|
| hey friend open notepad | Opens Notepad |
| hey friend visit google.com | Opens Google in browser |
| hey friend google search for machine learning | Searches Google |
| hey friend increase volume | Increases system volume |
| hey friend create folder | Creates folder on Desktop |
| hey friend create file | Creates file on Desktop |
| hey friend take rest | Shuts down assistant |

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install dikshant
```

> If `pyaudio` fails to install on Windows, use:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 🚀 Usage

After installation, run this in terminal:

```bash
dikshant
```

Then speak commands like:

- **"Hey friend, open notepad"**
- **"Hey friend, take rest"** *(to stop)*

---

## 🧑‍💻 Programmatic Use

```python
from dikshant import Dikshant

assistant = Dikshant()
assistant.start()
```

---

## 🛠 Requirements

Installed automatically, but include:

- `speechrecognition`
- `pyaudio`
- `pyttsx3`
- `pyautogui`

---

## 📃 License

Licensed under the **MIT License**.

---

## 👨‍💻 Author

**Dikshant Ghimire**  
[GitHub](https://github.com/dikshantgh) | [Email](mailto:dikkughimire@gmail.com)

---

## 🤝 Contribute

Pull requests, issues, and suggestions are welcome!  
Please follow best practices and format your code.

---

## 🧪 Future Plans

- Linux and Mac support
- AI/NLU integration
- GUI interface

# Dikshant - Windows Voice Assistant

**Dikshant** is a lightweight background voice assistant for Windows that activates on the phrase **"hey friend"**. It can perform system-level tasks like opening applications, shutting down, or executing custom commands — all using natural language.

---

## 🔥 Features

- 🎙️ Wake-word activation with **"hey friend"**
- 🖥️ Executes system commands (e.g., open apps, shutdown)
- 🧠 Understands natural language instructions
- 🔁 Runs in the background after launch
- 📦 Easy to install via `pip`

---

## Supported Commands (v0.1.0)
(All require wake phrase: "Hey friend")

1. Application Control
"Hey friend open notepad"

"Hey friend launch chrome"

"Hey friend start calculator"

2. Website Navigation
"Hey friend open youtube" → Opens YouTube in default browser

"Hey friend visit google" → Opens Google

"Hey friend go to github" → Opens GitHub

3. Assistant Control
"Hey friend take rest" → Stops the assistant

"Hey friend go to sleep" → Alternative stop command

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install dikshant
```

---

## 🚀 Usage

After installation, launch it from the terminal:

```bash
dikshant
```

Then simply speak commands like:

- **"Hey friend, open notepad"**
- **"Hey friend, take rest"** *(to stop the assistant)*

---


## 🛠 Requirements

Most dependencies will be auto-installed via `pip`, but core ones may include:

- `speechrecognition`
- `pyaudio` (may need manual install for Windows)
- `pyttsx3`
- `pywin32`

> 💡 If `pyaudio` fails during install, use:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 📃 License

This project is licensed under the **MIT License**.

---

## 🙋‍♂️ Author

**Dikshant Ghimire**  
Feel free to customize and extend!

---

## 💬 Contributions

Pull requests, issues, and suggestions are welcome!  
Please ensure you follow best practices and lint your code.

---

## 🧪 Coming Soon

- Cross-platform support (Linux/Mac)
- GUI interface
- Integration with AI-based NLU
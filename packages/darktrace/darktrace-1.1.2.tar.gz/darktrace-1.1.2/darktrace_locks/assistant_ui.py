# darktrace_locks/assistant_ui.py

import tkinter as tk
from tkinter import scrolledtext
from darktrace_locks.ai_assistant import ask_anuj
import threading
import keyboard

class AssistantUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Anuj - AI Assistant")
        self.root.configure(bg="#0f0f0f")
        self.root.geometry("400x250+1000+50")
        self.root.attributes('-topmost', True)

        self.visible = True
        self.current_lang = "en"

        # Header
        self.header = tk.Label(self.root, text="🧠 Anuj", fg="#00FF41", bg="#0f0f0f", font=("Consolas", 16, "bold"))
        self.header.pack(pady=5)

        # Chat display
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=48, height=8, bg="black", fg="#00FF41", insertbackground="#00FF41", font=("Consolas", 10))
        self.chat_area.pack(padx=10)
        self.chat_area.configure(state='disabled')

        # Input field
        self.input_field = tk.Entry(self.root, width=35, bg="#1a1a1a", fg="white", insertbackground="white", font=("Consolas", 10))
        self.input_field.pack(pady=5, padx=10, side=tk.LEFT, expand=True, fill=tk.X)
        self.input_field.bind("<Return>", self.send_input)

        # Language switcher
        self.lang_button = tk.Button(self.root, text="🌐", command=self.toggle_lang, bg="#1a1a1a", fg="white", font=("Consolas", 10))
        self.lang_button.pack(pady=5, padx=5, side=tk.RIGHT)

        # Keyboard shortcut
        keyboard.add_hotkey("ctrl+a", self.toggle_visibility)

        # Startup info
        self.add_to_chat("🔒 Press CTRL+A to toggle Anuj\n🌍 Language: English\n")

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self.root.mainloop()

    def toggle_visibility(self):
        self.visible = not self.visible
        self.root.attributes('-topmost', self.visible)
        self.root.withdraw() if not self.visible else self.root.deiconify()

    def toggle_lang(self):
        self.current_lang = "or" if self.current_lang == "en" else "en"
        lang_name = "Odia" if self.current_lang == "or" else "English"
        self.add_to_chat(f"🌍 Language switched to {lang_name}")

    def send_input(self, event):
        query = self.input_field.get().strip()
        self.input_field.delete(0, tk.END)
        if query:
            self.add_to_chat(f"> You: {query}")
            threading.Thread(target=self.get_response, args=(query,), daemon=True).start()

    def get_response(self, query):
        response = ask_anuj(query, self.current_lang)
        self.add_to_chat(f"🤖 Anuj: {response}")

    def add_to_chat(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)


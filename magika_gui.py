import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import threading
import re


class MagikaGUI:
    def __init__(self, root):
        self.root = root
        root.title("Magika GUI by EryriLabs")
        
        #Attempt to set the icon
        try:
            root.iconbitmap('Icon.ico')
        except Exception as e:
            print(e)

        # File selection frame
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.file_entry = tk.Entry(self.file_frame, state='disabled', width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.browse_button = tk.Button(self.file_frame, text="Browse", command=self.browse_files)
        self.browse_button.pack(side=tk.RIGHT, padx=5)

        self.browse_folder_button = tk.Button(self.file_frame, text="Browse Folder", command=self.browse_folder)
        self.browse_folder_button.pack(side=tk.RIGHT)

        # Options frame
        self.options_frame = tk.LabelFrame(root, text="Options", padx=10, pady=5)
        self.options_frame.pack(fill=tk.X, padx=10, pady=5)

        self.recursive_var = tk.BooleanVar()
        self.recursive_check = tk.Checkbutton(self.options_frame, text="Recursive", variable=self.recursive_var)
        self.recursive_check.grid(row=0, column=0, sticky="w")

        self.json_var = tk.BooleanVar()
        self.json_check = tk.Checkbutton(self.options_frame, text="JSON", variable=self.json_var)
        self.json_check.grid(row=0, column=1, sticky="w")

        self.jsonl_var = tk.BooleanVar()
        self.jsonl_check = tk.Checkbutton(self.options_frame, text="JSONL", variable=self.jsonl_var)
        self.jsonl_check.grid(row=0, column=2, sticky="w")

        self.mime_type_var = tk.BooleanVar()
        self.mime_type_check = tk.Checkbutton(self.options_frame, text="MIME Type", variable=self.mime_type_var)
        self.mime_type_check.grid(row=1, column=0, sticky="w")

        self.label_output_var = tk.BooleanVar()
        self.label_output_check = tk.Checkbutton(self.options_frame, text="Label", variable=self.label_output_var)
        self.label_output_check.grid(row=1, column=1, sticky="w")

        self.compat_mode_var = tk.BooleanVar()
        self.compat_mode_check = tk.Checkbutton(self.options_frame, text="Compatibility Mode", variable=self.compat_mode_var)
        self.compat_mode_check.grid(row=1, column=2, sticky="w")

        self.output_score_var = tk.BooleanVar()
        self.output_score_check = tk.Checkbutton(self.options_frame, text="Output Score", variable=self.output_score_var)
        self.output_score_check.grid(row=2, column=0, sticky="w")

        self.prediction_mode_var = tk.StringVar()
        self.prediction_mode_label = tk.Label(self.options_frame, text="Prediction Mode:")
        self.prediction_mode_label.grid(row=2, column=1, sticky="w")
        self.prediction_mode_combo = ttk.Combobox(self.options_frame, textvariable=self.prediction_mode_var, values=["best-guess", "medium-confidence", "high-confidence"], state="readonly")
        self.prediction_mode_combo.grid(row=2, column=2, sticky="w")

        # Run button
        self.run_button = tk.Button(root, text="Run Magika", command=self.run_magika)
        self.run_button.pack(pady=5)

        # Save Output button
        self.save_button = tk.Button(root, text="Save Output", command=self.save_output)
        self.save_button.pack(pady=5)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(root, height=15)
        self.output_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    def browse_files(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.file_entry.config(state='disabled')

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, folder_path)
            self.file_entry.config(state='disabled')

    def run_magika(self):
        self.output_text.delete(1.0, tk.END)
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a file or directory.")
            return

        command = ["magika", file_path] + self.build_command_options()
        threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()

    def build_command_options(self):
        options = []
        if self.recursive_var.get():
            options.append("--recursive")
        if self.json_var.get():
            options.append("--json")
        if self.jsonl_var.get():
            options.append("--jsonl")
        if self.mime_type_var.get():
            options.append("--mime-type")
        if self.label_output_var.get():
            options.append("--label")
        if self.compat_mode_var.get():
            options.append("--compatibility-mode")
        if self.output_score_var.get():
            options.append("--output-score")
        if self.prediction_mode_var.get():
            options += ["--prediction-mode", self.prediction_mode_var.get()]
        return options

    def execute_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        clean_output = self.strip_ansi_codes(output)
        self.output_text.insert(tk.END, clean_output)
        if error:
            clean_error = self.strip_ansi_codes(error)
            self.output_text.insert(tk.END, clean_error)

    def save_output(self):
        if self.json_var.get():
            default_ext = ".json"
            file_types = [("JSON files", "*.json"), ("All files", "*.*")]
        elif self.jsonl_var.get():
            default_ext = ".jsonl"
            file_types = [("JSONL files", "*.jsonl"), ("All files", "*.*")]
        else:
            default_ext = ".txt"
            file_types = [("Text files", "*.txt"), ("All files", "*.*")]

        file_path = filedialog.asksaveasfilename(defaultextension=default_ext, filetypes=file_types)
        if not file_path:
            return

        output_text = self.output_text.get(1.0, tk.END)
        try:
            with open(file_path, 'w') as file:
                file.write(output_text)
            messagebox.showinfo("Save Output", "Output saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Output", f"Failed to save file: {e}")

    @staticmethod
    def strip_ansi_codes(text):
        ansi_escape_pattern = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
        return ansi_escape_pattern.sub('', text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MagikaGUI(root)
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import shutil
import subprocess
from tkinter import ttk

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("File to EXE Converter")
        
        # Create label for file name
        self.file_label = tk.Label(self.master, text="No file selected.")
        self.file_label.pack(pady=10)
        
        # Create button to choose file
        self.choose_button = tk.Button(self.master, text="Choose File", command=self.choose_file)
        self.choose_button.pack(pady=10)
        
        # Create button to convert file
        self.convert_button = tk.Button(self.master, text="Convert to EXE", state=tk.DISABLED, command=self.convert_file)
        self.convert_button.pack(pady=10)
        
        # Create scrollable text box for output
        self.text_box = tk.Text(self.master, height=10)
        self.text_box.pack(pady=10)
        
        # Create button to copy output
        self.copy_output_button = tk.Button(self.master, text="Copy Terminal Output", state=tk.DISABLED, command=self.copy_output)
        self.copy_output_button.pack(pady=10)

        # Create button to open output directory
        self.open_output_button = tk.Button(self.master, text="Open Output Directory", state=tk.DISABLED, command=self.open_output_dir)
        self.open_output_button.pack(pady=10)
        
    def copy_output(self):
        # Copy the contents of the text box to the clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(self.text_box.get("1.0", tk.END))
        
    def open_output_dir(self):
        # Get output directory path
        output_dir = os.path.join(os.getcwd(), "dist")
        
        # Open output directory in file explorer
        if sys.platform == "win32":
            os.startfile(output_dir)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", output_dir])
        else:
            subprocess.Popen(["xdg-open", output_dir])


    def choose_file(self):
        # Open file dialog to select file
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Python files", "*.py")])
        
        if file_path:
            # Update file label with selected file
            self.file_label.config(text="Selected file: {}".format(file_path))
            
            # Enable convert button
            self.convert_button.config(state=tk.NORMAL)
        else:
            # Disable convert button
            self.convert_button.config(state=tk.DISABLED)
        
    def convert_file(self):
        # Get selected file path
        file_path = self.file_label.cget("text").split(": ")[-1]
        
        # Create output directory
        output_dir = "dist"
        os.makedirs(output_dir, exist_ok=True)
        
        # Get PyInstaller options
        options = [
            "--name=myapp",
            "--onefile",
            "--windowed",
            "--icon=my_icon.ico",
            "--clean",
            "--distpath={}".format(output_dir),
            file_path
        ]
        
        # Disable choose and convert buttons
        self.choose_button.config(state=tk.DISABLED)
        self.convert_button.config(state=tk.DISABLED)
        
        # Clear text box
        self.text_box.delete("1.0", tk.END)
        
        # Call PyInstaller using subprocess and redirect output to text box
        process = subprocess.Popen(["pyinstaller"] + options, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        for line in process.stdout:
            self.text_box.insert(tk.END, line)
            self.text_box.see(tk.END)
            self.master.update()
        
        # Enable choose button
        self.choose_button.config(state=tk.NORMAL)
        
        # Get executable path
        executable_path = os.path.join(output_dir, "myapp.exe")
        
        if os.path.exists(executable_path):
            # Display success message
            messagebox.showinfo("Success", "File converted to executable.")
        else:
            # Display error message
            messagebox.showerror("Error", "Failed to convert file to executable.")

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    app = App(root)
    
    # Set window size and position
    root.geometry("400x300+100+100")
    
    # Set window icon
    if sys.platform == "win32":
        root.iconbitmap("my_icon.ico")
    
    # Set window title
    root.title("File to EXE Converter")
    
    # Enable resizing of window
    root.resizable(True, True)
    
    # Run main loop
    root.mainloop()
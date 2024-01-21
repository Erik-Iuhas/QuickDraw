import os
import sys
import random
import tkinter as tk
import json
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from image_session import ImageSession

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickDraw")
        self.directories = []
        self.display_time = 30  # Default time in seconds
        self.setup_ui()

    def setup_ui(self):
        # Session Name Entry
        tk.Label(self.root, text="Session:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.session_name_entry = tk.Entry(self.root)
        self.session_name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='we')
        self.session_name_entry.insert(0,"Select_Title")

        # Listbox for directories with scrollbar
        self.directory_listbox = tk.Listbox(self.root)
        self.directory_listbox.grid(row=1, column=0, rowspan=4, padx=5, pady=5, sticky='nswe')
        scrollbar = tk.Scrollbar(self.root, orient='vertical', command=self.directory_listbox.yview)
        scrollbar.grid(row=1, column=1, rowspan=4, sticky='ns')
        self.directory_listbox['yscrollcommand'] = scrollbar.set

        # '+' and '-' buttons
        add_button = tk.Button(self.root, text='+', command=self.add_directory)
        add_button.grid(row=1, column=2, padx=5, pady=5)
        remove_button = tk.Button(self.root, text='-', command=self.remove_directory)
        remove_button.grid(row=2, column=2, padx=5, pady=5)

        # 'Save' and 'Load' buttons
        save_button = tk.Button(self.root, text='Save', command=self.save_session)
        save_button.grid(row=3, column=2, padx=5, pady=5)
        load_button = tk.Button(self.root, text='Load', command=self.load_session)
        load_button.grid(row=4, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Time (seconds):").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.time_entry = tk.Entry(self.root)
        self.time_entry.grid(row=5, column=1, padx=5, pady=5, sticky='we')
        self.time_entry.insert(0, "30")  # Default value for time

        # Dimension Entries
        tk.Label(self.root, text="Dimensions:").grid(row=6, column=0, padx=0, pady=5, sticky='w')
        tk.Label(self.root, text="width=").grid(row=6, column=1, sticky='e')
        self.width_entry = tk.Entry(self.root, width=5)
        self.width_entry.grid(row=6, column=2)
        self.width_entry.insert(0, "800")
        tk.Label(self.root, text="height=").grid(row=6, column=3, sticky='e')
        self.height_entry = tk.Entry(self.root, width=5)
        self.height_entry.grid(row=6, column=4, padx=(0,0))
        self.height_entry.insert(0, "600")

        # Start Session Button
        start_session_button = tk.Button(self.root, text="Start Session", command=self.start_session)
        start_session_button.grid(row=7, column=0, columnspan=3, padx=5, pady=20, sticky='we')
        

        # Configure the grid expansion behavior
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def add_directory(self):
        directory = filedialog.askdirectory()
        if directory and directory not in self.directories:
            self.directories.append(directory)
            self.directory_listbox.insert(tk.END, os.path.basename(directory))

    def remove_directory(self):
        selected_index = self.directory_listbox.curselection()
        if selected_index:
            self.directories.pop(selected_index[0])
            self.directory_listbox.delete(selected_index[0])

    def save_session(self):
        session_name = self.session_name_entry.get()
        self.display_time = int(self.time_entry.get())
        session_data = {
            'session_name': session_name,
            'directories': self.directories,
            'display_time': self.display_time
        }
        
        try:
            os.mkdir("Sessions")
        except:
            print("Dir Exists")

        with open(os.path.join("Sessions",f'{session_name}.json'), 'w') as file:
            json.dump(session_data, file)
        messagebox.showinfo("Session Saved", "Session configuration saved successfully.")

    def load_session(self):
        session_name = filedialog.askopenfilename(defaultextension=".json",
                                                  filetypes=[("JSON Files", "*.json")])
        if session_name:
            with open(session_name, 'r') as file:
                session_data = json.load(file)
            self.session_name_entry.delete(0, tk.END)
            self.session_name_entry.insert(0, os.path.splitext(os.path.basename(session_name))[0])
            self.directories = session_data.get('directories', [])
            self.display_time = session_data.get('display_time', 30)
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, str(self.display_time))
            self.directory_listbox.delete(0, tk.END)
            for directory in self.directories:
                self.directory_listbox.insert(tk.END, os.path.basename(directory))
            messagebox.showinfo("Session Loaded", "Session configuration loaded successfully.")


    def start_session(self):
        time_seconds = int(self.time_entry.get())
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())

        image_paths = []
        for directory in self.directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        image_paths.append(os.path.join(root, file))
        if image_paths:
            session = ImageSession(image_paths, self.display_time,session_name=self.session_name_entry.get(),window_size=(width, height))
            session.start_session()
        else:
            messagebox.showerror("Error", "No images found in the specified directories.")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

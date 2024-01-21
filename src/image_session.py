import tkinter as tk
import random 
from PIL import Image, ImageTk
import json
import os
import time

class ImageSession:
    def __init__(self, image_paths, display_time,session_name="default", window_size=(800, 600), valid_time_threshold=15):
        self.image_paths = image_paths
        random.shuffle(self.image_paths)
        self.session_name = session_name
        self.display_time = display_time
        self.window_size = window_size
        self.total_time_spent = 0
        self.valid_time_threshold = valid_time_threshold
        self.session_data = {}
        self.completed_count = 0
        self.current_index = 0
        self.remaining_time = self.display_time
        self.paused = False
        self.timer_job = None  # Initialize a variable to store the scheduled job
        self.start_time = None   
        self.session_start_time = time.strftime("%Y%m%d-%H%M%S")  # Format the current time
        self.valid_time = False
        
        self.log_directory = "Log"
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def start_session(self):
        self.window = tk.Toplevel()
        self.window.title("Image Viewer Session")


        control_frame = tk.Frame(self.window)
        control_frame.pack(fill=tk.X)

        back_button = tk.Button(control_frame, text="<< Back", command=self.prev_image)
        back_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(control_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT)

        forward_button = tk.Button(control_frame, text="Forward >>", command=self.next_image)
        forward_button.pack(side=tk.LEFT)

        self.time_label = tk.Label(control_frame, text=self.format_time(self.display_time))
        self.time_label.pack(side=tk.RIGHT)

        self.completed_label = tk.Label(control_frame, text=f"Completed: {self.completed_count}")
        self.completed_label.pack(side=tk.LEFT)


        self.canvas = tk.Canvas(self.window, width=self.window_size[0], height=self.window_size[1])
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.update_image()
        self.update_timer()

    def update_image(self):
        if self.current_index < len(self.image_paths):
            self.start_time = time.time()
            self.valid_time = False
            # Load and display the new image
            self.display_image(self.image_paths[self.current_index])
        else:
            self.window.destroy()

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((self.window_size[0], self.window_size[1]), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.window_size[0] // 2, self.window_size[1] // 2, image=photo, anchor=tk.CENTER)
        self.canvas.image = photo

        self.completed_label.config(text=f"Completed: {self.completed_count}")
        self.start_time = time.time()
        self.valid_time = False

    def update_timer(self):
        if self.timer_job:
            self.window.after_cancel(self.timer_job)  # Cancel the previous timer job

        if not self.paused and self.remaining_time > 0:
            self.remaining_time -= 1
            self.time_label.config(text=f"{self.remaining_time} seconds")
            self.timer_job = self.window.after(1000, self.update_timer)
        elif self.remaining_time <= 0:
            self.valid_time = True
            self.next_image()

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def update_session_data(self, time_spent):
        current_image = self.image_paths[self.current_index]
        rounded_time = round(time_spent)
        if current_image not in self.session_data:
            self.session_data[current_image] = []
        self.session_data[current_image].append(rounded_time)
        self.total_time_spent += rounded_time

        # Save the session data with total time spent
        self.session_data["Total_Time_Spent"] = self.total_time_spent
        filename = os.path.join(self.log_directory, f"{self.session_name}_{self.session_start_time}.json")
        with open(filename, 'w') as file:
            json.dump(self.session_data, file)


    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.update_timer()

    def next_image(self):
        time_spent = time.time() - self.start_time if self.start_time else 0
        if time_spent >= self.valid_time_threshold:
            self.valid_time = True
        if self.valid_time:
            self.completed_count += 1
            self.update_session_data(time_spent)
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
        else:
            self.current_index = 0  # Loop back to the first image
        self.reset_timer()
        self.update_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = len(self.image_paths) - 1
        self.reset_timer()
        self.update_image()

    def reset_timer(self):
        self.remaining_time = self.display_time
        self.update_timer()

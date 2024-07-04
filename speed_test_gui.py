import tkinter as tk
import speedtest
import threading
import math

class SpeedTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Internet Speed Test")
        master.geometry("400x400")

        self.canvas = tk.Canvas(master, width=300, height=400)
        self.canvas.pack(pady=20)

        self.draw_dial()

        self.speed_label = tk.Label(master, text="0 Mbps", font=("Arial", 16))
        self.speed_label.pack()

        self.download_label = tk.Label(master, text="Download: -- Mbps", font=("Arial", 12))
        self.download_label.pack()

        self.upload_label = tk.Label(master, text="Upload: -- Mbps", font=("Arial", 12))
        self.upload_label.pack()

        self.start_button = tk.Button(master, text="Start Test", command=self.start_test)
        self.start_button.pack(pady=10)

    def draw_dial(self):
        # Draw the semicircle
        self.canvas.create_arc(10, 10, 290, 290, start=0, extent=180, fill="lightgray")
        
        # Draw the scale
        for i in range(0, 101, 10):
            angle = i * math.pi / 100
            x = 150 - 140 * math.cos(angle)
            y = 150 - 140 * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 8))

        # Create the needle
        self.needle = self.canvas.create_line(180, 150, 180, 10, width=5, fill="red")

    def set_speed(self, speed):
        # Update the needle position
        angle = min(speed, 100) * math.pi / 100
        x = 150 - 140 * math.cos(angle)
        y = 150 - 140 * math.sin(angle)
        self.canvas.coords(self.needle, 150, 150, x, y)
        
        # Update the speed label
        self.speed_label.config(text=f"{speed:.2f} Mbps")

    def start_test(self):
        self.start_button.config(state=tk.DISABLED)
        self.download_label.config(text="Download: Testing...")
        self.upload_label.config(text="Upload: Waiting...")
        thread = threading.Thread(target=self.run_test)
        thread.start()

    def run_test(self):
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # Test and update download speed
        self.master.after(0, self.speed_label.config, {"text": "Testing Download..."})
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        self.master.after(0, self.set_speed, download_speed)
        self.master.after(0, self.download_label.config, {"text": f"Download: {download_speed:.2f} Mbps"})
        
        # Test and update upload speed
        self.master.after(0, self.speed_label.config, {"text": "Testing Upload..."})
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        self.master.after(0, self.set_speed, upload_speed)
        self.master.after(0, self.upload_label.config, {"text": f"Upload: {upload_speed:.2f} Mbps"})

        # Re-enable the start button
        self.master.after(0, self.start_button.config, {"state": tk.NORMAL})
        self.master.after(0, self.speed_label.config, {"text": "Test Completed"})

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()
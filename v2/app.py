import os
import threading
import time
import tkinter as tk
from tkinter import messagebox


class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Checker")
        self.is_pinging = False

        # Input field
        self.url_label = tk.Label(root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.pack()

        # Buttons
        self.start_button = tk.Button(
            root, text="Check Ping", command=self.start_pinging)
        self.start_button.pack()
        self.stop_button = tk.Button(
            root, text="Stop Checking", command=self.stop_pinging)
        self.stop_button.pack()

        # Output display
        self.output_label = tk.Label(root, text="", fg="blue")
        self.output_label.pack()

    def start_pinging(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return

        self.is_pinging = True
        self.output_label.config(text=f"Pinging {url}...")
        threading.Thread(target=self.ping_url,
                         args=(url,), daemon=True).start()

    def ping_url(self, url):
        while self.is_pinging:
            response = os.popen(f"ping -n 1 {url}").read()
            # response_tmp = os.system(f"ping -n 1 {url}")
            latency = ""
            if "Average" in response:
                # self.output_label.config(text=f"{url} is reachable")
                print(response)
                latency = response.split("Average=")[-1].split("ms")[0].strip()

                self.output_label.config(
                    text=f"Ping Output: {url} is reachable, Time = {latency}ms")
            else:
                self.output_label.config(text=f"{url} is not reachable")
            time.sleep(10)

    def stop_pinging(self):
        self.is_pinging = False
        self.output_label.config(text="Ping checking stopped.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()

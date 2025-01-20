import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import datetime
import json

# Embedded encryption key (hidden in the app)
embedded_key = b'qmD86oJ9UeT9WctM1b4zFvcd0-iXtTtecqtBkY0yDtc='


def load_secret_key():
    """
    Retrieve the embedded secret key.
    """
    return embedded_key


class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Checker")
        self.is_pinging = False
        self.license_path = self.load_license_path()
        self.license_valid = self.validate_license()

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

        if not self.license_valid:
            self.prompt_for_license()

    def load_license_path(self):
        """
        Load the previously saved license path if it exists.
        """
        if os.path.exists("license_path.json"):
            with open("license_path.json", "r") as file:
                return json.load(file).get("path")
        return None

    def save_license_path(self, path):
        """
        Save the license path to a JSON file.
        """
        with open("license_path.json", "w") as file:
            json.dump({"path": path}, file)

    def validate_license(self):
        """
        Validate the license file and check if it is still valid.
        """
        if not self.license_path or not os.path.exists(self.license_path):
            return False

        try:
            # Load the secret key embedded in the app
            secret_key = load_secret_key()

            with open(self.license_path, "rb") as license_file:
                encrypted_date = license_file.read()

            cipher = Fernet(secret_key)
            expiration_datetime_str = cipher.decrypt(encrypted_date).decode()
            expiration_datetime = datetime.datetime.strptime(
                expiration_datetime_str, "%Y-%m-%d %H:%M"
            )
            now = datetime.datetime.now()

            if now > expiration_datetime:
                messagebox.showerror("License Expired", "License has expired!")
                return False
            return True
        except Exception:
            messagebox.showerror(
                "Invalid License", "The selected license file is invalid!")
            return False

    def prompt_for_license(self):
        """
        Prompt the user to select a license file until a valid license is loaded
        or the user cancels the process.
        """
        while not self.license_valid:
            response = messagebox.askyesno(
                "License Required",
                "A valid license is required to continue. Do you want to select a license file?"
            )
            if not response:
                # Exit the loop if the user cancels
                self.output_label.config(
                    text="License required. Exiting functionality.")
                return

            license_path = filedialog.askopenfilename(
                title="Select License File",
                filetypes=(("License Files", "*.lic"), ("All Files", "*.*"))
            )
            if not license_path:
                messagebox.showwarning(
                    "No License Selected", "Please select a valid license.")
                continue

            self.license_path = license_path
            self.save_license_path(license_path)
            self.license_valid = self.validate_license()

    def start_pinging(self):
        if not self.license_valid:
            self.prompt_for_license()
            return

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
            latency = ""
            if "Average" in response:
                latency = response.split("Average=")[-1].split("ms")[0].strip()
                self.output_label.config(
                    text=f"Ping Output: {url} is reachable, Time = {latency}ms"
                )
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

import os
import json
import requests
import zipfile
import threading
import time
from tkinter import Tk, Label, Entry, Button, W, E, END, NORMAL, filedialog, messagebox, simpledialog, ttk, DISABLED

PADX = 10
PADY = 10

class DownloaderApp:
    """A GUI application for downloading game files."""

    CONFIG_FILE = 'config.json'
    DEFAULT_SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")
    CHUNK_SIZE = 8192

    def __init__(self, root):
        self.root = root
        self.root.title("CS2 FastDL")
        self.root.geometry('820x250')
        
        self._initialize_config()
        self._load_config_urls()
        self._create_widgets()
        self._layout_widgets()

        self.root['padx'] = 25
        self.root['pady'] = 25


    def _initialize_config(self):
        os.makedirs(self.DEFAULT_SAVE_PATH, exist_ok=True)
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    self.configs = json.load(f)
            else:
                self.configs = {"urls": {}, "save_path": self.DEFAULT_SAVE_PATH}
                with open(self.CONFIG_FILE, 'w') as f:
                    json.dump(self.configs, f)

            self.save_path = self.configs["save_path"]

            if not self.configs["urls"]:
                default_server_alias = "Test Server"
                default_server_url = "https://www.gcgfast.com/stresstest/cs2/"
                self.configs["urls"][default_server_alias] = default_server_url
                with open(self.CONFIG_FILE, 'w') as f:
                    json.dump(self.configs, f)

        except Exception as e:
            messagebox.showerror("Error", f"Error initializing config: {str(e)}")

    def _load_config_urls(self):
        try:
            self.urls = self.configs["urls"]
        except Exception as e:
            messagebox.showerror("Error", f"Error loading config URLs: {str(e)}")


    def merge_file_parts(self, url, num_parts):
        local_filename = url.split('/')[-1]
        local_filepath = os.path.join(self.save_path, local_filename)

        with open(local_filepath, 'wb') as f_out:
            for i in range(num_parts):
                part_filename = local_filename + f".part{i}"
                part_filepath = os.path.join(self.save_path, part_filename)
                if os.path.exists(part_filepath):
                    with open(part_filepath, 'rb') as f_in:
                        f_out.write(f_in.read())
                    os.remove(part_filepath)
                    print(f"Merged part {i} into {local_filename}")
                else:
                    print(f"Part {i} missing for {local_filename}")


    def extract_zip(self, zip_path):
        """Extracts the zip file and overwrites existing files."""
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.save_path)
        except Exception as e:
            self.update_status(f"Error extracting {zip_path}: {str(e)}", "red")


    def _prepare_config(self):
        os.makedirs(self.DEFAULT_SAVE_PATH, exist_ok=True)
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, 'r') as f:
                    self.configs = json.load(f)
            else:
                self.configs = {"urls": {}, "save_path": self.DEFAULT_SAVE_PATH}
                with open(self.CONFIG_FILE, 'w') as f:
                    json.dump(self.configs, f)

            self.urls = self.configs["urls"]
            self.save_path = self.configs["save_path"]

            default_server_alias = "Test Server"
            default_server_url = "https://www.gcgfast.com/stresstest/cs2/"
            if default_server_alias not in self.urls:
                self.urls[default_server_alias] = default_server_url
                with open(self.CONFIG_FILE, 'w') as f:
                    json.dump(self.configs, f)
                self.url_var['values'] = list(self.urls.keys())
                self.url_var.set(default_server_alias)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading config: {str(e)}")


    def download_file(self, url, file_path):
        try:
            local_filename = url.split('/')[-1]
            local_directory = os.path.join(self.save_path, os.path.dirname(file_path))
            os.makedirs(local_directory, exist_ok=True)
            
            local_filepath = os.path.join(local_directory, local_filename)
            response = requests.get(url, stream=True, timeout=5)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            start_time = time.time()

            with open(local_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        downloaded += len(chunk)
                        f.write(chunk)
                        elapsed_time = time.time() - start_time
                        speed = downloaded / (elapsed_time + 0.0001)
                        speed_str = f"{speed / (1024**2):.2f} MB/s"
                        self.root.after(0, lambda: self.speed_label.config(text=speed_str))
                        percentage = (downloaded / total_size) * 100
                        self.root.after(0, lambda: self.progress.config(value=percentage))

            if local_filename == "assets.zip":
                self.extract_zip(local_filepath)

            if os.path.exists(local_filepath):
                self.update_status(f"Download completed successfully for {url}", "green")
            else:
                self.update_status(f"Download failed for {url}", "red")
        except requests.exceptions.RequestException as e:
            self.update_status(f"Failed to download {url}. Error: {str(e)}", "red")



    def download_file_part(self, url, start_byte, end_byte, part_num, errors, retries=3):
        headers = {'Range': f"bytes={start_byte}-{end_byte}"}
        local_filename = url.split('/')[-1] + f".part{part_num}"
        local_filepath = os.path.join(self.save_path, local_filename)

        print(f"Starting download of part {part_num} from {start_byte} to {end_byte}")

        for _ in range(retries):
            try:
                with requests.get(url, headers=headers, stream=True, timeout=5) as r:
                    r.raise_for_status()
                    with open(local_filepath, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=self.CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                    print(f"Successfully downloaded part {part_num}")
                    return local_filepath
            except requests.exceptions.RequestException as e:
                error_message = f"Error downloading {url}: {str(e)}"
                if _ == retries - 1:
                    errors.append(error_message)
                    self.update_status(error_message, "red")
                else:
                    print(f"Retrying download of part {part_num}...")
        return None



    def _create_widgets(self):
        """Create the widgets for the app."""
        self.progress = ttk.Progressbar(self.root, orient='horizontal', mode='determinate')
        self.progress.grid(row=0, column=0, columnspan=4, sticky=W+E)

        self.status_label = Label(self.root, text="", fg="green")
        self.speed_label = Label(self.root, text="", fg="black")
        self.save_path_label = Label(self.root, text="Save Path:")
        self.server_selector_label = Label(self.root, text="Select Server:")
        self.save_path_entry = Entry(self.root, width=50)
        self.save_path_entry.insert(0, self.save_path)
        self.browse_button = Button(self.root, text="Browse", command=self.browse_save_path)

        self.url_var = ttk.Combobox(self.root, values=list(self.urls.keys()))
        if self.urls:
            self.url_var.current(0)
        self.add_url_button = Button(self.root, text="Add TXT URL", command=self.add_url)
        self.download_button = Button(self.root, text="Start Download", command=self.start_download)

    def _layout_widgets(self):
        """Layout the widgets in the app."""
        self.status_label.grid(row=1, column=0, pady=PADY, padx=PADX, columnspan=3, sticky=W+E)
        self.speed_label.grid(row=1, column=3, pady=PADY, padx=PADX, columnspan=1, sticky=W+E)

        self.save_path_label.grid(row=2, column=0, pady=(PADY, 0), sticky=W)
        self.save_path_entry.grid(row=3, column=0, columnspan=2, padx=(0, 20), sticky=W+E)
        self.browse_button.grid(row=3, column=2, padx=(0, 20), sticky=W)

        self.server_selector_label.grid(row=4, column=0, pady=(PADY, 0), sticky=W)
        self.url_var.grid(row=5, column=0, columnspan=2, padx=(0, 20), sticky=W+E)
        self.add_url_button.grid(row=5, column=2, padx=(0, 20), sticky=W)
        self.download_button.grid(row=5, column=3, padx=(0, 20), sticky=W)


    def browse_save_path(self):
        selected_path = filedialog.askdirectory(initialdir=self.save_path)
        if selected_path:
            if not selected_path.endswith("csgo"):
                selected_path = os.path.join(selected_path, "csgo")
                os.makedirs(selected_path, exist_ok=True)

            self.save_path = selected_path
            self.save_path_entry.delete(0, END)
            self.save_path_entry.insert(0, self.save_path)

            self.configs["save_path"] = self.save_path
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.configs, f)

    def add_url(self):
        url = simpledialog.askstring("Add Server URL", "Enter URL:")
        alias = simpledialog.askstring("URL Alias", "Enter a memorable alias for this URL:")
        if url and alias:
            self.urls[alias] = url
            self.url_var['values'] = list(self.urls.keys())
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.configs, f)


    def is_file_different(self, url):
        local_filename = url.split('/')[-1]
        local_filepath = os.path.join(self.save_path, local_filename)
        if not os.path.exists(local_filepath):
            return True

        try:
            response = requests.head(url, timeout=5)
            response.raise_for_status()
            remote_size = int(response.headers['Content-Length'])
            local_size = os.path.getsize(local_filepath)

            return local_size != remote_size
        except requests.exceptions.RequestException as e:
            self.update_status(f"Error accessing {url}: {str(e)}", "red")
            return False


    def update_status(self, message, color="green"):
        self.status_label.config(text=message, fg=color)
        self.root.update_idletasks()

    def start_download(self):
        self.download_button.config(state=DISABLED)

        download_thread = threading.Thread(target=self.download_process)
        download_thread.start()

    def download_process(self):
        selected_alias = self.url_var.get()
        base_url = self.urls.get(selected_alias)
        if not base_url:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please select or add a URL."))
            self.root.after(0, lambda: self.download_button.config(state=NORMAL))
            return

        file_list_url = os.path.join(base_url, "downloads.txt")
        try:
            response = requests.get(file_list_url, timeout=5)
            response.raise_for_status()
            files_to_download = response.text.split('\n')

            if not files_to_download:
                self.root.after(0, lambda: self.update_status("No files to download.", "blue"))
                return

            total_files = len(files_to_download)
            self.root.after(0, lambda: self.progress.config(value=index))

            for index, file_path in enumerate(files_to_download, start=1):
                if not file_path.strip():
                    continue
                file_url = os.path.join(base_url, file_path.strip())
                
                if self.is_file_different(file_url):
                    self.root.after(0, lambda: self.update_status(f"Downloading {file_url}"))
                    self.download_file(file_url, file_path.strip())

                    self.root.after(0, lambda: self.update_status(f"Downloaded {file_url}"))
                else:
                    self.root.after(0, lambda: self.update_status(f"File is up to date: {file_url}", "blue"))

                self.root.after(0, lambda: self.progress.config(value=index))

            self.root.after(0, lambda: messagebox.showinfo("Download Complete", "All files have been processed."))
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self.update_status(f"Error: {str(e)}", "red"))
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.root.after(0, lambda: self.download_button.config(state=NORMAL))


if __name__ == "__main__":
    root = Tk()
    app = DownloaderApp(root)
    root.mainloop()

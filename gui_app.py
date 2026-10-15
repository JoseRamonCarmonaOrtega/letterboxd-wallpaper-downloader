import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import requests


class WallpaperDownloaderApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Letterboxd Wallpaper Downloader")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        self.csv_path = tk.StringVar()
        self.api_key = tk.StringVar()
        self.output_dir = tk.StringVar(value="wallpapers_alta_calidad")

        self._build_ui()

    def _build_ui(self):
        p = {"padx": 20, "pady": 5}

        tk.Label(
            self.root, text="1. Selecciona tu CSV de Letterboxd:", font=("Arial", 10, "bold")
        ).pack(anchor="w", **p)
        frame_csv = tk.Frame(self.root)
        frame_csv.pack(fill="x", padx=20)
        tk.Entry(
            frame_csv, textvariable=self.csv_path, state="readonly", width=40
        ).pack(side="left", fill="x", expand=True)
        tk.Button(
            frame_csv, text="Buscar CSV...", command=self.select_csv
        ).pack(side="right", padx=(5, 0))

        tk.Label(
            self.root, text="2. Introduce tu API Key de TMDb:", font=("Arial", 10, "bold")
        ).pack(anchor="w", **p)
        tk.Entry(
            self.root, textvariable=self.api_key, show="*", width=50
        ).pack(anchor="w", padx=20)

        tk.Label(
            self.root, text="3. Carpeta de destino:", font=("Arial", 10, "bold")
        ).pack(anchor="w", **p)
        frame_folder = tk.Frame(self.root)
        frame_folder.pack(fill="x", padx=20)
        tk.Entry(frame_folder, textvariable=self.output_dir, width=40).pack(
            side="left", fill="x", expand=True
        )
        tk.Button(
            frame_folder, text="Cambiar...", command=self.select_folder
        ).pack(side="right", padx=(5, 0))

        self.btn_start = tk.Button(
            self.root,
            text="🚀 Comenzar Descarga",
            font=("Arial", 11, "bold"),
            bg="#28a745",
            fg="white",
            command=self.start_download_thread,
        )
        self.btn_start.pack(pady=15)

        self.progress = ttk.Progressbar(
            self.root, orient="horizontal", length=470, mode="determinate"
        )
        self.progress.pack(padx=20, pady=5)

        self.status_label = tk.Label(
            self.root, text="Esperando datos...", fg="gray"
        )
        self.status_label.pack(pady=5)

    def select_csv(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if path:
            self.csv_path.set(path)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def start_download_thread(self):
        if not self.csv_path.get() or not self.api_key.get():
            messagebox.showwarning(
                "Faltan datos", "Por favor selecciona un CSV e introduce tu API Key."
            )
            return

        self.btn_start.config(state="disabled")
        threading.Thread(target=self.run_download, daemon=True).start()

    def run_download(self):
        csv_file = self.csv_path.get()
        api_k = self.api_key.get()
        out_folder = self.output_dir.get()

        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el CSV: {e}")
            self.btn_start.config(state="normal")
            return

        total = len(df)
        success_count = 0

        for i, row in enumerate(df.iterrows()):
            _, data = row
            title = str(data["Name"]).strip()
            year = str(data["Year"]).strip()

            self.status_label.config(
                text=f"Descargando ({i+1}/{total}): {title}...", fg="black"
            )
            self.progress["value"] = ((i + 1) / total) * 100

            if self.download_single(title, year, api_k, out_folder):
                success_count += 1

            time.sleep(0.3)

        self.status_label.config(
            text=f"¡Completado! {success_count}/{total} descargados.", fg="green"
        )
        messagebox.showinfo(
            "Éxito",
            f"Proceso completado.\nSe guardaron {success_count} fondos en la carpeta '{out_folder}'.",
        )
        self.btn_start.config(state="normal")

    def download_single(self, title, year, api_key, folder):
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": api_key,
            "query": title,
            "year": year,
            "language": "es-ES",
        }
        try:
            res = requests.get(url, params=params).json()
            if res.get("results"):
                backdrop = res["results"][0].get("backdrop_path")
                if backdrop:
                    img_url = f"https://image.tmdb.org/t/p/original{backdrop}"
                    data = requests.get(img_url).content
                    clean_name = "".join(
                        [c for c in title if c.isalnum() or c == " "]
                    ).rstrip()
                    file_path = os.path.join(folder, f"{clean_name}_{year}.jpg")
                    with open(file_path, "wb") as f:
                        f.write(data)
                    return True
            return False
        except Exception:
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = WallpaperDownloaderApp(root)
    root.mainloop()

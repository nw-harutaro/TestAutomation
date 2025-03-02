import tkinter as tk
from tkinter import messagebox
import os

def show_warning_popup(message):
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを非表示にする
    messagebox.showwarning("警告", message)
    root.destroy()

def get_files_by_extension(folder_path, extensions):
    files_list = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            # 指定した拡張子がリストに含まれている場合のみ追加
            if any(file.endswith(f".{ext}") for ext in extensions):
                file_path = os.path.join(root, file)
                files_list.append({
                    "name": file, 
                    "path": file_path,
                    "time": os.path.getmtime(file_path)
                })
    files_list.sort(key=lambda x: x["time"], reverse=True)
    return files_list
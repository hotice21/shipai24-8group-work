import pandas as pd
# 窗口上传文件功能
import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

def compare_excel_columns(file1, file2, column_name):
    if not file1 or not file2:
        print("请确保两个文件都已选择。")
        return
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    col1 = set(df1[column_name].dropna())
    col2 = set(df2[column_name].dropna())
    repeated = col1 & col2
    not_in_file2 = col1 - col2
    not_in_file1 = col2 - col1
    print(f"重复内容: {repeated}")
    print(f"仅在第一个文件中的内容: {not_in_file2}")
    print(f"仅在第二个文件中的内容: {not_in_file1}")

root = tk.Tk()
root.title("对比Excel文件")

frame = tk.Frame(root)
frame.pack(padx=40, pady=40)

class label_update:
    def __init__(self, padx, pady):
        self.label = tk.Label(frame, text="拖动文件到此或点击选择上传：")
        self.label.pack(padx=padx, pady=pady)
        self.entry_file = tk.Entry(frame, width=40)
        self.entry_file.pack(pady=20)
        self.btn_select = tk.Button(frame, text=f"选择文件", command=self.select_file)
        self.btn_select.pack(pady=5)
        # 拖拽支持
        try:
            self.entry_file.drop_target_register(DND_FILES)
            self.entry_file.dnd_bind('<<Drop>>', self.on_drop)
        except Exception as e:
            pass
    def on_drop(self,event):
        file_path = event.data
        self.entry_file.delete(0, tk.END)
        self.entry_file.insert(0, file_path)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.entry_file.delete(0, tk.END)
        self.entry_file.insert(0, file_path)

excel_1 = label_update(20, 5)
excel_2 = label_update(20, 5)
entry_name = tk.Entry(frame, width=20)
entry_name.pack(pady=10)
btn_compare = tk.Button(frame, text="对比", command=lambda: compare_excel_columns(excel_1.entry_file.get(), excel_2.entry_file.get(), entry_name.get()))
btn_compare.pack(pady=10)
root.mainloop()

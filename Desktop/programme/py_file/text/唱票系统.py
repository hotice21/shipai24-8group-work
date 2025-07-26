import tkinter as tk

root = tk.Tk()
root.title("窗口示例")

frame = tk.Frame(root)
frame.pack(padx=80, pady=20)

class new_one:
    def __init__(self,row):
        self.entry=tk.Entry(frame, width=10)
        self.entry.grid(row=row, column=0)
        self.label = tk.Label(frame, text=0)
        self.label.grid(row=row, column=1)
        self.btn_plus = tk.Button(frame, text="+1", command=self.increment)
        self.btn_plus.grid(row=row, column=2)
        self.btn_minus = tk.Button(frame, text="-1", command=self.decrement)
        self.btn_minus.grid(row=row, column=3)

    def increment(self):
        value = int(self.label.cget("text"))
        self.label.config(text=value + 1)

    def decrement(self):
        value = int(self.label.cget("text"))
        if value > 0:
            self.label.config(text=value - 1)

list_of_role = []
row=1
def add_role():
    global row
    list_of_role.append(new_one(row))
    row += 1
def delete_role():
    global row
    if row > 1:
        row -= 1
        list_of_role[-1].entry.grid_forget()
        list_of_role[-1].label.grid_forget()
        list_of_role[-1].btn_plus.grid_forget()
        list_of_role[-1].btn_minus.grid_forget()
        list_of_role.pop()

# 复制按钮
copy_btn = tk.Button(frame, text="添加", command=add_role)
copy_btn.grid(row=0, column=1, pady=10)
delete_btn = tk.Button(frame, text="删除", command=delete_role)
delete_btn.grid(row=0, column=2, pady=10)

root.mainloop()

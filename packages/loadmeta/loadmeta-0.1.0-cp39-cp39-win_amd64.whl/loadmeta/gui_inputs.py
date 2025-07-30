import tkinter as tk
from tkinter import simpledialog, filedialog

def get_user_inputs():
    class MultiInputDialog(simpledialog.Dialog):
        def body(self, master):
            tk.Label(master, text="Database user:").grid(row=0, sticky="e")
            tk.Label(master, text="Database password:").grid(row=1, sticky="e")
            tk.Label(master, text="Database host:").grid(row=2, sticky="e")
            tk.Label(master, text="Database name:").grid(row=3, sticky="e")
            tk.Label(master, text="Raster file:").grid(row=4, sticky="e")

            self.user_var = tk.StringVar(value="user")
            self.passwd_var = tk.StringVar(value="pass")
            self.host_var = tk.StringVar(value="192.168.11.44")
            self.dbname_var = tk.StringVar(value="ZONA*")
            self.raster_var = tk.StringVar()

            self.user_entry = tk.Entry(master, textvariable=self.user_var)
            self.passwd_entry = tk.Entry(master, textvariable=self.passwd_var, show="*")
            self.host_entry = tk.Entry(master, textvariable=self.host_var)
            self.dbname_entry = tk.Entry(master, textvariable=self.dbname_var)
            self.raster_entry = tk.Entry(master, textvariable=self.raster_var, state="readonly")
            self.browse_btn = tk.Button(master, text="Browse...", command=self.browse_file)

            self.user_entry.grid(row=0, column=1)
            self.passwd_entry.grid(row=1, column=1)
            self.host_entry.grid(row=2, column=1)
            self.dbname_entry.grid(row=3, column=1)
            self.raster_entry.grid(row=4, column=1)
            self.browse_btn.grid(row=4, column=2)
            return self.user_entry

        def browse_file(self):
            filename = filedialog.askopenfilename(title="Select raster file")
            if filename:
                self.raster_var.set(filename)

        def apply(self):
            self.result = (
                self.user_var.get(),
                self.passwd_var.get(),
                self.host_var.get(),
                self.dbname_var.get(),
                self.raster_var.get()
            )

    root = tk.Tk()
    root.withdraw()
    dialog = MultiInputDialog(root, title="Database and Raster Inputs")
    root.destroy()
    if dialog.result:
        return dialog.result
    else:
        return None, None, None, None, None

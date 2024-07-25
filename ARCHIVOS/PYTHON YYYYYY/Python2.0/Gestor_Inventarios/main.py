import tkinter as tk
from inter_Grafica import GestorDeInventarioApp
import database as db

def on_closing():
    db.close_db()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorDeInventarioApp(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

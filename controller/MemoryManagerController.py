# controller.py
import tkinter as tk
from view.MemoryManagerView import MemoryManagerGUI


class Controller:
    def __init__(self):
        root = tk.Tk()
        app = MemoryManagerGUI(root)
        root.mainloop()

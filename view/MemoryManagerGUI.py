import tkinter as tk
from tkinter import ttk

class MemoryManagerView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Memory Manager GUI")
        self.create_widgets()

    def create_widgets(self):
        config_frame = ttk.Frame(self.root, padding="10")
        config_frame.grid(row=0, column=0, sticky="w")

        ttk.Label(config_frame, text="Memory Size:").grid(row=0, column=0, sticky="w")
        self.memory_size_entry = ttk.Entry(config_frame)
        self.memory_size_entry.grid(row=0, column=1, padx=5)

        ttk.Label(config_frame, text="Algorithm Type:").grid(row=1, column=0, sticky="w")
        self.algorithm_type_combobox = ttk.Combobox(config_frame, values=["first-fit", "best-fit", "worst-fit", "next-fit"])
        self.algorithm_type_combobox.grid(row=1, column=1, padx=5)
        self.algorithm_type_combobox.set("first-fit")

        ttk.Label(config_frame, text="Max Process Size:").grid(row=2, column=0, sticky="w")
        self.max_process_size_entry = ttk.Entry(config_frame)
        self.max_process_size_entry.grid(row=2, column=1, padx=5)

        ttk.Label(config_frame, text="Max Process Life Time:").grid(row=3, column=0, sticky="w")
        self.max_process_life_time_entry = ttk.Entry(config_frame)
        self.max_process_life_time_entry.grid(row=3, column=1, padx=5)

        ttk.Label(config_frame, text="Simulation Time:").grid(row=4, column=0, sticky="w")
        self.simulation_time_entry = ttk.Entry(config_frame)
        self.simulation_time_entry.grid(row=4, column=1, padx=5)

        ttk.Label(config_frame, text="Delay:").grid(row=5, column=0, sticky="w")
        self.delay_entry = ttk.Entry(config_frame)
        self.delay_entry.grid(row=5, column=1, padx=5)

        start_button = ttk.Button(config_frame, text="Start Simulation", command=self.controller.start_simulation)
        start_button.grid(row=6, columnspan=2, pady=10)

        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.grid(row=0, column=1, sticky="w")

        self.output_text = tk.Text(output_frame, height=20, width=50)
        self.output_text.grid(row=0, column=0)

    def run(self):
        self.root.mainloop()

    def update_output(self, text):
        self.output_text.insert(tk.END, text + "\n")

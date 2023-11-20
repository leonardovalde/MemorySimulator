import tkinter as tk
from tkinter import ttk
from MemoryManager import MemoryManager, Process
import random
import time

class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Manager GUI")

        self.create_widgets()

    def create_widgets(self):
        # Frame para la configuración
        config_frame = ttk.Frame(self.root, padding="10")
        config_frame.grid(row=0, column=0, sticky="w")

        # Configuración de la simulación
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

        # Botón para iniciar la simulación
        start_button = ttk.Button(config_frame, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=6, columnspan=2, pady=10)

        # Frame para la salida
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.grid(row=0, column=1, sticky="w")

        # Salida de la simulación
        self.output_text = tk.Text(output_frame, height=20, width=50)
        self.output_text.grid(row=0, column=0)

        

    def start_simulation(self):
        self.output_text.insert(tk.END, "")
        memory_size = int(self.memory_size_entry.get())
        algorithm_type = self.algorithm_type_combobox.get()
        max_process_size = int(self.max_process_size_entry.get())
        max_process_life_time = int(self.max_process_life_time_entry.get())
        simulation_time = int(self.simulation_time_entry.get())
        delay = float(self.delay_entry.get())

        self.memory_manager = MemoryManager(memory_size, algorithm_type)

        self.simulate_iteration(simulation_time, delay, max_process_size, max_process_life_time)

    def simulate_iteration(self, simulation_time, delay, max_process_size, max_process_life_time):
        if self.memory_manager.clock < simulation_time:
            process_size = random.randint(1, max_process_size)
            process_life_time = random.randint(1, max_process_life_time)
            process = Process(f"P{self.memory_manager.clock}", process_size,
                              self.memory_manager.clock + process_life_time)

            if self.memory_manager.allocate_memory(process):
                self.output_text.insert(tk.END,
                                        f"Allocated Process {process.id} of size {process.size} at clock {self.memory_manager.clock}\n")
            else:
                self.output_text.insert(tk.END,
                                        f"Failed to allocate Process {process.id} of size {process.size} at clock {self.memory_manager.clock}\n")

            self.output_text.delete(1.0, tk.END)

            # Append the memory state information to output_text
            self.output_text.insert(tk.END, f"Memory State at clock {self.memory_manager.clock}:\n")
            for i, partition in enumerate(self.memory_manager.partitions):
                status = f"Partition {i}: Size = {partition.size}, "
                if partition.is_free():
                    status += "Status = Free"
                else:
                    status += f"Status = Occupied by Process {partition.process.id}, Ends at {partition.end_time}"
                self.output_text.insert(tk.END, status + "\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")

            self.memory_manager.deallocate_memory()
            self.memory_manager.clock += 1
            self.root.after(int(delay * 1000), self.simulate_iteration, simulation_time, delay, max_process_size,
                            max_process_life_time)


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()

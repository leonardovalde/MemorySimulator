import tkinter as tk
from tkinter import ttk
from model.MemoryManager import MemoryManager, Process
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MemoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Manager GUI")

        # Frame for memory statistics
        stats_frame = ttk.Frame(self.root, padding="10")
        stats_frame.grid(row=1, column=1, sticky="w")

        # Memory statistics text
        self.stats_text = tk.Text(stats_frame, height=10, width=50)
        self.stats_text.grid(row=0, column=0)

        # Matplotlib initialization
        self.fig, self.ax = Figure(), None
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=2, sticky="w")

        self.create_widgets()

        # Initialize graph data
        self.graph_data = {
            'clocks': [],
            'allocations': [],
            'deallocations': [],
            'total_memory': [],
            'free_partitions': [],
            'occupied_partitions': [],
        }

    def create_widgets(self):
        # Frame for configuration
        config_frame = ttk.Frame(self.root, padding="10")
        config_frame.grid(row=0, column=0, sticky="w")

        # Configuration for simulation
        ttk.Label(config_frame, text="Memory Size:").grid(row=0, column=0, sticky="w")
        self.memory_size_entry = ttk.Entry(config_frame)
        self.memory_size_entry.grid(row=0, column=1, padx=5)

        ttk.Label(config_frame, text="Algorithm Type:").grid(row=1, column=0, sticky="w")
        self.algorithm_type_combobox = ttk.Combobox(config_frame,
                                                    values=["first-fit", "best-fit", "worst-fit", "next-fit"])
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

        # Button to start simulation
        start_button = ttk.Button(config_frame, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=6, columnspan=2, pady=10)

        # Frame for the output
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.grid(row=0, column=1, sticky="w")

        # Output of the simulation
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
        self.memory_manager.clock = 0

        # Reset the graph data
        self.graph_data = {
            'clocks': [],
            'allocations': [],
            'deallocations': [],
            'total_memory': [],
            'free_partitions': [],
            'occupied_partitions': [],
        }

        # Clear the existing plot
        if self.ax:
            self.ax.clear()
            self.canvas.draw()

        self.simulate_iteration(simulation_time, delay, max_process_size, max_process_life_time)

    def simulate_iteration(self, simulation_time, delay, max_process_size, max_process_life_time):
        if self.memory_manager.clock < simulation_time:
            process_size = random.randint(1, max_process_size)
            process_life_time = random.randint(1, max_process_life_time)
            process = Process(f"P{self.memory_manager.clock}", process_size,
                              self.memory_manager.clock + process_life_time)

            allocation_success = self.memory_manager.allocate_memory(process)
            self.memory_manager.deallocate_memory()

            # Update the output text and graph data
            self.update_output_text(process, allocation_success)
            self.update_graph_data(allocation_success)

            self.memory_manager.clock += 1

            self.update_memory_stats()
            self.show_graph()

            self.root.after(int(delay * 1000), self.simulate_iteration, simulation_time, delay, max_process_size,
                            max_process_life_time)

    def update_output_text(self, process, allocation_success):
        if allocation_success:
            self.output_text.insert(tk.END,
                                    f"Allocated Process {process.id} of size {process.size} at clock {self.memory_manager.clock}\n")
        else:
            self.output_text.insert(tk.END,
                                    f"Failed to allocate Process {process.id} of size {process.size} at clock {self.memory_manager.clock}\n")

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

    def update_graph_data(self, allocation_success):
        # Update graph data
        self.graph_data['clocks'].append(self.memory_manager.clock)
        self.graph_data['allocations'].append(len([p for p in self.memory_manager.partitions if not p.is_free()]))
        self.graph_data['deallocations'].append(len([p for p in self.memory_manager.partitions if p.is_free()]))
        self.graph_data['total_memory'].append(sum(partition.size for partition in self.memory_manager.partitions))
        self.graph_data['free_partitions'].append(
            sum(1 for partition in self.memory_manager.partitions if partition.is_free()))
        self.graph_data['occupied_partitions'].append(
            sum(1 for partition in self.memory_manager.partitions if not partition.is_free()))

    def update_memory_stats(self):
        # Calculate and update memory statistics
        total_memory = sum(partition.size for partition in self.memory_manager.partitions)
        allocated_memory = sum(
            partition.size for partition in self.memory_manager.partitions if not partition.is_free())
        unallocated_memory = total_memory - allocated_memory
        percentage_unallocated = (unallocated_memory / total_memory) * 100

        # Update the memory statistics text
        stats_info = f"Total Memory: {total_memory}\n"
        stats_info += f"Allocated Memory: {allocated_memory}\n"
        stats_info += f"Unallocated Memory: {unallocated_memory}\n"
        stats_info += f"Percentage Unallocated: {percentage_unallocated:.2f}%\n"

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats_info)

    def evaluate_performance(self):
        # Analyze and display performance metrics
        # For example, you can calculate and display average waiting time, response time, etc.
        waiting_times = [...]  # List of waiting times for each allocated process
        response_times = [...]  # List of response times for each allocated process

        avg_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        # Display performance metrics
        performance_info = f"Average Waiting Time: {avg_waiting_time:.2f}\n"
        performance_info += f"Average Response Time: {avg_response_time:.2f}\n"

        self.stats_text.insert(tk.END, performance_info)

    def show_graph(self):
        # Extract data for the graph
        clocks = self.graph_data['clocks']
        allocations = self.graph_data['allocations']
        deallocations = self.graph_data['deallocations']
        total_memory = self.graph_data['total_memory']
        free_partitions = self.graph_data['free_partitions']
        occupied_partitions = self.graph_data['occupied_partitions']

        # Plotting
        if not self.ax:
            self.ax = self.fig.add_subplot(111)

        self.ax.clear()
        self.ax.plot(clocks, allocations, label='Allocations')
        self.ax.plot(clocks, deallocations, label='Deallocations')
        self.ax.plot(clocks, total_memory, label='Total Memory')
        self.ax.plot(clocks, free_partitions, label='Free Partitions')
        self.ax.plot(clocks, occupied_partitions, label='Occupied Partitions')
        # Add more metrics as needed

        self.ax.set_xlabel('Clock Time')
        self.ax.set_ylabel('Count')
        self.ax.legend()

        # Draw the updated graph
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagerGUI(root)
    root.mainloop()

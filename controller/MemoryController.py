from MemoryManager import MemoryManager, Process
from view.MemoryManagerGUI import MemoryManagerView
import random
import time

class MemoryManagerController:
    def __init__(self):
        self.view = MemoryManagerView(self)

    def start_simulation(self):
        memory_size = int(self.view.memory_size_entry.get())
        algorithm_type = self.view.algorithm_type_combobox.get()
        max_process_size = int(self.view.max_process_size_entry.get())
        max_process_life_time = int(self.view.max_process_life_time_entry.get())
        simulation_time = int(self.view.simulation_time_entry.get())
        delay = float(self.view.delay_entry.get())

        self.memory_manager = MemoryManager(memory_size, algorithm_type)
        self.simulate_iteration(simulation_time, delay, max_process_size, max_process_life_time)

    def simulate_iteration(self, simulation_time, delay, max_process_size, max_process_life_time):
        if self.memory_manager.clock < simulation_time:
            process_size = random.randint(1, max_process_size)
            process_life_time = random.randint(1, max_process_life_time)
            process = Process(f"P{self.memory_manager.clock}", process_size, self.memory_manager.clock + process_life_time)

            if self.memory_manager.allocate_memory(process):
                self.view.update_output(f"Allocated Process {process.id} of size {process.size} at clock {self.memory_manager.clock}")
            else:
                self.view.update_output(f"Failed to allocate Process {process.id} of size {process.size} at clock {self.memory_manager.clock}")

            self.memory_manager.deallocate_memory()
            self.memory_manager.clock += 1
            self.view.root.after(int(delay * 1000), self.simulate_iteration, simulation_time, delay, max_process_size, max_process_life_time)

    def run(self):
        self.view.run()

if __name__ == "__main__":
    controller = MemoryManagerController()
    controller.run()

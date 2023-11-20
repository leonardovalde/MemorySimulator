import statistics
import time
import random
from model.MemoryManager import MemoryManager, Process

class MemoryManagerBenchmark:
    def __init__(self, memory_size, simulation_time, max_process_size, max_process_life_time, delay):
        """
        Initializes an instance of the class.

        Parameters:
            memory_size (int): The size of the memory.
            simulation_time (int): The time for which the simulation will run.
            max_process_size (int): The maximum size of a process.
            max_process_life_time (int): The maximum life time of a process.
            delay (int): The delay between each simulation step.

        Returns:
            None
        """
        self.memory_size = memory_size
        self.simulation_time = simulation_time
        self.max_process_size = max_process_size
        self.max_process_life_time = max_process_life_time
        self.delay = delay

    def run_benchmark(self, algorithm_types):
        """
        Runs a benchmark for a given list of algorithm types.

        Args:
            algorithm_types (list): A list of algorithm types to run the benchmark on.

        Returns:
            dict: A dictionary containing the results of the benchmark. The keys are algorithm types, and the values are dictionaries with the following keys:
                - 'Utilization': The utilization of the memory manager.
                - 'Failed Allocations': The number of failed memory allocations.
                - 'Execution Time': The execution time of the simulation.
        """
        results = {}
        for algorithm in algorithm_types:
            memory_manager = MemoryManager(self.memory_size, algorithm)
            utilization, failed_allocations, execution_time = self.run_simulation(memory_manager)
            results[algorithm] = {
                'Utilization': utilization,
                'Failed Allocations': failed_allocations,
                'Execution Time': execution_time
            }
        return results

    def run_simulation(self, memory_manager):
        """
        Run simulation for a given memory manager.

        Parameters:
            memory_manager (MemoryManager): The memory manager object used for simulation.

        Returns:
            tuple: A tuple containing the average memory utilization, the number of failed allocations, and the execution time.
                - average_utilization (float): The average memory utilization.
                - failed_allocations (int): The number of failed allocations.
                - execution_time (float): The execution time in seconds.
        """
        start_time = time.time()
        failed_allocations = 0
        total_memory_used = 0

        for _ in range(self.simulation_time):
            if random.randint(1, self.max_process_size) == 1:
                process_size = random.randint(1, 100)
                process_life_time = random.randint(1, self.max_process_life_time)
                process = Process(f"P{memory_manager.clock}", process_size, memory_manager.clock + process_life_time)
                if not memory_manager.allocate_memory(process):
                    failed_allocations += 1
            total_memory_used += sum(p.size for p in memory_manager.partitions if not p.is_free())
            memory_manager.deallocate_memory()
            memory_manager.clock += 1
            time.sleep(self.delay)

        execution_time = time.time() - start_time
        average_utilization = total_memory_used / (self.memory_size * self.simulation_time)
        return average_utilization, failed_allocations, execution_time

# Ejemplo de cómo usarlo
def main():
    memory_size = 1024
    simulation_time = 10
    max_process_size = 1
    max_process_life_time = 2
    delay = 1
    algorithm_types = ['first-fit', 'best-fit', 'worst-fit', 'next-fit']

    benchmark = MemoryManagerBenchmark(memory_size, simulation_time, max_process_size, max_process_life_time, delay)
    results = benchmark.run_benchmark(algorithm_types)
    for algorithm, result in results.items():
        print(f"Algorithm: {algorithm}, Results: {result}")

if __name__ == "__main__":
    main()

import statistics
import time
import random
from model.MemoryManager import MemoryManager, Process

class MemoryManagerBenchmark:
    def __init__(self, memory_size, simulation_time, max_process_size, max_process_life_time, delay):
        self.memory_size = memory_size
        self.simulation_time = simulation_time
        self.max_process_size = max_process_size
        self.max_process_life_time = max_process_life_time
        self.delay = delay

    def run_benchmark(self, algorithm_types):
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

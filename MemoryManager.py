import random
import time

class Process:
    def __init__(self, id, size, life_time):
        self.id = id
        self.size = size
        self.life_time = life_time

class MemoryPartition:
    def __init__(self, start, size, process=None):
        self.start = start
        self.size = size
        self.process = process
        self.end_time = None if process is None else process.life_time

    def is_free(self):
        return self.process is None

class MemoryManager:
    def __init__(self, memory_size, algorithm_type):
        self.partitions = [MemoryPartition(0, memory_size)]
        self.algorithm_type = algorithm_type
        self.clock = 0

    def allocate_memory(self, process):
        if self.algorithm_type == "first-fit":
            return self.first_fit(process)
        elif self.algorithm_type == "best-fit":
            return self.best_fit(process)
        elif self.algorithm_type == "worst-fit":
            return self.worst_fit(process)
        elif self.algorithm_type == "next-fit":
            return self.next_fit(process)
        return False

    def first_fit(self, process):
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                self.assign_process(partition, process)
                return True
        return False

    def best_fit(self, process):
        best_partition = None
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                if best_partition is None or partition.size < best_partition.size:
                    best_partition = partition
        if best_partition:
            self.assign_process(best_partition, process)
            return True
        return False


    def worst_fit(self, process):
        worst_partition = None
        for partition in self.partitions:
            if partition.is_free() and partition.size >= process.size:
                if worst_partition is None or partition.size > worst_partition.size:
                    worst_partition = partition
        if worst_partition:
            self.assign_process(worst_partition, process)
            return True
        return False

    def next_fit(self, process):
        start_index = self.last_allocated_index if hasattr(self, 'last_allocated_index') else 0
        n = len(self.partitions)
        for i in range(n):
            index = (start_index + i) % n
            partition = self.partitions[index]
            if partition.is_free() and partition.size >= process.size:
                self.assign_process(partition, process)
                self.last_allocated_index = index
                return True
        return False
    
    def assign_process(self, partition, process):
        if partition.size > process.size:
            new_partition = MemoryPartition(partition.start + process.size, partition.size - process.size)
            self.partitions.insert(self.partitions.index(partition) + 1, new_partition)
        partition.size = process.size
        partition.process = process
        partition.end_time = self.clock + process.life_time

    def deallocate_memory(self):
        # Desasignar memoria de procesos cuyo tiempo de vida ha expirado
        for partition in self.partitions:
            if partition.process and self.clock >= partition.end_time:
                partition.process = None
                partition.end_time = None

    def print_memory_state(self):
        print(f"Clock: {self.clock}")
        for i, partition in enumerate(self.partitions):
            status = f"Partition {i}: Size = {partition.size}, "
            if partition.is_free():
                status += "Status = Free"
            else:
                status += f"Status = Occupied by Process {partition.process.id}, Ends at {partition.end_time}"
            print(status)
        print("-" * 50)

    def simulate(self, simulation_time, delay, max_next_process_time, max_process_life_time):
        while self.clock < simulation_time:
            self.print_memory_state()

            if random.randint(1, max_next_process_time) == 1:
                process_size = random.randint(1, 100)  # Tamaño aleatorio del proceso
                process_life_time = random.randint(1, max_process_life_time)
                process = Process(f"P{self.clock}", process_size, self.clock + process_life_time)
                if self.allocate_memory(process):
                    print(f"Allocated Process {process.id} of size {process.size} at clock {self.clock}")
                else:
                    print(f"Failed to allocate Process {process.id} of size {process.size} at clock {self.clock}")

            self.deallocate_memory()
            self.clock += 1
            time.sleep(delay)


def main():
    memory_size = 1024
    algorithm_type = 'first-fit'
    max_process_size = 1
    max_process_life_time = 2
    simulation_time = 10
    delay = 1

    memory_manager = MemoryManager(memory_size, algorithm_type)
    memory_manager.simulate(simulation_time, delay, max_process_size, max_process_life_time)

if __name__ == "__main__":
    main()

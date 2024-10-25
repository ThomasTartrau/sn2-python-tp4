#Exercice 1
import threading

def exo1(k: int) -> list[str]:
    threads = []
    results = []

    def thread_function():
        results.append(f'{threading.current_thread().name} (run)')
    for i in range(k):
        thread = threading.Thread(target=thread_function, name=f'Thread-{i+1}')
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return results

#Exercice 2
import multiprocessing

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a list of numbers are prime and use multiprocessing to speed up the process
def exo2(numbers):
    with multiprocessing.Pool() as pool:
        return pool.map(is_prime, numbers)
    
#Exercice 3
import asyncio
import random
import time

class WaitAndValidateTask:
    def __init__(self):
        self.start_time = None

    # Function that return a random number between 1 and 2 (seconds)
    async def ask(self) -> int:
        return random.randint(1, 2)

    # Function that validate the task
    async def validate(self):
        self.start_time = time.time()

async def exo3(tasks: list[WaitAndValidateTask]):
    tasks_list = []

    # Call the ask method for each task
    for task in tasks:
        tasks_list.append(task.ask())

    # Wait for all the tasks to complete
    await asyncio.gather(*tasks_list)

    # Call the validate method for each task
    for task in tasks:
        await task.validate()

#Exercice 4
from multiprocessing import Process, Queue

class ProcessPool:
    # Initialize the ProcessPool with a number of processes
    def __init__(self, num_processes):
        self.queue = Queue()
        self.processes = [Process(target=self._worker) for _ in range(num_processes)]

    # Start the processes when entering
    def __enter__(self):
        for p in self.processes:
            p.start()
        return self.queue

    # Terminate the processes when exiting
    def __exit__(self, exc_type, exc_val, exc_tb):
        for _ in self.processes:
            self.queue.put(None)
        for p in self.processes:
            p.join()

    # Worker function to process tasks
    def _worker(self):
        while True:
            task = self.queue.get()
            if task is None:
                break
            self.queue.put(task * 2)

    def get_results(self):
        results = []
        while not self.queue.empty():
            results.append(self.queue.get())
        return results
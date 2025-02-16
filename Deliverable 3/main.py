import collections
import threading
import time
import random
import sys

# Memory Management: Paging System
class PagingSystem:
    def __init__(self, memory_size, page_size):
        self.memory_size = memory_size
        self.page_size = page_size
        self.page_table = {}
        self.frames = []
        self.frame_count = memory_size // page_size
        self.page_faults = 0
        self.lru_cache = collections.OrderedDict()

    def access_page(self, process_id, page_number, algorithm="FIFO"):
        key = (process_id, page_number)

        if key in self.page_table:
            if algorithm == "LRU":
                self.lru_cache.move_to_end(key)
            return "Page Hit"

        self.page_faults += 1
        if len(self.frames) >= self.frame_count:
            self.replace_page(algorithm)

        self.frames.append(key)
        self.page_table[key] = True
        if algorithm == "LRU":
            self.lru_cache[key] = True
        return "Page Fault"

    def replace_page(self, algorithm):
        if algorithm == "FIFO":
            evicted_page = self.frames.pop(0)
        elif algorithm == "LRU":
            evicted_page, _ = self.lru_cache.popitem(last=False)
        del self.page_table[evicted_page]
        print(f"Evicted: {evicted_page}")

    def stats(self):
        return {"Page Faults": self.page_faults, "Memory Usage": len(self.frames)}


# Process Synchronization: Producer-Consumer using Semaphores
class ProducerConsumer:
    def __init__(self, buffer_size):
        self.buffer = collections.deque()
        self.buffer_size = buffer_size
        self.empty_slots = threading.Semaphore(buffer_size)
        self.full_slots = threading.Semaphore(0)

    def produce(self, item):
        self.empty_slots.acquire()
        self.buffer.append(item)
        print(f"Produced: {item}")
        self.full_slots.release()

    def consume(self):
        self.full_slots.acquire()
        item = self.buffer.popleft()
        print(f"Consumed: {item}")
        self.empty_slots.release()
        return item

def producer(pc, iterations):
    for _ in range(iterations):
        item = random.randint(1, 100)
        pc.produce(item)
        time.sleep(random.uniform(0.1, 0.5))

def consumer(pc, iterations):
    for _ in range(iterations):
        pc.consume()
        time.sleep(random.uniform(0.1, 0.5))

def exit_shell():
    sys.exit(0)

def main():
    print("Custom Shell. Type 'exit' to quit.")
    # Memory Management Test
    paging = PagingSystem(memory_size=4, page_size=1)
    processes = [(1, 0), (1, 1), (1, 2), (2, 0), (1, 3), (1, 3)]  # (process_id, page_number)

    # Producer-Consumer Test
    pc = ProducerConsumer(buffer_size=5)
    producer_thread = threading.Thread(target=producer, args=(pc, 10))
    consumer_thread = threading.Thread(target=consumer, args=(pc, 10))
    while True:
        try:
            command = input("$ ").strip().split()
            if not command:
                continue

            cmd = command[0]
            args = command[1:]

            if cmd == "paging":
                if args[0] not in ("LRU","FIFO"):
                    print("Only supported LRU or FIFO")
                    continue

                for proc in processes:
                    process_id, page_number = proc
                    print("Paging Process:", process_id, ", Paging Number: ", page_number)
                    print(paging.access_page(*proc, algorithm=args[0]))

                print(paging.stats())
            elif cmd == "smp":
                producer_thread.start()
                consumer_thread.start()
                producer_thread.join()
                consumer_thread.join()
            elif cmd == "exit":
                exit_shell()
        except KeyboardInterrupt:
            print()  # For clean newline after Ctrl+C
        except EOFError:
            print("exit")
            break

# Example Usage
if __name__ == "__main__":
    main()

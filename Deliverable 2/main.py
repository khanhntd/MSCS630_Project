import sys
import time
import heapq
from collections import deque, defaultdict

def exit_shell():
    sys.exit(0)

class Process:
    def __init__(self, pid, name, duration, quantum, scheduling_time):
        self.pid = pid
        self.name = name
        self.remaining_time = duration
        self.quantum = quantum
        self.scheduling_time = scheduling_time

    def run(self):
        time_to_run = min(self.remaining_time, self.quantum)
        print(f"Running process {self.name} for {time_to_run} seconds...")
        time.sleep(time_to_run)
        self.remaining_time -= time_to_run
        return self.remaining_time > 0  # Return True if still running

class RoundRobinScheduler:
    def __init__(self):
        self.queue = deque()
        self.running_process = defaultdict(bool)
        self.waiting_time = defaultdict(float)
        self.response_time = defaultdict(float)
        self.turn_around_time = defaultdict(float)

    def add_process(self, process):
        self.queue.append(process)

    def run(self):
        time_start = time.time()
        while self.queue:
            process = self.queue.popleft()
            if process.pid not in self.running_process:
                self.waiting_time[process.pid] = time.time() - time_start
                self.response_time[process.pid] = time.time() - process.scheduling_time
                print(f"Process {process.name} waiting time is {self.waiting_time[process.pid]}.")
                print(f"Process {process.name} response time is {self.response_time[process.pid]}.")
            if process.run():
                self.running_process[process.pid] = True
                self.queue.append(process)
            else:
                self.turn_around_time[process.pid] = time.time() - process.scheduling_time
                print(f"Process {process.name} completed for {self.turn_around_time[process.pid]}.")

        waiting_time = self.waiting_time.values()
        response_time = self.response_time.values()
        turn_around_time = self.turn_around_time.values()
        print(f"Average waiting time is {sum(waiting_time)/len(waiting_time)}.")
        print(f"Average response time is {sum(response_time)/len(response_time)}.")
        print(f"Average turn around time is {sum(turn_around_time)/len(turn_around_time)}.")

class PriorityProcess:
    def __init__(self, pid, name, duration, quantum, priority, scheduling_time):
        self.pid = pid
        self.name = name
        self.duration = duration
        self.remaining_time = duration
        self.quantum = quantum
        self.priority = priority
        self.scheduling_time = scheduling_time

    def __lt__(self, other):
        return self.priority > other.priority  # Higher priority comes first

    def run(self):
        time_to_run = min(self.remaining_time, self.quantum)
        print(f"Running process {self.name} for {time_to_run} seconds...")
        time.sleep(time_to_run)
        self.remaining_time -= time_to_run
        return self.remaining_time > 0

class PriorityScheduler:
    def __init__(self):
        self.queue = []
        self.running_process = defaultdict(bool)
        self.waiting_time = defaultdict(float)
        self.response_time = defaultdict(float)
        self.turn_around_time = defaultdict(float)

    def add_process(self, process):
        heapq.heappush(self.queue, process)

    def run(self):
        time_start = time.time()
        while self.queue:
            process = heapq.heappop(self.queue)
            if process.pid not in self.running_process:
                self.waiting_time[process.pid] = time.time() - time_start
                self.response_time[process.pid] = time.time() - process.scheduling_time
                print(f"Process {process.name} waiting time is {self.waiting_time[process.pid]}.")
                print(f"Process {process.name} response time is {self.response_time[process.pid]}.")
            if process.run():
                self.running_process[process.pid] = True
                heapq.heappush(self.queue, process)
            else:
                self.turn_around_time[process.pid] = time.time() - process.scheduling_time
                print(f"Process {process.name} completed for {self.turn_around_time[process.pid]}.")

        waiting_time = self.waiting_time.values()
        response_time = self.response_time.values()
        turn_around_time = self.turn_around_time.values()
        print(f"Average waiting time is {sum(waiting_time)/len(waiting_time)}.")
        print(f"Average response time is {sum(response_time)/len(response_time)}.")
        print(f"Average turn around time is {sum(turn_around_time)/len(turn_around_time)}.")

def main():
    print("Custom Shell. Type 'exit' to quit.")
    round_robin_scheduler = RoundRobinScheduler()
    priority_scheduler = PriorityScheduler()

    while True:
        try:
            command = input("$ ").strip().split()
            if not command:
                continue

            cmd = command[0]
            args = command[1:]

            if cmd == "exit":
                exit_shell()
            elif cmd == 'round-robin':
                for i in range(0, len(args), 4):
                    pid = int(args[i])
                    name = args[i + 1]
                    duration = int(args[i + 2])
                    quantum = int(args[i + 3])
                    scheduling_time = time.time()
                    process = Process(pid, name, duration, quantum, scheduling_time)
                    round_robin_scheduler.add_process(process)
                round_robin_scheduler.run()
            elif cmd == 'priority-scheduler':
                for i in range(0, len(args), 5):
                    print(args)
                    pid = int(args[i])
                    name = args[i + 1]
                    duration = int(args[i + 2])
                    quantum = int(args[i + 3])
                    priority = int(args[i + 4])
                    scheduling_time = time.time()
                    process = PriorityProcess(pid, name, duration, quantum, priority, scheduling_time)
                    priority_scheduler.add_process(process)
                priority_scheduler.run()
            else:
                print("Unknown command")
        except KeyboardInterrupt:
            print()  # For clean newline after Ctrl+C
        except EOFError:
            print("exit")
            break

if __name__ == "__main__":
    main()

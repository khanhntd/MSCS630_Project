import os
import sys
import subprocess
import signal

jobs = {}
jobIdCounter = 1

def changeDirectory(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        print(f"cd: no such file or directory: {path}")

def printWorkingDirectory():
    print(os.getcwd())

def exitShell():
    sys.exit(0)

def echoMessage(message):
    print(message)

def clearScreen():
    os.system('clear')

def listDirectory(path="."):
    try:
        for item in os.listdir(path):
            print(item)
    except FileNotFoundError:
        print(f"ls: cannot access '{path}': No such file or directory")

def concatenateFile(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f"cat: {file_path}: No such file or directory")

def makeDirectory(directory_name):
    try:
        os.mkdir(directory_name)
    except FileExistsError:
        print(f"mkdir: cannot create directory '{directory_name}': File exists")

def removeDirectory(directory_name):
    try:
        os.rmdir(directory_name)
    except FileNotFoundError:
        print(f"rmdir: failed to remove '{directory_name}': No such file or directory")
    except OSError:
        print(f"rmdir: failed to remove '{directory_name}': Directory not empty")

def removeFile(file_name):
    try:
        os.remove(file_name)
    except FileNotFoundError:
        print(f"rm: cannot remove '{file_name}': No such file or directory")

def touchFile(file_name):
    with open(file_name, 'a'):
        os.utime(file_name, None)

def killProcess(pid):
    try:
        os.kill(int(pid), signal.SIGKILL)
    except ProcessLookupError:
        print(f"kill: {pid}: No such process")
    except ValueError:
        print(f"kill: {pid}: Invalid process ID")

def jobsList():
    for job_id, (pid, cmd, status) in jobs.items():
        print(f"[{job_id}] {status} {cmd} (PID: {pid})")

def foregroundJob(job_id):
    if job_id in jobs:
        pid, cmd, status = jobs.pop(job_id)
        if status != "Running":
            print(f"fg: job {job_id} is not running.")
        else:
            try:
                # Wait for the job to complete (bring it to the foreground)
                os.waitpid(pid, 0)
                print(f"Foreground: {cmd} (PID: {pid})")
            except ChildProcessError as e:
                print(f"Error: {e}")
    else:
        print(f"fg: no such job: {job_id}")

def backgroundJob(job_id):
    if job_id in jobs:
        pid, cmd, _ = jobs[job_id]
        os.kill(pid, signal.SIGCONT)
        jobs[job_id] = (pid, cmd, "Running")
        print(f"Background: {cmd} (PID: {pid})")
    else:
        print(f"bg: no such job: {job_id}")

def executeCommand(command, background=False):
    global jobIdCounter
    try:
        pid = os.fork()
        if pid == 0:  # Child process
            os.execvp(command[0], command)
        else:  # Parent process
            if background:
                jobs[jobIdCounter] = (pid, " ".join(command), "Running")
                print(f"[{jobIdCounter}] {pid}")
                jobIdCounter += 1
            else:
                os.waitpid(pid, 0)
    except FileNotFoundError:
        print(f"{command[0]}: command not found")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Custom Shell. Type 'exit' to quit.")
    while True:
        try:
            command = input("$ ").strip().split()
            if not command:
                continue

            cmd = command[0]
            args = command[1:]
            background = False

            if args and args[-1] == "&":
                background = True
                args = args[:-1]

            if cmd == "cd":
                changeDirectory(args[0] if args else "~")
            elif cmd == "pwd":
                printWorkingDirectory()
            elif cmd == "exit":
                exitShell()
            elif cmd == "echo":
                echoMessage(" ".join(args))
            elif cmd == "clear":
                clearScreen()
            elif cmd == "ls":
                listDirectory(args[0] if args else ".")
            elif cmd == "cat":
                if args:
                    concatenateFile(args[0])
                else:
                    print("cat: missing file operand")
            elif cmd == "mkdir":
                if args:
                    makeDirectory(args[0])
                else:
                    print("mkdir: missing operand")
            elif cmd == "rmdir":
                if args:
                    removeDirectory(args[0])
                else:
                    print("rmdir: missing operand")
            elif cmd == "rm":
                if args:
                    removeFile(args[0])
                else:
                    print("rm: missing operand")
            elif cmd == "touch":
                if args:
                    touchFile(args[0])
                else:
                    print("touch: missing file operand")
            elif cmd == "kill":
                if args:
                    killProcess(args[0])
                else:
                    print("kill: missing operand")
            elif cmd == "jobs":
                jobsList()
            elif cmd == "fg":
                if args:
                    foregroundJob(int(args[0]))
                else:
                    print("fg: missing job ID")
            elif cmd == "bg":
                if args:
                    backgroundJob(int(args[0]))
                else:
                    print("bg: missing job ID")
            else:
                executeCommand([cmd] + args, background=background)
        except KeyboardInterrupt:
            print()  # For clean newline after Ctrl+C
        except EOFError:
            print("exit")
            break

if __name__ == "__main__":
    main()

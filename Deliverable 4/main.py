import os
import subprocess

# User database (simulation)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# File permissions simulation
FILE_PERMISSIONS = {
    "system.txt": {"admin": "rw", "user": "r"},
    "user_data.txt": {"admin": "rw", "user": "rw"}
}

current_user = None

def authenticate():
    global current_user
    username = input("Username: ")
    password = input("Password: ")
    if username in USERS and USERS[username]["password"] == password:
        current_user = username
        print(f"Welcome, {username} ({USERS[username]['role']})")
    else:
        print("Authentication failed!")
        exit(1)

def check_permission(filename, operation):
    if filename not in FILE_PERMISSIONS:
        print("File does not exist")
        return False

    if current_user not in FILE_PERMISSIONS[filename]:
        print("User does not have permission to view the file")
        return False
    return operation in FILE_PERMISSIONS[filename][current_user]

def execute_command(command):
    parts = command.split("|")
    processes = []
    prev_proc = None

    for part in parts:
        part = part.strip().split()
        if part[0] in ["cat", "rm", "touch"] and len(part) > 1:
            filename = part[-1]
            operation = "r" if part[0] in ("cat") else "w"
            if not check_permission(filename, operation):
                print(f"Permission denied: {current_user} cannot {part[0]} {filename}")
                return

        if prev_proc is None:
            proc = subprocess.Popen(part, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen(part, stdin=prev_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(proc)
        prev_proc = proc

    output, error = processes[-1].communicate()
    print(output.decode())
    if error:
        print(error.decode())

def main():
    authenticate()
    print("Custom Shell. Type 'exit' to quit.")
    while True:
        try:
            command = input(f"{current_user}@shell$ ")
            if command.lower() == "exit":
                break
            execute_command(command)
        except KeyboardInterrupt:
            print()  # For clean newline after Ctrl+C
        except EOFError:
            print("exit")
            break

if __name__ == "__main__":
    main()

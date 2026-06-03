import hashlib
import os

USERS_TXT_PATH = os.path.expanduser("users.txt")
TASKS_TXT_PATH = os.path.expanduser("tasks.txt")


# Register a new user
def register():
    username = input("Enter new username:")

    with open(USERS_TXT_PATH, "r") as f:
        if any(line.split(",")[0] == username for line in f):
            print("Username already exists")
            return

    password = input("Enter new password:")
    hashed_pw = hash_password(password)

    with open(USERS_TXT_PATH, "a") as f:
        f.write(f"{username},{hashed_pw}\n")
    print("Registration successful!")


# User Login
def login():
    username = input("Username: ")
    password = input("Password: ")
    hashed_pw = hash_password(password)

    if os.path.exists(USERS_TXT_PATH):
        with open(USERS_TXT_PATH, "r") as f:
            for line in f:
                u, p = line.strip().split(",")
                if u == username and p == hashed_pw:
                    return username

    print("Invalid credentials.")
    return None


# Add Task
def add_task(user):
    desc = input("Task description: ")
    task_id = str(hash(desc + user))[-5:]  # Simple unique ID
    with open(TASKS_TXT_PATH, "a") as f:
        f.write(f"{user}|{task_id}|{desc}|Pending\n")
    print(f"Task added! (ID: {task_id})")


# View Task
def view_tasks(user):
    print(f"\n--- {user}'s Tasks ---")
    found = False
    with open(TASKS_TXT_PATH, "r") as f:
        for line in f:
            u, tid, desc, status = line.strip().split("|")
            if u == user:
                print(f"[{tid} {desc} - {status}]")
                found = True

    if not found:
        print("No tasks found.")


# Update Task (Mark as Complete/Delete)
def update_task(user, action):
    target_id = input(f"Enter Task ID to {action}: ")
    tasks = []
    updated = False

    with open(TASKS_TXT_PATH, "r") as f:
        for line in f:
            u, tid, desc, status = line.strip().split("|")
            if u == user and tid == target_id:
                if action == "complete":
                    tasks.append(f"{u}|{tid}|{desc}|Completed\n")
                    updated = True
                elif action == "delete":
                    updated = True
                    continue  # Skip adding to keep it deleted
            else:
                tasks.append(line)

    with open(TASKS_TXT_PATH, "w") as f:
        f.writelines(tasks)
    print("Task updated successfully!" if updated else "Task ID not found.")


# User Task Menu
def task_menu(user):
    while True:
        print("\n--- Select a Task Option ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Logout")
        choice = input("Select an option:")
        if choice == "1":
            add_task(user)
        elif choice == "2":
            view_tasks(user)
        elif choice == "3":
            update_task(user, "complete")
        elif choice == "4":
            update_task(user, "delete")
        elif choice == "5":
            break


# main function
def main():
    while True:
        print("\n--- Welcome to TaskManager ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select: ")
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                task_menu(user)
        elif choice == "3":
            break


# Helper Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_files_exist():
    for f in [USERS_TXT_PATH, TASKS_TXT_PATH]:
        if not os.path.exists(f):
            open(f, "w").close()


# Start of the program
if __name__ == "__main__":
    main()

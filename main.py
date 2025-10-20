import os
import sys

DATA_FILE = "data.db"

# Simple in-memory list-based index
# We'll store tuples like (key, value)
index = []


def load_data():
    """Load key-value pairs from data.db file into memory."""
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 2)
            if len(parts) < 3:
                continue
            command, key, value = parts
            if command == "SET":
                # Update index (last write wins)
                for i, (k, _) in enumerate(index):
                    if k == key:
                        index[i] = (key, value)
                        break
                else:
                    index.append((key, value))


def save_data(command, key, value=""):
    """Append command to data.db file."""
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        if command == "SET":
            f.write(f"SET {key} {value}\n")


def handle_set(key, value):
    """Handle SET command"""
    for i, (k, _) in enumerate(index):
        if k == key:
            index[i] = (key, value)
            break
    else:
        index.append((key, value))
    save_data("SET", key, value)


def handle_get(key):
    """Handle GET command"""
    for k, v in reversed(index):
        if k == key:
            print(v)
            return
    print("NULL")


def main():
    load_data()
    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if not line:
            continue

        parts = line.split(" ", 2)
        command = parts[0].upper()

        if command == "EXIT":
            break
        elif command == "SET" and len(parts) == 3:
            handle_set(parts[1], parts[2])
        elif command == "GET" and len(parts) == 2:
            handle_get(parts[1])
        else:
            print("ERROR: Invalid command")


if __name__ == "__main__":
    main()

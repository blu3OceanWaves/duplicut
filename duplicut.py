import os
import hashlib
import argparse
import shutil
import threading
import itertools
import sys
import time
from rich.console import Console
from rich.prompt import Confirm
from rich.text import Text

console = Console()

# Spinner animation
class Spinner:
    def __init__(self, message="Searching..."):
        self.spinner = itertools.cycle(['|', '/', '-', '\\'])
        self.stop_event = threading.Event()
        self.message = message
        self.thread = threading.Thread(target=self.run)

    def run(self):
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r{self.message} {next(self.spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(f"\r{self.message} done!   \n")

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()


def hash_file(path, block_size=65536):
    name = os.path.basename(path)
    home_dir = os.path.expanduser("~")
    if name.startswith('.') and path.startswith(home_dir):
        return None
    if not os.path.isfile(path):
        return None
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha.update(block)
    except (PermissionError, FileNotFoundError, OSError):
        console.print(f"⚠️ Could not read file {path}", style="dim yellow")
        return None
    return sha.hexdigest()


def find_duplicates(directory, recursive=True):
    hashes = {}
    duplicates = []

    if recursive:
        walker = os.walk(directory)
    else:
        walker = [(directory, [], os.listdir(directory))]

    for root, _, files in walker:
        for name in files:
            filepath = os.path.join(root, name)
            filehash = hash_file(filepath)
            if not filehash:
                continue

            if filehash in hashes:
                duplicates.append((filepath, hashes[filehash]))
            else:
                hashes[filehash] = filepath
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Duplicate Finder Tool")
    parser.add_argument("directory", help="Directory to scan for duplicates")
    parser.add_argument("--auto", action="store_true", help="Auto-remove duplicates without asking")
    parser.add_argument("--trash", action="store_true", help="Move to trash instead of permanent delete")
    parser.add_argument("--no-recursion", action="store_true", help="Only scan files in the top-level directory")
    args = parser.parse_args()

    # Print header
    console.print(Text("─────────────────────── 🔍 Duplicut ───────────────────────", style="bold cyan"))
    console.print(f"Arguments -> directory: {args.directory}, auto: {args.auto}, trash: {args.trash}, no-recursion: {args.no_recursion}\n")

    # Start spinner
    spinner = Spinner()
    spinner.start()

    duplicates = find_duplicates(args.directory, recursive=not args.no_recursion)

    # Stop spinner
    spinner.stop()

    if not duplicates:
        console.print(Text("✅ No duplicates found!", style="bold green"))
        console.print(Text("───────────────── EXITING ─────────────────", style="bold cyan"))
        return

    for dup, original in duplicates:
        console.print(f"Duplicate -> {original} == {dup}\n")

        if args.auto:
            choice = True
        else:
            console.print(Text("⚠️ WARNING: Removing files can affect system behavior. Be sure!\n", style="bold red"))
            choice = Confirm.ask("Do you want to remove this duplicate?", default=False)

        if choice:
            try:
                if args.trash:
                    trash_dir = os.path.expanduser("~/.local/share/Trash/files")
                    os.makedirs(trash_dir, exist_ok=True)
                    shutil.move(dup, trash_dir)
                    console.print(Text("🗑️ Moved to Trash\n", style="bold blue"))
                else:
                    os.remove(dup)
                    console.print(Text("🗑️ Removed permanently\n", style="bold red"))
            except Exception as e:
                console.print(Text(f"❌ Could not remove: {e}\n", style="bold red"))

    console.print(Text("───────────────── EXITING ─────────────────", style="bold cyan"))


if __name__ == "__main__":
    main()

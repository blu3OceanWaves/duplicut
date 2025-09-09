# Duplicut - Terminal Duplicate Finder

─────────────────────── 🔍 Duplicut ───────────────────────

## Description

Duplicut is a terminal-based duplicate file finder for Linux. It recursively scans directories to detect duplicate files and optionally allows you to remove them safely.

## Features

* Scans directories recursively or only top-level files.
* Displays duplicate files in a clean format: `file1 == file2`.
* Optional automatic removal of duplicates.
* Option to move duplicates to Trash instead of permanent deletion.
* Terminal-friendly output with Rich styling.
* Warning before removing files to prevent accidental system issues.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/blu3OceanWaves/duplicut.git
cd duplicut
```

2. Ensure Python 3 is installed.
3. Install required dependencies:

```bash
pip install rich
```

## Usage

```bash
python duplicut.py <directory> [--auto] [--trash] [--no-recursion]
```

### Arguments

* `<directory>`: Directory to scan for duplicates.
* `--auto`: Automatically remove duplicates without asking.
* `--trash`: Move duplicates to Trash instead of permanently deleting.
* `--no-recursion`: Only scan files in the top-level directory.

### Example

```bash
python duplicut.py /home/test --no-recursion
```

Output:

```
Arguments -> directory: /home/test, auto: False, trash: False, no-recursion: True
Duplicate -> /home/test/file1 == /home/test/file2
⚠️ WARNING: Removing files can affect system behavior. Be sure!
Do you want to remove this duplicate? [y/n] (n):
───────────────── EXITING ─────────────────
```

## Contact

For bugs, feedback, or questions, connect with me on LinkedIn:  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yassin-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yassin-el-wardioui-34016b332/)

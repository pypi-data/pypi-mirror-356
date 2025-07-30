# Scylla process dumper

**Scylla Process Dumper** is a lightweight and easy-to-use debugging tool designed to create dumps of running processes on Windows using Scylla. It helps developers and analysts capture the state of a process for debugging, reverse engineering, or forensic analysis.

---

## Features

- Dump live Windows processes quickly and reliably
- Simple command-line interface
- Supports dumping by process executable name or path
- Returns process exit code for scripting and automation
- Includes necessary binaries bundled for ease of use

---

## Installation

```bash
python3 -m pip install win32-scdump
```

---

## Usage

Run the scdump command in your terminal or command prompt, specifying the target executable name or path and the desired output filename for the dump.

```bash
scdump target_name.exe output_name.exe
```

target_process.exe — the name or path of the target process you want to dump.

output_dump.exe — the filename where the dumped executable will be saved.


## Example

To create a dump of the Notepad process and save it as notepad_dump.exe, run:

```bash
scdump notepad.exe notepad_dump.exe
```
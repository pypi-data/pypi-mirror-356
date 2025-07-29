![Win32Hooking Logo](https://mauricelambert.github.io/info/python/security/Win32Hooking_small.png "Win32Hooking logo")

# Win32Hooking

## Description

This module hooks IAT and EAT to monitor all external functions calls,
very useful for \[malware\] reverse and debugging.

> This module should run in a virtual machine without any EDR because it hook all exported and imported functions. Hooks may be detected and EDR can kill the process and removes files.
> 
> Some EDR inject DLL in the process and modify some elements to resolve functions by EAT, i wrote a little bypass to run it on a machine with a specific EDR. You can probably use it with an EDR but it's not recommended.

## Requirements

This package require:

 - python3
 - python3 Standard Library
 - PyPeLoader >= 0.2.0
 - PythonToolsKit >= 1.2.4


## Installation

### Pip

```bash
python3 -m pip install Win32Hooking
```

### Git

```bash
git clone "https://github.com/mauricelambert/Win32Hooking.git"
cd "Win32Hooking"
python3 -m pip install .
```

### Wget

```bash
wget https://github.com/mauricelambert/Win32Hooking/archive/refs/heads/main.zip
unzip main.zip
cd Win32Hooking-main
python3 -m pip install .
```

### cURL

```bash
curl -O https://github.com/mauricelambert/Win32Hooking/archive/refs/heads/main.zip
unzip main.zip
cd Win32Hooking-main
python3 -m pip install .
```

## Usages

### Command line

```bash
Win32Hooking              # Using CLI package executable
python3 -m Win32Hooking   # Using python module
python3 Win32Hooking.pyz  # Using python executable
Win32Hooking.exe          # Using python Windows executable

Win32Hooking "C:\Windows\System32\calc.exe"
```

### Python script

```python
from Win32Hooking import load

load(r"C:\Windows\System32\calc.exe")
```

## Links

 - [Pypi](https://pypi.org/project/Win32Hooking)
 - [Github](https://github.com/mauricelambert/Win32Hooking)
 - [Documentation](https://mauricelambert.github.io/info/python/security/Win32Hooking.html)
 - [Python executable](https://mauricelambert.github.io/info/python/security/Win32Hooking.pyz)
 - [Python Windows executable](https://mauricelambert.github.io/info/python/security/Win32Hooking.exe)

## License

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).

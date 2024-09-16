# IbaDatFile
IbaDatFile is a Pythonic wrapper for interacting with iba dat files through the Iba ```ibaFilesLite.dll```. This package simplifies access to the Iba dat file format, making it easier to work with the data in Python.

## Requirements
- Windows-only: This package is designed to work on Windows systems.
- In Python, the ```IbaFilesLite.dll``` COM object can be either 32-bit or 64-bit. To ensure compatibility, you must verify that the architecture of ```IbaFilesLite.dll``` matches your Python installation. For instance, if you're using a 32-bit ```IbaFilesLite.dll```, you need to run a 32-bit version of Python.
- Iba ```ibaFilesLite.dll```: You must have the Iba ```ibaFilesLite.dll``` installed and registered on your system.

## Getting Started
### Register Iba ```ibaFilesLite.dll```
Make sure the Iba ```ibaFilesLite.dll``` is properly registered on your system. You can do this by running the following command when you are in the directory through Command Prompt:


Copy code

```
regsvr32 path\to\ibaFilesLite.dll
```

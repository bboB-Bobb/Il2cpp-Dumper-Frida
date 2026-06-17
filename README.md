# Il2Cpp-Dumper-Frida

A streamlined, automated tool for dumping Unity IL2CPP structures using Frida. This tool features an integrated UI that automatically detects running processes, compiles the injection agent, and handles the dumping process.

## Features
- **Automated Setup:** Automatically installs necessary Python and Node.js dependencies.
- **Process Detection:** Dynamically fetches and lists running processes for easy selection.
- **Automated Compilation:** Handles TypeScript compilation for the Frida agent internally.
- **Organized Output:** Automatically creates isolated output directories and names dumps according to the target process.

## Compatibility
- **Unity Versions:** 5.3.x through 2022.x+
- **IL2CPP Versions:** v24 through v29+
- **Operating System:** Windows 10/11 (x64)

## Important: Anti-Cheat Warning
This tool utilizes Frida for process injection. Frida is actively detected by standard commercial anti-cheat software (e.g., Easy Anti-Cheat, BattlEye, XignCode3). 
If the target application is protected by an anti-cheat, you **must** bypass it or launch the application with the anti-cheat disabled. Failure to do so will result in attachment failures, application crashes, or account bans.

## Setup & Installation
1. Clone or download this repository.
2. Run `setup.bat`. 
   - This script will automatically verify your environment. If Python 3 or Node.js is missing, it will install them silently via Windows Package Manager (`winget`).
   - It will then install the required global Python package (`frida-tools`) and local Node.js packages.
3. If `setup.bat` installs core system dependencies (Python/Node.js), you will be prompted to close the terminal and run `setup.bat` a second time to refresh the system PATH.

## Usage
1. Launch the target game.
2. Run `run.bat` to open the Il2Cpp Dumper UI.
3. Select the target process from the dropdown menu. (Use the refresh button if your process is not listed).
4. Click **Inject & Dump**.
5. Once the dump is complete, the UI will automatically open the `Dumped` directory containing your output.

## Output Format
The dumper generates a `.cs` (C#) file containing reconstructed classes, structs, enums, and memory offsets. This file is saved to the `Dumped/` directory in the project root.

## Troubleshooting
- **Build failed or TS2304 errors:** Ensure you have run `setup.bat` to fetch the `node_modules`.
- **Frida process terminated / Game crashes:** The game's IL2CPP metadata may be heavily obfuscated, or an active anti-cheat is blocking the injection.
- **Automated installation fails:** Run `setup.bat` as an Administrator or temporarily disable aggressive antivirus software that may be blocking `winget` or `npm`.

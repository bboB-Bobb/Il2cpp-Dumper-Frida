# Il2Cpp Dumper

by **Hare** · [@bboB-Bobb](https://github.com/bboB-Bobb) · [YouTube](https://www.youtube.com/@bboB-Bobb)

> 🟢 **Active project** — Actively maintained and up to date.

## Compatibility
- **Unity Versions:** 5.3.x through 2022.x+
- **IL2CPP Versions:** v24 through v29+
- **Operating System:** Windows 10/11 (x64)

## Important
This tool utilizes Frida for process injection. Frida is actively detected by standard commercial anti-cheat software (e.g., Easy Anti-Cheat, BattlEye, XignCode3). 
If the target application is protected by an anti-cheat, you **must** bypass it or launch the application with the anti-cheat disabled. Failure to do so will result in attachment failures, application crashes, or account bans.

## Setup & Installation
1. Clone or download this repository.
2. Run `setup.bat`. 
   - This script will verify your environment and silently install Python 3 and Node.js via Windows Package Manager (`winget`) if they are missing.
   - It will then install the required global Python package (`frida-tools`) and local Node.js packages.
3. If `setup.bat` installs core system dependencies, you will be prompted to close the terminal and run `setup.bat` a second time to refresh the system PATH.

## Usage
1. Launch the target game.
2. Run `run.bat` to open the Il2Cpp Dumper UI.
3. Select the target process from the dropdown menu. (Use the refresh button if your process is not listed).
4. Click **Inject & Dump**.
5. Once the dump is complete, the UI will automatically open the `Dumped` directory containing your output.

## Output Format
The dumper generates a `.cs` (C#) file containing reconstructed classes, structs, enums, and memory offsets. This file is saved to the `Dumped/` directory in the project root.

## Troubleshooting
- **Build failed or TS2304 errors:** Ensure you have run `setup.bat` to fetch dependencies.
- **Frida process terminated / Game crashes:** The game's IL2CPP metadata may be obfuscated, or an active anti-cheat is blocking the injection.
- **Automated installation fails:** Run `setup.bat` as an Administrator or temporarily disable aggressive antivirus software.

If you cannot solve an issue, please open a ticket here:
https://github.com/bboB-Bobb/Il2cpp-Dumper-Frida/issues

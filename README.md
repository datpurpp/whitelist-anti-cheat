# Custom Whitelist Anti-Cheat 🛡️

An open-source Python security utility that implements a strict whitelisting philosophy to prevent game modifications and injection hacks. Instead of searching for known cheat signatures, this program explicitly defines and permits only the original, authentic physics, animations, and movement logic of the base game. Anything outside of these specific boundaries is instantly blacklisted, triggering an automatic session kick and compiling security logs.

## 🚀 Features
* **Whitelisting Architecture:** Only permits validated player movements and natural game conditions.
* **Anomaly Detection:** Tracks pixel movement steps and physics thresholds to instantly catch teleportation or speed hacks.
* **Session Management:** Gracefully kicks players when a physics manipulation or modified item/weapon is detected.
* **Open Source Template:** Built with a clean interface layout (such as Tkinter), serving as an upgradeable foundation for security-focused developer projects.

## ⚙️ How the Logic Works
The anti-cheat constantly monitors game state variables against an approved baseline rulebook:

* **Natural Inputs:** Basic directional movement (e.g., normal arrow key movement within standard step boundaries) is completely allowed.
* **Injection Exploits:** If a client manipulates packets or memory to suddenly shift 150 pixels instead of the legal 10-pixel maximum, an anomaly flag triggers.
* **Modification Blocks:** Attempts to load unauthorized items, one-shot weapons, or illegal wall collisions instantly invalidate the whitelist match.

## 💻 Getting Started

### Prerequisites
Make sure you have Python installed on your system.

### Installation
1. download
   ```
2. Navigate into the project folder:
   
   cd foldername
   ```

### Running the Script
open windows powershell nd run the command:

python anticheat.py
```

## 🛠️ Contributing & Upgrades
This repository is built to be an educational framework meant for upgrades and further development! Developers are encouraged to fork the code to implement advanced packet verification, hooks for dedicated engines, or persistent database security logging. 

Contributions are highly welcome. Feel free to open an issue or submit a **Pull Request** with your performance optimizations.

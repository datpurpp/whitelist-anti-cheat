import os
import time
import tkinter as tk
from tkinter import messagebox

class AntiCheatDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Behavioral Whitelist Anti-Cheat Demo")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Game Configuration & Whitelist Constants
        self.NORMAL_SPEED = 20 
        self.MAX_ALLOWED_DISTANCE = 25  # The whitelist boundary per frame
        self.is_banned = False

        # Initial Player State
        self.player_x = 300
        self.player_y = 200

        # UI Setup
        self.setup_ui()

        # Bind Legitimate Controls (Whitelisted Input)
        self.root.bind("<Up>", lambda e: self.move_player(0, -self.NORMAL_SPEED))
        self.root.bind("<Down>", lambda e: self.move_player(0, self.NORMAL_SPEED))
        self.root.bind("<Left>", lambda e: self.move_player(-self.NORMAL_SPEED, 0))
        self.root.bind("<Right>", lambda e: self.move_player(self.NORMAL_SPEED, 0))

    def setup_ui(self):
        # Game Canvas
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e", width=580, height=350)
        self.canvas.pack(pady=10)

        # Draw Player (Green Square)
        self.player_render = self.canvas.create_rectangle(
            self.player_x - 15, self.player_y - 15, 
            self.player_x + 15, self.player_y + 15, 
            fill="#4CAF50", outline=""
        )

        # Instructions Label
        instructions = (
            "VALID CONTROLS: Use the 4 Arrow Keys to move normally.\n"
            "The Anti-Cheat whitelists a maximum movement of 25 units per action."
        )
        self.lbl_info = tk.Label(self.root, text=instructions, justify="center", font=("Arial", 10))
        self.lbl_info.pack(pady=5)

        # Simulate Cheat Injection Button
        self.btn_cheat = tk.Button(
            self.root, 
            text="Simulate Injection: Trigger 'Teleport Hack' (Move 150px)", 
            bg="#f44336", fg="white", font=("Arial", 10, "bold"),
            command=self.trigger_teleport_cheat
        )
        self.btn_cheat.pack(pady=10)

    def move_player(self, delta_x, delta_y):
        """Processes player movement and runs it through the whitelist validator."""
        if self.is_banned:
            return

        # Calculate the intended destination
        new_x = self.player_x + delta_x
        new_y = self.player_y + delta_y

        # Run State Validation (The Whitelist Verification)
        if self.validate_state_whitelist(self.player_x, self.player_y, new_x, new_y):
            # If valid, update state and render
            self.player_x = new_x
            self.player_y = new_y
            self.canvas.coords(
                self.player_render, 
                self.player_x - 15, self.player_y - 15, 
                self.player_x + 15, self.player_y + 15
            )
        else:
            # If state falls outside the whitelist -> Flag, Kick, and Report
            self.enforce_kick_and_report(delta_x, delta_y)

    def validate_state_whitelist(self, old_x, old_y, new_x, new_y):
        """
        Whitelisting Philosophy Core: 
        Instead of checking for a specific cheat signature, we check if the math 
        matches known legal parameters. If the distance is physically impossible, it's a cheat.
        """
        # Calculate straight-line distance traveled
        distance_moved = ((new_x - old_x) ** 2 + (new_y - old_y) ** 2) ** 0.5
        
        # Whitelist Check
        if distance_moved <= self.MAX_ALLOWED_DISTANCE:
            return True
        return False

    def trigger_teleport_cheat(self):
        """Simulates an external modification pushing a state directly into the game."""
        # Force a massive illegal movement directly into the controller handler
        self.move_player(150, 0)

    def enforce_kick_and_report(self, invalid_dx, invalid_dy):
        """Locks the client game state, kicks the user, and dumps security telemetry."""
        self.is_banned = True
        self.canvas.itemconfig(self.player_render, fill="#ff0000") # Turn player red
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        report_filename = "anticheat_security_report.txt"

        # Generate local security telemetry dump
        report_data = (
            f"=== ANTI-CHEAT SECURITY TELEMETRY REPORT ===\n"
            f"Timestamp: {timestamp}\n"
            f"Violation Type: Illegal Client Position Delta (Speed/Teleport Injection)\n"
            f"Action Enforced: Connection Terminated & Hardware Flagged\n"
            f"-----------------------------------------\n"
            f"Baseline Maximum Step Allowed: {self.MAX_ALLOWED_DISTANCE} units\n"
            f"Attempted Client Step Request: X-Delta: {invalid_dx}, Y-Delta: {invalid_dy}\n"
            f"Status: FAIL (Anomaly Detected Outside Whitelist Parameters)\n"
            f"=========================================\n"
        )

        with open(report_filename, "w") as f:
            f.write(report_data)

        # Kick notice to client interface
        messagebox.showerror(
            "CONNECTION TERMINATED", 
            f"You have been kicked from the session.\n\n"
            f"Reason: Game state anomaly detected.\n"
            f"Security logs compiled in: {os.path.abspath(report_filename)}"
        )
        
        # Terminate game process gracefully
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = AntiCheatDemo(window)
    window.mainloop()

import customtkinter as ctk
import json
import sys
import os
import traceback
import subprocess
from datetime import datetime

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, "bsod_config.json")
    stock_mode = "--stock" in sys.argv

    if stock_mode:
        config = {
            "face_text": ":(",
            "face_size": 96,
            "text_size": 26,
            "stop_code": "CRITICAL_PROCESS_DIED",
            "percentage": 100,
            "bg_color": "#0078D7",
            "enable_shutdown": False,
            "message": (
                "Your PC ran into a problem and needs to restart.\n"
                "We're just collecting some error info, and then we'll shut down."
            ),
            "is_old": False,
            "classic_font": "Lucida Console"
        }
    else:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        # Fill missing keys with defaults
        defaults = {
            "face_text": ":(",
            "face_size": 96,
            "text_size": 26,
            "stop_code": "CRITICAL_PROCESS_DIED",
            "percentage": 100,
            "bg_color": "#0078D7",
            "enable_shutdown": False,
            "message": "Your PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll shut down.",
            "is_old": False,
            "classic_font": "Lucida Console"
        }
        for k, v in defaults.items():
            if k not in config:
                config[k] = v

    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.attributes("-fullscreen", True)
    app.overrideredirect(True)
    app.attributes("-topmost", True)
    app.configure(fg_color=config.get("bg_color", "#0078D7"))

    container = ctk.CTkFrame(app, fg_color=config.get("bg_color", "#0078D7"))
    container.pack(fill="both", expand=True)
    left = ctk.CTkFrame(container, fg_color=config.get("bg_color", "#0078D7"))
    left.pack(anchor="nw", padx=80, pady=80)

    if config.get("is_old", False):
        body = ctk.CTkLabel(
            left,
            text=(
                "A problem has been detected and Windows has been shut down to prevent damage\n"
                "to your computer.\n\n"
                "The problem seems to be caused by the following file: FAKE_DRIVER.SYS\n\n"
                "PAGE_FAULT_IN_NONPAGED_AREA\n\n"
                "If this is the first time you've seen this Stop error screen,\n"
                "restart your computer. If this screen appears again, follow\n"
                "these steps:\n\n"
                "Check to make sure any new hardware or software is properly installed.\n"
                "If this is a new installation, ask your hardware or software manufacturer\n"
                "for any Windows updates you might need.\n\n"
                "If problems continue, disable or remove any newly installed hardware\n"
                "or software. Disable BIOS memory options such as caching or shadowing.\n"
                "If you need to use Safe Mode to remove or disable components, restart\n"
                "your computer, press F8 to select Advanced Startup Options, and then\n"
                "select Safe Mode.\n\n"
                "Technical Information:\n"
                "*** STOP: 0x00000050 (0xFFFFF880009AA000, 0x0000000000000000, 0xFFFFF80002ACD123, 0x0000000000000000)\n"
                "*** FAKE_DRIVER.SYS - Address FFFFF880009AA000 base at FFFFF880009A0000, DateStamp 4a5bc11e"
            ),
            text_color="white",
            font=(config.get("classic_font", "Lucida Console"), 16, "bold"),
            justify="left"
        )
        body.pack(anchor="nw")
    else:
        face = ctk.CTkLabel(
            left,
            text=config.get("face_text", ":("),
            text_color="white",
            font=("Segoe UI", config.get("face_size", 96))
        )
        face.pack(anchor="nw", pady=(0, 20))
        body = ctk.CTkLabel(
            left,
            text=(
                config.get("message", "") + "\n\n"
                f"Stop code: {config.get('stop_code', 'UNKNOWN_ERROR')}\n\n"
                f"{config.get('percentage', 100)}% complete"
            ),
            text_color="white",
            font=("Segoe UI", config.get("text_size", 26)),
            justify="left"
        )
        body.pack(anchor="nw")

    def kill_switch(event=None):
        app.destroy()
        sys.exit(0)

    app.bind("<Control-Shift-q>", kill_switch)
    app.bind("<Control-Shift-Q>", kill_switch)

    if config.get("enable_shutdown", False) and not stock_mode:
        app.after(3000, lambda: subprocess.run(["shutdown", "/s", "/t", "30"]))

    app.mainloop()

except Exception as e:
    log_path = os.path.join(os.path.dirname(__file__), "bsod_error.log")
    with open(log_path, "a") as log:
        log.write("\n===== BSOD Crash Log =====\n")
        log.write(str(datetime.now()) + "\n")
        log.write(traceback.format_exc())
        log.write("\n")
    print("An error occurred while running the BSOD app. Details have been logged to bsod_error.log.")
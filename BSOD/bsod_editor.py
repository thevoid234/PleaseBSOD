import customtkinter as ctk
from tkinter import colorchooser, messagebox
import json
import os

# ------------------------
# CONFIG
# ------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "bsod_config.json")

def load_config():
    default_config = {
        "face_text": ":(",
        "message": "Your PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll shut down.",
        "bg_color": "#0078D7",
        "text_color": "#FFFFFF",
        "face_size": 96,
        "text_size": 26,
        "stop_code": "CRITICAL_PROCESS_DIED",
        "percentage": 100,
        "enable_shutdown": False,
        "is_old": False,
        "classic_font": "Lucida Console"
    }
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    for k, v in default_config.items():
        if k not in data:
            data[k] = v
    return data

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_config()

# ------------------------
# APP SETUP
# ------------------------
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("BSOD Editor")
app.geometry("1100x650")
app.configure(fg_color="#c0c0c0")
app.overrideredirect(True)

# Windows 98 colors
WIN98_GRAY = "#c0c0c0"
WIN98_DARK = "#808080"
WIN98_LIGHT = "#dfdfdf"
WIN98_TITLE_BLUE = "#000080"
WIN98_BORDER = "#000000"

# ------------------------
# CUSTOM TITLE BAR
# ------------------------
title_bar = ctk.CTkFrame(app, fg_color=WIN98_TITLE_BLUE, height=24, border_width=2, border_color=WIN98_BORDER)
title_bar.pack(side="top", fill="x")
title_bar.pack_propagate(False)

title_label = ctk.CTkLabel(
    title_bar,
    text="BSOD Editor",
    text_color="white",
    font=("MS Sans Serif", 11, "bold")
)
title_label.pack(side="left", padx=6, pady=2)

def start_move(event):
    app._drag_start_x = event.x
    app._drag_start_y = event.y

def do_move(event):
    x = app.winfo_x() + event.x - getattr(app, '_drag_start_x', 0)
    y = app.winfo_y() + event.y - getattr(app, '_drag_start_y', 0)
    app.geometry(f"+{x}+{y}")

title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)
title_label.bind("<Button-1>", start_move)
title_label.bind("<B1-Motion>", do_move)

button_frame = ctk.CTkFrame(title_bar, fg_color=WIN98_TITLE_BLUE)
button_frame.pack(side="right", padx=2, pady=2)

def create_title_button(parent, text, command):
    btn = ctk.CTkButton(
        parent,
        text=text,
        width=24,
        height=22,
        font=("MS Sans Serif", 10, "bold"),
        fg_color=WIN98_GRAY,
        text_color="black",
        hover_color=WIN98_LIGHT,
        border_color=WIN98_DARK,
        border_width=1,
        command=command
    )
    btn.pack(side="left", padx=1)
    return btn

minimize_btn = create_title_button(button_frame, "_", lambda: app.iconify())
maximize_btn = create_title_button(button_frame, "□", lambda: None)
close_btn = create_title_button(button_frame, "×", lambda: app.quit())

# ------------------------
# MAIN CONTENT
# ------------------------
main_frame = ctk.CTkFrame(app, fg_color=WIN98_GRAY, border_width=2, border_color=WIN98_BORDER)
main_frame.pack(fill="both", expand=True, padx=2, pady=(0,2))

controls = ctk.CTkFrame(main_frame, fg_color=WIN98_GRAY, border_width=1, border_color=WIN98_DARK)
controls.pack(side="left", fill="y", padx=10, pady=10)

scroll_frame = ctk.CTkScrollableFrame(controls, fg_color=WIN98_GRAY)
scroll_frame.pack(fill="both", expand=True, padx=2, pady=2)

preview_panel = ctk.CTkFrame(main_frame, fg_color=WIN98_GRAY, border_width=1, border_color=WIN98_DARK)
preview_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

preview_label = ctk.CTkLabel(
    preview_panel,
    text="Preview",
    font=("MS Sans Serif", 10, "bold"),
    text_color="black"
)
preview_label.pack(anchor="w", pady=(0, 5), padx=8)

preview_frame = ctk.CTkFrame(preview_panel, fg_color="white", border_width=2, border_color=WIN98_DARK)
preview_frame.pack(fill="both", expand=True, padx=8, pady=8)

# ------------------------
# CONTROL ELEMENTS
# ------------------------
def create_entry(label, value, width=180):
    label_widget = ctk.CTkLabel(
        scroll_frame,
        text=label,
        font=("MS Sans Serif", 9),
        text_color="black"
    )
    label_widget.pack(anchor="w", pady=(8, 2))
    entry = ctk.CTkEntry(
        scroll_frame,
        font=("MS Sans Serif", 9),
        fg_color="white",
        border_color=WIN98_DARK,
        border_width=1,
        width=width
    )
    entry.insert(0, str(value))
    entry.pack(fill="x", pady=(0, 5))
    return entry

face_entry = create_entry("Face Text", config.get("face_text", ":("))
face_size_entry = create_entry("Face Size", config.get("face_size", 96))
text_size_entry = create_entry("Text Size", config.get("text_size", 26))
stop_code_entry = create_entry("Stop Code", config.get("stop_code", "CRITICAL_PROCESS_DIED"))
percentage_entry = create_entry("Percentage", config.get("percentage", 100))

bg_label = ctk.CTkLabel(
    scroll_frame,
    text="Background Color",
    font=("MS Sans Serif", 9),
    text_color="black"
)
bg_label.pack(anchor="w", pady=(8, 2))

bg_frame = ctk.CTkFrame(scroll_frame, fg_color=WIN98_GRAY)
bg_frame.pack(fill="x", pady=(0, 5))

bg_entry = ctk.CTkEntry(
    bg_frame,
    font=("MS Sans Serif", 9),
    fg_color="white",
    border_color=WIN98_DARK,
    border_width=1
)
bg_entry.insert(0, config.get("bg_color", "#0078D7"))
bg_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

def choose_color():
    color = colorchooser.askcolor(title="Pick Background Color")
    if color[1]:
        bg_entry.delete(0, "end")
        bg_entry.insert(0, color[1])
        update_preview()

color_button = ctk.CTkButton(
    bg_frame,
    text="...",
    width=40,
    font=("MS Sans Serif", 9),
    fg_color=WIN98_GRAY,
    text_color="black",
    hover_color=WIN98_LIGHT,
    border_color=WIN98_DARK,
    border_width=1,
    command=choose_color
)
color_button.pack(side="right")

shutdown_label = ctk.CTkLabel(
    scroll_frame,
    text="System Settings",
    font=("MS Sans Serif", 9, "bold"),
    text_color="black"
)
shutdown_label.pack(anchor="w", pady=(10, 5))

shutdown_var = ctk.BooleanVar(value=config.get("enable_shutdown", False))
shutdown_checkbox = ctk.CTkCheckBox(
    scroll_frame,
    text="Enable Shutdown",
    variable=shutdown_var,
    font=("MS Sans Serif", 9),
    text_color="black"
)
shutdown_checkbox.pack(anchor="w", pady=3)

style_label = ctk.CTkLabel(
    scroll_frame,
    text="BSOD Style",
    font=("MS Sans Serif", 9, "bold"),
    text_color="black"
)
style_label.pack(anchor="w", pady=(10, 5))

is_old_var = ctk.BooleanVar(value=config.get("is_old", False))
modern_radio = ctk.CTkRadioButton(
    scroll_frame,
    text="Modern (Windows 8/10/11)",
    variable=is_old_var,
    value=False,
    font=("MS Sans Serif", 9),
    text_color="black"
)
modern_radio.pack(anchor="w")
classic_radio = ctk.CTkRadioButton(
    scroll_frame,
    text="Classic (Windows XP/Vista/7/98)",
    variable=is_old_var,
    value=True,
    font=("MS Sans Serif", 9),
    text_color="black"
)
classic_radio.pack(anchor="w")

classic_font_label = ctk.CTkLabel(
    scroll_frame,
    text="Classic BSOD Font",
    font=("MS Sans Serif", 9),
    text_color="black"
)
classic_font_label.pack(anchor="w", pady=(8, 2))

classic_font_entry = ctk.CTkEntry(
    scroll_frame,
    font=("MS Sans Serif", 9),
    fg_color="white",
    border_color=WIN98_DARK,
    border_width=1
)
classic_font_entry.insert(0, config.get("classic_font", "Lucida Console"))
classic_font_entry.pack(fill="x", pady=(0, 5))

button_panel = ctk.CTkFrame(scroll_frame, fg_color=WIN98_GRAY)
button_panel.pack(fill="x", pady=(15, 0))

def validate_int(entry, name, minval=1, maxval=999):
    try:
        val = int(entry.get())
        if not (minval <= val <= maxval):
            raise ValueError
        return val
    except Exception:
        messagebox.showerror("Invalid Input", f"{name} must be an integer between {minval} and {maxval}.")
        return None

def save_and_quit():
    if not save():
        return
    app.quit()

def save():
    face_size = validate_int(face_size_entry, "Face Size", 10, 400)
    text_size = validate_int(text_size_entry, "Text Size", 8, 100)
    percentage = validate_int(percentage_entry, "Percentage", 0, 100)
    if face_size is None or text_size is None or percentage is None:
        return False
    new_config = {
        "face_text": face_entry.get(),
        "face_size": face_size,
        "text_size": text_size,
        "stop_code": stop_code_entry.get(),
        "percentage": percentage,
        "bg_color": bg_entry.get(),
        "enable_shutdown": shutdown_var.get(),
        "message": "Your PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll shut down.",
        "is_old": is_old_var.get(),
        "classic_font": classic_font_entry.get()
    }
    save_config(new_config)
    update_preview()
    return True

save_button = ctk.CTkButton(
    button_panel,
    text="Save",
    font=("MS Sans Serif", 9),
    fg_color=WIN98_GRAY,
    text_color="black",
    hover_color=WIN98_LIGHT,
    border_color=WIN98_DARK,
    border_width=1,
    command=save,
    width=80
)
save_button.pack(pady=3)

save_quit_button = ctk.CTkButton(
    button_panel,
    text="Save & Quit",
    font=("MS Sans Serif", 9),
    fg_color=WIN98_GRAY,
    text_color="black",
    hover_color=WIN98_LIGHT,
    border_color=WIN98_DARK,
    border_width=1,
    command=save_and_quit,
    width=80
)
save_quit_button.pack(pady=3)

# ------------------------
# LIVE PREVIEW
# ------------------------
def update_preview(*args):
    for widget in preview_frame.winfo_children():
        widget.destroy()
    bg = bg_entry.get()
    preview_frame.configure(fg_color=bg)
    if is_old_var.get():
        body_label = ctk.CTkLabel(
            preview_frame,
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
            font=(classic_font_entry.get(), 16, "bold"),
            justify="left"
        )
        body_label.pack(anchor="nw", padx=40, pady=(40, 10))
    else:
        face_label = ctk.CTkLabel(
            preview_frame,
            text=face_entry.get(),
            text_color="white",
            font=("Segoe UI", int(face_size_entry.get()))
        )
        face_label.pack(anchor="nw", padx=40, pady=(40, 10))
        body_label = ctk.CTkLabel(
            preview_frame,
            text=(
                "Your PC ran into a problem and needs to restart.\n"
                "We're just collecting some error info, and then we'll shut down.\n\n"
                f"Stop code: {stop_code_entry.get()}\n\n"
                f"{percentage_entry.get()}% complete"
            ),
            text_color="white",
            font=("Segoe UI", int(text_size_entry.get())),
            justify="left"
        )
        body_label.pack(anchor="nw", padx=40)

for entry in [face_entry, face_size_entry, text_size_entry, stop_code_entry, percentage_entry]:
    entry.bind("<KeyRelease>", update_preview)
bg_entry.bind("<KeyRelease>", update_preview)
classic_font_entry.bind("<KeyRelease>", update_preview)
modern_radio.configure(command=update_preview)
classic_radio.configure(command=update_preview)
update_preview()

# ------------------------
# MAIN LOOP
# ------------------------
app.mainloop()

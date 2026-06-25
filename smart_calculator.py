"""
NextHikes IT Solutions - Project 2 (Smart Edition): Scientific Calculator
A GUI calculator built with Tkinter supporting:
  - Basic arithmetic
  - Scientific functions (trig, log, sqrt, power, factorial, constants)
  - Keyboard input
  - Calculation history (clickable to reuse)
  - Memory functions (M+, M-, MR, MC)
"""

import tkinter as tk
import math

# ------------------ State ------------------

memory_value = 0.0

# ------------------ Core Logic Functions ------------------

def update_display(value):
    """Append a value (number/operator/function) to the display."""
    current = entry_var.get()
    entry_var.set(current + str(value))


def clear_display():
    """Clear the display screen."""
    entry_var.set("")


def backspace():
    """Remove the last character from the display."""
    current = entry_var.get()
    entry_var.set(current[:-1])


def get_safe_context():
    """Restricted namespace for eval — only math helpers, no builtins."""
    return {
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "log": math.log10,
        "ln": math.log,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "fact": math.factorial,
        "abs": abs,
        "__builtins__": {}
    }


def calculate_result(event=None):
    """Evaluate the expression in the display, show result, log to history."""
    expression = entry_var.get()
    if not expression:
        return
    try:
        result = eval(expression, get_safe_context())
        entry_var.set(str(result))
        add_to_history(expression, str(result))
    except ZeroDivisionError:
        entry_var.set("Error: Div by 0")
    except Exception:
        entry_var.set("Error")


def apply_function(func_name):
    current = entry_var.get()
    entry_var.set(current + func_name + "(")


def apply_power():
    update_display("**")


def apply_factorial():
    current = entry_var.get()
    entry_var.set(f"fact({current})")


# ------------------ History ------------------

def add_to_history(expression, result):
    history_list.insert(tk.END, f"{expression} = {result}")
    history_list.yview(tk.END)  # auto-scroll to latest


def use_history_item(event):
    selection = history_list.curselection()
    if not selection:
        return
    text = history_list.get(selection[0])
    expression = text.split(" = ")[0]
    entry_var.set(expression)


def clear_history():
    history_list.delete(0, tk.END)


# ------------------ Memory ------------------

def memory_add():
    global memory_value
    try:
        memory_value += float(eval(entry_var.get(), get_safe_context()))
        memory_label.config(text=f"M: {memory_value}")
    except Exception:
        entry_var.set("Error")


def memory_subtract():
    global memory_value
    try:
        memory_value -= float(eval(entry_var.get(), get_safe_context()))
        memory_label.config(text=f"M: {memory_value}")
    except Exception:
        entry_var.set("Error")


def memory_recall():
    update_display(memory_value)


def memory_clear():
    global memory_value
    memory_value = 0.0
    memory_label.config(text="M: 0")


# ------------------ Mode Toggle ------------------

def toggle_mode():
    if sci_frame.winfo_ismapped():
        sci_frame.grid_remove()
        toggle_btn.config(text="Scientific Mode \u25BC")
        root.geometry("420x520")
    else:
        sci_frame.grid()
        toggle_btn.config(text="Basic Mode \u25B2")
        root.geometry("420x660")


# ------------------ Keyboard Support ------------------

def on_key_press(event):
    char = event.char
    keysym = event.keysym

    if char in "0123456789.+-*/()":
        update_display(char)
    elif keysym == "Return" or keysym == "KP_Enter":
        calculate_result()
    elif keysym == "BackSpace":
        backspace()
    elif keysym == "Escape":
        clear_display()
    elif char == "^":
        apply_power()


# ------------------ GUI Setup ------------------

root = tk.Tk()
root.title("Smart Scientific Calculator")
root.geometry("420x520")
root.resizable(False, False)
root.bind("<Key>", on_key_press)

entry_var = tk.StringVar()

# Top container: calculator (left) + history (right)
top_container = tk.Frame(root)
top_container.pack(expand=True, fill="both", padx=10, pady=10)

calc_side = tk.Frame(top_container)
calc_side.pack(side="left", expand=True, fill="both")

history_side = tk.Frame(top_container, width=140)
history_side.pack(side="right", fill="y", padx=(8, 0))

# ---- Display ----
display = tk.Entry(
    calc_side,
    textvariable=entry_var,
    font=("Arial", 20),
    justify="right",
    bd=8,
    relief=tk.RIDGE
)
display.pack(fill="x", pady=(0, 5), ipady=12)

# ---- Memory row ----
memory_frame = tk.Frame(calc_side)
memory_frame.pack(fill="x", pady=(0, 5))

memory_label = tk.Label(memory_frame, text="M: 0", font=("Arial", 9), anchor="w")
memory_label.pack(side="left", padx=2)

for label, cmd in [("MC", memory_clear), ("MR", memory_recall),
                    ("M+", memory_add), ("M-", memory_subtract)]:
    tk.Button(memory_frame, text=label, font=("Arial", 9), width=4, command=cmd).pack(side="right", padx=2)

# ---- Toggle button ----
toggle_btn = tk.Button(calc_side, text="Scientific Mode \u25BC", font=("Arial", 10),
                        command=toggle_mode)
toggle_btn.pack(fill="x", pady=(0, 5))

# ---- Main button container ----
main_frame = tk.Frame(calc_side)
main_frame.pack(expand=True, fill="both")
main_frame.grid_columnconfigure(0, weight=1)

# Scientific panel (hidden by default)
sci_frame = tk.Frame(main_frame)
sci_frame.grid(row=0, column=0, sticky="nsew")
sci_frame.grid_remove()

sci_buttons = [
    ("sin", lambda: apply_function("sin")),
    ("cos", lambda: apply_function("cos")),
    ("tan", lambda: apply_function("tan")),
    ("log", lambda: apply_function("log")),
    ("ln", lambda: apply_function("ln")),
    ("sqrt", lambda: apply_function("sqrt")),
    ("x^y", apply_power),
    ("x!", apply_factorial),
    ("\u03c0", lambda: update_display("pi")),
    ("e", lambda: update_display("e")),
    ("(", lambda: update_display("(")),
    (")", lambda: update_display(")")),
]

for i in range(4):
    sci_frame.grid_columnconfigure(i, weight=1)

for idx, (label, cmd) in enumerate(sci_buttons):
    r, c = divmod(idx, 4)
    sci_frame.grid_rowconfigure(r, weight=1)
    tk.Button(sci_frame, text=label, font=("Arial", 13), command=cmd).grid(
        row=r, column=c, sticky="nsew", padx=3, pady=3
    )

# Basic panel
btn_frame = tk.Frame(main_frame)
btn_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 0))

buttons = [
    ["7", "8", "9", "+"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "*"],
    ["c", "0", "=", "/"],
    [".", "<-", "", ""],
]

for i in range(len(buttons)):
    btn_frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    btn_frame.grid_columnconfigure(i, weight=1)


def make_command(label):
    if label == "c":
        return clear_display
    elif label == "=":
        return calculate_result
    elif label == "<-":
        return backspace
    elif label == "":
        return lambda: None
    else:
        return lambda: update_display(label)


for row_index, row in enumerate(buttons):
    for col_index, label in enumerate(row):
        if label == "":
            continue
        btn = tk.Button(
            btn_frame,
            text=label,
            font=("Arial", 16),
            command=make_command(label)
        )
        btn.grid(row=row_index, column=col_index, sticky="nsew", padx=4, pady=4)

main_frame.grid_rowconfigure(1, weight=1)

# ---- History panel ----
tk.Label(history_side, text="History", font=("Arial", 11, "bold")).pack(anchor="w")

history_list = tk.Listbox(history_side, font=("Arial", 9), width=20)
history_list.pack(expand=True, fill="both", pady=(2, 5))
history_list.bind("<Double-Button-1>", use_history_item)

tk.Button(history_side, text="Clear History", font=("Arial", 9), command=clear_history).pack(fill="x")

root.mainloop()

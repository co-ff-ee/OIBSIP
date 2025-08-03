import tkinter as tk
from tkinter import messagebox
import string
import random
import pyperclip
from datetime import datetime

def generate_password():
    try:
        length = int(length_entry.get())
        use_letters = letters_var.get()
        use_digits = digits_var.get()
        use_symbols = symbols_var.get()
        exclude_ambiguous = exclude_var.get()

        characters = ''
        if use_letters:
            characters += string.ascii_letters
        if use_digits:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        if exclude_ambiguous:
            ambiguous = 'ilLIoO01'
            characters = ''.join(c for c in characters if c not in ambiguous)

        if not characters:
            messagebox.showerror("Error", "No character types selected.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        # Copy to clipboard
        pyperclip.copy(password)

        # Save to log file
        with open("password_log.txt", "a") as file:
            file.write(f"{datetime.now()} - {password}\n")

        # Strength feedback
        strength = evaluate_strength(password)
        strength_label.config(text=f"Strength: {strength}")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

def evaluate_strength(pw):
    score = 0
    if any(c.islower() for c in pw): score += 1
    if any(c.isupper() for c in pw): score += 1
    if any(c.isdigit() for c in pw): score += 1
    if any(c in string.punctuation for c in pw): score += 1
    if len(pw) >= 12: score += 1

    if score >= 4:
        return "Strong"
    elif score == 3:
        return "Medium"
    else:
        return "Weak"

# GUI setup
root = tk.Tk()
root.title("🔐 Advanced Password Generator")
root.geometry("400x400")
root.resizable(False, False)

# UI elements
tk.Label(root, text="Enter password length:").pack(pady=5)
length_entry = tk.Entry(root)
length_entry.pack()

letters_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Include Letters", variable=letters_var).pack()

digits_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Include Digits", variable=digits_var).pack()

symbols_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Include Symbols", variable=symbols_var).pack()

exclude_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Exclude ambiguous characters (1/l/I/0/O)", variable=exclude_var).pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)

password_entry = tk.Entry(root, font=("Courier", 14), justify='center')
password_entry.pack(pady=10)

strength_label = tk.Label(root, text="Strength: ", font=("Arial", 12))
strength_label.pack()

tk.Label(root, text="Password copied to clipboard and saved.").pack(pady=5)

root.mainloop()

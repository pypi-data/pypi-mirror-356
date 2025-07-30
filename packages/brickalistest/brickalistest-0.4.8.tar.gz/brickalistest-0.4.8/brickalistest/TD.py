# testdrive/td.py

import tkinter as tk


def main():
    """
    Launch a simple Tkinter window with the text "Test Drive" centered.
    """
    root = tk.Tk()
    root.title("Test Drive")
    root.configure(bg="#3498db")

    label = tk.Label(
        root,
        text="Test Drive",
        font=("Helvetica", 24, "bold"),
        bg="#3498db",
        fg="white"
    )
    label.pack(expand=True)
    root.geometry("400x200")
    root.mainloop()


if __name__ == "__main__":
    main()

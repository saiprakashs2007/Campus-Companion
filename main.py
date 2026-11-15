
import tkinter as tk
from app import CampusCompanion


def main():

    # Create main application window
    root = tk.Tk()

    # Initialize Campus Companion
    app = CampusCompanion(root)

    # Start application
    root.mainloop()


if __name__ == "__main__":
    main()

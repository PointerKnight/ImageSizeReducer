import tkinter as tk
from app import ImageSizeReducer


def main():
    root = tk.Tk()
    app = ImageSizeReducer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

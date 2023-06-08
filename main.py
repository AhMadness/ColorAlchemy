import tkinter as tk
import colorsys
from matplotlib import colors as mcolors
from tkinter import colorchooser, ttk
from PIL import Image, ImageTk
from tkinter import Button
from collections import deque

class ColorConverter(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ColorAlchemy")
        self.configure(bg='grey20')

        self.entries = []
        self.placeholders = ["#FFFFFF", "Red", "Green", "Blue", "Hue", "Saturation", "Value", "Hue", "Saturation", "Lightness"]
        self.color_formats = ["HEX", "RGB", "HSV", "HSL"]

        self.entry_frame = tk.Frame(self, bg='grey20', padx=5, pady=5)
        self.entry_frame.grid(row=0, column=0, sticky='N')

        # Create history_frame inside the entry_frame, below other widgets
        self.history_frame = tk.Frame(self.entry_frame, bg='grey20', padx=4, pady=5)

        self.history_buttons = []

        for i, color_format in enumerate(self.color_formats):
            label = ttk.Label(self.entry_frame, text=color_format+":", background='grey20', foreground='white')
            label.grid(row=i, column=0, pady=10, padx=10)
            if color_format == "HEX":
                entry = ttk.Entry(self.entry_frame, width=10)
                entry.bind("<Return>", self.update_all_formats)
                entry.bind("<FocusIn>", self.select_all_text)
                entry.grid(row=i, column=1, padx=10)
                entry.insert(0, self.placeholders.pop(0))
                self.entries.append(entry)
            else:
                for j in range(3):
                    entry = ttk.Entry(self.entry_frame, width=10)
                    entry.bind("<Return>", self.update_all_formats)
                    entry.bind("<FocusIn>", self.select_all_text)
                    entry.grid(row=i, column=j+1, padx=10)
                    entry.insert(0, self.placeholders.pop(0))
                    self.entries.append(entry)

        # Create a label
        self.history_label = ttk.Label(self.entry_frame, text="Recent:", background='grey20', foreground='white')

        # Grid history_label before history_frame
        self.history_label.grid(row=len(self.color_formats) + 1, column=0, padx=10, sticky='W')

        # Grid history_frame after history_label
        self.history_frame.grid(row=len(self.color_formats) + 1, column=1, columnspan=4, sticky='W')

        image = Image.open("icon.png")
        image = image.resize((30, 25), Image.Resampling.LANCZOS)
        self.color_icon = ImageTk.PhotoImage(image)

        image2 = Image.open("copy.png")
        image2 = image2.resize((25, 25), Image.Resampling.LANCZOS)  # resize to fit button
        self.copy_icon = ImageTk.PhotoImage(image2)

        self.preview_frame = tk.Frame(self, bg='grey20', padx=5, pady=5)
        self.preview_frame.grid(row=0, column=1, rowspan=2, sticky='N')

        preview_label = ttk.Label(self.preview_frame, text="Preview:", background='grey20', foreground='white')
        preview_label.pack(pady=(24, 2))

        self.color_preview = tk.Canvas(self.preview_frame, width=100, height=100, background="#FFFFFF")
        self.color_preview.pack(padx=10, pady=(0, 2))

        color_button = tk.Button(self.preview_frame, image=self.color_icon, bg='grey20', bd=0, command=self.choose_color)
        color_button.pack(pady=2)

        # Add these lines to create the 'Copy' buttons when the application starts
        self.copy_hex_button = Button(self.entry_frame, image=self.copy_icon, bg='grey20', bd=0, command=self.copy_hex_to_clipboard)
        self.copy_hex_button.grid(row=0, column=2, padx=(0, 40))

        self.copy_rgb_button = Button(self.entry_frame, image=self.copy_icon, bg='grey20', bd=0, command=self.copy_rgb_to_clipboard)
        self.copy_rgb_button.grid(row=1, column=4, padx=10)

        self.copy_hsv_button = Button(self.entry_frame, image=self.copy_icon, bg='grey20', bd=0, command=self.copy_hsv_to_clipboard)
        self.copy_hsv_button.grid(row=2, column=4, padx=10)

        self.copy_hsl_button = Button(self.entry_frame, image=self.copy_icon, bg='grey20', bd=0, command=self.copy_hsl_to_clipboard)
        self.copy_hsl_button.grid(row=3, column=4, padx=10)

    def copy_to_clipboard(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)

    def copy_hex_to_clipboard(self):
        self.copy_to_clipboard(self.entries[0].get())

    def copy_rgb_to_clipboard(self):
        rgb = ", ".join(self.entries[i].get() for i in range(1, 4))
        self.copy_to_clipboard(f"rgb({rgb})")

    def copy_hsv_to_clipboard(self):
        hsv = self.entries[4].get() + "°," + "{:.2f}%".format(float(self.entries[5].get())) + "," + "{:.2f}%".format(float(self.entries[6].get()))
        self.copy_to_clipboard(f"hsv({hsv})")

    def copy_hsl_to_clipboard(self):
        hsl = self.entries[7].get() + "°," + "{:.2f}%".format(float(self.entries[8].get())) + "," + "{:.2f}%".format(float(self.entries[9].get()))
        self.copy_to_clipboard(f"hsl({hsl})")

    def update_all_formats(self, event):
        try:
            index = self.entries.index(event.widget)
            if index == 0:
                rgb = mcolors.hex2color(self.entries[index].get())
                hsv = colorsys.rgb_to_hsv(*rgb)
                hsl = colorsys.rgb_to_hls(*rgb)
                hexa = self.entries[index].get()
                self.set_color_values(rgb, hsv, hsl, hexa=hexa)
            elif index < 4:
                rgb = [self.get_float_value(i) for i in range(1, 4)]
                hsv = colorsys.rgb_to_hsv(*rgb)
                hsl = colorsys.rgb_to_hls(*rgb)
                hexa = mcolors.rgb2hex(rgb)
                self.set_color_values(rgb, hsv, hsl, hexa=hexa)
            elif index < 7:
                hsv = [self.get_float_value(i) / d for i, d in zip(range(4, 7), [360, 100, 100])]
                rgb = colorsys.hsv_to_rgb(*hsv)
                hsl = colorsys.rgb_to_hls(*rgb)
                hexa = mcolors.rgb2hex(rgb)
                self.set_color_values(tuple(rgb), tuple(hsv), tuple(hsl), hexa=hexa)
            else:
                hsl = [self.get_float_value(i) / d for i, d in zip(range(7, 10), [360, 100, 100])]
                rgb = colorsys.hls_to_rgb(*hsl)
                hsv = colorsys.rgb_to_hsv(*rgb)
                hexa = mcolors.rgb2hex(rgb)
                self.set_color_values(tuple(rgb), tuple(hsv), tuple(hsl), hexa=hexa)

        except ValueError:
            pass

    def create_copy_buttons(self, rgb, hsv, hsl, hexa):
        # Change 'Button' to 'self.copy_hex_button' and other buttons accordingly
        self.copy_hex_button.configure(command=lambda: self.copy_to_clipboard(hexa))
        self.copy_rgb_button.configure(command=lambda: self.copy_to_clipboard(f"rgb({','.join(map(str, [int(c * 255) for c in rgb]))})"))
        self.copy_hsv_button.configure(command=lambda: self.copy_to_clipboard(f"hsv({','.join(map(lambda v: f'{v}%' if v <= 1 else f'{v}°', hsv))})"))
        self.copy_hsl_button.configure(command=lambda: self.copy_to_clipboard(f"hsl({','.join(map(lambda v: f'{v}%' if v <= 1 else f'{v}°', hsl))})"))

    def choose_color(self):
        color = colorchooser.askcolor()
        if color[1]:  # if a color was selected
            rgb = color[0]
            rgb_normalized = tuple([x / 255 for x in rgb])
            hsv = colorsys.rgb_to_hsv(*rgb_normalized)
            hsl = colorsys.rgb_to_hls(*rgb_normalized)
            hexa = color[1]
            self.set_color_values(rgb_normalized, hsv, hsl, hexa=hexa, add_to_history=True)

    def select_all_text(self, event):
        event.widget.selection_range(0, tk.END)

    def set_color_values(self, rgb, hsv, hsl, hexa=None, add_to_history=True):
        # RGB
        for i, value in enumerate(rgb, 1):
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, str(int(value * 255)))
        # HSV, HSL
        for i, value in enumerate(hsv + hsl, 4):
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, "{:.2f}".format(value * [360, 100, 100, 360, 100, 100][i - 4]))
        # Hexa
        if hexa:
            self.entries[0].delete(0, tk.END)
            self.entries[0].insert(0, hexa)
        # Update color preview
        self.color_preview.config(background=hexa)
        # Update history
        if add_to_history:
            self.update_history(hexa)

    def select_history_color(self, color_hex):
        rgb_normalized = mcolors.hex2color(color_hex)
        hsv = colorsys.rgb_to_hsv(*rgb_normalized)
        hsl = colorsys.rgb_to_hls(*rgb_normalized)
        self.set_color_values(rgb_normalized, hsv, hsl, hexa=color_hex, add_to_history=False)


    def get_float_value(self, index):
        value = float(self.entries[index].get())
        return value / 255 if index < 4 else value

    def update_history(self, color):
        if len(self.history_buttons) >= 7:
            old_button = self.history_buttons.pop(0)
            old_button.destroy()
        color_button = tk.Button(self.history_frame, width=2, background=color, command=lambda color=color: self.color_button_command(color))
        color_button.pack(side='right', padx=6, pady=5)  # pack to the right
        self.history_buttons.append(color_button)

    def color_button_command(self, color):
        self.select_history_color(color)
        self.copy_to_clipboard(color)  # Adding this line to copy hex code to clipboard


if __name__ == "__main__":
    app = ColorConverter()
    app.update_history('#FFFFFF')
    app.mainloop()

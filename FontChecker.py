import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import pyperclip


def update_font(*args):
    selected_font = font_family.get()
    selected_size = font_size.get()
    text_label.config(font=(selected_font, int(selected_size)))


def change_font_with_arrows(event):
    fonts = list(font.families())
    current_font = font_family.get()
    current_index = fonts.index(current_font)

    new_index = current_index

    if event.keysym == 'Up':
        new_index = (current_index - 1) % len(fonts)
    elif event.keysym == 'Down':
        new_index = (current_index + 1) % len(fonts)

    font_family.set(fonts[new_index])
    update_font()


def update_text(event=None):
    text_label.config(text=text_entry.get())


def update_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code[1]:
        text_label.config(fg=color_code[1])
        update_color_codes(color_code[1])


def update_color_codes(color_code):
    r, g, b = tuple(int(color_code[i:i+2], 16) for i in (1, 3, 5))
    color_rgb.set(f"RGB ({r}, {g}, {b}) - CSS, JavaScript")
    color_hex.set(f"Hex {color_code} - CSS, HTML")


def copy_to_clipboard(text):
    pyperclip.copy(text)


def create_copy_button(text_variable, frame):
    label = tk.Label(frame, textvariable=text_variable, bg="white")
    label.pack(side=tk.LEFT)
    button = tk.Button(frame, text="Copy", command=lambda: copy_to_clipboard(text_variable.get()))
    button.pack(side=tk.LEFT)


def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    update_mode()


def update_mode():
    mode_colors = ("gray20", "gray30", "white", "black") \
        if dark_mode \
        else ("SystemButtonFace", "white", "black", "white")
    root.config(bg=mode_colors[0])
    text_entry.config(bg=mode_colors[1], fg=mode_colors[2])
    text_label.config(bg=mode_colors[0], fg=mode_colors[2])
    color_button.config(bg=mode_colors[1], fg=mode_colors[2])
    mode_button.config(bg=mode_colors[1], fg=mode_colors[2])
    font_select.config(bg=mode_colors[1], fg=mode_colors[2])
    font_size_select.config(bg=mode_colors[1], fg=mode_colors[2])
    copy_font_button.config(bg=mode_colors[1], fg=mode_colors[2])
    for frame in [rgb_frame, hex_frame]:
        frame.config(bg="white")


root = tk.Tk()
root.title("Font Checker")
root.geometry("600x400")

dark_mode = False

font_family = tk.StringVar(root, value='Arial')
font_select = tk.OptionMenu(root, font_family, *font.families(), command=update_font)
font_select.pack(pady=10)

font_size = tk.StringVar(root, value='25')
font_size_select = tk.OptionMenu(root, font_size, *range(8, 60), command=update_font)
font_size_select.pack(pady=10)

text_entry = tk.Entry(root)
text_entry.pack(pady=10)
text_entry.bind("<KeyRelease>", update_text)

text_label = tk.Label(root, text="Sample Text", font=("Arial", 25), fg="#000000")
text_label.pack(pady=10)

color_button = tk.Button(root, text="Choose Color", command=update_color)
color_button.pack(pady=10)

copy_font_button = tk.Button(root, text="Copy Font Name", command=lambda: copy_to_clipboard(font_family.get()))
copy_font_button.pack(pady=10)

color_rgb = tk.StringVar(value="RGB (0, 0, 0) - CSS, JavaScript")
color_hex = tk.StringVar(value="Hex #000000 - CSS, HTML")

rgb_frame = tk.Frame(root, bg="white")
create_copy_button(color_rgb, rgb_frame)
rgb_frame.pack(pady=2)

hex_frame = tk.Frame(root, bg="white")
create_copy_button(color_hex, hex_frame)
hex_frame.pack(pady=2)

mode_button = tk.Button(root, text="Dark Mode", command=toggle_mode)
mode_button.pack(side=tk.LEFT, anchor="sw", padx=10, pady=10)

root.bind('<Up>', change_font_with_arrows)
root.bind('<Down>', change_font_with_arrows)

# Fußzeilen-Text
footer_text = tk.StringVar(value="Erstellt von 3mmooo")

# Fußzeilen-Label
footer_label = tk.Label(root, textvariable=footer_text, bg="white")
footer_label.pack(side=tk.BOTTOM, anchor='w', padx=145, pady=10)


root.mainloop()

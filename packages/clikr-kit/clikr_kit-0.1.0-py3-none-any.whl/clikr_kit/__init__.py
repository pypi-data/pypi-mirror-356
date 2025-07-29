import tkinter as tk

app = None
clicks = 0

def compile_kit(
    button_text,
    x, y,
    button_bg, button_fg,
    x_1, y_1,
    label_bg, label_fg,
    bg="white",
    fullscreen=False,
    geo="400x400",
    title="Game made by: clikr-kit",
    button_font=("Arial", 15),
    dev_clicks=0,
    label_font=("Arial", 25)
):
    global app, clicks

    if app is None:
        app = tk.Tk()
        app.config(bg=bg)
        app.geometry(geo)
        app.title(title)
        clicks = dev_clicks

        label = tk.Label(text=str(clicks), bg=label_bg, fg=label_fg, font=label_font)
        label.place(x=x_1, y=y_1)

        def clicked():
            global clicks  # <-- FIXED: use 'global' here
            clicks += 1
            label.config(text=str(clicks))

        click = tk.Button(text=button_text, bg=button_bg, fg=button_fg, font=button_font, command=clicked)
        click.place(x=x, y=y)

        if isinstance(fullscreen, bool):
            app.attributes("-fullscreen", fullscreen)
        else:
            print(f"[clikr_kit] Warning: 'fullscreen' should be True or False, got {fullscreen}. Defaulting to False.")
            app.attributes("-fullscreen", False)

        app.mainloop()

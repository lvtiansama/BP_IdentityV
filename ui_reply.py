import tkinter as tk

def handle_default_text(event):
    widget = event.widget
    default_text = widget.default_text
    if widget.get() == default_text:
        widget.delete(0, tk.END)
        widget.config(foreground="black")
    widget.unbind("<Button-1>")
    widget.unbind("<FocusIn>")

def handle_focus_out(event):
    widget = event.widget
    default_text = widget.default_text
    if widget.get() == "":
        widget.insert(tk.END, default_text)
        widget.config(foreground="gray")
    if widget.get() == default_text:
        widget.config(foreground="gray")
    widget.bind("<Button-1>", handle_default_text)
    widget.bind("<FocusIn>", handle_default_text)

if __name__ == '__main__':
    print("in ui_reply")

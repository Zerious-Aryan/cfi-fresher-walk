import tkinter as tk
from tkinter import filedialog, messagebox
from functools import partial
from PIL import Image, ImageTk
import os

from backend.profile_manager import ProfileManager

ASSETS_PATH = os.path.abspath("assets")

root = tk.Tk()
root.title("Select a Profile")
root.geometry("800x600")
root.configure(bg="black")

manager = ProfileManager()

def open_profile_window(profile):
    win = tk.Toplevel(root)
    win.title(profile['name'])
    win.geometry("400x300")
    win.configure(bg="black")
    tk.Label(win, text=f"Welcome, {profile['name']}!", font=("Arial", 20), fg="white", bg="black").pack(expand=True)

def on_enter(event):
    widget = event.widget
    widget.config(width=200, height=200)

def on_leave(event):
    widget = event.widget
    widget.config(width=130, height=130)

def render_profiles():
    for widget in profile_frame.winfo_children():
        widget.destroy()

    profiles = manager.get_profiles()
    columns = 5

    for i, profile in enumerate(profiles):
        img_path = profile['image']
        if not os.path.exists(img_path):
            continue

        normal_size = (130, 130)
        hover_size = (200, 200)


        raw_img = Image.open(img_path).convert("RGBA")
        img_normal = raw_img.resize(normal_size, Image.LANCZOS)
        img_hover = raw_img.resize(hover_size, Image.LANCZOS)

        tk_img_normal = ImageTk.PhotoImage(img_normal)
        tk_img_hover = ImageTk.PhotoImage(img_hover)

        profile_box = tk.Frame(profile_frame, bg="black")
        row = i // columns
        col = i % columns
        profile_box.grid(row=row, column=col, padx=15, pady=15)


        img_label = tk.Label(profile_box, image=tk_img_normal, bg="black", cursor="hand2")
        img_label.image_normal = tk_img_normal
        img_label.image_hover = tk_img_hover
        img_label.config(image=tk_img_normal)

  
        img_label.bind("<Enter>", lambda e, w=img_label: w.config(image=w.image_hover))
        img_label.bind("<Leave>", lambda e, w=img_label: w.config(image=w.image_normal))


        img_label.bind("<Button-1>", lambda e, p=profile: open_profile_window(p))

        img_label.pack()

        name_label = tk.Label(profile_box, text=profile['name'], fg="white", bg="black", font=("Arial", 12))
        name_label.pack(pady=5)

def open_add_profile_window():
    def submit():
        name = name_entry.get().strip()
        img_path = image_path_var.get()

        if not name or not img_path:
            messagebox.showwarning("Input Error", "Please enter a name and choose an image.")
            return

        if not os.path.exists(img_path):
            messagebox.showerror("File Error", "Selected image does not exist.")
            return

        manager.add_profile(name, img_path)
        render_profiles()
        win.destroy()

    def browse_image():
        file_path = filedialog.askopenfilename(
            title="Select Profile Image",
            filetypes=[("PNG Files", "*.png")],
            initialdir=ASSETS_PATH
        )
        if file_path:
            image_path_var.set(file_path)

    win = tk.Toplevel(root)
    win.title("Add New Profile")
    win.geometry("400x200")
    win.configure(bg="black")

    tk.Label(win, text="Name:", fg="white", bg="black", font=("Arial", 12)).pack(pady=(20, 5))
    name_entry = tk.Entry(win, font=("Arial", 12))
    name_entry.pack()

    tk.Button(win, text="Browse Image", command=browse_image).pack(pady=10)
    image_path_var = tk.StringVar()
    tk.Label(win, textvariable=image_path_var, bg="black", fg="gray", font=("Arial", 10)).pack()

    tk.Button(win, text="Add Profile", command=submit, bg="green", fg="white").pack(pady=15)

profile_frame = tk.Frame(root, bg="black")
profile_frame.pack(expand=True)

if __name__ == "__main__":
    render_profiles()

    add_button = tk.Button(
        root,
        text="+ Add Profile",
        font=("Arial", 14),
        bg="#222",
        fg="white",
        activebackground="#333",
        command=open_add_profile_window
    )
    add_button.pack(pady=10)

    root.mainloop()

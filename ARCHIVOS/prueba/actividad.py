import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import datetime
import sqlite3

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS photos
                       (id INTEGER PRIMARY KEY,
                        file_path TEXT,
                        publish_time TEXT,
                        delete_time TEXT)''')
    conn.commit()

def update_table():
    cursor.execute('''PRAGMA table_info(photos)''')
    columns = [column[1] for column in cursor.fetchall()]
    if 'delete_time' not in columns:
        cursor.execute('''ALTER TABLE photos ADD COLUMN delete_time TEXT''')
        conn.commit()

def upload_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if file_path:
        choice = messagebox.askyesno("Programar Foto", "¿Quieres programar la foto para una fecha y hora específicas?")
        if choice:  # Programar la foto
            photo_time_str = simpledialog.askstring("Fecha y Hora", "Introduce la fecha y hora de publicación (YYYY-MM-DD HH:MM):")
            delete_time_str = simpledialog.askstring("Fecha y Hora de Eliminación", "Introduce la fecha y hora de eliminación (YYYY-MM-DD HH:MM):")
            try:
                photo_time = datetime.datetime.strptime(photo_time_str, "%Y-%m-%d %H:%M") if photo_time_str else None
                delete_time = datetime.datetime.strptime(delete_time_str, "%Y-%m-%d %H:%M") if delete_time_str else None
                if photo_time:
                    photos.append((file_path, photo_time, delete_time))
                    save_photo_to_db(file_path, photo_time, delete_time)
                    messagebox.showinfo("Éxito", "Foto programada con éxito.")
                else:
                    messagebox.showwarning("Advertencia", "La fecha y hora de publicación no pueden estar vacías.")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha y hora inválido. Use YYYY-MM-DD HH:MM.")
        else:  # Subir la foto inmediatamente
            current_time = datetime.datetime.now()
            show_photo(file_path)
            save_photo_to_db(file_path, current_time, None)
            messagebox.showinfo("Éxito", "Foto subida con éxito.")

def save_photo_to_db(file_path, publish_time, delete_time):
    publish_time_str = publish_time.strftime("%Y-%m-%d %H:%M") if publish_time else None
    delete_time_str = delete_time.strftime("%Y-%m-%d %H:%M") if delete_time else None
    cursor.execute("INSERT INTO photos (file_path, publish_time, delete_time) VALUES (?, ?, ?)",
                   (file_path, publish_time_str, delete_time_str))
    conn.commit()

def load_photos_from_db():
    cursor.execute("SELECT file_path, publish_time, delete_time FROM photos")
    rows = cursor.fetchall()
    for row in rows:
        file_path, publish_time_str, delete_time_str = row
        publish_time = datetime.datetime.strptime(publish_time_str, "%Y-%m-%d %H:%M") if publish_time_str else None
        delete_time = datetime.datetime.strptime(delete_time_str, "%Y-%m-%d %H:%M") if delete_time_str else None
        photos.append((file_path, publish_time, delete_time))
        if not publish_time:
            show_photo(file_path, delete_time)

def check_photos():
    now = datetime.datetime.now()
    for photo in photos[:]:
        photo_path, publish_time, delete_time = photo
        if publish_time and now >= publish_time:
            show_photo(photo_path, delete_time)
            photos.remove(photo)
            delete_photo_from_db(photo_path)
            if delete_time:
                photos.append((photo_path, None, delete_time))
        if delete_time and now >= delete_time:
            remove_photo_from_gallery(photo_path)
            photos.remove(photo)
            delete_photo_from_db(photo_path)
    root.after(1000, check_photos)  # Verificar cada segundo

def delete_photo_from_db(file_path):
    cursor.execute("DELETE FROM photos WHERE file_path = ?", (file_path,))
    conn.commit()

def show_photo(photo_path, delete_time=None):
    image = Image.open(photo_path)
    image.thumbnail((200, 200))  # Redimensionar la imagen para la galería
    photo = ImageTk.PhotoImage(image)

    photo_frame = tk.Frame(gallery_frame, bd=2, relief=tk.RAISED)
    photo_label = tk.Label(photo_frame, image=photo)
    photo_label.image = photo  # Mantener referencia a la imagen
    photo_label.pack()
    photo_frame.pack(side=tk.LEFT, padx=5, pady=5)

    photo_frames[photo_path] = photo_frame  # Guardar el frame para referencia futura

def remove_photo_from_gallery(photo_path):
    if photo_path in photo_frames:
        frame = photo_frames.pop(photo_path)
        frame.pack_forget()
        frame.destroy()

def main():
    global root, gallery_frame, photos, photo_frames, conn, cursor
    root = tk.Tk()
    root.title("Galería de Fotos Programadas")

    conn = sqlite3.connect('photo_gallery.db')
    cursor = conn.cursor()
    create_table()
    update_table()

    photos = []  # Lista para almacenar las fotos y sus tiempos de publicación
    photo_frames = {}  # Diccionario para almacenar los frames de fotos

    upload_button = tk.Button(root, text="Subir Foto", command=upload_photo)
    upload_button.pack()

    gallery_frame = tk.Frame(root)
    gallery_frame.pack()

    load_photos_from_db()
    check_photos()  # Iniciar la verificación de fotos

    root.mainloop()

if __name__ == "__main__":
    main()








import tkinter as tk  
from tkinter import filedialog, messagebox  
import sqlite3  
from PIL import Image, ImageTk 
import requests  
from io import BytesIO  

#================================== Función principal para gestionar la publicidad ==========================================

def gestionar_publicidad():
    # Función interna para conectar a la base de datos SQLite
    def conectar_base_datos():
        conn = sqlite3.connect('cartelera.db')  # Conectar a la base de datos
        cur = conn.cursor()  # Crear un cursor para ejecutar consultas SQL

        # Crear tabla para imágenes de publicidad si no existe
        cur.execute('''
        CREATE TABLE IF NOT EXISTS imagenes_publicidad (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT
        )
        ''')

        # Crear tabla para películas publicitarias si no existe
        cur.execute('''
        CREATE TABLE IF NOT EXISTS publicidad_peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT
        )
        ''')

        conn.commit()  # Confirmar los cambios en la base de datos

        return conn, cur  # Devolver la conexión y el cursor

    # Función interna para cargar una imagen desde URL o archivo
    def cargar_imagen(url):
        if url.startswith('http://') or url.startswith('https://'):
            response = requests.get(url)  # Obtener la imagen desde una URL
            img_data = BytesIO(response.content)  # Convertir los datos binarios de la imagen
        else:
            with open(url, 'rb') as f:
                img_data = BytesIO(f.read())  # Leer la imagen desde un archivo local
        return img_data  # Devolver los datos de la imagen

    # Función interna para mostrar las imágenes en el canvas
    def mostrar_imagenes(tabla, conn, cur, frame_imagenes, canvas, img_refs):
        # Limpiar el canvas antes de mostrar nuevas imágenes
        canvas.delete("all")

        # Crear un nuevo frame dentro del canvas
        interior_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=interior_frame, anchor="nw")

        # Consultar las imágenes desde la tabla especificada
        cur.execute(f"SELECT id, url FROM {tabla}")
        imagenes = cur.fetchall()

        if not imagenes:
            mensaje = "No se han subido imágenes." if tabla == 'imagenes_publicidad' else "No hay películas publicitarias."
            lbl_aviso = tk.Label(interior_frame, text=mensaje, bg="white")
            lbl_aviso.pack(pady=50)  # Mostrar un mensaje si no hay imágenes
        else:
            col_count = 0
            row_count = 0

            for img_id, img_url in imagenes:
                img_data = cargar_imagen(img_url)  # Cargar la imagen desde la URL o archivo
                img = Image.open(img_data)
                img.thumbnail((300, 300))  # Redimensionar la imagen a una miniatura
                img_tk = ImageTk.PhotoImage(img)  # Convertir la imagen PIL a formato Tkinter

                # Mostrar la imagen en un Label dentro del interior_frame
                lbl_img = tk.Label(interior_frame, image=img_tk)
                lbl_img.image = img_tk  # Mantener una referencia para evitar que Python la elimine
                lbl_img.grid(row=row_count, column=col_count, padx=10, pady=10)

                # Mantener referencia a la imagen en el diccionario img_refs
                img_refs[img_id] = img_tk

                # Botón para eliminar la imagen, con función lambda para pasar el id de la imagen
                btn_eliminar = tk.Button(interior_frame, text="Eliminar", command=lambda i=img_id: eliminar_imagen(i, tabla, conn, cur, frame_imagenes, canvas, img_refs), bg="black", fg="white")
                btn_eliminar.grid(row=row_count + 1, column=col_count)

                # Separador entre las imágenes
                separator = tk.Frame(interior_frame, height=2, bd=1, relief=tk.SUNKEN, bg="black")
                separator.grid(row=row_count + 2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

                col_count += 1
                if col_count == 3:
                    col_count = 0
                    row_count += 3

        # Configurar el tamaño del interior_frame dentro del canvas
        interior_frame.update_idletasks()  # Asegura que el frame tiene el tamaño correcto
        canvas.configure(scrollregion=canvas.bbox("all"))  # Configurar la región de desplazamiento

    # Función interna para eliminar una imagen de la base de datos
    def eliminar_imagen(img_id, tabla, conn, cur, frame_imagenes, canvas, img_refs):
        cur.execute(f"DELETE FROM {tabla} WHERE id=?", (img_id,))
        conn.commit()  # Aplicar cambios en la base de datos
        mostrar_imagenes(tabla, conn, cur, frame_imagenes, canvas, img_refs)  # Actualizar la visualización de imágenes

    # Función interna para añadir una nueva imagen a la base de datos
    def anadir_imagen(tabla, conn, cur, frame_imagenes, canvas, img_refs):
        archivo = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])  # Abrir el dialogo para seleccionar archivo
        if archivo:
            cur.execute(f"INSERT INTO {tabla} (url) VALUES (?)", (archivo,))
            conn.commit()  # Aplicar cambios en la base de datos
            mostrar_imagenes(tabla, conn, cur, frame_imagenes, canvas, img_refs)  # Actualizar la visualización de imágenes

    # Función interna para configurar la interfaz de usuario principal
    def configurar_interfaz():
        root = tk.Toplevel()  # Crear una ventana principal
        root.title("Cartelera")  # Título de la ventana
        root.geometry("1000x600")  # Tamaño inicial de la ventana
        #bloquear el tamaño de la ventana
        root.resizable(False, False)
        root.configure(bg="white")  # Color de fondo de la ventana

        conn, cur = conectar_base_datos()  # Conectar a la base de datos al iniciar la interfaz

        frame_botones = tk.Frame(root, bg="black")  # Crear un frame para los botones
        frame_botones.pack(fill=tk.X)  # Empaquetar el frame en la ventana principal

        global tabla  # Definir la variable global tabla para mantener el estado actual
        tabla = 'imagenes_publicidad'  # Inicialmente mostrar imágenes de publicidad

        img_refs = {}  # Diccionario para mantener las referencias de las imágenes

        # Función para actualizar la tabla de imágenes mostradas
        def actualizar_tabla(tabla_seleccionada):
            global tabla
            tabla = tabla_seleccionada  # Cambiar la tabla actual
            mostrar_imagenes(tabla, conn, cur, frame_imagenes, canvas, img_refs)  # Mostrar imágenes actualizadas
            lbl_info.config(text=f"Viendo: {tabla}")  # Actualizar la etiqueta de información

        # Botones para seleccionar qué tipo de imágenes mostrar
        btn_imagenes_publicidad = tk.Button(frame_botones, text="Imagenes Publicidad", command=lambda: actualizar_tabla('imagenes_publicidad'), bg="white", fg="black")
        btn_imagenes_publicidad.pack(side=tk.LEFT, padx=20, pady=20)

        btn_peliculas_publicidad = tk.Button(frame_botones, text="Peliculas Publicidad", command=lambda: actualizar_tabla('publicidad_peliculas'), bg="white", fg="black")
        btn_peliculas_publicidad.pack(side=tk.LEFT, padx=20, pady=20)

        # Botón para añadir una nueva imagen
        btn_anadir = tk.Button(frame_botones, text="Añadir", command=lambda: anadir_imagen(tabla, conn, cur, frame_imagenes, canvas, img_refs), bg="white", fg="black")
        btn_anadir.pack(side=tk.RIGHT, padx=20, pady=20)

        # Frame para mostrar las imágenes
        frame_imagenes = tk.Frame(root, bg="white")
        frame_imagenes.pack(fill=tk.BOTH, expand=True)

        lbl_info = tk.Label(root, text="Viendo: Ninguno", bg="white")
        lbl_info.pack(pady=10)  # Etiqueta para mostrar el estado actual (qué tipo de imágenes se están viendo)

        # Scrollbar vertical para el canvas de imágenes
        scrollbar = tk.Scrollbar(frame_imagenes, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(frame_imagenes, bg="white", yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        # Configurar el canvas para expandirse dinámicamente con el contenido
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mostrar las imágenes iniciales al abrir la interfaz
        mostrar_imagenes(tabla, conn, cur, frame_imagenes, canvas, img_refs)

        root.mainloop()  # Ejecutar el bucle principal de la interfaz

        conn.close()  # Cerrar la conexión a la base de datos al salir de la interfaz

    configurar_interfaz()  # Llamar a la función para configurar la interfaz principal





















    




    












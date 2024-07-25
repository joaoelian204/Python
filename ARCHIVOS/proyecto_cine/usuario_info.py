import tkinter as tk
from PIL import Image, ImageTk
from configuracion import * 

def mostrar_perfil(cuerpo_principal, usuario):
    """
    Muestra los detalles de un usuario en un contenedor principal.
    
    Args:
        cuerpo_principal (tk.Frame): El marco donde se mostrarán los detalles del usuario.
        usuario (dict): Un dict con los detalles del usuario.
    """
    # Limpiar el contenido del contenedor principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Configurar el contenedor principal
    cuerpo_principal.configure(bg="#EAEAEA", padx=20, pady=20)

    # Crear un marco para centrar el contenido
    frame_central = tk.Frame(cuerpo_principal, bg="#FFFFFF", relief=tk.RIDGE, bd=2)
    frame_central.pack(pady=20, padx=320, fill=tk.BOTH, expand=True)

    # Título del perfil
    titulo = tk.Label(frame_central, text="Perfil del Usuario", font=('Helvetica', 20, 'bold'), bg="#FFFFFF", fg="#333333")
    titulo.pack(pady=20)

    # Cargar la imagen del usuario
    imagen = "/home/joaoelian/Documentos/perfil.png"
    try:
        imagen = Image.open(imagen)
        imagen_resized = imagen.resize((350, 350))  # Ajustar el tamaño de la imagen
        imagen_tk = ImageTk.PhotoImage(imagen_resized)
    except IOError as e:
        print("Error al cargar la imagen:", e)
        return

    # Widget Label para mostrar la imagen del usuario
    label_imagen = tk.Label(frame_central, image=imagen_tk, bg="#FFFFFF", relief=tk.SOLID, bd=2)
    label_imagen.image = imagen_tk  # Guardar una referencia para evitar que la imagen se borre
    label_imagen.pack(pady=10)

    # Mostrar otros detalles del usuario
    detalles = [
        f"Nombre: {usuario['nombre']} {usuario['apellido']}",
        f"Correo Electrónico: {usuario['correo']}",
        f"País: {usuario['pais']}",
        f"Provincia: {usuario['provincia']}",
        f"Ciudad: {usuario['ciudad']}",
        f"Cédula: {usuario['cedula']}"
    ]

    for detalle in detalles:
        label_detalle = tk.Label(frame_central, text=detalle, font=('Arial', 12), bg="#FFFFFF", fg="#555555")
        label_detalle.pack(pady=7)







import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO



def crear_boton(frame, texto, comando):
    button = tk.Button(frame, text=texto, command=comando, bg="#000000", fg="white", font=("Arial", 13), relief=tk.RAISED, borderwidth=3)
    button.pack(pady=5)

def crear_estado_asiento(frame, estado, color):
    tk.Label(frame, text=estado, bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
    canvas = tk.Canvas(frame, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
    canvas.create_rectangle(5, 5, 15, 15, fill=color)
    canvas.pack(anchor=tk.W)

# Crear la ventana principal
def crear_ventana_principal():
    ventana = tk.Tk()
    ventana.geometry("550x695")
    ventana.resizable(False, False)
    ventana.title("Reserva de Asientos de Cine")
    ventana.configure(bg="#F0F0F0")
    return ventana

# Función para cargar y redimensionar imágenes
def cargar_imagen(url_imagen, size):
    response = requests.get(url_imagen)
    imagen = Image.open(BytesIO(response.content))
    imagen = imagen.resize(size, Image.LANCZOS)  
    return ImageTk.PhotoImage(imagen)

# Cargar y mostrar imagen de fondo
def mostrar_imagen_fondo(ventana, ruta_imagen):
    imagen_fondo = cargar_imagen(ruta_imagen, (550, 695))
    label_fondo = tk.Label(ventana, image=imagen_fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)



def seleccionar_asiento(fila, asiento, asientos_actuales, botones, selecciones_pendientes, actualizar_contador):
    """Selecciona un asiento y actualiza su estado."""
    if asientos_actuales[fila][asiento] == 0:
        asientos_actuales[fila][asiento] = 2  # Marcar como seleccionado (no confirmado)
        botones[fila][asiento].config(bg="#FFD700", text="S")
        selecciones_pendientes.append((fila, asiento))
        actualizar_contador()
    elif asientos_actuales[fila][asiento] == 1:
        messagebox.showwarning("Reserva", f"Asiento {chr(65+asiento)}{fila+1} ya está ocupado")
    elif asientos_actuales[fila][asiento] == 2:
        asientos_actuales[fila][asiento] = 0  # Desmarcar selección
        botones[fila][asiento].config(bg="#32CD32", text="L")
        selecciones_pendientes.remove((fila, asiento))
        actualizar_contador()

def confirmar_reservas(selecciones_pendientes, asientos_actuales, botones, actualizar_contador):
    """Confirma las reservas seleccionadas."""
    if selecciones_pendientes:
        for fila, asiento in selecciones_pendientes:
            asientos_actuales[fila][asiento] = 1  # Marcar como ocupado
            botones[fila][asiento].config(bg="#FF6347", text="O")
        selecciones_pendientes.clear()
        actualizar_contador()
        messagebox.showinfo("Reserva", "Reservas confirmadas con éxito")
    else:
        messagebox.showwarning("Reserva", "No hay asientos seleccionados para confirmar")

def actualizar_contador(asientos_actuales, lbl_contador):
    """Actualiza el contador de asientos libres y seleccionados."""
    libres = sum(row.count(0) for row in asientos_actuales)
    seleccionados = sum(row.count(2) for row in asientos_actuales)
    lbl_contador.config(text=f"Puestos libres: {libres} \n Seleccionados: {seleccionados}")

def actualizar_asientos(asientos_actuales, botones):
    """Actualiza la visualización de los asientos."""
    for fila in range(8):
        for asiento in range(8):
            if asientos_actuales[fila][asiento] == 0:
                botones[fila][asiento].config(bg="#32CD32", text="L")
            elif asientos_actuales[fila][asiento] == 1:
                botones[fila][asiento].config(bg="#FF6347", text="O")
            elif asientos_actuales[fila][asiento] == 2:
                botones[fila][asiento].config(bg="#9400D3", text="S")

def hay_asientos_disponibles(asientos_sala):
    """Verifica si hay asientos disponibles en una sala."""
    for fila in asientos_sala:
        if 0 in fila:  # Si hay al menos un asiento disponible en esta fila
            return True
    return False

def encontrar_mejor_puesto(asientos_actuales, botones):
    """Encuentra el mejor asiento disponible."""
    for fila in range(8):
        mejor_distancia = float('inf')  # Inicializamos la mejor distancia con un valor infinito
        mejor_asiento = None
        for asiento in range(8):
            if asientos_actuales[fila][asiento] == 0:
                # Calculamos la distancia al centro de la fila
                distancia = abs(asiento - 3.5)  # El asiento central está en la posición 3.5
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_asiento = asiento
        if mejor_asiento is not None:
            botones[fila][mejor_asiento].config(bg="#40E0D0")  # Resaltamos el mejor asiento
            return

def volver_a_pelicula(frame_hora, frame_peliculas):
    """Vuelve al menú de selección de película."""
    frame_hora.pack_forget()
    frame_peliculas.pack()

def volver_a_hora(frame_sala, frame_hora):
    """Vuelve al menú de selección de hora."""
    frame_sala.pack_forget()
    frame_hora.pack()

def volver_a_sala(frame_asientos, frame_sala):
    """Vuelve al menú de selección de sala."""
    frame_asientos.pack_forget()
    frame_sala.pack()




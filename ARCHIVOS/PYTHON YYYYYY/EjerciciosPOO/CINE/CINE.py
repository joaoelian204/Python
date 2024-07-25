import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# LISTA DE RESERVAS------------------------------------------------------------------------------------------------------------------------------

# Variable para almacenar las reservas realizadas
reservas_realizadas = []

# Variable para almacenar las selecciones de asientos pendientes de confirmación
selecciones_pendientes = []

# URL DE LAS IMG, HORAS Y TITULOS DE LAS PELICULAS----------------------------------------------------------------------------------------------------------------

# Datos de ejemplo
peliculas = {
    "Bohemian Rhapsody": {
        "horarios": ["10:00", "13:00", "16:00", "19:00"],
        "imagen_url": "https://colonfilm.com/wp-content/uploads/2021/04/bohemian-rhapsody-poster.webp"
    },
    "Avatar": {
        "horarios": ["11:00", "14:00", "17:00", "20:00"],
        "imagen_url": "https://m.media-amazon.com/images/I/61UukTiUWKL._AC_UF894,1000_QL80_.jpg"
    },
    "Back to the Future": {
        "horarios": ["12:00", "15:00", "18:00", "21:00"],
        "imagen_url": "https://i.blogs.es/682e23/81174579c578a791d10e4566f2732eac/450_1000.jpg"
    }
}

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Matriz de asientos----------------------------------------------------------------------------------------------------------------

# Datos de ejemplo de asientos (asientos vacíos se representan con 0 y ocupados con 1)
asientos = [[[0]*8 for _ in range(8)] for _ in range(3)]

# -----------------------------------------------------------------------------------------------

# FUNCIONES PARA LA INTERFAZ GRAFICA------------------------------------------------------------------------------------------------------------------------------

# Función para ver los horarios de una película
def ver_horarios(pelicula):
    horarios_disponibles = "\n".join(peliculas[pelicula]["horarios"])
    messagebox.showinfo("Horarios Disponibles", f"Horarios disponibles para {pelicula}:\n{horarios_disponibles}")

# Función para seleccionar una película
def seleccionar_pelicula(pelicula):
    frame_peliculas.pack_forget()
    horas.set(peliculas[pelicula]["horarios"])
    frame_hora.pack()

# Función para seleccionar una hora
def seleccionar_hora():
    seleccion = lista_horas.curselection()
    if seleccion:
        hora = lista_horas.get(seleccion)
        frame_hora.pack_forget()
        frame_sala.pack()
    else:
        messagebox.showwarning("Selección inválida", "Por favor seleccione una hora.")

# Función para seleccionar una sala
def seleccionar_sala():
    seleccion_sala = lista_salas.curselection()
    if seleccion_sala:
        sala_index = seleccion_sala[0]
        global asientos_actuales
        asientos_actuales = asientos[sala_index]
        actualizar_asientos()
        if not hay_asientos_disponibles(asientos_actuales):
            messagebox.showwarning("Sala Llena", "Lo sentimos, esta sala está llena. Por favor, seleccione otra sala.")
            return
        frame_sala.pack_forget()
        frame_asientos.pack()
    else:
        messagebox.showwarning("Selección inválida", "Por favor seleccione una sala.")

# Función para seleccionar un asiento
def seleccionar_asiento(fila, asiento):
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

# Función para confirmar las reservas seleccionadas
def confirmar_reservas():
    if selecciones_pendientes:
        for fila, asiento in selecciones_pendientes:
            asientos_actuales[fila][asiento] = 1  # Marcar como ocupado
            botones[fila][asiento].config(bg="#FF6347", text="O")
            reservas_realizadas.append((fila, asiento))
        selecciones_pendientes.clear()
        actualizar_contador()
        messagebox.showinfo("Reserva", "Reservas confirmadas con éxito")
    else:
        messagebox.showwarning("Reserva", "No hay asientos seleccionados para confirmar")

# Función para actualizar el contador de puestos libres
def actualizar_contador():
    libres = sum(row.count(0) for row in asientos_actuales)
    seleccionados = sum(row.count(2) for row in asientos_actuales)
    lbl_contador.config(text=f"Puestos libres: {libres} \n Seleccionados: {seleccionados}")

# Función para actualizar la visualización de los asientos
def actualizar_asientos():
    for fila in range(8):
        for asiento in range(8):
            if asientos_actuales[fila][asiento] == 0:
                botones[fila][asiento].config(bg="#32CD32", text="L")
            elif asientos_actuales[fila][asiento] == 1:
                botones[fila][asiento].config(bg="#FF6347", text="O")
            elif asientos_actuales[fila][asiento] == 2:
                botones[fila][asiento].config(bg="#9400D3", text="S")

# Función para verificar si hay asientos disponibles en una sala
def hay_asientos_disponibles(asientos_sala):
    for fila in asientos_sala:
        if 0 in fila:  # Si hay al menos un asiento disponible en esta fila
            return True
    return False

# Función para encontrar el mejor asiento disponible
def encontrar_mejor_puesto():
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


# Función para volver al menú de selección de película
def volver_a_pelicula():
    frame_hora.pack_forget()
    frame_peliculas.pack()

# Función para volver al menú de selección de hora
def volver_a_hora():
    frame_sala.pack_forget()
    frame_hora.pack()

# Función para volver al menú de selección de sala
def volver_a_sala():
    frame_asientos.pack_forget()
    frame_sala.pack()

# ----------------------------------------------------------------------------------------------------------------------------------------------------

# INTERFAZ GRAFICA------------------------------------------------------------------------------------------------------------------------------

# VENTANA PRINCIPAL DE LA APLICACION ---------------------------------------------------------------------------------------------------------------------

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("550x695")
ventana.resizable(False, False)
ventana.title("Reserva de Asientos de Cine")
ventana.configure(bg="#F0F0F0")

# Cargar la imagen de fondo
ruta_imagen = "/home/joaoelian/Descargas/fondo.png"
imagen = Image.open(ruta_imagen)
imagen = imagen.resize((550, 695), Image.LANCZOS)  # Redimensionar la imagen
imagen_fondo = ImageTk.PhotoImage(imagen)

# Crear un widget Label para mostrar la imagen de fondo
label_fondo = tk.Label(ventana, image=imagen_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)


# VENTANA (MARCO) PELICULA------------------------------------------------------------------------------------------------------------------------------

# Crear el marco para la selección de película
frame_peliculas = tk.Frame(ventana, bg="#FFFFFF")
frame_peliculas.pack(side=tk.TOP,padx=25, pady=25)

# UBICACION DE LAS IMAGENES DE LAS PELICULAS-----------------------------------------------------------------------------------------------------------

# Mostrar las imágenes de las películas y agregar botón para ver horarios
for pelicula, info in peliculas.items():
    url_imagen = info["imagen_url"]
    response = requests.get(url_imagen)
    imagen = Image.open(BytesIO(response.content))
    imagen = imagen.resize((120, 120), Image.LANCZOS)  # Tamaño reducido de la imagen
    imagen = ImageTk.PhotoImage(imagen)

    label = tk.Label(frame_peliculas, image=imagen, text=pelicula, compound=tk.TOP, bg="#FFFFFF", font=("Arial", 12))
    label.image = imagen  # Mantener una referencia a la imagen
    label.pack(side=tk.TOP, padx=10, pady=10)
    
    boton_ver = tk.Button(frame_peliculas, text="Seleccionar Hora y Sala", command=lambda p=pelicula: seleccionar_pelicula(p))
    boton_ver.pack(side=tk.TOP, padx=5, pady=5)
    
# VENTANA (MARCO) HORA------------------------------------------------------------------------------------------------------------------------------
# Crear el marco para la selección de hora
frame_hora = tk.Frame(ventana, bg="#F0F0F0", padx=30, pady=30)
horas = tk.StringVar(value=[])
frame_hora.pack()
tk.Label(frame_hora, text="Seleccione una Hora:", bg="#F0F0F0", font=("Arial", 15)).pack()
lista_horas = tk.Listbox(frame_hora, listvariable=horas, selectbackground="#FF6347", font=("Arial", 12))
lista_horas.pack(side=tk.TOP, padx=10, pady=10)
tk.Button(frame_hora, text="Seleccionar Sala", command=seleccionar_hora, bg="#000000", fg="white", font=("Arial", 13)).pack(pady=5)
tk.Button(frame_hora, text="Volver", command=volver_a_pelicula, padx=15, bg="#000000", fg="white", font=("Arial", 13)).pack(pady=5)

# VENTANA (MARCO) SALA------------------------------------------------------------------------------------------------------------------------------

# Crear el marco para la selección de sala
frame_sala = tk.Frame(ventana, bg="#F0F0F0", padx=70, pady=70)
tk.Label(frame_sala, text="Seleccione una Sala:", bg="#F0F0F0", font=("Arial", 15)).pack()
lista_salas = tk.Listbox(frame_sala, selectbackground="#FF6347", font=("Arial", 12))
for i in range(1, 4):
    lista_salas.insert(tk.END, f"Sala {i}")
lista_salas.pack()
tk.Button(frame_sala, text="Seleccionar", command=seleccionar_sala, bg="#000000", fg="white", font=("Arial", 13)).pack(pady=5)
tk.Button(frame_sala, text="Volver", command=volver_a_hora, padx=15, bg="#000000", fg="white", font=("Arial", 13)).pack(pady=5)

# VENTANA (MARCO) ASIENTO------------------------------------------------------------------------------------------------------------------------------

# Crear el marco para la selección de asientos
frame_asientos = tk.Frame(ventana, bg="#F0F0F0", padx=10, pady=10)
tk.Label(frame_asientos, text="Seleccione un Asiento:", bg="#F0F0F0", font=("Arial", 15)).pack()
botones = []
frame_botones = tk.Frame(frame_asientos, bg="#F0F0F0")
frame_botones.pack()
asientos_actuales = None

# BOTONES SELECCION DE ASIENTOS--------------------------------------------------------------------------------------------------------------

# Crear los botones para seleccionar los asientos
for fila in range(8):
    fila_botones = tk.Frame(frame_botones, bg="#F0F0F0")
    fila_botones.pack()
    fila_botones_list = []
    for asiento in range(8):
        btn = tk.Button(fila_botones, text=f"L", width=4, bg="#32CD32", fg="white",
                        command=lambda f=fila, a=asiento: seleccionar_asiento(f, a))
        btn.pack(side=tk.LEFT, padx=2, pady=2)
        fila_botones_list.append(btn)
    botones.append(fila_botones_list)
    
# CONTADORES------------------------------------------------------------------------------------------------------------------------------

# Etiqueta para mostrar el número de puestos libres
lbl_contador = tk.Label(frame_asientos, text="Puestos libres: 64 \n Seleccionados: 0", bg="#F0F0F0", font=("Arial", 12))
lbl_contador.pack(pady=5)

# BOTONES----------------------------------------------------------------------------------------------------------------------------------

# Botón para encontrar los mejores puestos disponibles
tk.Button(frame_asientos, text="    Mejores Puestos    ", command=encontrar_mejor_puesto,padx=8, pady=8, bg="#000000", fg="white", font=("Arial", 12)).pack(pady=5)
# Botón para confirmar las reservas seleccionadas
tk.Button(frame_asientos, text="  Confirmar Reservas  ", command=confirmar_reservas, padx=8, pady=8, bg="#000000", fg="white", font=("Arial", 12)).pack(pady=5)
# Botón para volver al menú de selección de sala
tk.Button(frame_asientos, text=" Volver ", command=volver_a_sala,padx=8, pady=8, bg="#000000", fg="white", font=("Arial", 12)).pack(pady=5)

# CONFIGURACION COLORES L y O ---------------------------------------------------------------------------------------------------------------

# Etiqueta para mostrar el estado de los asientos ("L: libre" , "O: ocupado", "S: seleccionar")
tk.Label(frame_asientos, text="L: libre", bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
# Canvas para mostrar un cuadrado pequeño de color para asientos libres
canvas_libre = tk.Canvas(frame_asientos, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
canvas_libre.create_rectangle(5, 5, 15, 15, fill="#32CD32")
canvas_libre.pack(anchor=tk.W)
tk.Label(frame_asientos, text="O: ocupado", bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
# Canvas para mostrar un cuadrado pequeño de color para asientos ocupados
canvas_ocupado = tk.Canvas(frame_asientos, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
canvas_ocupado.create_rectangle(5, 5, 15, 15, fill="#FF6347")
canvas_ocupado.pack(anchor=tk.W)
#Configuracion del color de seleccion
tk.Label(frame_asientos, text="S: seleccionar", bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
# Canvas para mostrar un cuadrado pequeño de color para asientos seleccionados
canvas_ocupado = tk.Canvas(frame_asientos, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
canvas_ocupado.create_rectangle(5, 5, 15, 15, fill="#FFD700")
canvas_ocupado.pack(anchor=tk.W)

# EJECUCION DE LA VENTANA--------------------------------------------------------------------------------------------------------------
# Ejecutar la ventana
ventana.mainloop()
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Lista para almacenar las reservas realizadas
reservas_realizadas = []

# Datos de películas y asientos
peliculas = {
    "Pelicula 1": {
        "horarios": ["10:00", "13:00", "16:00", "19:00"],
        "imagen_url": "https://colonfilm.com/wp-content/uploads/2021/04/bohemian-rhapsody-poster.webp"
    },
    "Pelicula 2": {
        "horarios": ["11:00", "14:00", "17:00", "20:00"],
        "imagen_url": "https://m.media-amazon.com/images/I/61UukTiUWKL._AC_UF894,1000_QL80_.jpg"
    },
    "Pelicula 3": {
        "horarios": ["12:00", "15:00", "18:00", "21:00"],
        "imagen_url": "https://i.blogs.es/682e23/81174579c578a791d10e4566f2732eac/450_1000.jpg"
    }
}

# Matriz de asientos (0: libre, 1: ocupado)
asientos = [[[0]*8 for _ in range(8)] for _ in range(3)]

# Funciones para la interfaz gráfica
def ver_horarios(pelicula):
    horarios_disponibles = "\n".join(peliculas[pelicula]["horarios"])
    messagebox.showinfo("Horarios Disponibles", f"Horarios disponibles para {pelicula}:\n{horarios_disponibles}")

def seleccionar_pelicula(pelicula):
    frame_peliculas.pack_forget()
    horas.set(peliculas[pelicula]["horarios"])
    frame_hora.pack()

def seleccionar_hora():
    seleccion = lista_horas.curselection()
    if seleccion:
        frame_hora.pack_forget()
        frame_sala.pack()
    else:
        messagebox.showwarning("Selección inválida", "Por favor seleccione una hora.")

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

def reservar_asiento(fila, asiento):
    if asientos_actuales[fila][asiento] == 0:
        asientos_actuales[fila][asiento] = 1
        botones[fila][asiento].config(bg="#FF6347", text="O")
        actualizar_contador()
        reservas_realizadas.append((fila, asiento))
        messagebox.showinfo("Reserva", f"Asiento {chr(65+asiento)}{fila+1} reservado con éxito")
    else:
        messagebox.showwarning("Reserva", f"Asiento {chr(65+asiento)}{fila+1} ya está ocupado")

def actualizar_contador():
    libres = sum(row.count(0) for row in asientos_actuales)
    lbl_contador.config(text=f"Puestos libres: {libres}")

def actualizar_asientos():
    for fila in range(8):
        for asiento in range(8):
            if asientos_actuales[fila][asiento] == 0:
                botones[fila][asiento].config(bg="#32CD32", text="L")
            else:
                botones[fila][asiento].config(bg="#FF6347", text="O")

def hay_asientos_disponibles(asientos_sala):
    return any(0 in fila for fila in asientos_sala)

def encontrar_mejor_puesto():
    for fila in range(8):
        mejor_distancia = float('inf')
        mejor_asiento = None
        for asiento in range(8):
            if asientos_actuales[fila][asiento] == 0:
                distancia = abs(asiento - 3.5)
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_asiento = asiento
        if mejor_asiento is not None:
            botones[fila][mejor_asiento].config(bg="#FFD700")
            return

def borrar_ultima_reserva():
    if reservas_realizadas:
        fila, asiento = reservas_realizadas.pop()
        asientos_actuales[fila][asiento] = 0
        botones[fila][asiento].config(bg="#32CD32", text="L")
        actualizar_contador()
        messagebox.showinfo("Reserva", f"Última reserva ({chr(65+asiento)}{fila+1}) borrada con éxito")
    else:
        messagebox.showinfo("Reserva", "No hay reservas para borrar")

def volver_a_pelicula():
    frame_hora.pack_forget()
    frame_peliculas.pack()

def volver_a_hora():
    frame_sala.pack_forget()
    frame_hora.pack()

def volver_a_sala():
    frame_asientos.pack_forget()
    frame_sala.pack()

def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if usuario == "Elian" and contrasena == "2004":
        frame_login.pack_forget()
        frame_peliculas.pack()
    else:
        messagebox.showwarning("Inicio de Sesión Fallido", "Usuario o contraseña incorrectos")

# Interfaz gráfica
ventana = tk.Tk()
ventana.geometry("550x695")
ventana.resizable(False, False)
ventana.title("Reserva de Asientos de Cine")
ventana.configure(bg="#F0F0F0")

# Marco para el inicio de sesión
frame_login = tk.Frame(ventana, bg="#F0F0F0", padx=20, pady=20)
frame_login.pack()

# Agregar imagen de inicio de sesión
url_imagen_login = "https://blogs.unsw.edu.au/nowideas/files/2017/03/invertir-cine.jpg"  # Cambia esto por la URL de tu imagen
response = requests.get(url_imagen_login)
imagen_login = Image.open(BytesIO(response.content))
imagen_login = imagen_login.resize((350, 350), Image.LANCZOS)
imagen_login = ImageTk.PhotoImage(imagen_login)

label_imagen_login = tk.Label(frame_login, image=imagen_login, bg="#F0F0F0")
label_imagen_login.image = imagen_login
label_imagen_login.pack()

tk.Label(frame_login, text="Usuario:", bg="#F0F0F0", font=("Arial", 15), padx=20, pady=10).pack(pady=10)
entry_usuario = tk.Entry(frame_login, font=("Arial", 12))
entry_usuario.pack()
tk.Label(frame_login, text="Contraseña:", bg="#F0F0F0", font=("Arial", 15), padx=20, pady=10).pack(pady=10)
entry_contrasena = tk.Entry(frame_login, show="*", font=("Arial", 12))
entry_contrasena.pack()
tk.Button(frame_login, text="Iniciar Sesión", command=iniciar_sesion, bg="#FF6347", fg="white", font=("Arial", 13), padx=20, pady=10).pack(pady=20)

# Marco para la selección de película
frame_peliculas = tk.Frame(ventana, bg="#F0F0F0", padx=20, pady=20)

for pelicula, info in peliculas.items():
    url_imagen = info["imagen_url"]
    response = requests.get(url_imagen)
    imagen = Image.open(BytesIO(response.content))
    imagen = imagen.resize((120, 120), Image.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)
    
    label = tk.Label(frame_peliculas, image=imagen, text=pelicula, compound=tk.TOP, bg="#F0F0F0")
    label.image = imagen
    label.pack(side=tk.TOP, padx=10, pady=10)
    
    boton_ver = tk.Button(frame_peliculas, text="Seleccionar Hora y Sala", command=lambda p=pelicula: seleccionar_pelicula(p))
    boton_ver.pack(side=tk.TOP, padx=5, pady=5)

# Marco para la selección de hora
frame_hora = tk.Frame(ventana, bg="#F0F0F0", padx=70, pady=70)
horas = tk.StringVar(value=[])
tk.Label(frame_hora, text="Seleccione una Hora:", bg="#F0F0F0", font=("Arial", 15)).pack()
lista_horas = tk.Listbox(frame_hora, listvariable=horas, selectbackground="#FF6347", font=("Arial", 12))
lista_horas.pack()
tk.Button(frame_hora, text="Seleccionar Sala", command=seleccionar_hora, bg="#FF6347", fg="white", font=("Arial", 13)).pack(pady=10)
tk.Button(frame_hora, text="Volver", command=volver_a_pelicula, padx=15, bg="#32CD32", fg="white", font=("Arial", 13)).pack(pady=10)

# Marco para la selección de sala
frame_sala = tk.Frame(ventana, bg="#F0F0F0", padx=70, pady=70)
tk.Label(frame_sala, text="Seleccione una Sala:", bg="#F0F0F0", font=("Arial", 15)).pack()
lista_salas = tk.Listbox(frame_sala, selectbackground="#FF6347", font=("Arial", 12))
for i in range(1, 4):
    lista_salas.insert(tk.END, f"Sala {i}")
lista_salas.pack()
tk.Button(frame_sala, text="Seleccionar Asientos", command=seleccionar_sala, bg="#FF6347", fg="white", font=("Arial", 13)).pack(pady=10)
tk.Button(frame_sala, text="Volver", command=volver_a_hora, padx=15, bg="#32CD32", fg="white", font=("Arial", 13)).pack(pady=10)

# Marco para la selección de asientos
frame_asientos = tk.Frame(ventana, bg="#F0F0F0", padx=10, pady=10)
tk.Label(frame_asientos, text="Seleccione un Asiento:", bg="#F0F0F0", font=("Arial", 15)).pack()
botones = []
frame_botones = tk.Frame(frame_asientos, bg="#F0F0F0")
frame_botones.pack()

asientos_actuales = None

# Crear los botones para seleccionar los asientos
for fila in range(8):
    fila_botones = tk.Frame(frame_botones, bg="#F0F0F0")
    fila_botones.pack()
    fila_botones_list = []
    for asiento in range(8):
        btn = tk.Button(fila_botones, text="L", width=4, bg="#32CD32", fg="white",
                        command=lambda f=fila, a=asiento: reservar_asiento(f, a))
        btn.pack(side=tk.LEFT, padx=2, pady=2)
        fila_botones_list.append(btn)
    botones.append(fila_botones_list)

# Etiqueta para mostrar el número de puestos libres
lbl_contador = tk.Label(frame_asientos, text="Puestos libres: 64", bg="#F0F0F0", font=("Arial", 12))
lbl_contador.pack(pady=10)

# Botón para encontrar los mejores puestos disponibles
tk.Button(frame_asientos, text="Mejores Puestos", command=encontrar_mejor_puesto, padx=8, pady=8, bg="#FFD700", fg="white", font=("Arial", 12)).pack(pady=5)
# Botón para borrar la última reserva realizada
tk.Button(frame_asientos, text="Borrar Última Reserva", command=borrar_ultima_reserva, padx=8, pady=8, bg="#FF6347", fg="white", font=("Arial", 12)).pack(pady=5)
# Botón para volver al menú de selección de sala
tk.Button(frame_asientos, text="Volver", command=volver_a_sala, padx=8, pady=8, bg="#32CD32", fg="white", font=("Arial", 12)).pack(pady=5)

# Etiqueta para mostrar el estado de los asientos ("L: libre" y "O: ocupado")
tk.Label(frame_asientos, text="L: libre", bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
canvas_libre = tk.Canvas(frame_asientos, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
canvas_libre.create_rectangle(5, 5, 15, 15, fill="#32CD32")
canvas_libre.pack(anchor=tk.W)
tk.Label(frame_asientos, text="O: ocupado", bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
canvas_ocupado = tk.Canvas(frame_asientos, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
canvas_ocupado.create_rectangle(5, 5, 15, 15, fill="#FF6347")
canvas_ocupado.pack(anchor=tk.W)

# Ejecutar la ventana
ventana.mainloop()

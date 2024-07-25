import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
from colores import *  # Asegúrate de importar los colores adecuados
import login  # Importar el módulo de login para usar la variable global usuario_id_global
from datetime import datetime  # Importar datetime para manejar la fecha y hora
import json  # Importar json para manejar el almacenamiento de tickets

# Conectar a la base de datos de películas (se creará si no existe)
conn_peliculas = sqlite3.connect('cartelera.db')
cursor_peliculas = conn_peliculas.cursor()

# Conectar a la base de datos de usuarios (se creará si no existe)
conn_usuarios = sqlite3.connect('usuarios.db')
cursor_usuarios = conn_usuarios.cursor()

# Crear las tablas si no existen
cursor_peliculas.execute('''
CREATE TABLE IF NOT EXISTS peliculas (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    genero TEXT,
    duracion TEXT,
    imagen TEXT,
    sinopsis TEXT
)
''')

cursor_peliculas.execute('''
CREATE TABLE IF NOT EXISTS horarios (
    id INTEGER PRIMARY KEY,
    id_pelicula INTEGER,
    horario TEXT,
    sala TEXT,
    FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
)
''')

# Crear la tabla reservas en la base de datos de usuarios
cursor_usuarios.execute('''
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    id_pelicula INTEGER,
    hora TEXT,
    sala TEXT,
    asiento TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
    FOREIGN KEY (id_pelicula) REFERENCES peliculas (id)
)
''')

# Variable global para almacenar los asientos seleccionados
asientos_seleccionados = {}

# Función para crear y mostrar el estado de los asientos
def crear_estado_asientos(frame):
    estado = {
        "simbolo": ("L", "O", "S"),
        "estados": ("Libre", "Ocupado", "Seleccionado"),
        "colores": (color_libre, color_ocupado, color_seleccionado)
    }
    for i in range(3):
        estado_frame = tk.Frame(frame, bg=color_fondo, bd=2, relief="groove")
        estado_frame.grid(row=i, column=0, pady=10, padx=10, sticky='ew')
        
        canvas_estado = tk.Canvas(estado_frame, width=20, height=20, bg=color_fondo, highlightthickness=0)
        canvas_estado.create_rectangle(2, 2, 18, 18, fill=estado['colores'][i])
        canvas_estado.pack(side=tk.LEFT, padx=5)
        
        tk.Label(estado_frame, text=f"{estado['simbolo'][i]}: {estado['estados'][i]}", bg=color_fondo, fg="black", font=fuente_estado_asiento).pack(side=tk.LEFT)

# Función para mostrar el registro de asientos
def mostrar_registro_asientos(cuerpo_principal, pelicula_id, hora, sala_index, usuario_id):
    # Limpiar el cuerpo_principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Dividir el cuerpo principal en dos frames
    frame_izquierdo = tk.Frame(cuerpo_principal, bg="black")
    frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    frame_derecho = tk.Frame(cuerpo_principal, bg=color_fondo)
    frame_derecho.grid(row=0, column=1, sticky="nsew", padx=50, pady=20)

    cuerpo_principal.grid_columnconfigure(0, weight=3)
    cuerpo_principal.grid_columnconfigure(1, weight=1)
    cuerpo_principal.grid_rowconfigure(0, weight=1)

    # Obtener los asientos seleccionados para esta combinación de película, hora y sala
    key = (pelicula_id, hora, sala_index)

    if key not in asientos_seleccionados:
        asientos_seleccionados[key] = [[0]*11 for _ in range(11)]
    matriz_asientos = asientos_seleccionados[key]

    # Consultar las reservas existentes en la base de datos para marcarlas como ocupadas
    cursor_usuarios.execute('''
        SELECT asiento FROM reservas
        WHERE id_pelicula = ? AND hora = ? AND sala = ?
    ''', (pelicula_id, hora, sala_index))
    reservas_existentes = cursor_usuarios.fetchall()

    for reserva in reservas_existentes:
        asiento = reserva[0]
        fila = ord(asiento[0]) - ord('A')  # Convertir letra a índice de fila
        columna = int(asiento[1:]) - 1  # Convertir número de columna a índice
        matriz_asientos[fila][columna] = 2  # Marcar asiento como ocupado

    # Cargar las imágenes de los asientos
    img_libre = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientolibre.png").resize((60, 60)))
    img_ocupado = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientoocupado.png").resize((60, 60)))
    img_seleccionado = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientoseleccionado.png").resize((60, 60)))
    img_mejor_asiento = ImageTk.PhotoImage(Image.open("/home/joaoelian/Descargas/asientomejor.png").resize((60, 60)))
    
    # Función para seleccionar un asiento
    def seleccionar_asiento(i, j):
        if 0 <= i < 11 and 0 <= j < 11:
            estado_actual = matriz_asientos[i][j]
            if estado_actual == 0:  # Asiento libre
                matriz_asientos[i][j] = 1  # Marcar como seleccionado
                botones_asientos[i][j].configure(image=img_seleccionado)
            elif estado_actual == 1:  # Asiento seleccionado
                matriz_asientos[i][j] = 0  # Volver a marcar como libre
                botones_asientos[i][j].configure(image=img_libre)
            elif estado_actual == 2:  # Asiento ocupado
                messagebox.showerror("Error", "Este asiento ya está ocupado.")

    # Crear y mostrar el título de la selección de asientos
    label_horarios = tk.Label(frame_izquierdo, text="Selecciona tus asientos", font=("Helvetica", 24, "bold"), fg=color_titulo, bg="black")
    label_horarios.pack(pady=(10, 20))

    # Crear un frame para contener la matriz de botones
    frame_asientos = tk.Frame(frame_izquierdo, bg="black")
    frame_asientos.pack(expand=True)

    # Crear la matriz de botones para los asientos
    botones_asientos = []
    for i in range(11):
        fila_botones = []
        for j in range(11):
            boton = tk.Button(frame_asientos, image=img_libre, width=60, height=60, bd=2, relief="raised")
            boton.grid(row=i, column=j, padx=5, pady=5)
            boton.config(command=lambda i=i, j=j: seleccionar_asiento(i, j))
            if matriz_asientos[i][j] == 1:
                boton.config(image=img_seleccionado)
            elif matriz_asientos[i][j] == 2:
                boton.config(image=img_ocupado)
            fila_botones.append(boton)
        botones_asientos.append(fila_botones)

    # Función para buscar los cuatro mejores asientos
    def buscar_mejor_asiento():
        mejores_asientos = []
        for i in range(11):
            for j in range(11):
                if matriz_asientos[i][j] == 0:
                    mejores_asientos.append((i, j, abs(3 - i) + abs(3 - j)))
        mejores_asientos.sort(key=lambda x: x[2])
        for i in range(min(4, len(mejores_asientos))):
            fila, columna, _ = mejores_asientos[i]
            botones_asientos[fila][columna].configure(image=img_mejor_asiento)

    # Función para confirmar las reservas
    def confirmar_reservas():
        if usuario_id is None:
            messagebox.showerror("Error", "No se ha identificado el usuario.")
            return
        
        reservas = []
        asientos_confirmados = []  # Lista para almacenar los asientos confirmados
        for i in range(11):
            for j in range(11):
                if matriz_asientos[i][j] == 1:
                    matriz_asientos[i][j] = 2
                    botones_asientos[i][j].configure(image=img_ocupado)
                    fila = chr(i + ord('A'))  # Convertir fila a letra
                    columna = j + 1  # Convertir columna a número
                    asiento = f"{fila}{columna}"
                    sala_numero = int(sala_index.replace('Sala ', ''))
                    reservas.append((usuario_id, pelicula_id, hora, f"Sala {sala_numero}", asiento))
                    asientos_confirmados.append(asiento)  # Añadir asiento a la lista de confirmados

        cursor_usuarios.executemany('INSERT INTO reservas (id_usuario, id_pelicula, hora, sala, asiento) VALUES (?, ?, ?, ?, ?)', reservas)
        conn_usuarios.commit()

        # Generar y mostrar el ticket
        generar_ticket(usuario_id, pelicula_id, hora, f"Sala {sala_numero}", asientos_confirmados)
        messagebox.showinfo("Reservas Confirmadas", "¡Tus reservas han sido confirmadas!")

    # Función para generar el ticket
    def generar_ticket(usuario_id, pelicula_id, hora, sala, asientos):
        usuario_nombre = obtener_nombre_usuario(usuario_id)
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pelicula_nombre = obtener_nombre_pelicula(pelicula_id)
        
        ticket_texto = (
            f"CINEMA MANTA\n"
            f"------------------------\n"
            f"Usuario: {usuario_nombre}\n"
            f"Película: {pelicula_nombre}\n"
            f"Hora: {hora}\n"
            f"Sala: {sala}\n"
            f"Asientos: {', '.join(asientos)}\n"
            f"Fecha y Hora: {fecha_hora_actual}\n"
            f"------------------------\n"
            f"¡Disfruta la película!\n"
        )
        
        # Mostrar el ticket en el cuadro de texto
        ticket_display.delete(1.0, tk.END)
        ticket_display.insert(tk.END, ticket_texto)

        # Guardar el ticket en un archivo JSON
        guardar_ticket(usuario_nombre, {
            "usuario": usuario_nombre,
            "pelicula": pelicula_nombre,
            "hora": hora,
            "sala": sala,
            "asientos": asientos,
            "fecha_hora": fecha_hora_actual
        })

    # Función para obtener el nombre del usuario (implementa esta función según tu estructura de base de datos)
    def obtener_nombre_usuario(usuario_id):
        cursor_usuarios.execute('SELECT nombre FROM usuarios WHERE id = ?', (usuario_id,))
        resultado = cursor_usuarios.fetchone()
        return resultado[0] if resultado else "Desconocido"

    # Función para obtener el nombre de la película (implementa esta función según tu estructura de base de datos)
    def obtener_nombre_pelicula(pelicula_id):
        cursor_peliculas.execute('SELECT titulo FROM peliculas WHERE id = ?', (pelicula_id,))
        resultado = cursor_peliculas.fetchone()
        return resultado[0] if resultado else "Desconocido"

    # Función para guardar el ticket en un archivo JSON
    def guardar_ticket(usuario_nombre, ticket_info):
        try:
            with open('tickets.json', 'r') as file:
                tickets = json.load(file)
        except FileNotFoundError:
            tickets = {}
        
        if usuario_nombre not in tickets:
            tickets[usuario_nombre] = []

        tickets[usuario_nombre].append(ticket_info)

        with open('tickets.json', 'w') as file:
            json.dump(tickets, file, indent=4)

    # Crear y mostrar el estado de los asientos
    crear_estado_asientos(frame_derecho)
    
    # Crear y colocar el botón para confirmar reservas
    boton_confirmar = tk.Button(frame_derecho, text="Guardar Selección", fg=COLOR_TEXTO_NORMAL, bg=COLOR_BOTON_NORMAL, font=("Helvetica", 16), bd=2, relief="raised", command=confirmar_reservas)
    boton_confirmar.grid(row=3, column=0, pady=10, sticky='ew')

    # Crear y colocar el botón para buscar el mejor asiento
    boton_buscar_mejor = tk.Button(frame_derecho, text="Buscar Mejor Asiento", fg=COLOR_TEXTO_NORMAL, bg=COLOR_BOTON_NORMAL, font=("Helvetica", 16), bd=2, relief="raised", command=buscar_mejor_asiento)
    boton_buscar_mejor.grid(row=4, column=0, pady=10, sticky='ew')

    # Crear el cuadro de texto para mostrar el ticket generado
    ticket_display = tk.Text(frame_derecho, height=10, width=50, bg="white", fg="black", font=("Helvetica", 12), bd=2, relief="sunken")
    ticket_display.grid(row=5, column=0, pady=10, sticky='ew')















import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from db import *
from utils import *
from constants import ANCHO_IMAGEN, ALTO_IMAGEN, imagenes_pelis, COLOR_CUERPO_PRINCIPAL

#========================================= FUNCIONES PARA LA CARGA DE PELICULA  ===============================================

# Número de columnas por fila para mostrar las películas
COLUMNAS_POR_FILA = 5

# Función para mostrar/ocultar el panel lateral del menú
def toggle_panel(menu_lateral):
    # Si el menú lateral es visible, lo oculta
    if menu_lateral.winfo_viewable():
        menu_lateral.pack_forget()
    # Si el menú lateral está oculto, lo muestra
    else:
        menu_lateral.pack(side=tk.LEFT, fill=tk.Y)

# Función para mostrar la cartelera de películas
def mostrar_cartelera(cuerpo_principal):
    # Carga la lista de películas desde la base de datos o archivo
    peliculas = cargar_cartelera()

    # Limpia el área principal antes de mostrar las películas
    clear_frame(cuerpo_principal)

    # Itera sobre cada película y la muestra en el área principal
    for idx, pelicula in enumerate(peliculas):
        mostrar_pelicula(cuerpo_principal, idx, pelicula)

# Función para mostrar los detalles de una película individual
def mostrar_pelicula(cuerpo_principal, idx, pelicula):
    titulo = pelicula[1]
    genero = pelicula[2]
    duracion = pelicula[3]
    sinopsis = pelicula[4]

    try:
        # Intenta cargar la imagen de la película
        if pelicula[5] in imagenes_pelis:
            foto = imagenes_pelis[pelicula[5]]
        else:
            imagen = Image.open(pelicula[5])
            imagen = imagen.resize((ANCHO_IMAGEN, ALTO_IMAGEN), Image.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            imagenes_pelis[pelicula[5]] = foto
    except Exception as e:
        # Si hay un error al cargar la imagen, lo imprime y establece la foto como None
        print(f"Error al cargar la imagen {pelicula[5]}: {e}")
        foto = None

    # Crea un contenedor (frame) para la película con un borde elevado
    frame_pelicula = tk.Frame(cuerpo_principal, bd=2, relief=tk.RAISED, padx=10, pady=10, bg="#000000")
    frame_pelicula.grid(row=idx // COLUMNAS_POR_FILA, column=idx % COLUMNAS_POR_FILA, padx=10, pady=10)

    # Si la imagen se cargó correctamente, la muestra en el contenedor
    if foto:
        label_imagen = tk.Label(frame_pelicula, image=foto)
        # Necesario para evitar que la imagen sea recolectada por el garbage collector
        label_imagen.image = foto
        label_imagen.pack()

        
#===================================== INFORMACION DE LAS PELICULA EN LA CARTELERA ==========================================

    # Crea una etiqueta para mostrar el título de la película
    label_titulo = tk.Label(frame_pelicula, text=titulo, font=("Arial", 14), bg="#000000", fg="#ffffff")
    label_titulo.pack()

    # Crea una etiqueta para mostrar el género de la película
    label_genero = tk.Label(frame_pelicula, text=f"Género: {genero}", bg="#000000", fg="#ffffff")
    label_genero.pack()

    # Crea una etiqueta para mostrar la duración de la película en minutos
    label_duracion = tk.Label(frame_pelicula, text=f"Duración: {duracion} min", bg="#000000", fg="#ffffff")
    label_duracion.pack()
    
#============================================== BOTONES ELIMINAR Y EDITAR  =================================================

    # Crea un botón para editar la película
    boton_editar = tk.Button(frame_pelicula, text="Editar", bg="#fff", fg="#000000", 
                        command=lambda id_pelicula=pelicula[0]: mostrar_ventana_edicion(id_pelicula, cuerpo_principal))
    boton_editar.pack(pady=10)

    # Crea un botón para eliminar la película
    boton_eliminar = tk.Button(frame_pelicula, text="Eliminar", bg="#fff", fg="#000000",
                        command=lambda id_pelicula=pelicula[0], ventana=frame_pelicula: confirmar_eliminar(id_pelicula, ventana, cuerpo_principal))
    boton_eliminar.pack(pady=10) 
    
#============================================== FUNCION DE ELIMINAR PELICULA ===============================================

# Función para confirmar la eliminación de una película
def confirmar_eliminar(id_pelicula, ventana, cuerpo_principal):
    # Muestra un cuadro de mensaje para confirmar la eliminación
    if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de eliminar esta película?"):
        # Si se confirma, elimina la película
        eliminar_pelicula(id_pelicula)
        # Muestra un mensaje de eliminación exitosa
        messagebox.showinfo("Eliminación Exitosa", "La película ha sido eliminada.")
        # Destruye el marco de la película eliminado
        ventana.destroy()
        # Actualiza la cartelera mostrando todas las películas restantes
        mostrar_cartelera(cuerpo_principal)

# Función para limpiar todos los widgets de un frame
def clear_frame(frame):
    # Itera sobre todos los widgets hijos del frame y los destruye
    for widget in frame.winfo_children():
        widget.destroy()


#============================================== VENTANA EDITAR PELICULAS ===================================================

# Función para mostrar una ventana de edición de película
def mostrar_ventana_edicion(id_pelicula, cuerpo_principal):
    """
    Muestra una ventana para editar los datos de una película.

    Args:
        id_pelicula (int): El ID de la película a editar.
        cuerpo_principal (tk.Frame): El frame principal de la aplicación
    """
    # Crea una nueva ventana de nivel superior para la edición
    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Película")
    ventana_edicion.configure(bg="white")
    
    # Configura el estilo para los widgets ttk
    estilo = ttk.Style()
    estilo.configure('TLabel', background="white", font=('Arial', 11))
    estilo.configure('TEntry', font=('Arial', 11))
    estilo.configure('TButton', font=('Arial', 11), background="white")

    # Selecciona la película a editar
    pelicula = seleccionar_pelicula(id_pelicula)

    # Crea un frame para el formulario de edición
    frame_formulario = tk.Frame(ventana_edicion, bg="white", padx=10, pady=10)
    frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Crea entradas para los diferentes campos de la película
    entry_titulo = crear_label_y_entry(frame_formulario, "Título:", pelicula[1], 0, 0 )
    entry_genero = crear_label_y_entry(frame_formulario, "Género:", pelicula[2], 1, 0 )
    entry_duracion = crear_label_y_entry(frame_formulario, "Duración (minutos):", pelicula[3], 2, 0)

    # Estilo para la sinopsis
    estilo_label_sinopsis = {'bg': "white", 'fg': '#333', 'font': ('Arial', 11)}
    estilo_entry_sinopsis = {'bg': 'white', 'fg': '#333', 'font': ('Arial', 11)}

    # Crea una etiqueta y un cuadro de texto para la sinopsis
    label_sinopsis = tk.Label(frame_formulario, text="Sinopsis:", **estilo_label_sinopsis)
    label_sinopsis.grid(row=3, column=0, padx=10, pady=10, sticky=tk.NE)

    entry_sinopsis = tk.Text(frame_formulario, width=40, height=10, **estilo_entry_sinopsis)
    entry_sinopsis.grid(row=3, column=1, padx=10, pady=10, sticky=tk.NSEW)
    entry_sinopsis.insert(tk.END, pelicula[4])

    # Crea una entrada para la imagen
    entry_imagen = crear_label_y_entry(frame_formulario, "Imagen:", pelicula[5], 4, 0,)

    # Función para seleccionar una imagen y mostrarla en la entrada
    def seleccionar_imagen_y_mostrar():
        filename = seleccionar_imagen()
        if filename:
            entry_imagen.config(state="normal")
            entry_imagen.delete(0, tk.END)
            entry_imagen.insert(0, filename)
            entry_imagen.config(state="readonly")

    # Botón para seleccionar una imagen
    boton_seleccionar_imagen = ttk.Button(frame_formulario, text="Seleccionar Imagen", command=seleccionar_imagen_y_mostrar)
    boton_seleccionar_imagen.grid(row=4, column=2, padx=10, pady=10)

    # Sección de horarios y salas
    frame_horarios = tk.Frame(ventana_edicion, bg="white", padx=10, pady=10)
    frame_horarios.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)

    # Etiqueta para la sección de horarios y salas
    label_horarios = ttk.Label(frame_horarios, text="Horarios y Salas:", font=('Arial', 12, 'bold'))
    label_horarios.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)

    # Cargar los horarios de la película
    horarios = cargar_horarios_pelicula(id_pelicula)

    # Mostrar cada horario existente con opciones para editar y eliminar
    for horario in horarios:
        horario_str = f"{horario[2]} - Sala: {horario[3]}"
        row_frame = tk.Frame(frame_horarios, bg="white")
        row_frame.grid(row=horarios.index(horario) + 1, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
        
        # Crea una etiqueta para mostrar el horario y la sala
        label_horario = ttk.Label(row_frame, text=horario_str)
        label_horario.grid(row=0, column=0, padx=10, pady=5)
        
        # Crea botones para editar y eliminar el horario
        boton_editar_horario = ttk.Button(row_frame, text="Editar", 
                                        command=lambda id_horario=horario[0]: mostrar_ventana_edicion_horario(id_horario, cuerpo_principal))
        boton_editar_horario.grid(row=0, column=1, padx=5, pady=5)

        boton_eliminar_horario = ttk.Button(row_frame, text="Eliminar", 
                                            command=lambda id_horario=horario[0], row_frame=row_frame: eliminar_horario_local(id_horario, row_frame))
        boton_eliminar_horario.grid(row=0, column=2, padx=5, pady=5)

        boton_info_sala = ttk.Button(row_frame, text="Info Sala", command=lambda sala=horario[3]: mostrar_info_sala(id_pelicula, sala))
        boton_info_sala.grid(row=0, column=3, padx=5, pady=5)
    
    # Entradas para agregar nuevos horarios y salas
    entry_nuevo_horario = crear_label_y_entry(frame_horarios, "Nuevo Horario:", "", len(horarios) + 1, 0)
    entry_nueva_sala = crear_label_y_entry(frame_horarios, "Nueva Sala:", "", len(horarios) + 1, 1)

    # Función para agregar un nuevo horario
    def agregar_horario():
        nuevo_horario = entry_nuevo_horario.get()
        nueva_sala = entry_nueva_sala.get()
        if nuevo_horario and nueva_sala:
            id_nuevo_horario = insertar_horario(id_pelicula, nuevo_horario, nueva_sala)
            horarios.append((id_nuevo_horario, id_pelicula, nuevo_horario, nueva_sala))
            horario_str = f"{nuevo_horario} - Sala: {nueva_sala}"
            row_frame = tk.Frame(frame_horarios, bg="white")
            row_frame.grid(row=len(horarios) + 1, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

            label_horario = ttk.Label(row_frame, text=horario_str)
            label_horario.grid(row=0, column=0, padx=10, pady=5)

            boton_editar_horario = ttk.Button(row_frame, text="Editar", 
                                            command=lambda id_horario=id_nuevo_horario: mostrar_ventana_edicion_horario(id_horario, cuerpo_principal))
            boton_editar_horario.grid(row=0, column=1, padx=5, pady=5)

            boton_eliminar_horario = ttk.Button(row_frame, text="Eliminar", 
                                                command=lambda id_horario=id_nuevo_horario, row_frame=row_frame: eliminar_horario_local(id_horario, row_frame))
            boton_eliminar_horario.grid(row=0, column=2, padx=5, pady=5)

            boton_info_sala = ttk.Button(row_frame, text="Info Sala", command=lambda sala=nueva_sala: mostrar_info_sala(id_pelicula, sala))
            boton_info_sala.grid(row=0, column=3, padx=5, pady=5)

            entry_nuevo_horario.delete(0, tk.END)
            entry_nueva_sala.delete(0, tk.END)

    # Botón para agregar un nuevo horario
    boton_agregar_horario = ttk.Button(frame_horarios, text="Agregar Horario", command=agregar_horario)
    boton_agregar_horario.grid(row=len(horarios) + 1, column=2, padx=10, pady=10)

    # Crea un frame negro para los botones de actualizar y cancelar
    frame_botones = tk.Frame(ventana_edicion, bg="black", padx=10, pady=10)
    frame_botones.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NSEW)

    # Función para actualizar los datos de la película
    def actualizar_datos_pelicula():
        titulo = entry_titulo.get()
        genero = entry_genero.get()
        duracion = entry_duracion.get()
        sinopsis = entry_sinopsis.get("1.0", tk.END).strip()
        imagen = entry_imagen.get()

        if titulo and duracion:
            actualizar_pelicula(id_pelicula, titulo, genero, duracion, sinopsis, imagen)
            eliminar_horarios_por_pelicula(id_pelicula)
            for horario in horarios:
                insertar_horario(id_pelicula, horario[2], horario[3])
            messagebox.showinfo("Actualización Exitosa", "La película ha sido actualizada.")
            ventana_edicion.destroy()
            mostrar_cartelera(cuerpo_principal)
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")

    # Botón para actualizar la película
    boton_actualizar = tk.Button(frame_botones, text="Actualizar Película", command=actualizar_datos_pelicula, bg="black", fg="white")
    boton_actualizar.grid(row=0, column=0, padx=10, pady=10)

    # Botón para cancelar la edición y cerrar la ventana
    boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=ventana_edicion.destroy, bg="black", fg="white")
    boton_cancelar.grid(row=0, column=1, padx=10, pady=10)

    # Configura las columnas y filas de la ventana de edición
    ventana_edicion.columnconfigure(0, weight=1)
    ventana_edicion.rowconfigure(5, weight=1)

# Función para eliminar un horario localmente
def eliminar_horario_local(id_horario, row_frame):
    # Muestra un cuadro de mensaje para confirmar la eliminación del horario
    if messagebox.askyesno("Eliminar Horario", "¿Estás seguro de que deseas eliminar este horario?"):
        # Si se confirma, elimina el horario y destruye el frame de la fila
        eliminar_horario(id_horario)
        row_frame.destroy()

#================================================= VENTANA DE INFO SALA ==============================================

COLOR_CUERPO_PRINCIPAL = "#f0f0f0"
NUM_FILAS = 11
NUM_COLUMNAS = 11

def mostrar_info_sala(id_pelicula, sala):
    """
    Muestra información detallada de una sala, incluyendo la disposición de los asientos
    y los usuarios que han reservado asientos en esa sala para una película específica.

    Args:
        id_pelicula (int): El ID de la película.
        sala (int): El número de la sala.
    """
    global tabla_usuarios  # Declarar tabla_usuarios como global

    def resetear_asientos():
        """
        Resetea todos los asientos a su estado libre ('L') y elimina todas las reservas
        de la base de datos para la película y sala actuales.
        """
        for i in range(NUM_FILAS):
            for j in range(NUM_COLUMNAS):
                matriz_asientos[i][j] = 'L'
                lbl_asientos[i][j].config(text='L', bg='#00ff00')

        # Conectar a la base de datos y eliminar las reservas
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM reservas WHERE id_pelicula = ? AND sala = ?', (id_pelicula, sala))
        conn.commit()
        conn.close()

        # Actualizar la información de la sala y mostrar los usuarios
        actualizar_info_sala()
        mostrar_usuarios()

    def actualizar_info_sala():
        """
        Actualiza la información de los asientos en la sala, marcando los asientos ocupados ('O')
        y mostrando la cantidad de asientos libres y ocupados.
        """
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute('SELECT asiento FROM reservas WHERE id_pelicula = ? AND sala = ?', (id_pelicula, sala))
        reservas = cursor.fetchall()

        for reserva in reservas:
            asiento_ocupado = reserva[0]
            if len(asiento_ocupado) == 2:
                fila = ord(asiento_ocupado[0]) - ord('A')
                columna = int(asiento_ocupado[1]) - 1
            elif len(asiento_ocupado) == 3:
                fila = ord(asiento_ocupado[0]) - ord('A')
                columna = int(asiento_ocupado[1:]) - 1
            matriz_asientos[fila][columna] = 'O'
            lbl_asientos[fila][columna].config(text='O', bg='#ff0000')

        conn.close()

        puestos_libres = sum(row.count('L') for row in matriz_asientos)
        puestos_ocupados = sum(row.count('O') for row in matriz_asientos)

        lbl_puestos_libres.config(text=f"Puestos libres: {puestos_libres}")
        lbl_puestos_ocupados.config(text=f"Puestos ocupados: {puestos_ocupados}")

    def mostrar_usuarios():
        """
        Muestra una lista de usuarios que han reservado asientos en la sala para la película actual,
        incluyendo el número de asientos reservados por cada usuario.
        """
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.nombre, COUNT(r.asiento) as asientos
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id
            WHERE r.id_pelicula = ? AND r.sala = ?
            GROUP BY u.nombre
        ''', (id_pelicula, sala))
        usuarios = cursor.fetchall()

        for row in tabla_usuarios.get_children():
            tabla_usuarios.delete(row)

        for usuario in usuarios:
            tabla_usuarios.insert('', 'end', values=(usuario[0], usuario[1]))

        conn.close()

    def resaltar_asientos(event):
        """
        Resalta los asientos ocupados por un usuario seleccionado en la lista de usuarios.
        """
        for i in range(NUM_FILAS):
            for j in range(NUM_COLUMNAS):
                if matriz_asientos[i][j] == 'O':
                    lbl_asientos[i][j].config(bg='#ff0000')

        selected_items = tabla_usuarios.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        usuario = tabla_usuarios.item(selected_item, 'values')[0]

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT asiento
            FROM reservas r
            JOIN usuarios u ON r.id_usuario = u.id
            WHERE u.nombre = ? AND r.id_pelicula = ? AND r.sala = ?
        ''', (usuario, id_pelicula, sala))
        asientos = cursor.fetchall()

        for asiento in asientos:
            asiento_ocupado = asiento[0]
            if len(asiento_ocupado) == 2:
                fila = ord(asiento_ocupado[0]) - ord('A')
                columna = int(asiento_ocupado[1]) - 1
            elif len(asiento_ocupado) == 3:
                fila = ord(asiento_ocupado[0]) - ord('A')
                columna = int(asiento_ocupado[1:]) - 1

            lbl_asientos[fila][columna].config(bg='#0000ff')

        conn.close()

    # Configuración de la ventana de información de la sala
    ventana_sala = tk.Toplevel()
    ventana_sala.title(f"Información de Sala {sala}")
    ventana_sala.geometry('900x750')
    ventana_sala.resizable(False, False)
    ventana_sala.configure(bg="#2c3e50")

    # Conexión a la base de datos y obtención de reservas
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT asiento FROM reservas WHERE id_pelicula = ? AND sala = ?', (id_pelicula, sala))
    reservas = cursor.fetchall()

    # Creación de la matriz de asientos
    matriz_asientos = [['L' for _ in range(NUM_COLUMNAS)] for _ in range(NUM_FILAS)]
    lbl_asientos = []

    for reserva in reservas:
        asiento_ocupado = reserva[0]
        if len(asiento_ocupado) == 2:
            fila = ord(asiento_ocupado[0]) - ord('A')
            columna = int(asiento_ocupado[1]) - 1
        elif len(asiento_ocupado) == 3:
            fila = ord(asiento_ocupado[0]) - ord('A')
            columna = int(asiento_ocupado[1:]) - 1
        matriz_asientos[fila][columna] = 'O'

    # Creación del frame para la matriz de asientos
    frame_matriz = tk.Frame(ventana_sala, bg="#2c3e50")
    frame_matriz.pack(side=tk.LEFT, padx=10, pady=10)

    for i in range(NUM_FILAS):
        fila_asientos = []
        for j in range(NUM_COLUMNAS):
            texto_asiento = matriz_asientos[i][j]
            estado_color = '#ff0000' if texto_asiento == 'O' else '#00ff00'

            lbl_asiento = tk.Label(frame_matriz, text=texto_asiento, width=4, height=2, relief=tk.RAISED, borderwidth=2, bg=estado_color)
            lbl_asiento.grid(row=i, column=j, padx=5, pady=5)
            fila_asientos.append(lbl_asiento)

        lbl_asientos.append(fila_asientos)

    # Creación del frame para la información adicional de la sala
    frame_info = tk.Frame(ventana_sala, bg="#2c3e50")
    frame_info.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    # Creación de la tabla de usuarios
    tabla_usuarios = ttk.Treeview(frame_info, columns=("Usuario", "Asientos"), show='headings')
    tabla_usuarios.heading("Usuario", text="Usuario")
    tabla_usuarios.heading("Asientos", text="Asientos")
    tabla_usuarios.column("Usuario", width=150)
    tabla_usuarios.column("Asientos", width=100)
    tabla_usuarios.pack(pady=10)
    tabla_usuarios.bind('<<TreeviewSelect>>', resaltar_asientos)

    # Etiquetas para mostrar los puestos libres y ocupados
    lbl_puestos_libres = tk.Label(frame_info, text="", font=('Arial', 12), bg="#2c3e50", fg="#fff")
    lbl_puestos_libres.pack(pady=10)
    lbl_puestos_ocupados = tk.Label(frame_info, text="", font=('Arial', 12), bg="#2c3e50", fg="#fff")
    lbl_puestos_ocupados.pack(pady=10)

    # Botón para resetear los asientos
    btn_resetear = tk.Button(frame_info, text="Resetear asientos", font=('Arial', 12), command=resetear_asientos, bg="#e74c3c", fg="#fff")
    btn_resetear.pack(pady=10)

    # Mostrar los usuarios y actualizar la información de la sala
    mostrar_usuarios()
    actualizar_info_sala()
    conn.close()
#============================================== VENTANA EDICION HORARIOS ===================================================

def mostrar_ventana_edicion_horario(id_horario, cuerpo_principal):
    """
    Muestra una ventana para editar los detalles de un horario específico.

    Args:
        id_horario (int): El ID del horario a editar.
        cuerpo_principal (tk.Frame): El marco principal de la interfaz.
    """
    # Crear una nueva ventana de nivel superior para la edición del horario
    ventana_edicion_horario = tk.Toplevel()
    ventana_edicion_horario.title("Editar Horario")
    ventana_edicion_horario.configure(bg="white")

    # Obtener el horario actual de la base de datos
    horario = seleccionar_horario(id_horario)

    # Crear un frame para el formulario de edición
    frame_formulario = tk.Frame(ventana_edicion_horario, bg="white", padx=10, pady=10)
    frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Crear entradas para editar el horario y la sala
    entry_horario = crear_label_y_entry(frame_formulario, "Horario:", horario[2], 0, 0)
    entry_sala = crear_label_y_entry(frame_formulario, "Sala:", horario[3], 1, 0)

    def guardar_cambios_horario():
        """
        Guarda los cambios realizados en el horario y la sala.
        """
        nuevo_horario = entry_horario.get()
        nueva_sala = entry_sala.get()

        try:
            # Actualizar el horario en la base de datos
            actualizar_horario(id_horario, nuevo_horario, nueva_sala)
            messagebox.showinfo("Actualización Exitosa", "Los cambios han sido guardados.")
            ventana_edicion_horario.destroy()
            mostrar_cartelera(cuerpo_principal)
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el horario: {e}")

    # Crear un frame negro para los botones de guardar cambios y cancelar
    frame_botones = tk.Frame(ventana_edicion_horario, bg="black", padx=10, pady=10)
    frame_botones.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Crear botones para guardar cambios y cancelar
    boton_guardar = tk.Button(frame_botones, text="Guardar Cambios", command=guardar_cambios_horario, bg="black", fg="white")
    boton_guardar.grid(row=0, column=0, padx=10, pady=10)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=ventana_edicion_horario.destroy, bg="black", fg="white")
    boton_cancelar.grid(row=0, column=1, padx=10, pady=10)

    # Configura las columnas y filas de la ventana de edición del horario
    ventana_edicion_horario.columnconfigure(0, weight=1)
    ventana_edicion_horario.rowconfigure(0, weight=1)
    ventana_edicion_horario.resizable(False, False)

def cargar_horarios_pelicula(id_pelicula):
    """
    Carga los horarios asociados a una película específica desde la base de datos.

    Args:
        id_pelicula (int): El ID de la película.

    Returns:
        list: Una lista de horarios con sus detalles.
    """
    horarios = []
    conn, cursor = conectar_db()
    
    # Seleccionar horarios de la base de datos
    cursor.execute('SELECT id, id_pelicula, horario, sala FROM horarios WHERE id_pelicula=?', (id_pelicula,))
    for row in cursor.fetchall():
        horarios.append(row)
    
    cerrar_db(conn)
    return horarios

#============================================== VENTANA AGREGAR PELICULAS ===================================================

def mostrar_ventana_agregar(cuerpo_principal):
    """
    Muestra una ventana para agregar una nueva película con sus detalles y horarios.

    Args:
        cuerpo_principal (tk.Frame): El marco principal de la interfaz.
    """
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Película")
    ventana_agregar.configure(bg='white')  # Fondo blanco para la ventana

    frame_formulario = tk.Frame(ventana_agregar, bg='white', padx=10, pady=10)
    frame_formulario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Crear entradas para los detalles de la película
    entry_titulo = crear_label_y_entry(frame_formulario, "Título:", "", 0, 0)
    entry_genero = crear_label_y_entry(frame_formulario, "Género:", "", 1, 0)
    entry_duracion = crear_label_y_entry(frame_formulario, "Duración (minutos):", "", 2, 0)

    # Crear entrada para la sinopsis
    estilo_label_sinopsis = {'bg': 'white', 'fg': '#333', 'font': ('Arial', 11)}
    estilo_entry_sinopsis = {'bg': '#fff', 'fg': '#333', 'font': ('Arial', 11)}

    label_sinopsis = tk.Label(frame_formulario, text="Sinopsis:", **estilo_label_sinopsis)
    label_sinopsis.grid(row=3, column=0, padx=10, pady=10, sticky=tk.NE)

    entry_sinopsis = tk.Text(frame_formulario, width=40, height=10, **estilo_entry_sinopsis)
    entry_sinopsis.grid(row=3, column=1, padx=10, pady=10, sticky=tk.NSEW)

    # Crear entrada para la imagen
    entry_imagen = crear_label_y_entry(frame_formulario, "Imagen:", "", 4, 0)

    def seleccionar_imagen_y_mostrar():
        """
        Permite seleccionar una imagen y mostrar su ruta en la entrada correspondiente.
        """
        filename = seleccionar_imagen()
        if filename:
            entry_imagen.config(state="normal")
            entry_imagen.delete(0, tk.END)
            entry_imagen.insert(0, filename)
            entry_imagen.config(state="readonly")

    boton_seleccionar_imagen = ttk.Button(frame_formulario, text="Seleccionar Imagen", command=seleccionar_imagen_y_mostrar)
    boton_seleccionar_imagen.grid(row=4, column=2, padx=10, pady=10)

    # Crear el marco para los horarios
    frame_horarios = tk.Frame(ventana_agregar, bg='white', padx=10, pady=10)
    frame_horarios.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)

    label_horarios = ttk.Label(frame_horarios, text="Horarios y Salas:", font=('Arial', 12, 'bold'), background='white')
    label_horarios.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)

    horarios = []

    def agregar_horario():
        """
        Agrega un nuevo horario a la lista de horarios y lo muestra en la interfaz.
        """
        nuevo_horario = entry_nuevo_horario.get()
        nueva_sala = entry_nueva_sala.get()
        if nuevo_horario and nueva_sala:
            horarios.append((nuevo_horario, nueva_sala))
            horario_str = f"{nuevo_horario} - Sala: {nueva_sala}"
            row_frame = tk.Frame(frame_horarios, bg='white')
            row_frame.grid(row=len(horarios) + 1, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)

            label_horario = ttk.Label(row_frame, text=horario_str)
            label_horario.grid(row=0, column=0, padx=10, pady=5)

            boton_eliminar_horario = ttk.Button(row_frame, text="Eliminar", command=lambda row_frame=row_frame,
                                                horario_str=horario_str: (horarios.remove((nuevo_horario, nueva_sala)), 
                                                                        row_frame.destroy()))
            boton_eliminar_horario.grid(row=0, column=1, padx=5, pady=5)

            entry_nuevo_horario.delete(0, tk.END)
            entry_nueva_sala.delete(0, tk.END)

    entry_nuevo_horario = crear_label_y_entry(frame_horarios, "Nuevo Horario:", "", 1, 0)
    entry_nueva_sala = crear_label_y_entry(frame_horarios, "Nueva Sala:", "", 1, 1)

    boton_agregar_horario = ttk.Button(frame_horarios, text="Agregar Horario", command=agregar_horario)
    boton_agregar_horario.grid(row=1, column=2, padx=10, pady=10)

    # Crear el frame negro para los botones de guardar y cancelar
    frame_botones = tk.Frame(ventana_agregar, bg='black', padx=10, pady=10)
    frame_botones.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky=tk.EW)

    def guardar_pelicula():
        """
        Guarda la nueva película en la base de datos junto con sus horarios.
        """
        titulo = entry_titulo.get()
        genero = entry_genero.get()
        duracion = entry_duracion.get()
        sinopsis = entry_sinopsis.get("1.0", tk.END).strip()
        imagen = entry_imagen.get()

        if titulo and duracion:
            # Insertar la película en la base de datos
            id_pelicula = insertar_pelicula(titulo, genero, duracion, sinopsis, imagen)
            # Insertar los horarios en la base de datos
            for horario, sala in horarios:
                insertar_horario(id_pelicula, horario, sala)
            messagebox.showinfo("Registro Exitoso", "La película ha sido agregada.")
            ventana_agregar.destroy()
            mostrar_cartelera(cuerpo_principal)
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")

    boton_guardar = tk.Button(frame_botones, text="Guardar Película", command=guardar_pelicula, bg='black', fg='white')
    boton_guardar.grid(row=0, column=0, padx=10, pady=10)

    boton_cancelar = tk.Button(frame_botones, text="Cancelar", command=ventana_agregar.destroy, bg='black', fg='white')
    boton_cancelar.grid(row=0, column=1, padx=10, pady=10)

    ventana_agregar.resizable(False, False)


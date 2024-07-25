import tkinter as tk
from tkinter import ttk
import sqlite3

#===================== Funciones para mostrar información de usuarios =====================

# Función para mostrar la información detallada de un usuario y sus reservas
def mostrar_info_usuario(id_usuario):
    ventana_info = tk.Toplevel()
    ventana_info.title("Información de Usuario y Reservas")
    ventana_info.geometry('600x400') 
    ventana_info.configure(bg='white')  # Fondo blanco para la ventana

    # Conectar a la base de datos y obtener la información del usuario
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre, correo, genero FROM usuarios WHERE id = ?', (id_usuario,))
    usuario_info = cursor.fetchone()
    
    # Crear etiquetas para mostrar la información del usuario
    lbl_nombre = ttk.Label(ventana_info, text=f"Nombre: {usuario_info[0]}", font=('Helvetica', 14), background='white')
    lbl_nombre.pack(pady=10)
    lbl_correo = ttk.Label(ventana_info, text=f"Correo: {usuario_info[1]}", font=('Helvetica', 12), background='white')
    lbl_correo.pack(pady=5)
    lbl_genero = ttk.Label(ventana_info, text=f"Género: {usuario_info[2]}", font=('Helvetica', 12), background='white')
    lbl_genero.pack(pady=5)
    
    # Crear un estilo para la tabla
    estilo_tabla = ttk.Style()
    estilo_tabla.configure('EstiloTabla.Treeview', font=('Helvetica', 10), rowheight=25)
    estilo_tabla.configure('EstiloTabla.Treeview.Heading', font=('Helvetica', 12, 'bold'), background='#4CAF50', foreground='white')

    # Crear una tabla para mostrar las reservas del usuario
    tabla = ttk.Treeview(ventana_info, columns=('Pelicula', 'Hora', 'Sala', 'Asiento'), show='headings', style='EstiloTabla.Treeview')
    tabla.heading('Pelicula', text='Pelicula')
    tabla.heading('Hora', text='Hora')
    tabla.heading('Sala', text='Sala')
    tabla.heading('Asiento', text='Asiento')
    tabla.column('Pelicula', width=120, anchor='center')
    tabla.column('Hora', width=120, anchor='center')
    tabla.column('Sala', width=120, anchor='center')
    tabla.column('Asiento', width=120, anchor='center')
    tabla.pack(padx=20, pady=20)
    
    # Obtener las reservas del usuario
    cursor.execute('''
    SELECT 'Pelicula ' || reservas.id_pelicula, reservas.hora, reservas.sala, reservas.asiento
    FROM reservas
    WHERE id_usuario = ?
    ''', (id_usuario,))
    reservas = cursor.fetchall()
    
    # Insertar las reservas en la tabla
    for reserva in reservas:
        tabla.insert('', 'end', values=reserva)
    if not reservas:
        tabla.insert('', 'end', values=('NULL', 'NULL', 'NULL', 'NULL'))
    conn.close()

# Función para mostrar la ventana de usuarios
def mostrar_ventana_usuarios():
    ventana_usuarios = tk.Toplevel()
    ventana_usuarios.title("Lista de Usuarios")
    ventana_usuarios.geometry('500x400')
    ventana_usuarios.configure(bg='white')  # Fondo blanco para la ventana
    
    # Conectar a la base de datos y obtener la lista de usuarios
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    
    # Crear un estilo para los botones
    estilo_boton = ttk.Style()
    estilo_boton.configure('EstiloBoton.TButton', background='#4CAF50', foreground='white', font=('Helvetica', 12))
    
    # Crear un marco negro para los botones
    frame_botones = tk.Frame(ventana_usuarios, bg='black', padx=10, pady=10)
    frame_botones.pack(fill=tk.BOTH, expand=True)
    
    # Crear un botón para cada usuario
    for usuario in usuarios:
        id_usuario = usuario[0]
        nombre_usuario = usuario[1]
        btn_usuario = tk.Button(frame_botones, text=nombre_usuario, bg='black', fg='white', font=('Helvetica', 12),
                                command=lambda id=id_usuario: mostrar_info_usuario(id))
        btn_usuario.pack(pady=5, padx=10, fill=tk.X)


















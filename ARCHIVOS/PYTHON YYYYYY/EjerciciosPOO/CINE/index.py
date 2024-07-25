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

# URL DE LAS IMG, HORAS Y TITULOS DE LAS PELICULAS----------------------------------------------------------------------------------------------
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

# Estado inicial de los asientos en las 3 salas
asientos = [[[0]*8 for _ in range(8)] for _ in range(3)]

# FUNCIONES AUXILIARES ---------------------------------------------------------------------------------------------------------------------------
# Función para crear botones
def crear_boton(frame, texto, comando):
    """
    Crea un botón con estilo personalizado y lo agrega a un frame.
    
    :param frame: Frame donde se añadirá el botón.
    :param texto: Texto que se mostrará en el botón.
    :param comando: Función que se ejecutará al hacer clic en el botón.
    """
    button = tk.Button(frame, text=texto, command=comando, bg="#000000", fg="white", font=("Arial", 12), relief=tk.RAISED, borderwidth=3, padx=10, pady=5)
    button.pack(pady=10)

# Función para crear indicadores de estado de asientos
def crear_estado_asiento(frame, estado, color):
    """
    Crea un indicador visual para el estado de un asiento.
    
    :param frame: Frame donde se añadirá el indicador.
    :param estado: Texto que describe el estado del asiento.
    :param color: Color del indicador visual.
    """
    tk.Label(frame, text=estado, bg="#F0F0F0", font=("Arial", 14)).pack(anchor=tk.W)
    canvas = tk.Canvas(frame, width=15, height=15, bg="#F0F0F0", highlightthickness=0)
    canvas.create_rectangle(5, 5, 15, 15, fill=color)
    canvas.pack(anchor=tk.W)

# Función para cargar y redimensionar imágenes
def cargar_imagen(url_imagen, size):
    """
    Descarga una imagen desde una URL y la redimensiona.
    
    :param url_imagen: URL de la imagen a descargar.
    :param size: Tamaño al que se redimensionará la imagen.
    :return: Imagen redimensionada en formato PhotoImage.
    """
    response = requests.get(url_imagen)
    imagen = Image.open(BytesIO(response.content))
    imagen = imagen.resize(size, Image.LANCZOS)  
    return ImageTk.PhotoImage(imagen)

# CREACIÓN DE LA VENTANA PRINCIPAL ---------------------------------------------------------------------------------------------------------------
def crear_ventana_principal():
    """
    Crea y configura la ventana principal de la aplicación.
    
    :return: Objeto de la ventana principal.
    """
    ventana = tk.Tk()
    ventana.geometry("600x750")
    ventana.resizable(False, False)
    ventana.title("Reserva de Asientos de Cine")
    ventana.configure(bg="#2C3E50")
    return ventana

# FUNCIONES PARA NAVEGACIÓN ENTRE VISTAS ---------------------------------------------------------------------------------------------------------
def volver_a_pelicula(frame_hora, frame_peliculas):
    """
    Cambia la vista de horarios a la vista de películas.
    
    :param frame_hora: Frame de selección de horarios.
    :param frame_peliculas: Frame de selección de películas.
    """
    frame_hora.pack_forget()
    frame_peliculas.pack()

def volver_a_hora(frame_sala, frame_hora):
    """
    Cambia la vista de salas a la vista de horarios.
    
    :param frame_sala: Frame de selección de salas.
    :param frame_hora: Frame de selección de horarios.
    """
    frame_sala.pack_forget()
    frame_hora.pack()

def volver_a_sala(frame_asientos, frame_sala):
    """
    Cambia la vista de asientos a la vista de salas.
    
    :param frame_asientos: Frame de selección de asientos.
    :param frame_sala: Frame de selección de salas.
    """
    frame_asientos.pack_forget()
    frame_sala.pack()

# VISTA DE SELECCIÓN DE HORARIOS -----------------------------------------------------------------------------------------------------------------
def seleccionar_hora(pelicula):
    """
    Muestra los horarios disponibles para la película seleccionada.
    
    :param pelicula: Nombre de la película seleccionada.
    """
    frame_peliculas.pack_forget()
    frame_hora.pack()

    for widget in frame_hora.winfo_children():
        widget.destroy()
    tk.Frame(frame_hora, bg="#2C3E50", height=150,width=350).pack()
    tk.Label(frame_hora, text=f"Selecciona una hora para\n{pelicula}", bg="#34495E", fg="white", font=("Arial", 15)).pack(pady=15)
    
    for hora in peliculas[pelicula]["horarios"]:
        crear_boton(frame_hora, hora, lambda h=hora: seleccionar_sala(pelicula, h))
    
    crear_boton(frame_hora, "Volver", lambda: volver_a_pelicula(frame_hora, frame_peliculas))

# VISTA DE SELECCIÓN DE SALAS -------------------------------------------------------------------------------------------------------------------
def seleccionar_sala(pelicula, hora):
    """
    Muestra las salas disponibles para la película y hora seleccionadas.
    
    :param pelicula: Nombre de la película seleccionada.
    :param hora: Hora seleccionada.
    """
    frame_hora.pack_forget()
    frame_sala.pack()

    for widget in frame_sala.winfo_children():
        widget.destroy()
    tk.Frame(frame_sala, bg="#2C3E50", height=150,width=350).pack()
    tk.Label(frame_sala, text=f"Selecciona una sala para ver \n{pelicula} a las {hora}", bg="#34495E", fg="white", font=("Arial", 15)).pack(pady=25)
    
    for i in range(3):
        crear_boton(frame_sala, f"Sala {i+1}", lambda s=i: seleccionar_asientos(pelicula, hora, s))
    
    crear_boton(frame_sala, "Volver", lambda: volver_a_hora(frame_sala, frame_hora))

# VISTA DE SELECCIÓN DE ASIENTOS -----------------------------------------------------------------------------------------------------------------
def seleccionar_asientos(pelicula, hora, sala):
    """
    Permite seleccionar los asientos en la sala elegida y manejar las reservas.
    
    :param pelicula: Nombre de la película seleccionada.
    :param hora: Hora seleccionada.
    :param sala: Sala seleccionada.
    """
    frame_sala.pack_forget()
    frame_asientos.pack()

    asientos_actuales = asientos[sala]
    botones = []

    def actualizar_contador():
        """
        Actualiza el contador de asientos libres y seleccionados.
        """
        libres = sum(row.count(0) for row in asientos_actuales)
        seleccionados = sum(row.count(2) for row in asientos_actuales)
        lbl_contador.config(text=f"Puestos libres: {libres} \n Seleccionados: {seleccionados}")

    def seleccionar_asiento(fila, asiento):
        """
        Maneja la selección y deselección de asientos.
        
        :param fila: Fila del asiento seleccionado.
        :param asiento: Número del asiento seleccionado.
        """
        if asientos_actuales[fila][asiento] == 0:
            asientos_actuales[fila][asiento] = 2
            botones[fila][asiento].config(bg="#FFD700", text="S")
            selecciones_pendientes.append((fila, asiento))
        elif asientos_actuales[fila][asiento] == 1:
            messagebox.showwarning("Reserva", f"Asiento {chr(65+asiento)}{fila+1} ya está ocupado")
        elif asientos_actuales[fila][asiento] == 2:
            asientos_actuales[fila][asiento] = 0
            botones[fila][asiento].config(bg="#32CD32", text="L")
            selecciones_pendientes.remove((fila, asiento))
        actualizar_contador()

    def encontrar_mejor_puesto():
        """
        Resalta el mejor asiento disponible basado en la cercanía al centro de la fila.
        """
        for fila in range(8):
            mejor_distancia = float('inf')  # Inicializamos la mejor distancia con un valor infinito
            mejor_asiento = None
            for asiento in range(8):
                if asientos_actuales[fila][asiento] == 0:
                    distancia = abs(asiento - 3.5)
                    # Calculamos la distancia al centro de la fila
                    distancia = abs(asiento - 3.5)  # El asiento central está en la posición 3.5
                    if distancia < mejor_distancia:
                        mejor_distancia = distancia
                        mejor_asiento = asiento
                    if mejor_asiento is not None:
                        botones[fila][mejor_asiento].config(bg="#40E0D0")  # Resaltamos el mejor asiento
                    return  
        
    def crear_estado_asientos(frame):
        """
    Crea y muestra etiquetas y lienzos para representar el estado de los asientos.
        """
        estado = {
        "simbolo": ("L", "O", "S"),
        "estados": ("libre", "ocupado", "seleccionado"),
        "colores": ("#32CD32", "#FF6347", "#FFD700")
        } 
        for i in range(3):
            tk.Label(frame, text=f"{estado['simbolo'][i]}: {estado['estados'][i]}", bg="#34495E", font=("Arial", 14)).pack(anchor=tk.W)
            canvas_estado = tk.Canvas(frame, width=15, height=15, bg="#34495E", highlightthickness=0)
            canvas_estado.create_rectangle(5, 5, 15, 15, fill=estado['colores'][i])
            canvas_estado.pack(anchor=tk.W)

    def confirmar_reservas():
        """
        Confirma las reservas seleccionadas y actualiza el estado de los asientos.
        """
        if selecciones_pendientes:
            for fila, asiento in selecciones_pendientes:
                asientos_actuales[fila][asiento] = 1
                botones[fila][asiento].config(bg="#FF6347", text="O")
            selecciones_pendientes.clear()
            actualizar_contador()
            messagebox.showinfo("Reserva", "Reservas confirmadas con éxito")
        else:
            messagebox.showwarning("Reserva", "No hay asientos seleccionados para confirmar")


    lbl_contador = tk.Label(frame_asientos, text="", bg="#34495E", fg="white", font=("Arial", 13))
    lbl_contador.pack(pady=10)
    actualizar_contador()

    frame_botones = tk.Frame(frame_asientos, bg="#34495E")
    frame_botones.pack(pady=10)

    for fila in range(8):
        fila_botones = tk.Frame(frame_botones, bg="#34495E")
        fila_botones.pack()
        fila_botones_list = []
        for asiento in range(8):
            btn = tk.Button(fila_botones, text=f"L", width=4, bg="#32CD32", fg="white",
                            command=lambda f=fila, a=asiento: seleccionar_asiento(f, a))
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            fila_botones_list.append(btn)
        botones.append(fila_botones_list)

    crear_boton(frame_asientos, "Confirmar Selección", confirmar_reservas)
    crear_boton(frame_asientos, "Encontrar Mejor Puesto", encontrar_mejor_puesto)
    crear_boton(frame_asientos, "Volver", lambda: volver_a_sala(frame_asientos, frame_sala))
    crear_estado_asientos(frame_asientos)


# CREACIÓN Y CONFIGURACIÓN DE LA VENTANA PRINCIPAL -------------------------------------------------------------------------------------------------
def main():
    global frame_peliculas, frame_hora, frame_sala, frame_asientos
    ventana = crear_ventana_principal()
    
    frame_peliculas = tk.Frame(ventana, bg="#34495E")
    frame_hora = tk.Frame(ventana, bg="#34495E")
    frame_sala = tk.Frame(ventana, bg="#34495E")
    frame_asientos = tk.Frame(ventana, bg="#34495E")

    frame_peliculas.pack()

    for pelicula in peliculas:
        imagen = cargar_imagen(peliculas[pelicula]["imagen_url"], (110, 110))
        label_imagen = tk.Label(frame_peliculas, image=imagen)
        label_imagen.image = imagen
        label_imagen.pack(pady=20)
        tk.Label(frame_peliculas, text=pelicula, bg="#34495E", fg="white", font=("Arial", 15)).pack(pady=5)
        crear_boton(frame_peliculas, "Ver Horas y Salas", lambda p=pelicula: seleccionar_hora(p))

    ventana.mainloop()

if __name__ == "__main__":
    main()








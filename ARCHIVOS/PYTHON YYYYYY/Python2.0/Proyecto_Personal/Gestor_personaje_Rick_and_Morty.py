import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import io

def buscar_personaje(nombre_personaje):
    url = "https://rickandmortyapi.com/graphql"

    # Definir la consulta GraphQL con una variable para el nombre del personaje
    consulta = """
    query ($name: String!) {
        characters(filter: { name: $name }) {
        results {
            name
            image
            status
            species
            gender
        }
        }
    }
    """

    # Definir las variables para la consulta
    variables = {
        "name": nombre_personaje
    }

    # Definir la carga útil (payload) con la consulta y las variables
    payload = {
        "query": consulta,
        "variables": variables
    }

    # Enviar la solicitud POST al endpoint de GraphQL
    respuesta = requests.post(url, json=payload)

    # Verificar si la solicitud fue exitosa
    if respuesta.status_code == 200:
        datos = respuesta.json()
        if 'data' in datos and 'characters' in datos['data'] and 'results' in datos['data']['characters']:
            return datos['data']['characters']['results']
        else:
            return None
    else:
        messagebox.showerror("Error", f"La consulta falló con el código de estado {respuesta.status_code}")
        return None

def mostrar_personaje():
    nombre = entry_nombre.get()
    personajes = buscar_personaje(nombre)
    
    if personajes:
        personaje = personajes[0]  # Mostrar el primer resultado

        label_nombre.config(text=f"Nombre: {personaje['name']}")
        label_estado.config(text=f"Estado: {personaje['status']}")
        label_especie.config(text=f"Especie: {personaje['species']}")
        label_genero.config(text=f"Género: {personaje['gender']}")
        
        # Mostrar la imagen del personaje
        response = requests.get(personaje['image'])
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        label_imagen.config(image=photo)
        label_imagen.image = photo  # Guardar referencia para evitar que se elimine
    else:
        messagebox.showinfo("No encontrado", "No se encontraron personajes con ese nombre.")

# Configurar la ventana principal
ventana = tk.Tk()
ventana.title("Buscador de Personajes - Rick and Morty")

frame = ttk.Frame(ventana, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiqueta y entrada para el nombre del personaje
label_prompt = ttk.Label(frame, text="Introduce el nombre del personaje:")
label_prompt.grid(row=0, column=0, sticky=tk.W)

entry_nombre = ttk.Entry(frame, width=30)
entry_nombre.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Botón para buscar
boton_buscar = ttk.Button(frame, text="Buscar", command=mostrar_personaje)
boton_buscar.grid(row=0, column=2, sticky=tk.W)

# Etiquetas para mostrar la información del personaje
label_nombre = ttk.Label(frame, text="Nombre: ")
label_nombre.grid(row=1, column=0, columnspan=3, sticky=tk.W)

label_estado = ttk.Label(frame, text="Estado: ")
label_estado.grid(row=2, column=0, columnspan=3, sticky=tk.W)

label_especie = ttk.Label(frame, text="Especie: ")
label_especie.grid(row=3, column=0, columnspan=3, sticky=tk.W)

label_genero = ttk.Label(frame, text="Género: ")
label_genero.grid(row=4, column=0, columnspan=3, sticky=tk.W)

# Etiqueta para mostrar la imagen del personaje
label_imagen = ttk.Label(frame)
label_imagen.grid(row=5, column=0, columnspan=3)

# Ajustar el tamaño de la ventana
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

frame.columnconfigure(1, weight=1)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()




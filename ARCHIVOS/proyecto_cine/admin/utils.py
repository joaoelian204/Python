import tkinter as tk
from tkinter import filedialog

def seleccionar_imagen():
    """
    Abre un cuadro de diálogo para seleccionar un archivo de imagen y retorna la ruta del archivo seleccionado.

    Retorna:
        str: La ruta del archivo de imagen seleccionado.
    """
    # Abre un cuadro de diálogo para seleccionar un archivo de imagen
    filename = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg")])
    # Retorna la ruta del archivo seleccionado
    return filename

def bind_hover_events(button):
    """
    Asigna eventos de hover a un botón para cambiar su color de fondo al pasar el cursor sobre él.

    Parámetros:
        button (tk.Button): El botón al que se le asignarán los eventos de hover.
    """
    # Asigna el evento para cambiar el color de fondo a verde cuando el cursor está sobre el botón
    button.bind("<Enter>", lambda e: button.config(bg="#4CAF50"))
    # Asigna el evento para restaurar el color de fondo original cuando el cursor se retira del botón
    button.bind("<Leave>", lambda e: button.config(bg="#2196F3"))

def crear_label_y_entry(parent, texto_label, valor_entry, row, column):
    """
    Crea y coloca un par de Label y Entry en un widget padre especificado.

    Parámetros:
        parent (tk.Widget): El widget padre en el que se colocarán el Label y el Entry.
        texto_label (str): El texto que se mostrará en el Label.
        valor_entry (str): El valor inicial que se establecerá en el Entry.
        row (int): La fila en la que se colocarán el Label y el Entry en la cuadrícula.
        column (int): La columna en la que se colocarán el Label y el Entry en la cuadrícula.

    Retorna:
        tk.Entry: El widget Entry creado.
    """
    # Estilos para el Label y el Entry
    estilo_label = {'bg': '#ffffff', 'fg': '#333', 'font': ('Arial', 11)}
    estilo_entry = {'bg': '#ffffff', 'fg': '#333', 'font': ('Arial', 11)}

    # Crea el Label con el texto especificado y lo coloca en la cuadrícula
    label = tk.Label(parent, text=texto_label, **estilo_label)
    label.grid(row=row, column=column, padx=10, pady=10, sticky=tk.E)

    # Crea el Entry con el valor inicial especificado y lo coloca en la cuadrícula
    entry = tk.Entry(parent, width=40, **estilo_entry)
    entry.grid(row=row, column=column+1, padx=10, pady=10)
    entry.insert(0, valor_entry)

    # Retorna el Entry creado
    return entry

def crear_boton(parent, texto, comando, color_fondo, fila, columna, padx=10, pady=10):
    """
    Crea y coloca un botón en un widget padre especificado.

    Parámetros:
        parent (tk.Widget): El widget padre en el que se colocará el botón.
        texto (str): El texto que se mostrará en el botón.
        comando (func): La función que se ejecutará cuando se haga clic en el botón.
        color_fondo (str): El color de fondo del botón.
        fila (int): La fila en la que se colocará el botón en la cuadrícula.
        columna (int): La columna en la que se colocará el botón en la cuadrícula.
        padx (int, opcional): El relleno horizontal alrededor del botón. Por defecto es 10.
        pady (int, opcional): El relleno vertical alrededor del botón. Por defecto es 10.

    Retorna:
        tk.Button: El widget Button creado.
    """
    # Crea el botón con el texto, comando y color de fondo especificados
    boton = tk.Button(parent, text=texto, command=comando, bg=color_fondo, fg='#fff')
    # Coloca el botón en la cuadrícula con el padding especificado
    boton.grid(row=fila, column=columna, padx=padx, pady=pady)
    # Retorna el botón creado
    return boton


import tkinter as tk
from tkinter import font
from detalles_pelicula import mostrar_detalles_pelicula
from PIL import Image, ImageTk

def leer_imagen(path, size):
    """
    Lee una imagen desde el sistema de archivos y la redimensiona al tamaño especificado.
    
    Args:
        path (str): La ruta del archivo de imagen.
        size (tuple): El tamaño al que se debe redimensionar la imagen (ancho, alto).
        
    Returns:
        ImageTk.PhotoImage: La imagen redimensionada.
    """
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

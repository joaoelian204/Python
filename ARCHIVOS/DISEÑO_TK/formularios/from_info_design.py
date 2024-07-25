import tkinter as tk
import util.util_ventana as util_ventana

class formularioInfoDesign(tk.Toplevel):
    
    
    def __init__(self) -> None:
        super().__init__()
        
    def config_window(self):
        #Configuracion de la ventana
        self.title("CINE GUI")
        w,h = 400, 100
        util_ventana.centrar_ventana(self,w,h)
        
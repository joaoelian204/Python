from tkinter import *

ventana = Tk()
ventana.title("Calculadora")
i = 0
# Entrada
entrada_tex = Entry(ventana, font=("Calibri 20"))
entrada_tex.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
#funcion
def click_boton(valor):
    global i
    entrada_tex.insert(i, valor)
    i += 1

def borrar():
    entrada_tex.delete(0, END)
    i = 0
    
def hacer_oper():
    ecuacion = entrada_tex.get()
    resultado = eval(ecuacion)
    entrada_tex.delete(0,END)
    entrada_tex.insert(0, resultado)
    i = 0
#Botones
boton1 = Button(ventana, text="1", font=("Calibri 15"), width=5, height=2, command= lambda: click_boton(1))
boton2 = Button(ventana, text="2", font=("Calibri 15"), width=5, height=2, command=lambda: click_boton(2))
boton3 = Button(ventana, text="3", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(3))
boton4 = Button(ventana, text="4", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(4))
boton5 = Button(ventana, text="5", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(5))
boton6 = Button(ventana, text="6", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(6))
boton7 = Button(ventana, text="7", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(7))
boton8 = Button(ventana, text="8", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(8))
boton9 = Button(ventana, text="9", font=("Calibri 15"), width=5, height=2 , command=lambda: click_boton(9))
boton0 = Button(ventana, text="0", font=("Calibri 15"), width=13, height=2 , command=lambda: click_boton(0))
#Botones de operaciones
boton_borrar = Button(ventana, text="AC ", font=("Calibri 15"), width=5, height=2, command=lambda: borrar())
boton_parentesis1= Button(ventana, text="(", font=("Calibri 15"), width=5, height=2, command=lambda: click_boton("("))
boton_parentesis2 = Button(ventana, text=")", font=("Calibri 15"), width=5, height=2, command=lambda: click_boton(")"))
boton_punto = Button(ventana, text=".", font=("Calibri 15"), width=5, height=2, command=lambda: click_boton("."))
#Botones de operaciones
boton1_divi = Button(ventana, text="/", font=("Calibri 15"), width=5, height=2,command= lambda: click_boton("/"))
boton1_multi = Button(ventana, text="*", font=("Calibri 15"), width=5, height=2, command=lambda: click_boton("*"))
boton1_suma = Button(ventana, text="+", font=("Calibri 15"), width=5, height=2,  command=lambda: click_boton("+"))
boton1_resta = Button(ventana, text="-", font=("Calibri 15"), width=5, height=2, command=lambda: click_boton("-"))
boton1_igual= Button(ventana, text="= ", font=("Calibri 15"), width=5, height=2,command= lambda: hacer_oper())

#Agregar botones
boton_borrar.grid(row=1, column=0, padx=5, pady=5)
boton_parentesis1.grid(row=1, column=1, padx=5, pady=5)
boton_parentesis2.grid(row=1, column=2, padx=5, pady=5)
boton1_divi.grid(row=1, column=3, padx=5, pady=5)
#Botones de los números
boton1.grid(row=2, column=0, padx=5, pady=5)
boton2.grid(row=2, column=1, padx=5, pady=5)
boton3.grid(row=2, column=2, padx=5, pady=5)
boton1_multi.grid(row=2, column=3, padx=5, pady=5)

boton4.grid(row=3, column=0, padx=5, pady=5)
boton5.grid(row=3, column=1, padx=5, pady=5)
boton6.grid(row=3, column=2, padx=5, pady=5)
boton1_resta.grid(row=3, column=3, padx=5, pady=5)

boton7.grid(row=4, column=0, padx=5, pady=5)
boton8.grid(row=4, column=1, padx=5, pady=5)
boton9.grid(row=4, column=2, padx=5, pady=5)
boton1_suma.grid(row=4, column=3, padx=5, pady=5)

boton0.grid(row=5, column=0,columnspan= 2, padx=5, pady=5)
boton_punto.grid(row=5, column=2, padx=5, pady=5)
boton1_igual.grid(row=5, column=3, padx=5, pady=5)



ventana.mainloop()
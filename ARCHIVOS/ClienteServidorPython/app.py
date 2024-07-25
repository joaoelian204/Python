import socket
import threading
import tkinter as tk
from tkinter import messagebox, StringVar, Radiobutton
import json

def enviar_mensaje(msg):
    try:
        client_socket.send(msg.encode('utf-8'))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el mensaje: {e}")

def recibir_mensajes():
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Datos recibidos: {data}")  # Línea de depuración
            if data.startswith("ENCUESTA:"):
                _, encuesta_json, encuesta_id = data.split(":", 2)
                encuesta = json.loads(encuesta_json)  # Asegúrate de que esta línea funcione
                mostrar_encuesta(encuesta, encuesta_id)
            elif data.startswith("RESULTADOS:"):
                _, resultados_json = data.split(":", 1)
                resultados = json.loads(resultados_json)
                actualizar_resultados(resultados)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            print(f"Datos recibidos: {data}")
        except Exception as e:
            print(f"Error al recibir mensaje: {e}")
            break



def mostrar_encuesta(encuesta, encuesta_id):
    encuesta_label.config(text=f"Pregunta: {encuesta['pregunta']}")
    var.set(None)
    for widget in opciones_frame.winfo_children():
        widget.destroy()
    for opcion in encuesta['opciones']:
        Radiobutton(opciones_frame, text=opcion, variable=var, value=opcion).pack(anchor="w")
    responder_button.config(command=lambda: enviar_respuesta(encuesta_id))
    encuesta_frame.pack()

def enviar_respuesta(encuesta_id):
    respuesta = var.get()
    if respuesta:
        print(f"Enviando respuesta: {respuesta} para la encuesta ID: {encuesta_id}")
        enviar_mensaje(f"RESPUESTA:{encuesta_id}:{respuesta}")
    else:
        messagebox.showwarning("Respuesta vacía", "Por favor seleccione una opción.")

def actualizar_resultados(resultados):
    resultados_text.config(state=tk.NORMAL)
    resultados_text.delete(1.0, tk.END)
    resultados_text.insert(tk.END, json.dumps(resultados, indent=4))
    resultados_text.config(state=tk.DISABLED)

# Configuración de la interfaz gráfica (GUI)
root = tk.Tk()
root.title("Cliente de Encuestas")
root.geometry("400x400")
root.resizable(False, False)

encuesta_frame = tk.Frame(root)
encuesta_label = tk.Label(encuesta_frame, text="", font=("Arial", 14))
encuesta_label.pack(pady=10)
var = StringVar()
opciones_frame = tk.Frame(encuesta_frame)
opciones_frame.pack(pady=5)
responder_button = tk.Button(encuesta_frame, text="Responder", command=None)
responder_button.pack(pady=10)

resultados_label = tk.Label(root, text="Resultados de la Encuesta:", font=("Arial", 12))
resultados_label.pack(pady=10)
resultados_text = tk.Text(root, height=10, state=tk.DISABLED)
resultados_text.pack(pady=10, padx=10)

# Conexión al servidor mediante socket
host = 'localhost'
port = 8051  # Cambiado a 8051

client_socket = socket.socket()
try:
    client_socket.connect((host, port))
    print("Conectado al servidor")
except Exception as e:
    messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor: {e}")
    root.destroy()

# Iniciar un hilo para recibir mensajes del servidor
recv_thread = threading.Thread(target=recibir_mensajes, daemon=True)
recv_thread.start()

root.mainloop()












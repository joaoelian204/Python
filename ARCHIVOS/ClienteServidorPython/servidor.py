import socket
import threading
from tkinter import Tk, Label, Entry, Button, messagebox, Text
import json

# Configuración del servidor
host = 'localhost'
port = 8051  # Cambiado a 8051


# Crear un socket para el servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

clientes = []
resultados_encuesta = {}

def manejar_cliente(client_socket, client_address):
    global resultados_encuesta
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            if data.startswith("RESPUESTA:"):
                _, encuesta_id, respuesta = data.split(":", 2)
                encuesta_id = int(encuesta_id)
                print(f"Respuesta recibida: {respuesta} para la encuesta ID: {encuesta_id}")
                if encuesta_id in resultados_encuesta:
                    resultados_encuesta[encuesta_id][respuesta] += 1
                enviar_resultados()
        except Exception as e:
            print(f"Error en la comunicación con el cliente {client_address}: {e}")
            break

    client_socket.close()

def enviar_encuesta(encuesta):
    encuesta_id = len(resultados_encuesta)
    resultados_encuesta[encuesta_id] = {opcion: 0 for opcion in encuesta['opciones']}
    encuesta_json = json.dumps(encuesta)
    print(f"Enviando encuesta: {encuesta_json}")  # Línea de depuración
    for cliente in clientes:
        cliente.sendall(f"ENCUESTA:{encuesta_json}:{encuesta_id}".encode('utf-8'))


def enviar_resultados():
    resultados_json = json.dumps(resultados_encuesta)
    for cliente in clientes:
        cliente.sendall(f"RESULTADOS:{resultados_json}".encode('utf-8'))

def aceptar_clientes():
    while True:
        client_socket, client_address = server_socket.accept()
        clientes.append(client_socket)
        threading.Thread(target=manejar_cliente, args=(client_socket, client_address)).start()

def iniciar_encuesta():
    pregunta = pregunta_entry.get()
    opciones = opciones_text.get("1.0", "end-1c").splitlines()
    if pregunta and opciones:
        encuesta = {"pregunta": pregunta, "opciones": opciones}
        enviar_encuesta(encuesta)
    else:
        messagebox.showwarning("Encuesta incompleta", "Por favor ingrese una pregunta y opciones.")

# Configuración de la interfaz gráfica (GUI) del servidor
root = Tk()
root.title("Servidor de Encuestas")
root.geometry("400x300")

pregunta_label = Label(root, text="Nueva Pregunta:", font=("Arial", 12))
pregunta_label.pack(pady=10)
pregunta_entry = Entry(root, font=("Arial", 12))
pregunta_entry.pack(pady=5)
opciones_label = Label(root, text="Opciones (una por línea):", font=("Arial", 12))
opciones_label.pack(pady=10)
opciones_text = Text(root, height=5, font=("Arial", 12))
opciones_text.pack(pady=5)
enviar_button = Button(root, text="Enviar Encuesta", command=iniciar_encuesta, font=("Arial", 12))
enviar_button.pack(pady=10)

# Iniciar el hilo para aceptar clientes
threading.Thread(target=aceptar_clientes, daemon=True).start()

root.mainloop()








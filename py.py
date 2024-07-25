import tkinter as tk
import sounddevice as sd
import numpy as np
import whisper
import threading
import torch

# Cargar el modelo Whisper
model = whisper.load_model("base")

# Definir la función para capturar audio y transcribir
def record_and_transcribe():
    # Configuración de parámetros
    duration = 5  # Duración de la grabación en segundos
    sample_rate = 16000  # Frecuencia de muestreo

    # Capturar audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    # Convertir a numpy array
    audio_data = np.squeeze(recording)

    # Asegurar que los datos de audio estén en el formato correcto
    if len(audio_data.shape) == 2:  # Si el audio es estéreo, convertirlo a mono
        audio_data = np.mean(audio_data, axis=1)

    # Convertir a tensor de PyTorch
    audio_tensor = torch.tensor(audio_data, dtype=torch.float32)

    # Transcribir el audio
    result = model.transcribe(audio_tensor, fp16=False, language='es')
    transcribed_text.set(result["text"])

# Definir la función para el botón
def on_button_click():
    threading.Thread(target=record_and_transcribe).start()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Transcripción de Audio en Tiempo Real")

transcribed_text = tk.StringVar()

label = tk.Label(root, text="Pulsa el botón y habla")
label.pack(pady=10)

button = tk.Button(root, text="Grabar y Transcribir", command=on_button_click)
button.pack(pady=10)

result_label = tk.Label(root, textvariable=transcribed_text, wraplength=400)
result_label.pack(pady=10)

root.mainloop()

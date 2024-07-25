import whisper

# Cargar el modelo base
model = whisper.load_model("base")

# Transcribir el archivo de audio
result = model.transcribe("/home/joaoelian/Descargas/cuento.mp3")

# Imprimir la transcripción
print(result["text"])

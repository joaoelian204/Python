from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Ruta para subir la imagen
@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica si se envió un archivo
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo'}), 400
    
    file = request.files['file']
    
    # Verifica si el archivo tiene nombre
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400
    
    # Guarda el archivo en una carpeta temporal
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)
    
    # Genera la URL pública del archivo subido
    base_url = request.base_url.rsplit('/', 1)[0]
    file_url = f"{base_url}/{filepath}"
    
    return jsonify({'url': file_url}), 200

if __name__ == '__main__':
    app.run(debug=True)

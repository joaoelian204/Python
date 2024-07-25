import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)

# Crear la base de datos y las tablas dentro del contexto de la aplicación
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    images = Image.query.all()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            new_image = Image(filename=filename)
            db.session.add(new_image)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if image:
        # Eliminar archivo del sistema de archivos
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        # Eliminar registro de la base de datos
        db.session.delete(image)
        db.session.commit()
        flash('Image deleted successfully.')
    else:
        flash('Image not found.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

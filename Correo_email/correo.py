import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# Datos de acceso al correo (utiliza variables de entorno por seguridad)
correo = os.getenv('EMAIL_USER', 'cineprueba34@gmail.com')
password = os.getenv('EMAIL_PASS', 'uboy coxy skrv ibsa')

# Información del usuario y destinatario
usuario = 'Elian'
asunto = 'Verificación de Cuenta'
destinatario = ['anahimero69@gmail.com']

# Leer el archivo HTML y reemplazar el nombre del usuario
html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
        }}
        .container {{
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            max-width: 600px;
            margin: auto;
        }}
        .header {{
            text-align: center;
            padding-bottom: 20px;
        }}
        .body {{
            text-align: left;
        }}
        .footer {{
            text-align: center;
            padding-top: 20px;
            font-size: 0.8em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Hola, viejo amigo</h2>
        </div>
        <div class="body">
            <p>Hola {usuario},</p>
            <p>tenia tiempo sin saver de ti, te queria recomendar esta pagina para generar dinero, solo ingresa al enlace y te aseguro que te haras millonario.</p>
            <p><a href="http://example.com/verify">Verificar Cuenta</a></p>
            <img src="https://img.freepik.com/foto-gratis/colores-arremolinados-interactuan-danza-fluida-sobre-lienzo-que-muestra-tonos-vibrantes-patrones-dinamicos-que-capturan-caos-belleza-arte-abstracto_157027-2892.jpg?size=626&ext=jpg&ga=GA1.1.2008272138.1721088000&semt=sph" alt="Imagen de bienvenida" style="width:100%;height:auto;">
        </div>
        <div class="footer">
            <p>Este es un correo electrónico generado automáticamente, por favor no responda a este mensaje.</p>
        </div>
    </div>
</body>
</html>
"""

# Crear el mensaje
msg = MIMEMultipart()
msg['From'] = formataddr((usuario, correo))
msg['To'] = ', '.join(destinatario)
msg['Subject'] = asunto

# Adjuntar el cuerpo del mensaje en HTML
msg.attach(MIMEText(html, 'html'))

# Crear la conexión y enviar el mensaje
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(correo, password)
        server.sendmail(correo, destinatario, msg.as_string())
    print('Correo enviado exitosamente')
except smtplib.SMTPException as e:
    print(f"Error al enviar el correo: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")



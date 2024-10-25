from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
    # Obtener datos del JSON de la solicitud
    data = request.get_json()
    recipient_email = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    # Credenciales de correo desde las variables de entorno
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    # Crear el mensaje de correo
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conectar al servidor de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Iniciar conexión segura
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.close()
        return jsonify({'message': 'Correo enviado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

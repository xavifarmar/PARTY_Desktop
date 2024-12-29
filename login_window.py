import sys
import pymysql
import bcrypt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Qt
from home_window import HomeWindow  # Importamos la clase HomeWindow desde home_window.py

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iniciar sesión")
        self.setGeometry(100, 100, 400, 450)  # Tamaño y posición de la ventana
        self.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")  # Fondo blanco

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Título de la aplicación o formulario
        self.title_label = QLabel("Iniciar sesión", self)
        self.title_label.setStyleSheet("""
            font-size: 30px;
            color: #333;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            margin-bottom: 20px;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)

        # Campo de texto para el nombre de usuario
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Usuario")
        self.username_field.setStyleSheet("""
            background-color: #F9F9F9;
            border-radius: 8px;
            border: 1px solid #D1D1D1;
            padding: 10px;
            font-size: 16px;
            color: #333;
        """)

        # Campo de texto para la contraseña
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText("Contraseña")
        self.password_field.setStyleSheet("""
            background-color: #F9F9F9;
            border-radius: 8px;
            border: 1px solid #D1D1D1;
            padding: 10px;
            font-size: 16px;
            color: #333;
        """)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #950909;  /* Rojo brillante */
                color: white;
                font-size: 18px;
                padding: 2px 0;
                border-radius: 8px;
                border: none;
                margin-top: 20px

            }
            QPushButton:hover {
                background-color: #B30000;
            }
        """)
        self.login_button.setFixedHeight(45)

        # Conectar el botón al método login_user
        self.login_button.clicked.connect(self.login_user)

        # Añadir los elementos al layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_field.text()
        password = self.password_field.text()

        # Conexión a la base de datos
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="4party"
            )

            cursor = connection.cursor()
            query = "SELECT id, email, password FROM users WHERE email = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if result:
                user_id = result[0]  # ID del usuario (lo obtenemos de la base de datos)
                db_password_hash = result[2]
                if bcrypt.checkpw(password.encode('utf-8'), db_password_hash.encode('utf-8')):
                    self.open_home_window(user_id)  # Pasamos el ID al abrir HomeWindow
                else:
                    QMessageBox.warning(self, "Error", "Credenciales incorrectas")
            else:
                QMessageBox.warning(self, "Error", "Credenciales incorrectas")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def open_home_window(self, user_id):
        self.close()  # Cerrar la ventana de login
        self.home_window = HomeWindow(user_id)  # Pasamos el ID del usuario
        self.home_window.show()  # Mostrar la ventana HomeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

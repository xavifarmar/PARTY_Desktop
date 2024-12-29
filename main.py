
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from login_window import LoginWindow

class Login(QWidget):

# Función principal que arranca la aplicación
    if __name__ == "__main__":
        app = QApplication(sys.argv)

        login_window = LoginWindow()

        login_window.show()
        # Muestra la ventana
        sys.exit(app.exec())

from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton
from conexion import get_connection  # Para la conexión a la base de datos
import pymysql

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir Producto")
        self.setGeometry(300, 300, 400, 300)

        self.name_input = QLineEdit(self)
        self.price_input = QLineEdit(self)
        self.image_url_input = QLineEdit(self)

        form_layout = QFormLayout()
        form_layout.addRow("Nombre del Producto:", self.name_input)
        form_layout.addRow("Precio:", self.price_input)
        form_layout.addRow("URL de la Imagen:", self.image_url_input)

        self.add_button = QPushButton("Añadir Producto", self)
        self.add_button.clicked.connect(self.add_product)

        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.close)

        form_layout.addRow(self.add_button, self.cancel_button)

        self.setLayout(form_layout)

    def add_product(self):
        """Añadir producto a la base de datos."""
        name = self.name_input.text()
        price = self.price_input.text()
        image_url = self.image_url_input.text()

        if not name or not price or not image_url:
            print("Por favor, complete todos los campos")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            insert_query = "INSERT INTO products (name, price) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, price))
            product_id = cursor.lastrowid  # Obtener el ID del producto insertado

            insert_image_query = "INSERT INTO product_images (product_id, image_url, is_primary) VALUES (%s, %s, 1)"
            cursor.execute(insert_image_query, (product_id, image_url))

            connection.commit()

            self.parent().load_products()  # Recargar productos
            self.close()

        except pymysql.MySQLError as e:
            print(f"Error al añadir producto: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

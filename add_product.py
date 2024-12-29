from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QPushButton
from PySide6.QtCore import Qt
import pymysql
from conexion import get_connection

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Añadir Producto")
        self.setGeometry(300, 300, 400, 450)

        # Entradas del formulario
        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.price_input = QLineEdit(self)
        self.stock_input = QLineEdit(self)
        self.category_id_input = QLineEdit(self)
        self.color_id_input = QLineEdit(self)
        self.gender_id_input = QLineEdit(self)
        self.clothing_type_id_input = QLineEdit(self)
        self.image_url_input = QLineEdit(self)

        # Layout para el formulario de añadir producto
        form_layout = QFormLayout()
        form_layout.addRow("Nombre del Producto:", self.name_input)
        form_layout.addRow("Descripción:", self.description_input)
        form_layout.addRow("Precio:", self.price_input)
        form_layout.addRow("Stock:", self.stock_input)
        form_layout.addRow("ID Categoría:", self.category_id_input)
        form_layout.addRow("ID Color:", self.color_id_input)
        form_layout.addRow("ID Género:", self.gender_id_input)
        form_layout.addRow("ID Tipo de Ropa:", self.clothing_type_id_input)
        form_layout.addRow("URL de la Imagen:", self.image_url_input)

        # Botón de agregar
        self.add_button = QPushButton("Añadir Producto", self)
        self.add_button.setStyleSheet("""...""")  # Estilos de botón
        self.add_button.clicked.connect(self.add_product)

        # Botón de cancelar
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.setStyleSheet("""...""")  # Estilos de botón
        self.cancel_button.clicked.connect(self.close)

        # Añadir los botones al layout
        form_layout.addRow(self.add_button, self.cancel_button)

        self.setLayout(form_layout)

    def add_product(self):
        """Añadir producto a la base de datos."""
        name = self.name_input.text()
        description = self.description_input.text() or None
        price = self.price_input.text()
        stock = self.stock_input.text()
        category_id = self.category_id_input.text() or None
        color_id = self.color_id_input.text() or None
        gender_id = self.gender_id_input.text() or None
        clothing_type_id = self.clothing_type_id_input.text() or None
        image_url = self.image_url_input.text()

        # Validación básica
        if not name or not price or not stock:
            print("Por favor, complete todos los campos requeridos")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Inserción en la tabla de productos
            insert_query = """
            INSERT INTO products
            (name, description, price, stock, category_id, color_id, gender_id, clothing_type_id, view_count, like_count, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 0, 0, current_timestamp())
            """
            cursor.execute(insert_query, (
                name, description, price, stock, category_id, color_id, gender_id, clothing_type_id
            ))
            product_id = cursor.lastrowid  # Obtener el ID del producto insertado

            # Inserción en la tabla de imágenes
            if image_url:
                insert_image_query = """
                INSERT INTO product_images (product_id, image_url, is_primary)
                VALUES (%s, %s, 1)
                """
                cursor.execute(insert_image_query, (product_id, image_url))

            connection.commit()

            # Recargar los productos en la ventana principal
            self.parent().load_products()
            self.close()

        except pymysql.MySQLError as e:
            print(f"Error al añadir producto: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

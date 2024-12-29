from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QScrollArea, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from conexion import get_connection  # Importar la conexión desde conexion.py
import requests  # Asegúrate de tener requests instalado

class ProductWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Productos")
        self.setGeometry(100, 100, 872, 599)
        self.setStyleSheet(self.get_styles())

        # Almacenar el user_id para utilizarlo en la consulta
        self.user_id = user_id

        # Crear un layout principal
        layout = QVBoxLayout(self)

        # Crear un área con scroll para mostrar los productos
        self.products_area = QScrollArea(self)
        self.products_area.setWidgetResizable(True)
        self.products_area.setAlignment(Qt.AlignTop)
        self.products_widget = QWidget(self.products_area)
        self.products_layout = QGridLayout(self.products_widget)

        # Añadir el área de productos al layout principal
        layout.addWidget(self.products_area)

        # Llamar al método que carga los productos
        self.load_products()

    def get_styles(self):
        return """
            QWidget {
                background-color: #f5f5f5;
                color: #333;
                font-family: 'Arial', sans-serif;
                font-size: 16px;
            }

            QLabel {
                font-size: 18px;
                color: #333;
                font-weight: bold;
                margin-bottom: 10px;
            }

            QScrollArea {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 10px;
            }

            QScrollArea QWidget {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }

            QWidget > QWidget {
                margin-top: 15px;
                margin-bottom: 15px;
            }

            QPushButton {
                background-color: #e60000;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px 15px;
                border: none;
            }

            QPushButton:hover {
                background-color: #b30000;
            }

            QLabel[product-image] {
                border: 2px solid #333;
                border-radius: 10px;
                padding: 5px;
            }
        """

    def load_products(self):
        # Limpiar la lista de productos antes de cargar nuevos
        for i in range(self.products_layout.count()):
            widget = self.products_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Usar la conexión desde el archivo conexion.py
        try:
            connection = get_connection()  # Usamos la función para obtener la conexión
            cursor = connection.cursor()
            query = """
            SELECT p.id, p.name, p.price, pi.image_url, pi.is_primary, p.color_id
            FROM products p
            INNER JOIN product_images pi ON p.id = pi.product_id
            WHERE pi.is_primary = 1
            ORDER BY p.id;
            """
            cursor.execute(query)
            products = cursor.fetchall()

            # Cargar los productos y sus imágenes
            row, col = 0, 0
            for product in products:
                product_id, name, price, image_url, is_primary, color_id = product

                # Crear un widget para cada producto
                product_widget = QWidget(self)
                product_layout = QVBoxLayout(product_widget)

                # Nombre del producto
                name_label = QLabel(name, self)
                name_label.setStyleSheet("font-size: 20px; color: #333; font-weight: bold;")
                product_layout.addWidget(name_label)

                # Precio del producto
                price_label = QLabel(f"Precio: ${price}", self)
                price_label.setStyleSheet("font-size: 16px; color: #555;")
                product_layout.addWidget(price_label)

                # Cargar la imagen del producto
                image_label = QLabel(self)
                self.load_image_from_url(image_url, image_label)
                product_layout.addWidget(image_label)

                # Botón para eliminar el producto
                delete_button = QPushButton("Eliminar producto", self)
                delete_button.clicked.connect(lambda _, p_id=product_id: self.delete_product(p_id))
                product_layout.addWidget(delete_button)

                # Añadir el widget del producto al layout
                self.products_layout.addWidget(product_widget, row, col)

                # Pasar a la siguiente columna
                col += 1
                if col > 2:  # Si llegamos a 3 columnas, mover a la siguiente fila
                    col = 0
                    row += 1

            # Refrescar el área de productos
            self.products_area.setWidget(self.products_widget)

        except Exception as e:
            print(f"Error al cargar productos: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def delete_product(self, product_id):
        """Eliminar producto de la base de datos"""
        try:
            connection = get_connection()  # Usamos la función para obtener la conexión
            cursor = connection.cursor()

            # Eliminar el producto de la base de datos
            delete_query = "DELETE FROM products WHERE id = %s"
            cursor.execute(delete_query, (product_id,))
            connection.commit()

            # Recargar la lista de productos
            self.load_products()

        except Exception as e:
            print(f"Error al eliminar el producto: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def load_image_from_url(self, url, label):
        """Carga una imagen desde una URL y la establece en el QLabel."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))  # Ajustar tamaño de la imagen
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("border: 2px solid #333; border-radius: 10px; padding: 5px;")
            else:
                print(f"Error al descargar la imagen: {response.status_code}")
        except Exception as e:
            print(f"Error al descargar la imagen: {e}")

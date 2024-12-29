from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QGridLayout, QFormLayout, QLineEdit, QLabel, QComboBox, QFrame, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import pymysql
from conexion import get_connection  # Para la conexión a la base de datos

# Diccionarios con los mapeos de los IDs y nombres
CATEGORIES = {
    1: "Vestidos", 2: "Trajes", 3: "Camisas", 4: "Pantalones",
    5: "Accesorios", 6: "Zapatos", 7: "Joyería", 8: "Chaquetas",
    9: "Cinturones", 10: "Corbatas", 11: "Pajaritas", 12: "Anillos"
}

CLOTHING_TYPES = {
    1: "Vestidos", 2: "Trajes", 3: "Camisas", 4: "Pantalones",
    5: "Accesorios", 6: "Zapatos", 7: "Joyería", 8: "Chaquetas",
    9: "Cinturones", 10: "Corbatas", 11: "Pajaritas", 12: "Anillos"
}

COLORS = {
    1: "Rojo", 2: "Azul marino", 3: "Negro", 4: "Blanco", 5: "Dorado",
    6: "Plateado", 7: "Verde", 8: "Rosa", 9: "Morado", 10: "Gris",
    11: "Amarillo", 12: "Naranja", 13: "Beige", 14: "Vino", 15: "Turquesa",
    16: "Marron"
}

GENDERS = {
    1: "Masculino", 2: "Femenino", 3: "Unisex"
}

class HomeWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.user_id = user_id
        self.setGeometry(100, 100, 872, 599)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Contenedor principal con un QHBoxLayout para dividir la pantalla en dos
        main_layout = QHBoxLayout()

        # Layout para los botones de navegación (QVBoxLayout para los botones en columna)
        button_layout = QVBoxLayout()
        self.btn_show_products = QPushButton("Mostrar Productos", self)
        self.btn_add_product = QPushButton("Añadir Producto", self)
        self.btn_logout = QPushButton("Cerrar sesión", self)

        button_style = """
            QPushButton {
                background-color: #950909;
                color: white;
                font-size: 16px;
                padding: 12px 20px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7a0707;
            }
            QPushButton:pressed {
                background-color: #5f0606;
            }
        """
        self.btn_show_products.setStyleSheet(button_style)
        self.btn_add_product.setStyleSheet(button_style)
        self.btn_logout.setStyleSheet(button_style)

        button_layout.addWidget(self.btn_show_products)
        button_layout.addWidget(self.btn_add_product)
        button_layout.addWidget(self.btn_logout)

        # Línea separadora (ahora de color gris oscuro)
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #333333; height: 2px;")  # Asegura que la línea sea visible

        # Columna de contenido (productos o formulario)
        self.content_widget = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_widget)

        # Área para mostrar los productos
        self.products_area = QScrollArea(self)
        self.products_area.setWidgetResizable(True)
        self.products_area.setAlignment(Qt.AlignTop)
        self.products_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.products_widget = QWidget(self.products_area)
        self.products_layout = QGridLayout(self.products_widget)
        self.products_area.setWidget(self.products_widget)

        # Formulario para añadir un producto
        self.add_product_form = self.create_add_product_form()

        # Añadir los widgets al layout de contenido
        self.content_layout.addWidget(self.products_area)
        self.content_layout.addWidget(self.add_product_form)

        # Inicialmente ocultamos el formulario de añadir productos
        self.add_product_form.setVisible(False)

        # Conectar las acciones de los botones
        self.btn_show_products.clicked.connect(self.show_products)
        self.btn_add_product.clicked.connect(self.show_add_product_form)
        self.btn_logout.clicked.connect(self.close)

        # Layout principal (divide en dos columnas: botones a la izquierda y contenido a la derecha)
        main_layout.addLayout(button_layout)  # Columna izquierda (botones)
        main_layout.addWidget(separator)  # Separador
        main_layout.addWidget(self.content_widget)  # Columna derecha (productos o formulario)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_products(self):
        """Mostrar la lista de productos."""
        self.products_area.setVisible(True)
        self.add_product_form.setVisible(False)
        self.load_products()

    def show_add_product_form(self):
        """Mostrar el formulario de añadir producto."""
        self.products_area.setVisible(False)
        self.add_product_form.setVisible(True)

    def load_products(self):
        """Método para cargar los productos."""
        # Limpiar la lista de productos antes de cargar
        for i in range(self.products_layout.count()):
            widget = self.products_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        try:
            connection = get_connection()
            cursor = connection.cursor()
            query = """
            SELECT p.id, p.name, p.price, pi.image_url
            FROM products p
            INNER JOIN product_images pi ON p.id = pi.product_id
            WHERE pi.is_primary = 1
            ORDER BY p.id;
            """
            cursor.execute(query)
            products = cursor.fetchall()

            row, col = 0, 0
            for product in products:
                product_id, name, price, image_url = product

                product_widget = QWidget(self)
                product_layout = QVBoxLayout(product_widget)

                product_container = QWidget(self)
                product_container.setStyleSheet("""
                    background-color: #f0f0f0;
                    border-radius: 10px;
                    border: 1px solid #dcdcdc;
                """)
                product_layout.addWidget(product_container)

                image_label = QLabel(self)
                pixmap = QPixmap(image_url)
                image_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
                image_label.setAlignment(Qt.AlignCenter)

                name_label = QLabel(name, self)
                name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #950909;")
                price_label = QLabel(f"${price}", self)
                price_label.setStyleSheet("font-size: 12px; color: #666666;")

                product_layout.addWidget(image_label)
                product_layout.addWidget(name_label)
                product_layout.addWidget(price_label)

                self.products_layout.addWidget(product_widget, row, col)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

            connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error al cargar los productos: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def create_add_product_form(self):
        """Crea el formulario para añadir productos."""
        form_widget = QWidget(self)
        form_layout = QFormLayout(form_widget)

        # Campos del formulario
        self.name_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.price_input = QLineEdit(self)
        self.stock_input = QLineEdit(self)
        self.image_url_input = QLineEdit(self)  # Campo para la URL de la imagen

        # Campos desplegables
        self.category_combobox = QComboBox(self)
        self.color_combobox = QComboBox(self)
        self.gender_combobox = QComboBox(self)
        self.clothing_type_combobox = QComboBox(self)

        # Estilo para los combobox
        combobox_style = """
           QComboBox {
               background-color: white;
               color: black;
               padding: 5px;
               border-radius: 5px;
               border: 1px solid #ccc;
               font-size: 16px;
           }

           QComboBox::drop-down {
               border: none;
               background-color: #f9f9f9;
           }

           QComboBox::down-arrow {
               image: url('down_arrow.png');
           }

           QComboBox:hover {
               border: 1px solid #950909;
           }

           QComboBox QAbstractItemView {
               background-color: white;
               color: black;
               border: 1px solid #ccc;
           }

           QComboBox QAbstractItemView::item {
               background-color: white;
               color: black;
           }

           QComboBox QAbstractItemView::item:hover {
               background-color: #f9f9f9;
               color: black;
           }
           """

        self.category_combobox.setStyleSheet(combobox_style)
        self.color_combobox.setStyleSheet(combobox_style)
        self.gender_combobox.setStyleSheet(combobox_style)
        self.clothing_type_combobox.setStyleSheet(combobox_style)

        # Añadir texto de ayuda en los campos
        self.name_input.setPlaceholderText("Ingrese el nombre del producto")
        self.description_input.setPlaceholderText("Ingrese la descripción del producto")
        self.price_input.setPlaceholderText("Ingrese el precio")
        self.stock_input.setPlaceholderText("Ingrese la cantidad de stock")
        self.image_url_input.setPlaceholderText("Ingrese la URL de la imagen")

        # Estilo para los inputs
        input_style = """
        background-color: #F9F9F9;
        border-radius: 8px;
        border: 1px solid #D1D1D1;
        padding: 10px;
        font-size: 16px;
        color: #333;
        """
        self.name_input.setStyleSheet(input_style)
        self.description_input.setStyleSheet(input_style)
        self.price_input.setStyleSheet(input_style)
        self.stock_input.setStyleSheet(input_style)
        self.image_url_input.setStyleSheet(input_style)

        # Rellenar los combobox con las listas, mostrando los nombres pero guardando los IDs
        for id, name in CATEGORIES.items():
            self.category_combobox.addItem(name, id)
        for id, name in COLORS.items():
            self.color_combobox.addItem(name, id)
        for id, name in GENDERS.items():
            self.gender_combobox.addItem(name, id)
        for id, name in CLOTHING_TYPES.items():
            self.clothing_type_combobox.addItem(name, id)

        # Etiquetas y campos
        form_layout.addRow("Nombre del Producto:", self.name_input)
        form_layout.addRow("Descripción:", self.description_input)
        form_layout.addRow("Precio:", self.price_input)
        form_layout.addRow("Stock:", self.stock_input)
        form_layout.addRow("URL de la Imagen:", self.image_url_input)  # Campo URL imagen

        form_layout.addRow("Categoría:", self.category_combobox)
        form_layout.addRow("Color:", self.color_combobox)
        form_layout.addRow("Género:", self.gender_combobox)
        form_layout.addRow("Tipo de Ropa:", self.clothing_type_combobox)

        # Botón para añadir producto
        self.add_button = QPushButton("Añadir Producto", self)
        self.add_button.setStyleSheet("""
            QPushButton {
                height: 20px;
                background-color: #950909;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #7a0707;
            }
            QPushButton:pressed {
                background-color: #5f0606;
            }
        """)
        self.add_button.clicked.connect(self.add_product)

        # Aseguramos que el botón se añada al final del formulario
        form_layout.addRow("", self.add_button)

        form_widget.setLayout(form_layout)
        return form_widget

    def add_product(self):
        """Añadir producto a la base de datos."""
        name = self.name_input.text()
        description = self.description_input.text()
        price = self.price_input.text()
        stock = self.stock_input.text()
        image_url = self.image_url_input.text()  # Obtener la URL de la imagen
        category_id = self.category_combobox.currentData()  # Obtener el ID seleccionado
        color_id = self.color_combobox.currentData()
        gender_id = self.gender_combobox.currentData()
        clothing_type_id = self.clothing_type_combobox.currentData()

        if not name or not description or not price or not stock or not image_url:
            print("Por favor, complete todos los campos")
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO products (name, description, price, stock, category_id, color_id, gender_id, clothing_type_id, view_count, like_count, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp())
            """
            cursor.execute(insert_query, (name, description, price, stock, category_id, color_id, gender_id, clothing_type_id, 0, 0))

            product_id = cursor.lastrowid  # Obtener el ID del producto recién insertado

            # Insertar la imagen URL
            insert_image_query = """
            INSERT INTO product_images (product_id, image_url, is_primary)
            VALUES (%s, %s, 1)
            """
            cursor.execute(insert_image_query, (product_id, image_url))

            connection.commit()
            print("Producto añadido correctamente")
        except pymysql.MySQLError as e:
            print(f"Error al añadir el producto: {e}")
        finally:
            if connection:
                cursor.close()
                connection.close()

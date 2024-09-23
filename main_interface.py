import time
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QFormLayout,
    QWidget,
    QLineEdit,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
)
from styles import frame_menu, btn_ingreso, title_menu, input_product
from codigo import ReadBarcode


class BarcodeReaderWorker(QObject):
    # Definir una señal para enviar datos al hilo principal
    # barcode_signal = pyqtSignal(str)
    product_signal = pyqtSignal(dict)

    add_product_signal = pyqtSignal(bool)
    # product_input_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        # Crear una instancia de la clase ReadBarcode
        self.read = ReadBarcode()

    def run(self):
        print("method run")
        self.read.read()
        product = self.read.search_code()
        print(f"product {product} ", type(product))

        if not product:
            print("hay que hacer algo aqui")
            self.product_signal.emit({})
        else:
            print("producot encontrado")
            self.product_signal.emit(product)

    def add(self, product):
        print("agregando producto")
        print(product)
        was_added = self.read.add_product("CODIGO", product)

        if not was_added:
            self.add_product_signal.emit(False)
        else:
            self.add_product_signal.emit(True)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # self.read_barcode = ReadBarcode()

        self.title_body = ""

        # Configuración de la ventana principal
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 480)
        MainWindow.setFixedSize(790, 480)  # Tamaño fijo de la ventana
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Crear el QGridLayout principal
        self.grid_layout = QGridLayout(self.centralwidget)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)  # Márgenes opcionales
        self.grid_layout.setSpacing(10)  # Espaciado entre widgets

        # Crear el menú (1/3 del ancho)
        self.menu_frame = QtWidgets.QFrame(self.centralwidget)
        self.menu_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.menu_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.menu_layout = QtWidgets.QVBoxLayout(self.menu_frame)

        # Título del menú
        self.menu_title = QtWidgets.QLabel("Zuany Group", self.menu_frame)
        self.menu_title.setStyleSheet(
            "font-size: 18px; font-weight: bold; text-align: center;"
        )
        self.menu_title.setFixedSize(250, 60)
        self.menu_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Botones del menú
        button_height = 120
        self.btn_ingresar = QtWidgets.QPushButton("Ingresar Producto", self.menu_frame)
        self.btn_ingresar.setStyleSheet(btn_ingreso)

        self.btn_salida = QtWidgets.QPushButton("Salida de Productos", self.menu_frame)
        self.btn_salida.setStyleSheet(btn_ingreso)

        self.btn_ingresar.setFixedHeight(button_height)
        self.btn_salida.setFixedHeight(button_height)

        self.btn_ingresar.clicked.connect(self.add_product)

        self.menu_layout.addWidget(self.btn_ingresar)
        self.menu_layout.addWidget(self.btn_salida)

        # Añadir el menú al QGridLayout en la primera columna (1/3 del ancho)
        self.grid_layout.addWidget(
            self.menu_frame, 0, 0, 2, 1
        )  # Ocupa 2 filas 1 columna

        # Crear el cuerpo principal (2/3 del ancho)
        self.body_frame = QtWidgets.QFrame(self.centralwidget)
        self.body_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.body_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.body_layout = QtWidgets.QVBoxLayout(self.body_frame)

        # Título del cuerpo
        self.title_label = QtWidgets.QLabel(self.title_body, self.body_frame)
        self.title_label.setFixedSize(500, 60)
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Formulario del cuerpo
        self.form_widget = QWidget()
        self.body_layout.addWidget(self.title_label)

        # Añadir el cuerpo principal al QGridLayout en las dos últimas columnas (2/3 del ancho)
        self.grid_layout.addWidget(
            self.body_frame, 0, 1, 2, 2
        )  # Ocupa 2 filas, 2 columnas

        # Configurar la ventana principal
        MainWindow.setCentralWidget(self.centralwidget)

    def generate_body_add_product(self):
        # self.title_body = "Ingreso de Productos"
        # self.title_label.setText(self.title_body)

        self.form_layout = QtWidgets.QFormLayout()
        self.product_name = QtWidgets.QLineEdit()
        self.product_code = QtWidgets.QLineEdit()
        self.form_layout.addRow("Nombre Producto:", self.product_name)
        self.form_layout.addRow("Código:", self.product_code)

        self.body_layout.addWidget(self.title_label)
        self.body_layout.addLayout(self.form_layout)

    def create_worker(self):
        try:
            if (
                hasattr(self, "thread")
                and isinstance(self.thread, QThread)
                and self.thread.isRunning()
            ):
                return  # Evitar iniciar múltiples hilos simultáneamente

            print("Creando worker")
            # Crear el hilo y el worker
            self.thread = QThread()
            self.worker = BarcodeReaderWorker()
            # Mover el worker al hilo
            self.worker.moveToThread(self.thread)
        except Exception as error:
            print(f"Error \n {error}")

    def finish_worker(self):
        try:
            # Detener el hilo cuando termine el trabajo
            self.thread.quit()
            self.thread.wait()
        except Exception as error:
            print(f"Error \n {error}")

    def add_product(self):
        try:
            self.create_worker()
            self.worker.product_signal.connect(self.update_data_product)
            # Conectar las señales
            self.thread.started.connect(self.worker.run)
            # Iniciar el hilo
            self.thread.start()

        except Exception as error:
            print(f"Error \n {error}")

    def update_data_product(self, product):
        """Actualiza la interfaz con el progreso recibido del hilo."""
        print(f"productooo: {product}")
        if not product:
            self.title_body = f"Producto Nuevo"
            self.title_label.setText(self.title_body)
            # muestra el formulario de ingreso de productos
            self.show_form_product()

        if product:
            self.title_body = f"Ingreso de Productos"
            self.title_label.setText(self.title_body)

        # Detener el hilo cuando termine el trabajo
        self.finish_worker()

    def show_form_product(self):
        """Genera y muestra un formulario de ingreso de datos"""
        form_layout = QFormLayout()

        # Crear campos de formulario
        self.name_product_input = QLineEdit()
        self.category_input = QLineEdit()
        self.amount_input = QLineEdit()

        # Aplicar estilos CSS a los QLineEdit
        style_input = input_product()
        self.name_product_input.setStyleSheet(style_input)
        self.category_input.setStyleSheet(style_input)
        self.amount_input.setStyleSheet(style_input)

        form_layout.addRow("Producto:", self.name_product_input)
        form_layout.addRow("Categoria:", self.category_input)
        form_layout.addRow("Cantidad:", self.amount_input)

        # boton para guardar
        button_layout = QHBoxLayout()
        save_button = QPushButton("Guardar")
        button_layout.addWidget(save_button)

        # Crear un widget contenedor para el formulario y el botón
        form_container = QWidget()
        form_container_layout = QHBoxLayout(form_container)
        form_container_layout.addLayout(form_layout)
        form_container_layout.addLayout(button_layout)

        # Establecer el formulario y el botón en el form_widget
        self.form_widget.setLayout(form_container_layout)

        # Agregar el formulario al QVBoxLayout del QFrame
        self.body_layout.addWidget(self.form_widget)
        # save_button.clicked.connect(self.get_product_input)

        # self.create_worker()
        # # Iniciar el hilo
        # self.thread.start()
        # Conectar las señales
        # self.thread.started.connect(self.worker.add)

        print("esta haciendo algo")
        save_button.clicked.connect(self.get_product_input)
        self.create_worker()

        # self.worker.add_product_signal.connect(self.get_product_input)

    def get_product_input(self):

        product = {
            "name": self.name_product_input.text(),
            "category": self.category_input.text(),
            "amount": self.amount_input.text(),
        }
        print(product)

        print(
            product["name"],
            product["name"] == "",
            product["category"] == "",
            not product["amount"].isdigit(),
        )

        if (
            (product["name"] == "")
            or (product["category"] == "")
            or (not product["amount"].isdigit())
        ):
            print("Error al ingresar el producto")
            # Mostrar mensaje de error
            self.show_error_message()
        else:

            # Conectar la señal de éxito/fallo al método del worker
            self.worker.add_product_signal.connect(self.handle_product_addition)

            # Pasar el producto al worker cuando el hilo inicie
            self.thread.started.connect(self.worker.add(product))

            # Iniciar el hilo
            self.thread.start()

            # self.worker.add.emit(product)
            # # Conectar las señales
            # self.thread.started.connect(self.worker.add)

            # # Mostrar mensaje de éxito
            # self.show_success_message()

            # limpiar los input
            self.name_product_input.clear()
            self.category_input.clear()
            self.amount_input.clear()

            # Esperar 2 segundos antes de ocultar el formulario
            QTimer.singleShot(500, self.hide_form)

    def handle_product_addition(self, success):
        """Maneja la respuesta del worker sobre si el producto fue añadido"""
        if success:
            # Mostrar mensaje de éxito
            self.show_success_message()
            # Limpiar los campos
            self.name_product_input.clear()
            self.category_input.clear()
            self.amount_input.clear()
            # Ocultar el formulario después de 2 segundos
            QTimer.singleShot(2000, self.hide_form)
        else:
            print("Error al agregar el producto")
            self.show_error_message()

    def show_error_message(self):
        """Muestra una alerta de producto ingresado erroneamente"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Error")
        msg.setText("Error al ingresar el producto")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

        # Detener el hilo cuando termine el trabajo
        self.finish_worker()
        # Esperar 2 segundos antes de ocultar el formulario
        QTimer.singleShot(2000, self.hide_form)

    def show_success_message(self):
        """Muestra una alerta de producto ingresado correctamente"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Producto Ingresado")
        msg.setText("El producto fue ingresado correctamente.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

        # Esperar 2 segundos antes de ocultar el formulario
        QTimer.singleShot(2000, self.hide_form)

    def hide_form(self):
        """Oculta el formulario después de 2 segundos"""
        self.form_widget.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

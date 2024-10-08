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
    QComboBox,
)
from styles import frame_menu, btn_ingreso, title_menu, input_product
from codigo import ReadBarcode


class BarcodeReaderWorker(QObject):
    # Definir una señal para enviar datos al hilo principal
    product_signal = pyqtSignal(dict)
    add_product_signal = pyqtSignal(bool)

    def __init__(self, readBarcode):
        super().__init__()
        self.readBarcodeInstance = readBarcode
        self.barcode = ""

    def run(self):
        self.barcode = self.readBarcodeInstance.read()
        product = self.readBarcodeInstance.search_code()

        if not product:
            self.product_signal.emit({})
        else:
            self.product_signal.emit(product)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.title_body = ""
        # Configuración de la ventana principal
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 480)
        MainWindow.setFixedSize(790, 480)  # Tamaño fijo de la ventana
        self.setWindowTitle("Control de Inventario - Zuany Group")
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

        self.btn_ingresar.clicked.connect(self.add_product_btn)
        self.btn_salida.clicked.connect(self.remove_product_btn)

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
            self.readBarcodeInstance = ReadBarcode()
            # Crear el hilo y el worker
            self.thread = QThread()
            self.worker = BarcodeReaderWorker(self.readBarcodeInstance)
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

    def add_product_btn(self):
        try:
            self.title_body = f"Lectura de Productos"
            self.title_label.setText(self.title_body)

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
        try:
            if not product:
                self.title_body = f"Producto Nuevo"
                self.title_label.setText(self.title_body)
                # muestra el formulario de ingreso de productos
                self.show_form_product()

            if product:
                print(product)
                self.title_body = f"Producto Encontrado: " + product["name"]
                self.title_label.setText(self.title_body)

                self.show_form_product()

                was_added = self.readBarcodeInstance.update_amount_product("add")
                if was_added:
                    print("producto actualizado")
                    self.finish_worker()

        except Exception as error:
            print(f"error:\n{error}")

    def show_form_amount(self, type: str = "add"):
        """Formulario para ingresar cantidad de producto agregado y/o eliminado"""
        try:
            # print()
            form_layout = QFormLayout()
            # Crear campos de formulario
            self.amount_input = QLineEdit()
            # Aplicar estilos CSS a los QLineEdit
            style_input = input_product()
            self.amount_input.setStyleSheet(style_input)
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
            save_button.clicked.connect(self.show_form_entry_product)

        except Exception as error:
            print(f"error:\n{error}")

    def add_amount_product(self):
        """Agregar cantidad al excel"""
        try:
            amount = self.amount_input.text()
            print("amount:", amount)
            # was_added = self.readBarcodeInstance.write_specific_cell(0)

        except Exception as error:
            print(f"error:\n{error}")

    def show_form_product(self):
        """Genera y muestra un formulario de ingreso de datos"""
        form_layout = QFormLayout()

        # Crear campos de formulario
        self.name_product_input = QLineEdit()
        self.category_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.unit_input = QComboBox()
        self.unit_input.addItem("Unidad")
        self.unit_input.addItem("L")
        self.unit_input.addItem("Kg")

        # Aplicar estilos CSS a los QLineEdit
        style_input = input_product()
        self.name_product_input.setStyleSheet(style_input)
        self.category_input.setStyleSheet(style_input)
        self.amount_input.setStyleSheet(style_input)
        self.unit_input.setStyleSheet(style_input)
        form_layout.addRow("Producto:", self.name_product_input)
        form_layout.addRow("Categoria:", self.category_input)
        form_layout.addRow("Cantidad:", self.amount_input)
        form_layout.addRow("Unidad de Medida:", self.unit_input)

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
        save_button.clicked.connect(self.show_form_entry_product)

    def show_form_entry_product(self):
        product = {
            "name": self.name_product_input.text(),
            "category": self.category_input.text(),
            "amount": self.amount_input.text(),
            "unit": self.unit_input.currentText(),
        }
        # print(product)
        if (
            (product["name"] == "")
            or (product["category"] == "")
            or (not product["amount"].isdigit())
            or (product["unit"] == "")
        ):
            print("Error al ingresar el producto")
            self.show_error_message()
        else:
            # was_added = self.readBarcodeInstance.add_product(
            #     "CODIGO", product["amount"]
            # )

            was_added_inventory_general = self.readBarcodeInstance.write_specific_cell(
                "INVENTARIO GENERAL", "", product
            )
            was_added_inventory = self.readBarcodeInstance.write_specific_cell(
                "INVENTARIO", "ENTRADA", product
            )

            if was_added_inventory_general and was_added_inventory:
                print("producto agregado")
                # Esperar 2 segundos antes de ocultar el formulario
                QTimer.singleShot(500, self.hide_form)
            else:
                print("error al guardar el producto")

            # Limpiar los inputs
            self.name_product_input.clear()
            self.category_input.clear()
            self.amount_input.clear()
            self.unit_input.clear()
            self.finish_worker()

    def remove_product_btn(self):
        try:
            self.create_worker()
            self.worker.product_signal.connect(self.product_removed)
            # Conectar las señales
            self.thread.started.connect(self.worker.run)
            # Iniciar el hilo
            self.thread.start()

        except Exception as error:
            print(f"Error \n {error}")

    def product_removed(self, product):
        try:
            print("producto a remover", product)

            was_removed = self.readBarcodeInstance.remove_product()

            if was_removed:
                self.title_body = f"Producto removido"
                self.title_label.setText(self.title_body)
            else:
                print("::::(())")

        except Exception as error:
            print(f"Error \n {error}")

    def handle_product_addition(self, success):
        """Maneja la respuesta del worker sobre si el producto fue añadido"""
        if success:
            # Mostrar mensaje de éxito
            self.show_success_message()
            # Limpiar los campos
            self.name_product_input.clear()
            self.category_input.clear()
            self.amount_input.clear()

            print("ingresadoooo")
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

import time
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from styles import frame_menu, btn_ingreso, title_menu

from codigo import ReadBarcode


class BarcodeReaderWorker(QObject):
    # Definir una señal para enviar datos al hilo principal
    barcode_read = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Crear una instancia de la clase ReadBarcode
        self.read = ReadBarcode()

    def run(self):
        print("method run")
        barcode = self.read.read()
        product = self.read.search_code()
        print(f"product {product}")
        if barcode:
            print("Lectura completa")
            self.barcode_read.emit(barcode)


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
        self.grid_layout = QtWidgets.QGridLayout(self.centralwidget)
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
        )  # Ocupa 2 filas1 columna

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
        self.form_layout = QtWidgets.QFormLayout()
        # self.product_name = QtWidgets.QLineEdit()
        # self.product_code = QtWidgets.QLineEdit()
        # self.form_layout.addRow("Nombre Producto:", self.product_name)
        # self.form_layout.addRow("Código:", self.product_code)

        self.body_layout.addWidget(self.title_label)
        self.body_layout.addLayout(self.form_layout)

        # Añadir el cuerpo principal al QGridLayout en las dos últimas columnas (2/3 del ancho)
        self.grid_layout.addWidget(
            self.body_frame, 0, 1, 2, 2
        )  # Ocupa 2 filas, 2 columnas

        # Configurar la ventana principal
        MainWindow.setCentralWidget(self.centralwidget)

    def generate_body_add_product(self):
        self.title_body = "Ingreso de Productos"
        self.title_label.setText(self.title_body)

        # self.form_layout = QtWidgets.QFormLayout()
        # self.product_name = QtWidgets.QLineEdit()
        # self.product_code = QtWidgets.QLineEdit()
        # self.form_layout.addRow("Nombre Producto:", self.product_name)
        # self.form_layout.addRow("Código:", self.product_code)

        # self.body_layout.addWidget(self.title_label)
        # self.body_layout.addLayout(self.form_layout)

    def add_product(self):
        try:
            if (
                hasattr(self, "thread")
                and isinstance(self.thread, QThread)
                and self.thread.isRunning()
            ):
                return  # Evitar iniciar múltiples hilos simultáneamente
            print("ingreso productos")
            # Crear el hilo y el worker
            self.thread = QThread()
            self.worker = BarcodeReaderWorker()

            # Mover el worker al hilo
            self.worker.moveToThread(self.thread)
            self.worker.barcode_read.connect(self.update_data_product)

            # Conectar las señales
            self.thread.started.connect(self.worker.run)

            # Iniciar el hilo
            self.thread.start()
        except Exception as error:
            print(f"Error \n {error}")

    def update_data_product(self, barcode):
        """Actualiza la interfaz con el progreso recibido del hilo."""
        # self.label.setText(f"Progreso: {value}")
        self.title_body = f"Ingreso de Productos {barcode}"
        self.title_label.setText(self.title_body)

        # # Detener el hilo cuando termine el trabajo
        self.thread.quit()
        self.thread.wait()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

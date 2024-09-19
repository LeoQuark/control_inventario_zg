from PyQt6 import QtCore, QtGui, QtWidgets
from styles import frame_menu, btn_ingreso, title_menu

from codigo import ReadBarcode


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.read_barcode = ReadBarcode()
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
            print("ingreso productos")
            self.generate_body_add_product()
            code = self.read_barcode.read()
            print(code)
            self.read_barcode.search_code(code)
        except:
            print("error")

        #         self.read_barcode = ReadBarcode()

        #         MainWindow.setObjectName("MainWindow")
        #         MainWindow.resize(790, 480)
        #         self.setFixedSize(790, 480)
        #         self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        #         self.centralwidget.setObjectName("centralwidget")

        #         # Frame Menu
        #         self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        #         self.frame.setGeometry(QtCore.QRect(0, 0, 151, 461))
        #         self.frame.setStyleSheet(frame_menu)
        #         self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        #         self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        #         self.frame.setObjectName("frame")

        #         # btn ingreso productos
        #         self.btn_ingreso_producto = QtWidgets.QPushButton(parent=self.frame)
        #         self.btn_ingreso_producto.setGeometry(QtCore.QRect(10, 150, 131, 71))
        #         font = QtGui.QFont()
        #         font.setPointSize(10)
        #         font.setBold(True)
        #         self.btn_ingreso_producto.setFont(font)
        #         self.btn_ingreso_producto.setStyleSheet(btn_ingreso)
        #         self.btn_ingreso_producto.setStyleSheet(btn_ingreso)
        #         self.btn_ingreso_producto.setObjectName("btn_ingreso_producto")
        #         # Conectar el clic del botón a una función
        #         self.btn_ingreso_producto.clicked.connect(self.ingreso_productos)

        #         # btn salida de productos
        #         self.btn_salida_producto = QtWidgets.QPushButton(parent=self.frame)
        #         self.btn_salida_producto.setGeometry(QtCore.QRect(10, 230, 131, 71))
        #         font = QtGui.QFont()
        #         font.setPointSize(10)
        #         font.setBold(True)
        #         self.btn_salida_producto.setFont(font)
        #         self.btn_salida_producto.setStyleSheet("border-radius: 8px;\n"
        # "background-color: rgb(0, 37, 132);")
        #         self.btn_salida_producto.setObjectName("btn_salida_producto")

        #         # titulo del menu
        #         self.title = QtWidgets.QLabel(parent=self.frame)
        #         self.title.setEnabled(False)
        #         self.title.setGeometry(QtCore.QRect(10, 40, 131, 20))
        #         self.title.setStyleSheet(title_menu)
        #         self.title.setObjectName("title")

        #         # footer
        #         self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        #         self.frame_2.setGeometry(QtCore.QRect(150, 430, 641, 31))
        #         self.frame_2.setStyleSheet("background-color: #E2E2E2;")
        #         self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        #         self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        #         self.frame_2.setObjectName("frame_2")

        #         # body
        #         self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        #         self.frame_3.setGeometry(QtCore.QRect(160, 10, 621, 411))
        #         self.frame_3.setStyleSheet("background-color: #E2E2E2;\n"
        # "border-radius: 8px;")
        #         self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        #         self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        #         self.frame_3.setObjectName("frame_3")

        #         # # Crear un layout dentro del QFrame
        #         # self.frame_layout = QtWidgets.QVBoxLayout()
        #         # self.frame_3.setLayout(self.frame_layout)

        #         # # texto
        #         # # self.title_body = QtWidgets.QLabel(parent=self.frame)
        #         # self.title_body = QtWidgets.QLabel("Codigo de barra", self)
        #         # self.title_body.setStyleSheet("font-size: 16px; color: black; padding: 10px;")

        #         # self.frame_layout.addWidget(self.title_body)
        #         # self.title_body.setGeometry(0,120,100,100)

        #         # Crear un QGridLayout dentro del QFrame
        #         self.frame_layout = QtWidgets.QGridLayout()
        #         self.frame_layout.setContentsMargins(10, 10, 10, 10)  # Margenes opcionales
        #         self.frame_3.setLayout(self.frame_layout)

        #         # Crear un QLabel con texto
        #         self.title_body = QtWidgets.QLabel("Código de barra", self.frame_3)
        #         self.title_body.setStyleSheet("font-size: 16px; color: black; padding: 10px;")

        #         # Añadir el QLabel al QGridLayout en una posición específica
        #         self.frame_layout.addWidget(self.title_body, 0, 1)  # Fila 0, Columna 0

        #         self.frame_layout.addWidget(self.title_body, 1, 2)
        #         # self.frame_3.

        #         # ----
        #         self.title.setEnabled(False)
        #         self.title.setGeometry(QtCore.QRect(10, 40, 131, 20))
        #         self.title.setStyleSheet(title_menu)
        #         self.title.setObjectName("title")

        #         self.frame_2.raise_()
        #         self.frame.raise_()
        #         # self.frame_3.raise_()
        #         MainWindow.setCentralWidget(self.centralwidget)
        #         self.statusBar = QtWidgets.QStatusBar(parent=MainWindow)
        #         self.statusBar.setObjectName("statusBar")
        #         MainWindow.setStatusBar(self.statusBar)

        #         self.retranslateUi(MainWindow)
        #         QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # def retranslateUi(self, MainWindow):
        #         _translate = QtCore.QCoreApplication.translate
        #         MainWindow.setWindowTitle(_translate("MainWindow", "Sistema de Control de Inventario ZG"))
        #         self.btn_ingreso_producto.setText(_translate("MainWindow", "Ingresar Producto"))
        #         self.btn_salida_producto.setText(_translate("MainWindow", "Salida de Producto"))
        #         self.title.setText(_translate("MainWindow", "TextLabel"))

        # def ingreso_productos(self):
        #         print("ingreso productos")
        #         # self.read_barcode.read()
        #         self.read_barcode.search_code()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

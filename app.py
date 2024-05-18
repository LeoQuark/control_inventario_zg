import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QColor, QPalette

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle("Sistema de control de inventario - Zuany Group")
        self.setGeometry(100, 100, 500, 400)

        # Configurar el layout
        layout = QVBoxLayout()

        # Botón de entrada de productos
        btn_entrada = QPushButton("Entrada de Productos", self)
        btn_entrada.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")
        btn_entrada.clicked.connect(self.entrada_productos)
        layout.addWidget(btn_entrada)

        # Botón de salida de productos
        btn_salida = QPushButton("Salida de Productos", self)
        btn_salida.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")
        btn_salida.clicked.connect(self.salida_productos)
        layout.addWidget(btn_salida)

        # Widget central
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def entrada_productos(self):
        print("Acción: Entrada de Productos")

    def salida_productos(self):
        print("Acción: Salida de Productos")

def main():
    app = QApplication(sys.argv)

    # Configurar tema dark
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    app.setPalette(dark_palette)

    # Crear la ventana principal
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
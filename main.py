import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from main_interface import Ui_MainWindow  # Importa la clase generada de la interfaz

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Configura la interfaz

def main():
    app = QApplication(sys.argv)  # Crea la aplicación
    window = MainWindow()         # Crea la ventana principal
    window.show()                 # Muestra la ventana
    sys.exit(app.exec())          # Ejecuta el ciclo de eventos

if __name__ == "__main__":
    main()

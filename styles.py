frame_menu = """
    background-color:  #001243;
    color: rgb(255, 255, 255);
"""

btn_ingreso = """
    QPushButton{
        background-color: #6A6FD2;
        border-radius: 8px;
    }
    
    QPushButton:hover{
        background-color: lightgreen;
        color: white;
    }
    
    QPushButton:pressed {
        background-color: green;
        color: white;
    }
"""

btn_salida = """
    QPushButton{
        background-color: #6A6FD2;
        border-radius: 8px;
    }
    
    QPushButton:hover{
        background-color: lightgreen;
        color: white;
    }
    
    QPushButton:pressed {
        background-color: green;
        color: white;
    }
"""

title_menu = """
    QLabel {
        font-size: 24px;
        color: white;
        padding: 10px;
    }
"""


def input_product():
    return (
        "background-color: white;"
        "border: 1px solid gray;"
        "border-radius: 4px;"
        "padding: 5px;"
        "color: black;"
    )

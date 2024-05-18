import keyboard
import pandas as pd
import datetime
import uuid as uid

from helpers.read_code import read_barcode
from helpers.read_inventory import read_excel_inventory, search_cell_row, input_update_product,output_update_product, get_total_product, update_specific_cell

file_path = "./data"

# class Barcode:
#     barcode = ""
#     exist = False

#     product = ""

#     def __init__(self, barcode, exist):
#         self.barcode = barcode
#         self.exist = True

#     def __str__(self):
#         return f"{self.barcode}, {self.exist}"

#     def verify_if_exists()

    
    

def listen_barcode(barcode):

    if not barcode or barcode == "":
        return False

    print("El código de barras escaneado es:", barcode)
    woorkbook = read_excel_inventory(file_path)
    
    cell_row =  search_cell_row(woorkbook, barcode, "ENTRADAS")
            
    if cell_row is False:
        print("product not exists")
        return False
    
    
    #input_update_product(woorkbook, cell_row)
    total_product = get_total_product(woorkbook, "ENTRADAS", "CODIGO")
    update_specific_cell

    update_specific_cell(woorkbook, "ENTRADAS", "TOTAL PRODUCTO", total_product)


    woorkbook.save(f"{file_path}/inventory.xlsx")

    # if data_product["exist"] is False:
    #     print("error")
    #     return False

    # print(data_product)
    # print(data_product["data"])

    # update_product(PATH_DATA, barcode)


    return True

def main():
    while True:
        # print("Escanea el código de barras y presiona Enter cuando termines:")

        barcode = read_barcode()

        listen =  listen_barcode(barcode)

        if not listen: 
            print("exit program")
            break
    


# def menu_app(option):
#     if option = 1:


if __name__ == "__main__":
    print(uid.uuid4())
    
    main()


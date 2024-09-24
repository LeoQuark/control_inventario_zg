import keyboard
import pandas as pd
import datetime
import uuid as uid

from datetime import datetime
from helpers.read_code import read_barcode
from helpers.read_inventory import (
    read_excel_inventory,
    search_cell_row,
    input_update_product,
    output_update_product,
    get_total_product,
    update_specific_cell,
    # add_product,
    get_all_products,
)

file_path = "./data"
rows = "ABCDE"

columns = {
    "CODIGO": "A",
    "PRODUCTO": "B",
    "CATEGORIA": "C",
    "CANTIDAD": "D",
    "FECHA": "E",
}


class ReadBarcode:
    def __init__(self):
        self.code = ""
        self.cell_row = ""

        # print("inicio de clase")

    def read(self):
        try:
            code = ""
            while True:
                # Leer el evento del teclado
                event = keyboard.read_event()
                # Asegúrate de que el evento no es None
                if event is None:
                    continue

                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == "enter":
                        # Si se presiona "enter", termina la lectura
                        break
                    else:
                        # Concatenar los caracteres al código de barras
                        code += event.name

            # print("Código leído:", code)
            self.code = code
            return code

        except Exception as error:
            print(f"Error \n{error}")

    def search_code(self):
        try:
            self.woorkbook = read_excel_inventory(file_path)
            cell_row = search_cell_row(self.woorkbook, self.code)

            if cell_row is False:
                print("product not exists")
                return False

            dicc_products = get_all_products(self.woorkbook)

            product_exist = {}
            for product in dicc_products:
                if self.code == product["code"]:
                    input_update_product(self.woorkbook, cell_row)
                    self.woorkbook.save(f"{file_path}/inventory.xlsx")
                    product_exist = product

            # print(product_exist, type(product_exist))
            if not product_exist:
                return False
            return product_exist

        except Exception as error:
            print(f"Error \n{error}")

    def add_product(self, columns_name, product, amount=1) -> bool:
        try:

            print("add_product function", self.code)
            sheet = self.woorkbook["INVENTARIO"]

            # for cell in sheet[columns[columns_name]]:
            for cell in sheet[columns[columns_name]]:
                if cell.row < 4:
                    continue
                if cell.value is None:
                    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # dicc_products = get_all_products(woorkbook)
                    # product = verify_product(dicc_products, barcode)
                    if product is False:
                        return False

                    # sheet[f"J{cell.row}"].value = product["code"]
                    sheet[f"J{cell.row}"].value = self.code
                    sheet[f"K{cell.row}"].value = product["name"]
                    sheet[f"L{cell.row}"].value = product["category"]
                    sheet[f"D{cell.row}"].value = date_now
                    sheet[f"E{cell.row}"].value = (
                        product["amount"] if not product["amount"] else amount
                    )

                    return True

        except Exception as error:
            print(f"Error \n{error}")


# def listen_barcode(barcode):

#     if not barcode or barcode == "":
#         return False

#     print("El código de barras escaneado es:", barcode)
#     woorkbook = read_excel_inventory(file_path)

#     cell_row = search_cell_row(woorkbook, barcode, "ENTRADAS")

#     if cell_row is False:
#         print("product not exists")
#         return False

#     # dicc_products = get_all_products(woorkbook)
#     # print(dicc_products)

#     # input_update_product(woorkbook, cell_row)
#     # total_product = get_total_product(woorkbook, "ENTRADAS", "CODIGO")
#     # update_specific_cell

#     test = add_product(woorkbook, "ENTRADAS", "CODIGO", barcode)
#     print("test", test)
#     # update_specific_cell(woorkbook, "ENTRADAS", "TOTAL PRODUCTO", total_product)

#     woorkbook.save(f"{file_path}/inventory.xlsx")

#     return True


# def main():
#     while True:
#         # print("Escanea el código de barras y presiona Enter cuando termines:")
#         barcode = read_barcode()
#         listen = listen_barcode(barcode)

#         if not listen:
#             print("exit program")
#             break


# # def menu_app(option):
# #     if option = 1:

# if __name__ == "__main__":
#     # print(uid.uuid4())
#     main()

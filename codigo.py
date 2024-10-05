import keyboard
import pandas as pd
import datetime
import uuid as uid
from typing import Dict

from datetime import datetime
from helpers.read_code import read_barcode
from helpers.read_inventory import (
    read_excel_inventory,
    search_cell_row,
    input_update_product,
    write_specific_cell,
    output_update_product,
    get_total_product,
    # add_product,
    get_all_products,
)

file_path = "./data"
rows = "ABCDE"

columns = {
    "CODIGO": ["J", "R"],
    "PRODUCTO": ["K", "S"],
    "CATEGORIA": ["L", "T"],
    "FECHA": ["M", "U"],
    "CANTIDAD": ["N", "V"],
}


class ReadBarcode:
    def __init__(self):
        self.code = ""
        self.woorkbook = read_excel_inventory(file_path)
        self.date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.product = {}

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

            self.code = code
            return code

        except Exception as error:
            print(f"Error \n{error}")

    def get_all_products(self) -> dict[any, any] | bool:
        try:
            sheet = self.woorkbook["INVENTARIO"]
            list_code = []
            for cell in sheet["J"]:
                if cell.row < 4:
                    continue
                if cell.value is None:
                    break
                list_code.append(cell.value)

            df_product = pd.DataFrame(data={"codigos": list_code})
            unique_product = df_product["codigos"].unique()

            dicc_products = []
            for cell in sheet["J"]:
                if cell.row < 4:
                    continue
                if cell.value is None:
                    break
                if cell.value in unique_product:
                    dicc_products.append(
                        {
                            "cell_row": cell.row,
                            "code": cell.value,
                            "name": sheet[f"K{cell.row}"].value,
                            "category": sheet[f"L{cell.row}"].value,
                            "amount": sheet[f"N{cell.row}"].value,
                        }
                    )

            return dicc_products

        except Exception as error:
            print(f"Error \n{error}")
            return False

    def search_code(self):
        try:
            cell_row = search_cell_row(self.woorkbook, self.code)

            if cell_row is False:
                print("product not exists")
                return False

            dicc_products = self.get_all_products()
            product_exist = {}

            for product in dicc_products:
                if self.code == product["code"]:
                    product_exist = product
                    self.product = product

            if not product_exist:
                return False
            return product_exist

        except Exception as error:
            print(f"Error \n{error}")

    def write_specific_cell(self, type: int):
        """
        escribe en una celda especifica del excel
        input:
            type (int): 0 para escribir en entrada y 1 para salida
        """
        try:

            sheet = self.woorkbook["INVENTARIO"]
            # R columnas para salidas y J columna para entradas
            type_sheet = "J" if type == 0 else "R"
            print("type", type_sheet)
            next_cell_row = len(sheet[type_sheet]) + 1
            print("next_cell_row", next_cell_row)
            cell_row = self.product["cell_row"]
            print("cell_row", cell_row)

            current_amount = self.product["amount"]

            # cell_row = next_cell_row
            print(f"columna: {columns['CODIGO'][type]}{cell_row}")

            sheet[f"J{next_cell_row}"].value = self.code
            sheet[f"K{next_cell_row}"].value = self.product["name"]
            sheet[f"L{next_cell_row}"].value = self.product["category"]
            sheet[f"M{next_cell_row}"].value = self.date_now
            sheet[f"N{next_cell_row}"].value = (
                self.product["amount"] if not self.product["amount"] else amount
            )

            # sheet[f"{columns['CODIGO'][type]}{cell_row}"].value = self.product["code"]
            # sheet[f"{columns['PRODUCTO'][type]}{cell_row}"].value = self.product["name"]
            # sheet[f"{columns['CATEGORIA'][type]}{cell_row}"].value = self.product[
            #     "category"
            # ]
            # sheet[f"{columns['FECHA'][type]}{cell_row}"].value = self.date_now
            # sheet[f"{columns['CANTIDAD'][type]}{cell_row}"].value = (
            #     int(self.product["amount"]) - 1 if type == 1 else self.product["amount"]
            # )

            return True

        except:
            print("error")
            return False

    def update_amount_product(self, operation: str = "add"):
        try:
            sheet = self.woorkbook["INVENTARIO"]
            cell_row = self.product["cell_row"]

            add_or_subtract = lambda x: 1 if operation == "add" else -1
            sheet[f"N{cell_row}"].value = int(self.product["amount"]) + add_or_subtract(
                operation
            )
            self.woorkbook.save(f"{file_path}/inventory.xlsx")
            print("actualizado")
            return True

        except Exception as error:
            print(f"Error: {error}")
            return False

    def add_product(self, amount=1) -> bool:
        try:
            print("add_product function", self.product)
            sheet = self.woorkbook["INVENTARIO"]
            next_cell_row = len(sheet["J"]) + 1

            sheet[f"J{next_cell_row}"].value = self.code
            sheet[f"K{next_cell_row}"].value = self.product["name"]
            sheet[f"L{next_cell_row}"].value = self.product["category"]
            sheet[f"M{next_cell_row}"].value = self.date_now
            sheet[f"N{next_cell_row}"].value = (
                self.product["amount"] if not self.product["amount"] else amount
            )
            self.woorkbook.save(f"{file_path}/inventory.xlsx")
            return True

        except Exception as error:
            print(f"Error \n{error}")

    def remove_product(self):
        try:
            print("remove product", self.code)

            sheet = self.woorkbook["INVENTARIO"]
            write_cell = self.write_specific_cell(1)
            was_substract = self.update_amount_product("subtract")

            if not write_cell or not was_substract:
                return False

            self.woorkbook.save(f"{file_path}/inventory.xlsx")
            return True

        except Exception as error:
            print(f"Error \n{error}")

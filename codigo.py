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

# columnas para inventario general
columns_inventario_general = {
    "CODIGO": ["A"],
    "PRODUCTO": ["B"],
    "CATEGORIA": ["C"],
    "STOCK": ["D"],
    "UNIDAD": ["E"],
    "UMBRAL": ["F"],
}

# columnas para inventario [entrada, salida]
columns_inventario = {
    "CODIGO": ["B", "K"],
    "PRODUCTO": ["C", "L"],
    "CATEGORIA": ["D", "M"],
    "FECHA": ["E", "N"],
    "CANTIDAD": ["F", "O"],
    "MEDIDA": ["G", "P"],
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
                event = keyboard.read_event()
                if event is None:
                    continue
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == "enter":
                        break
                    else:
                        code += event.name

            self.code = code
            return code

        except Exception as error:
            print(f"Error \n{error}")

    def get_all_products(self) -> dict[any, any] | bool:
        try:
            sheet = self.woorkbook["INVENTARIO GENERAL"]
            list_code = []
            for cell in sheet["A"]:
                if cell.row < 4:
                    continue
                if cell.value is None:
                    break
                list_code.append(cell.value)

            df_product = pd.DataFrame(data={"codigos": list_code})
            unique_product = df_product["codigos"].unique()

            dicc_products = []
            for cell in sheet["A"]:
                if cell.row < 4:
                    continue
                if cell.value is None:
                    break
                if cell.value in unique_product:
                    dicc_products.append(
                        {
                            "cell_row": cell.row,
                            "code": cell.value,
                            "name": sheet[f"B{cell.row}"].value,
                            "category": sheet[f"C{cell.row}"].value,
                            "stock": sheet[f"D{cell.row}"].value,
                            "umbral": sheet[f"E{cell.row}"].value,
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
            print("dicc_products:", dicc_products)
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

    def write_specific_cell(self, sheet: str, type: int, product: Dict):
        """
        escribe en una celda especifica del excel
        input:
            type (int): entrada o salida
        """
        try:
            print("product:", product)
            print("type:", type)
            excel_sheet = self.woorkbook[sheet]
            print(excel_sheet)

            if sheet == "INVENTARIO GENERAL":
                next_cell_row = len(excel_sheet["A"]) + 1
                print("next_cell_row:", next_cell_row, type(next_cell_row))
                print(next_cell_row)

                print(sheet[f"A{next_cell_row}"].value)

                sheet[f"A{next_cell_row}"].value = self.code
                sheet[f"B{next_cell_row}"].value = product["name"]
                sheet[f"C{next_cell_row}"].value = product["category"]
                sheet[f"D{next_cell_row}"].value = product["amount"]
                sheet[f"E{next_cell_row}"].value = product["unit"]

            else:
                # type es entrada la columna a verificar es B si es salida es K
                type_sheet = 0 if type == "ENTRADA" else 1
                next_cell_row = (
                    len(excel_sheet[columns_inventario["CODIGO"][type_sheet]]) + 1
                )

                sheet[
                    f"{columns_inventario.CODIGO[type_sheet]}{next_cell_row}"
                ].value = self.code
                sheet[
                    f"{columns_inventario.PRODUCTO[type_sheet]}{next_cell_row}"
                ].value = product["name"]
                sheet[
                    f"{columns_inventario.CATEGORIA[type_sheet]}{next_cell_row}"
                ].value = product["category"]
                sheet[
                    f"{columns_inventario.FECHA[type_sheet]}{next_cell_row}"
                ].value = self.date_now
                sheet[
                    f"{columns_inventario.CANTIDAD[type_sheet]}{next_cell_row}"
                ].value = product["amount"]
                sheet[
                    f"{columns_inventario.MEDIDA[type_sheet]}{next_cell_row}"
                ].value = product["unit"]

            self.woorkbook.save(f"{file_path}/inventory.xlsx")
            return True

        except Exception as error:
            print(f"Error: {error}")
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

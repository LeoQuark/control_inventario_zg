import pandas as pd
import openpyxl as xlsx
from datetime import datetime

rows = "ABCDE"

columns = {
    "CODIGO": "A",
    "PRODUCTO": "B",
    "CATEGORIA": "C",
    "CANTIDAD": "D",
    "FECHA": "E",
    "TOTAL PRODUCTO": "H1",
    "TOTAL ENTRADAS": "H2",
}


def read_excel_inventory(file_path="./data") -> xlsx:
    """
    se carga el excel de inventario
    input:
        file_path (str, no requerido) -> ruta donde se encuentra el excel de inventario
    output
        woorkbook (xlsx openpyxl) -> woorkbook del inventario (excel)
    """
    woorkbook = xlsx.load_workbook(f"{file_path}/inventory.xlsx")
    return woorkbook


def search_cell_row(woorkbook, barcode) -> int | bool:
    """
    se buscar si existe el codigo de producto en la hoja de INVENTARIO en la primera columna (A)
    input:
        woorkbook (xlsx openpyxl) -> woorkbook del inventario (excel)
        barcode (str) -> codigo de barra
    output:
        cell.row (int) -> numero de la celda en donde se encuentra el codigo
        or
        (bool) -> en caso de que no encuentre el codigo en el inventario o error al encontrar la columna
    """
    try:
        sheet = woorkbook["INVENTARIO"]

        # recorro la columna A (codigo) buscando el barcode detectado
        for cell in sheet["J"]:
            if cell.row < 3:
                continue
            if cell.value is None:
                return False

            if cell.value == barcode:
                # print(f"barcode in cell row: {cell.row}")
                return cell.row
    except:
        print("error")
        return False


def input_update_product(woorkbook, cell_row, amount=False) -> bool:
    """
    se actualiza la cantidad del producto, se suma 1 en caso de no agregar la cantidad (entrada)
    input:
        woorkbook (xlsx openpyxl) -> woorkbook del inventario (excel)
        cell_row (int) -> numero de la celda en donde se encuentra el producto
        amount (int, no requerido) -> cantidad del producto a sumar en el inventario
    output:
        (bool) -> true si realiza la actualizacion de la cantidad del producto, false en caso de error
    """
    try:
        sheet = woorkbook["INVENTARIO"]
        amount_update = lambda x: int(x) if amount is not False else 1
        current_value = int(sheet[f"N{cell_row}"].value)
        # print(f"current_value: {current_value}, amount_update: {amount_update(amount)}")

        update_value = current_value + amount_update(amount)

        sheet[f"N{cell_row}"].value = update_value
        print("actualizado", sheet[f"N{cell_row}"].value)
        return True

    except Exception as error:
        print(f"Error: {error}")
        return False


def get_total_product(woorkbook, sheet_name, columns_name) -> int:
    print("sasa")
    try:
        sheet = woorkbook[sheet_name]
        # recorro la columna A (codigo) buscando el barcode detectado
        list_code = []
        for cell in sheet[columns[columns_name]]:
            if cell.row < 4:
                continue
            if cell.value is None:
                break
            list_code.append(cell.value)

        df_product = pd.DataFrame(data={"codigos": list_code})
        unique_product = df_product["codigos"].unique()

        return len(unique_product)

    except:
        print("error")
        return False


def update_specific_cell(woorkbook, sheet_name, columns_name, value) -> bool:
    try:
        sheet = woorkbook[sheet_name]
        sheet[columns[columns_name]].value = value
        return True

    except:
        print("error")
        return False


# usado
def get_all_products(woorkbook) -> dict[any, any] | bool:
    try:
        sheet = woorkbook["INVENTARIO"]
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
                        "code": cell.value,
                        "name": sheet[f"K{cell.row}"].value,
                        "category": sheet[f"L{cell.row}"].value,
                    }
                )

        return dicc_products

    except Exception as error:
        print(f"Error \n{error}")
        return False


def verify_product(dicc_products, barcode) -> dict[any, any] | bool:
    for product in dicc_products:
        if barcode in product["code"]:
            print("encontrado ------------------------\n", product)
            return product

    return False


def output_update_product(woorkbook, cell_row, amount=False) -> bool:
    """
    se actualiza la cantidad del producto, se resta 1 en caso de no agregar la cantidad (salida)

    input:
        woorkbook (xlsx openpyxl) -> woorkbook del inventario (excel)
        cell_row (int) -> numero de la celda en donde se encuentra el producto
        amount (int, no requerido) -> cantidad del producto a sumar en el inventario
    output:
        (bool) -> true si realiza la actualizacion de la cantidad del producto, false en caso de error
    """
    try:
        sheet = woorkbook["SALIDA"]
        amount_update = lambda x: int(x) if amount is not False else 1
        current_value = int(sheet[f"D{cell_row}"].value)
        print(f"current_value: {current_value}")

        sheet[f"D{cell_row}"].value = current_value - amount_update(amount)
        print("actualizado", sheet["D5"].value)
        return True

    except:
        print("error")
        return False

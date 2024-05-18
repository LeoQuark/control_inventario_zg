import pandas as pd
import openpyxl as xlsx

def read_excel_inventory(file_path = "./data"):
    """
    se obtiene el excel de inventario en base a un path

    input: 
        path (str) -> ruta donde se encuentra el excel de inventario
    output
        df_inventory (dataframe) -> df del inventario
    
    """

    woorkbook = xlsx.load_workbook(f"{file_path}/inventory.xlsx")
    # sheet = woorkbook["INGRESO"]
    return woorkbook

def search_cell_row(sheet, barcode):
    for cell in sheet["A"]:
        if cell.value is None:
            return False

        if cell.value == barcode:
            print(f"barcode in cell row: {cell.row}, {cell}")
            return cell.row

def update_product(woorkbook, cell_row, amount=False):

   try:
        sheet = woorkbook["INGRESO"]

        amount_update = lambda x: int(x) if amount is not False else 1

        current_value = int(sheet[f"D{cell_row}"].value)
        print(f"current_value: {current_value}")

        sheet[f"D{cell_row}"].value = current_value + amount_update(amount)

        print("actualizado: ",current_value + amount_update(amount))

        print(sheet["D5"].value)

   except:
       print("error")

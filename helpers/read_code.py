import keyboard

def read_barcode():
    code = ""
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "enter":
                # Cuando se presiona Enter, se termina de leer el código de barras
                break
            else:
                # Se concatena el carácter al código de barras
                code += event.name   
    return code

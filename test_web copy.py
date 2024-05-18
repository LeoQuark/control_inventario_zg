# import cv2
# import pygame
# from pyzbar.pyzbar import decode

# def play_sound():
#     pygame.mixer.init()
#     pygame.mixer.music.load("./sound/beep.wav")  # Ruta al archivo de sonido
#     pygame.mixer.music.play()

# def detect_barcode(frame):
#     # Convertir la imagen a escala de grises
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detectar códigos de barras en la imagen
#     decoded_objects = decode(gray)
#     barcode_data = ""
#     # Dibujar cuadros delimitadores alrededor de los códigos de barras detectados
#     for obj in decoded_objects:
#         # Obtener las coordenadas y el contenido del código de barras
#         x, y, w, h = obj.rect
#         barcode_data = obj.data.decode("utf-8")
#         barcode_type = obj.type
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
#         # Mostrar el contenido del código de barras
#         cv2.putText(frame, f"{barcode_type}: {barcode_data}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         print(barcode_data)

#         # Reproducir un sonido cuando se detecta un código de barras
#         if barcode_data != "":
#             play_sound()
#             break
    
#     return frame




# def main():
#     # Abrir la cámara web
#     cap = cv2.VideoCapture(0)

#     while True:
#         # Capturar un frame de la cámara
#         ret, frame = cap.read()

#         if ret:
#             # Detectar códigos de barras en el frame
#             frame_with_barcodes = detect_barcode(frame)

#             # Mostrar el frame con los códigos de barras detectados
#             cv2.imshow("Barcode Detector", frame_with_barcodes)

#         # Salir del bucle si se presiona la tecla 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Liberar la cámara y cerrar todas las ventanas
#     cap.release()
#     cv2.destroyAllWindows()



# ---------------------------------------------------------- otra forma
# import logging
# import cv2 
# from pyzbar.pyzbar import decode
# from pydub import AudioSegment
# from pydub.playback import play

# def main():
    


#     # capture webcam 
#     cap = cv2.VideoCapture(0)

#     song = AudioSegment.from_wav("./sound/beep.wav")
#     tecla = keyboard.read_event()

#     while cap.isOpened():
#         success,frame = cap.read()
#         # flip the image like mirror image 
#         frame  = cv2.flip(frame,1)
#         # detect the barcode 
#         detectedBarcode = decode(frame)
#         # if no any barcode detected 
#         if not detectedBarcode:
#             print("No any Barcode Detected")
        
#         # if barcode detected 
#         else:
#             # codes in barcode 
#             for barcode in detectedBarcode:
#                 # if barcode is not blank 
#                 if barcode.data != "":
#                     cv2.putText(frame,str(barcode.data),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,255),2)
#                     play(song)
#                     cv2.imwrite("code.png",frame)


#         cv2.imshow('scanner' , frame)
#         if cv2.waitKey(1) == ord('q'):
#             break

# if __name__ == "__main__":
#     main()



# import keyboard

# def capturar_tecla():
#     while True:
#         tecla = keyboard.read_event()
#         print("Tecla capturada:", tecla.name)

# capturar_tecla()

import keyboard

list_code = []

def leer_codigo_de_barras():
    codigo = ""
    while True:
        evento = keyboard.read_event()
        if evento.event_type == keyboard.KEY_DOWN:
            if evento.name == "enter":
                # Cuando se presiona Enter, se termina de leer el código de barras
                break
            else:
                # Se concatena el carácter al código de barras
                codigo += evento.name
    list_code.append(codigo)    
    return codigo

def main():
    while True:
        # print("Escanea el código de barras y presiona Enter cuando termines:")
        codigo_de_barras = leer_codigo_de_barras()
        
        print("El código de barras escaneado es:", codigo_de_barras, list_code)

if __name__ == "__main__":
    main()


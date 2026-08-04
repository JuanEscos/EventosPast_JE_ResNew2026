# 01ExtractorHTMLFlow_GPT_fix.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FLOW AGILITY - EXTRACTOR DE HTML DE RESULTADOS COMBINADOS
==========================================================

DESCRIPCIÓN:
------------
Script especializado en la extracción masiva de HTML de resultados de mangas
desde FlowAgility.com. Convierte URLs de rings/dates en HTML descargado de
resultados combinados, implementando técnicas avanzadas de hidratación de páginas.

OBJETIVO PRINCIPAL:
-------------------
Transformar: /zone/runs/ring/<ring_id>/date/<fecha>
En:          /zone/prints/run/<uuid>/combined_results.html

FUNCIONALIDADES CLAVE:
----------------------
✓ HIDRATACIÓN COMPLETA DE PÁGINAS
  - Scroll automático hasta el fondo de la página
  - Detección y clic en botones "Load more"/"Ver más"
  - Scroll en contenedores internos con overflow
  - Detección inteligente de estancamiento

✓ EXTRACCIÓN ROBUSTA DE UUIDs
  - Expresiones regulares optimizadas para UUIDs de FlowAgility
  - Preferencia por UUIDs en contexto (/runs/, runId)
  - Eliminación automática de duplicados

✓ DESCARGAS MASIVAS DE HTML
  - Descarga automática de páginas combined_results
  - Nomenclatura consistente: 0001_uuid_combined_results.html
  - Manejo de errores y reintentos implícitos

✓ CONFIGURACIÓN FLEXIBLE
  - Entrada desde JSON o línea de comandos
  - Soporte para Chrome y Edge con perfiles persistentes
  - Fallback a URLs embebidas si falla el JSON

FLUJO DE PROCESAMIENTO:
-----------------------
1. CARGA DE URLs
   │
2. HIDRATACIÓN DE PÁGINA RING/DATE
   │  ├── Scroll principal
   │  ├── Scroll en contenedores internos  
   │  └── Clic en botones "Load more"
   │
3. EXTRACCIÓN DE UUIDs
   │  ├── Búsqueda contextual priorizada
   │  └── Deduplicación automática
   │
4. DESCARGA DE HTML
   │  ├── Navegación a /zone/prints/run/<uuid>/combined_results
   │  └── Guardado local con timestamp implícito

CARACTERÍSTICAS TÉCNICAS AVANZADAS:
-----------------------------------
• DETECCIÓN DE ESTANCAMIENTO: Para cuando no hay nuevos UUIDs tras 3 rondas
• MANEJO DE PERFILES: Usa perfiles existentes o crea temporales si están bloqueados
• SCROLL INTELIGENTE: En ventana principal + contenedores internos con overflow
• EXTRACCIÓN CONTEXTUAL: Prioriza UUIDs que aparecen en rutas /runs/ o parámetros runId

ARCHIVOS DE ENTRADA/SALIDA:
---------------------------
ENTRADA:
  - rings_YYYY-MM-DD.json (campo 'url')
  - O URLs pasadas por línea de comandos
  - O lista de fallback embebida

SALIDA:
  - Results/prints_html/0001_uuid_combined_results.html
  - Results/prints_html/0002_uuid_combined_results.html
  - ...

VARIABLES CRÍTICAS CONFIGURABLES:
---------------------------------
- PAGE_SETTLE_SECONDS: Tiempo de carga inicial (12.0s)
- SCROLL_PAUSE_SECONDS: Pausa entre scrolls (1.5s)  
- MAX_ROUNDS: Máximo de rondas de hidratación (50)
- STAGNANT_LIMIT: Límite de estancamiento (3 rondas)

USO:
----
# Procesar JSON por defecto
python 01ExtractorHTMLFlow_GPT_fix.py

# Procesar JSON específico  
python 01ExtractorHTMLFlow_GPT_fix.py mi_archivo.json

# Procesar URL específica
python 01ExtractorHTMLFlow_GPT_fix.py "https://www.flowagility.com/zone/runs/ring/..."

DEPENDENCIAS:
-------------
- selenium: Automatización web avanzada
- regex: Extracción de patrones UUID
- pathlib: Manejo de rutas cross-platform

MANEJO DE ERRORES:
------------------
- Timeouts configurables para carga de páginas
- Fallback a perfiles temporales si los principales están bloqueados
- Continuación tras errores en URLs individuales
- Logging descriptivo del progreso

@author: Sistema de Extracción Automatizado
@version: 1.0 (Optimizado para FlowAgility)
@date: {fecha_actual}

   
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
import sys
import time
import json
import shutil
import tempfile
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from datetime import datetime, date, timedelta # Tiempo
from dotenv import load_dotenv
from pathlib import Path  # si no lo tenías ya


    
    
# Sonidos
try:
    import winsound
except ImportError:
    winsound = None
import time
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
################################################



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
print('\n' + Fore.YELLOW + 'INICIO Programa.'.center(80, '-') + Style.RESET_ALL)


# In[ ]: # **************************************     CONFIG    *****************************************
# Archivo con las URLs (cada registro tiene el campo 'url')
INPUT_JSON = str(Path(parent_dir) / "output" / "rings.json")
# --- .env + login FlowAgility ---
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    # Cuando ejecutas desde Spyder / IPython
    SCRIPT_DIR = Path.cwd()

BASE_URL  = "https://www.flowagility.com"
LOGIN_URL = f"{BASE_URL}/user/login"

ENV_PATH = SCRIPT_DIR / ".env"
load_dotenv(ENV_PATH)

FLOW_EMAIL = os.getenv("FLOW_EMAIL", "")
FLOW_PASS  = os.getenv("FLOW_PASS", "")

from dotenv import load_dotenv
from pathlib import Path

try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path.cwd()


headless_env = str(os.getenv("HEADLESS", "")).lower()
if headless_env:
    HEADLESS = headless_env in ("1", "true", "yes", "on", "t")

# 👉 Debug temporal
print(f"[DEBUG] FLOW_EMAIL={FLOW_EMAIL!r}, HEADLESS={HEADLESS}")

headless_env = str(os.getenv("HEADLESS", "")).lower()
if headless_env:
    HEADLESS = headless_env in ("1", "true", "yes", "on", "t")

# Fallback manual por si falla la lectura del JSON
RING_URLS_FALLBACK = [


    "https://www.flowagility.com/zone/runs/ring/160248c9-5817-4b3f-889f-2e8a741f5269/date/2025-12-26",
                    
    
]

BROWSER = "chrome"   # "chrome" o "edge"
HEADLESS = False     # pon True si quieres sin ventana
USE_PROFILE = True
if os.getenv("GITHUB_ACTIONS") == "true" or os.name != "nt":
    USE_PROFILE = False

# Rutas habituales de perfiles
CHROME_USER_DATA_DIRS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",         # 64-bit bin
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",   # 32-bit bin
]
CHROME_PROFILE_DIR = r"C:\Users\Juan\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Default"  # o "Profile 1"

EDGE_BINARIES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
EDGE_PROFILE_DIR = r"C:\Users\Juan\AppData\Local\Microsoft\Edge\User Data"
EDGE_PROFILE_NAME = "Default"

OUT_DIR = Path("Results") / "prints_html" # 😊✨😊✨😊✨😊✨
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Tiempos y scroll
PAGE_SETTLE_SECONDS = 12.0   # tiempo inicial para que cargue la página
PRINT_WAIT_SECONDS = 0.9
TOTAL_TIMEOUT = 25           # timeout de espera a <body>

SCROLL_PAUSE_SECONDS = 1.5
MAX_ROUNDS = 50             # rondas de hidratación por ring/date
STAGNANT_LIMIT = 3          # si 3 rondas seguidas no crece el nº de UUIDs -> paramos


# Filtro por fechas (formato YYYY-MM-DD) 😊✨😊✨😊✨😊✨
DATE_FILTER_ENABLED = True
today = datetime.now().date()
START_DATE = "2022-01-01"
# START_DATE = (today - timedelta(days=7)).strftime("%Y-%m-%d")

#END_DATE   = "2025-07-01"
END_DATE   = today.strftime("%Y-%m-%d")

print(f"📆 Ventana móvil: {START_DATE} -> {END_DATE}")
##############################################################################

UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
# Mapa para saber qué event_id corresponde a cada URL de ring/date
EVENT_ID_BY_RING_URL = {}
RING_URL_RE = re.compile(
    r"(https?://(?:www\.)?flowagility\.com)?(/zone/runs/ring/[0-9a-f\-]{36}/date/\d{4}-\d{2}-\d{2})",
    re.I
)

def extract_ring_urls_from_html(html: str) -> list[str]:
    urls = set()
    for domain, path in RING_URL_RE.findall(html or ""):
        if domain:
            urls.add(domain + path)
        else:
            urls.add("https://www.flowagility.com" + path)
    return sorted(urls)


def first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def profile_locked(profile_path: str) -> bool:
    """Detecta bloqueo del perfil (Chrome/Edge) mirando archivos de bloqueo."""
    if not profile_path or not os.path.exists(profile_path):
        return False
    # Chrome/Edge crean 'LOCK' o 'Singleton*'
    if os.path.exists(os.path.join(profile_path, "LOCK")):
        return True
    for item in os.listdir(profile_path):
        if item.lower().startswith("singleton"):
            return True
    return False

def build_driver():
    """Construye un driver robusto para Chrome/Edge con fallback a perfil temporal."""
    import platform
    if platform.system() == "Linux":
        os.system("pkill -9 chrome")
        os.system("pkill -9 chromedriver")

    temp_profile = None

    if BROWSER.lower() == "chrome":
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        opts = ChromeOptions()

        chrome_bin = first_existing(CHROME_USER_DATA_DIRS)
        if chrome_bin:
            opts.binary_location = chrome_bin

        if HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        if USE_PROFILE:
            profile_path = os.path.join(CHROME_PROFILE_DIR, CHROME_PROFILE_NAME)
            if profile_locked(profile_path):
                temp_profile = tempfile.mkdtemp(prefix="chrome_profile_")
                opts.add_argument(f"--user-data-dir={temp_profile}")
            else:
                opts.add_argument(f"--user-data-dir={CHROME_PROFILE_DIR}")
                opts.add_argument(f"--profile-directory={CHROME_PROFILE_NAME}")

        driver = webdriver.Chrome(options=opts)
        driver._temp_profile = temp_profile
        return driver

    else:
        from selenium.webdriver.edge.options import Options as EdgeOptions
        opts = EdgeOptions()

        edge_bin = first_existing(EDGE_BINARIES)
        if edge_bin:
            opts.binary_location = edge_bin

        if HEADLESS:
            opts.add_argument("--headless")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-features=RendererCodeIntegrity")
        opts.add_argument("--window-size=1400,1800")

        if USE_PROFILE:
            profile_path = os.path.join(EDGE_PROFILE_DIR, EDGE_PROFILE_NAME)
            if profile_locked(profile_path):
                temp_profile = tempfile.mkdtemp(prefix="edge_profile_")
                opts.add_argument(f"--user-data-dir={temp_profile}")
            else:
                opts.add_argument(f"--user-data-dir={EDGE_PROFILE_DIR}")
                opts.add_argument(f"--profile-directory={EDGE_PROFILE_NAME}")

        driver = webdriver.Edge(options=opts)
        driver._temp_profile = temp_profile
        return driver

def cleanup_driver(driver):
    try:
        driver.quit()
    except Exception:
        pass
    temp_profile = getattr(driver, "_temp_profile", None)
    if temp_profile and os.path.exists(temp_profile):
        try:
            shutil.rmtree(temp_profile, ignore_errors=True)
        except Exception:
            pass

def try_accept_cookies(driver, timeout: int = 6):
    if not driver:
        return
    end = time.time() + timeout
    while time.time() < end:
        for xp in [
            "//button[contains(., 'De acuerdo')]",
            "//button[contains(., 'Aceptar')]",
            "//button[contains(., 'Accept')]",
            "//a[contains(., 'Accept')]",
        ]:
            try:
                WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, xp)))
                driver.find_element(By.XPATH, xp).click()
                return
            except Exception:
                continue


def login(driver):
    """
    Hace login en FlowAgility usando FLOW_EMAIL y FLOW_PASS del .env.
    Debe llamarse justo después de crear el driver.
    """
    if not FLOW_EMAIL or not FLOW_PASS:
        raise RuntimeError(
            "Credenciales vacías. Revisa .env (FLOW_EMAIL y FLOW_PASS)."
        )

    driver.get(LOGIN_URL)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Intentar aceptar cookies antes de tocar el formulario
    try_accept_cookies(driver)

    # Localizar campos de email y password
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@type,'email')]")
        )
    )
    passwd = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@type='password']")
        )
    )

    # Rellenar credenciales
    email.clear()
    email.send_keys(FLOW_EMAIL)
    passwd.clear()
    passwd.send_keys(FLOW_PASS)

    # Enviar formulario
    passwd.submit()

    # Esperar a que cambie la URL (ya no debe contener /user/login)
    WebDriverWait(driver, 30).until_not(
        EC.url_contains("/user/login")
    )
    time.sleep(1.6)
    print("✓ Login realizado en FlowAgility.")



def load_ring_items_from_json(path: str) -> list[dict]:
    """
    Devuelve una lista de items:
      - {"kind":"ring", "url": ".../zone/runs/ring/.../date/YYYY-MM-DD", "event_id": "..."}
      - {"kind":"runs", "url": ".../zone/event/<event_id>/runs", "event_id": "..."}  (fallback)
    """
    global EVENT_ID_BY_RING_URL
    EVENT_ID_BY_RING_URL = {}

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"No existe el JSON de entrada: {p}")

    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("items", [])

    if not isinstance(data, list):
        raise ValueError("El JSON debe ser una lista de objetos o un dict con clave 'items'.")

    # Filtro de fechas SOLO para URLs que llevan /date/YYYY-MM-DD
    date_from = date_to = None
    if DATE_FILTER_ENABLED:
        if START_DATE:
            date_from = datetime.strptime(START_DATE, "%Y-%m-%d").date()
        if END_DATE:
            date_to = datetime.strptime(END_DATE, "%Y-%m-%d").date()

    items = []
    seen = set()

    for row in data:
        if not isinstance(row, dict):
            continue

        u = row.get("url")
        if not isinstance(u, str):
            continue
        u = u.strip()

        ev_id = row.get("event_id") or row.get("EVENT_ID") or "unknown_event"

        # 1) ring/date normal
        if u.startswith("https://www.flowagility.com/zone/runs/ring/") and "/date/" in u:
            if DATE_FILTER_ENABLED and (date_from or date_to):
                m = re.search(r"/date/(\d{4}-\d{2}-\d{2})", u)
                if not m:
                    continue
                d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                if date_from and d < date_from:
                    continue
                if date_to and d > date_to:
                    continue

            key = ("ring", u)
            if key not in seen:
                seen.add(key)
                items.append({"kind": "ring", "url": u, "event_id": ev_id})
                EVENT_ID_BY_RING_URL[u] = ev_id

        # 2) fallback /runs (como tu registro NO_RING)
        elif u.startswith("https://www.flowagility.com/zone/event/") and u.endswith("/runs"):
            # OJO: aquí NO aplicamos filtro por fecha porque no hay /date/
            key = ("runs", u)
            if key not in seen:
                seen.add(key)
                items.append({"kind": "runs", "url": u, "event_id": ev_id})

    if DATE_FILTER_ENABLED and (date_from or date_to):
        print(f"📆 Filtro fechas: {START_DATE or '-∞'} -> {END_DATE or '+∞'}")
    print(f"📥 Items en JSON: {len(items)} (ring + runs fallback)")
    return items


    def normalize_ring_url(u: str) -> str | None:
        if not isinstance(u, str):
            return None
        u = u.strip()

        # aceptar relativa
        if u.startswith("/zone/runs/ring/"):
            u = BASE_URL + u

        # normalizar dominio (www opcional) y http->https
        u = re.sub(r"^http://", "https://", u, flags=re.I)
        u = re.sub(r"^https://flowagility\.com", "https://www.flowagility.com", u, flags=re.I)

        # validar patrón ring/date
        if not re.search(r"^https://www\.flowagility\.com/zone/runs/ring/[0-9a-f\-]{36}/date/\d{4}-\d{2}-\d{2}$", u, flags=re.I):
            return None
        return u

    urls_raw = []
    for row in data:
        if not isinstance(row, dict):
            continue

        u0 = row.get("url")  # rings.json usa "url"
        u = normalize_ring_url(u0)
        if not u:
            continue

        # filtro por fechas leyendo /date/YYYY-MM-DD de la URL
        if DATE_FILTER_ENABLED and (date_from or date_to):
            m = re.search(r"/date/(\d{4}-\d{2}-\d{2})$", u)
            if not m:
                continue
            d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if date_from and d < date_from:
                continue
            if date_to and d > date_to:
                continue

        urls_raw.append(u)

        # mapear event_id si viene
        ev_id = row.get("event_id") or row.get("EVENT_ID")
        if ev_id:
            EVENT_ID_BY_RING_URL[u] = ev_id

    # dedup preservando orden
    seen = set()
    out = []
    for u in urls_raw:
        if u not in seen:
            seen.add(u)
            out.append(u)

    if DATE_FILTER_ENABLED and (date_from or date_to):
        print(f"📆 Filtro fechas: {START_DATE or '-∞'} -> {END_DATE or '+∞'}")
    print(f"📥 URLs en JSON (tras filtro): {len(urls_raw)} | únicas: {len(out)}")
    return out




def extract_run_uuids_from_html(html: str) -> list[str]:
    """Extrae UUIDs de run de la página."""
    all_guids = set(UUID_RE.findall(html))
    contextual = set()
    for m in re.finditer(r"(?:/run[s]?/|runId[^A-Za-z0-9])([0-9a-f-]{36})", html, flags=re.I):
        gid = UUID_RE.search(m.group(0))
        if gid:
            contextual.add(gid.group(0))
    # preferimos contextuales; si no hay, usamos todos
    return sorted(contextual or all_guids)

def _click_load_more(driver) -> int:
    """Intenta pulsar botones/enlaces de tipo 'Load more', 'Show more', 'Más', etc."""
    clicks = 0
    xpaths = [
        "//button[normalize-space()='Load more' or normalize-space()='Show more' or contains(., 'Load more') or contains(., 'Show more')]",
        "//a[normalize-space()='Load more' or normalize-space()='Show more' or contains(., 'Load more') or contains(., 'Show more')]",
        "//button[contains(., 'Más') or contains(., 'Cargar más') or contains(., 'Ver más')]",
        "//a[contains(., 'Más') or contains(., 'Cargar más') or contains(., 'Ver más')]",
    ]
    for xp in xpaths:
        try:
            for el in driver.find_elements(By.XPATH, xp):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    time.sleep(0.2)
                    if el.is_displayed() and el.is_enabled():
                        el.click()
                        clicks += 1
                        time.sleep(SCROLL_PAUSE_SECONDS)
                except Exception:
                    pass
        except Exception:
            pass
    return clicks

def _scroll_all_scrollables(driver):
    """Hace scroll en contenedores internos con overflow (scroll propio)."""
    script_find = """
    const nodes = Array.from(document.querySelectorAll('*'));
    return nodes.filter(n => {
      const s = getComputedStyle(n);
      if (!s) return false;
      const oh = n.scrollHeight > n.clientHeight + 5;
      const ow = n.scrollWidth  > n.clientWidth  + 5;
      return (oh || ow) && (s.overflowY !== 'visible' || s.overflowX !== 'visible');
    }).slice(0, 8);
    """
    try:
        scrollables = driver.execute_script(script_find)
    except Exception:
        scrollables = []

    for el in scrollables:
        try:
            driver.execute_script("arguments[0].scrollTop = 0;", el)
            last = -1
            for _ in range(20):
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", el)
                time.sleep(0.25)
                cur = driver.execute_script("return arguments[0].scrollTop;", el)
                if cur == last:
                    break
                last = cur
        except StaleElementReferenceException:
            continue
        except Exception:
            continue

def wait_for_ring_loaded(driver, url: str):
    """
    Abre la URL de ring/date y 'hidrata' la página:
    - espera al <body>
    - hace scroll general
    - hace scroll en contenedores internos
    - pulsa botones de 'Load more / Ver más'
    hasta que el nº de UUIDs deja de crecer.
    """
    driver.get(url)
    WebDriverWait(driver, TOTAL_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(PAGE_SETTLE_SECONDS)

    last_count = -1
    stagnant = 0

    for _ in range(MAX_ROUNDS):
        # 1) intenta ver más
        clicks = _click_load_more(driver)

        # 2) scroll al fondo de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SECONDS)

        # 3) scroll interno en contenedores
        _scroll_all_scrollables(driver)
        time.sleep(0.2)

        # 4) mide cuántos UUIDs hay ahora en el DOM
        html = driver.page_source
        cur = len(extract_run_uuids_from_html(html))

        if cur <= last_count and clicks == 0:
            stagnant += 1
        else:
            stagnant = 0
        last_count = max(last_count, cur)

        if stagnant >= STAGNANT_LIMIT:
            break

    # vuelve arriba del todo
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.2)

def save_print_html(driver, run_uuid: str, index: int, total: int, event_id: str):
    """
    Abre la página de impresión de la manga y guarda el HTML.

    El nombre del archivo incluye:
      - número de archivo (index)
      - event_id
      - run_uuid  (para no sobrescribir varias mangas del mismo evento)
    """
    print_url = f"https://www.flowagility.com/zone/prints/run/{run_uuid}/combined_results"
    driver.get(print_url)
    time.sleep(PRINT_WAIT_SECONDS)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except Exception:
        pass

    html = driver.page_source

    safe_event_id = event_id or "unknown_event"
    # Si quisieras SOLO el event_id, sería: f"{index:04d}_{safe_event_id}.html"
    out = OUT_DIR / f"{index:04d}_{safe_event_id}_{run_uuid}_combined_results.html"
    out.write_text(html, encoding="utf-8")

    print(f"[{index}/{total}] Guardado archivo para event_id={safe_event_id} -> {out.name}")


def main():
    global INPUT_JSON

    # 1) Elegir fuente de entrada
    direct_url = None
    if len(sys.argv) > 1:
        arg1 = sys.argv[1].strip()
        if arg1.startswith("http://") or arg1.startswith("https://"):
            direct_url = arg1
            print("▶ Usando solo la URL pasada por línea de comandos.")
        else:
            INPUT_JSON = arg1

    # 2) Construir lista de items
    try:
        if direct_url:
            # si te pasan una URL directa, asumimos que es ring/date
            items = [{"kind": "ring", "url": direct_url, "event_id": "unknown_event"}]
        else:
            items = load_ring_items_from_json(INPUT_JSON)
    except Exception as e:
        print(f"⚠️ No se pudieron cargar items desde JSON ({INPUT_JSON}): {e}")
        print("➡️  Usando RING_URLS_FALLBACK embebidas.")
        items = [{"kind": "ring", "url": u, "event_id": "unknown_event"} for u in RING_URLS_FALLBACK]

    if not items:
        print("⚠️ No hay URLs para procesar.")
        return

    # 3) Crear driver UNA vez y loguear
    driver = build_driver()
    try:
        login(driver)

        seen = set()
        all_run_ids = []

        # 4) Procesar items
        for item in items:
            kind = item["kind"]
            url  = item["url"]
            event_id = item.get("event_id", "unknown_event")

            print(f"\n➡ Abriendo ({kind}): {url}")

            try:
                if kind == "ring":
                    wait_for_ring_loaded(driver, url)
                    html = driver.page_source

                    run_ids = extract_run_uuids_from_html(html)
                    new = [u for u in run_ids if u not in seen]
                    seen.update(new)
                    all_run_ids.extend((u, event_id) for u in new)

                    print(f"🔎 ring: {len(run_ids)} UUIDs, {len(new)} nuevos, event_id={event_id}")

                else:
                    # kind == "runs"
                    driver.get(url)
                    WebDriverWait(driver, TOTAL_TIMEOUT).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    time.sleep(PAGE_SETTLE_SECONDS)

                    last_count = -1
                    stagnant = 0
                    for _ in range(MAX_ROUNDS):
                        clicks = _click_load_more(driver)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(SCROLL_PAUSE_SECONDS)
                        _scroll_all_scrollables(driver)
                        time.sleep(0.2)

                        html = driver.page_source
                        cur = len(extract_run_uuids_from_html(html))

                        if cur <= last_count and clicks == 0:
                            stagnant += 1
                        else:
                            stagnant = 0
                        last_count = max(last_count, cur)

                        if stagnant >= STAGNANT_LIMIT:
                            break

                    html = driver.page_source
                    run_ids = extract_run_uuids_from_html(html)
                    new = [u for u in run_ids if u not in seen]
                    seen.update(new)
                    all_run_ids.extend((u, event_id) for u in new)

                    print(f"🔎 runs: {len(run_ids)} UUIDs, {len(new)} nuevos, event_id={event_id}")

            except Exception as exc:
                print(f"⚠️ Error cargando {url}: {exc}")
                continue

        # 5) Guardar prints
        if not all_run_ids:
            print("⚠️ No se encontraron UUIDs de mangas.")
            return

        total_runs = len(all_run_ids)
        print(f"\n🖨  Abriendo prints y guardando HTML ({total_runs} runs en total):")

        for i, (run_uuid, event_id) in enumerate(all_run_ids, start=1):
            try:
                save_print_html(driver, run_uuid, i, total_runs, event_id)
            except Exception as e:
                print(f"⚠️ Error con run {run_uuid} (event_id={event_id}): {e}")

        print("✅ Terminado.")

    finally:
        cleanup_driver(driver)


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
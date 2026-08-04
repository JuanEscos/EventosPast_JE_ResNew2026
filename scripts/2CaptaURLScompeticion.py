#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
02CaptaURLScompeticion.py
ENTRADA: ./output/01events_past_all.json creado por 01EventosPast_all_URLs_json.py
SALIDA: ./output/01events_past_all.json creado por 01EventosPast_all_URLs_json.py


FLOW AGILITY - SCRAPER AVANZADO DE RINGS CON METADATOS TEMPORALES
==================================================================

DESCRIPCIÓN:
------------
Scraper especializado para la extracción completa de rings (pistas/anillos) 
desde FlowAgility.com, incluyendo análisis temporal avanzado y agrupación 
inteligente por eventos.

CARACTERÍSTICAS MEJORADAS:
--------------------------
✓ Navegación temporal inteligente por fechas de eventos
✓ Detección y deduplicación de rings por (evento, ring, fecha)
✓ Cálculo automático de first_date y last_date por evento
✓ Exportación dual: JSON detallado + CSV resumido
✓ Preservación completa de metadatos de eventos

FUNCIONALIDADES PRINCIPALES:
----------------------------
1. AUTENTICACIÓN SEGURA
   - Login automatizado con gestión de cookies
   - Credenciales via .env con validación
   - Modo headless/configurable

2. EXTRACCIÓN TEMPORAL AVANZADA
   - Navegación secuencial por fechas disponibles
   - Detección de enlaces de rings con validación de URL
   - Procesamiento incremental con control de duplicados

3. METADATOS ENRIQUECIDOS
   - Herencia de metadatos de eventos (club, lugar, organización)
   - Cálculo de rango temporal (primera/última fecha)
   - Agrupación inteligente por evento

4. EXPORTACIÓN COMPLETA
   - JSON: Estructura completa para análisis detallado
   - CSV: Resumen agrupado con métricas temporales
   - Codificación UTF-8 para caracteres internacionales

ESTRUCTURA DE SALIDA:
---------------------
JSON (rings_YYYY-MM-DD.json):
  - Lista completa de todos los rings con metadatos completos
  - Incluye timestamps de scraping y URLs completas

CSV (rings_YYYY-MM-DD.csv):
  - Una fila por evento con rings agrupados
  - Campos: event_id, nombre, club, lugar, organizacion, fechas
  - Métricas: rings_count, first_date, last_date, rings_list

DEPENDENCIAS:
-------------
- selenium >= 4.0: Automatización web
- python-dotenv: Gestión de configuración
- pathlib: Manejo de rutas cross-platform
- typing: Anotaciones de tipo para mejor mantenibilidad

CONFIGURACIÓN:
--------------
Archivo .env requerido:
  FLOW_EMAIL = tu_email@dominio.com
  FLOW_PASS  = tu_contraseña
  HEADLESS   = 0/1 (modo visible/oculto)

USO:
----
Ejecución directa:
  $ python script.py

Integración modular:
  from script import FlowAgilityScraper
  scraper = FlowAgilityScraper()
  scraper.run(Path("ruta/al/events.json"))

MÉTRICAS CALCULADAS:
--------------------
• rings_count: Número total de rings por evento
• first_date: Primera fecha disponible con rings
• last_date: Última fecha disponible con rings  
• rings_list: Lista formateada "ring_id (fecha) | ..."

MANEJO DE ERRORES:
------------------
- Timeouts configurables para elementos dinámicos
- Reintentos automáticos en fallos de navegación
- Validación de URLs y fechas
- Logging descriptivo del progreso

@author: Sistema Automatizado
@version: 2.0 (Mejorado con análisis temporal)
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


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os  # Gestión de archivos
import re
import json, csv, time
from pathlib import Path
from datetime import datetime, date
from typing import Optional, List, Dict, Set

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


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
print('\n' + Fore.YELLOW + 'INICIO Programa.'.center(80, '-') + Style.RESET_ALL)


# flowagility_scrape_rings_and_runs.py
# Extrae:
#  - RINGS: URLs /zone/runs/ring/<ring_id>/date/<yyyy-mm-dd>
#  - RUNS fallback: URLs /zone/run/<run_id>/{start_order,results,combined_results}
#
# Requisitos:
#   pip install selenium python-dotenv


import os
import re
import json
import csv
import time
from pathlib import Path
from datetime import datetime, date
from typing import Optional, List, Dict, Set

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================================
# PATHS / ENV
# ==========================================================
try:
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    SCRIPT_DIR = Path.cwd()

DEFAULT_OUTDIR = str(SCRIPT_DIR / "output")

BASE_URL  = "https://www.flowagility.com"
LOGIN_URL = f"{BASE_URL}/user/login"

ENV_PATH = SCRIPT_DIR / ".env"
load_dotenv(ENV_PATH)

FLOW_EMAIL = os.getenv("FLOW_EMAIL", "")
FLOW_PASS  = os.getenv("FLOW_PASS", "")

HEADLESS = False
headless_env = str(os.getenv("HEADLESS", "")).lower().strip()
if headless_env != "":
    HEADLESS = headless_env in ("1", "true", "yes", "on", "t")

print(f"[DEBUG] FLOW_EMAIL={FLOW_EMAIL!r}, HEADLESS={HEADLESS}")


# ==========================================================
# HELPERS
# ==========================================================
def _parse_date(s: str):
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except Exception:
        return None


def _norm(ev: dict) -> dict:
    """
    Normaliza un registro de evento admitiendo:
      - Nuevo esquema: claves planas (event_id, enlaces_runs, enlaces_info, enlaces_participantes, ...)
      - Esquema antiguo: 'id', 'enlaces': {'runs','info','participantes', ...}
    """
    enlaces = ev.get("enlaces") or {}

    event_id = ev.get("event_id") or ev.get("id") or ""
    nombre   = ev.get("nombre")
    club     = ev.get("club")
    lugar    = ev.get("lugar")
    organiz  = ev.get("organizacion") or ev.get("organización")
    fechas   = ev.get("fechas")
    estado   = ev.get("estado")
    estado_t = ev.get("estado_tipo")
    flag     = ev.get("pais_bandera") or ev.get("pais") or ""

    enlaces_runs  = ev.get("enlaces_runs") or enlaces.get("runs")
    enlaces_info  = ev.get("enlaces_info") or enlaces.get("info")
    enlaces_part  = ev.get("enlaces_participantes") or enlaces.get("participantes")

    return {
        "event_id": event_id,
        "nombre": nombre,
        "club": club,
        "lugar": lugar,
        "organizacion": organiz,
        "fechas": fechas,
        "estado": estado,
        "estado_tipo": estado_t,
        "pais_bandera": flag,
        "enlaces_runs": enlaces_runs,
        "enlaces_info": enlaces_info,
        "enlaces_participantes": enlaces_part
    }


def load_runs_from_json(json_path: Path) -> List[dict]:
    """
    Carga eventos del JSON (nuevo o antiguo) y devuelve lista con runs_url + metadatos normalizados.
    Además imprime cuántos se descartan y por qué.
    """
    if not json_path.exists():
        raise FileNotFoundError(f"No existe el archivo: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_list = data if isinstance(data, list) else []
    total = len(raw_list)

    eventos = []
    skipped = []

    for raw in raw_list:
        ev = _norm(raw)
        runs = ev.get("enlaces_runs")

        if not (isinstance(runs, str) and runs.startswith(f"{BASE_URL}/zone/event/") and runs.endswith("/runs")):
            skipped.append({
                "event_id": ev.get("event_id"),
                "nombre": ev.get("nombre"),
                "enlaces_runs": runs
            })
            continue

        eventos.append({**ev, "runs_url": runs})

    if skipped:
        print(f"[INFO] JSON trae {total} eventos. Se usarán {len(eventos)} con /runs. Se descartan {len(skipped)} sin runs válido.")
        # Muestra un resumen corto (para no spamear)
        for s in skipped[:8]:
            print(f"  - SKIP event_id={s.get('event_id')} nombre={s.get('nombre')!r} runs={s.get('enlaces_runs')!r}")
        if len(skipped) > 8:
            print("  ... (más skips ocultos)")
    else:
        print(f"[INFO] JSON trae {total} eventos. Todos tienen /runs válido.")

    return eventos


# ==========================================================
# SCRAPER
# ==========================================================
class FlowAgilityScraper:
    def __init__(self, outdir: str = DEFAULT_OUTDIR):
        self.driver: Optional[webdriver.Chrome] = None
        self.outdir = outdir

        # Dedup global por (event_id, ring_id, url_date)
        self.all_rings_keys: Set[tuple] = set()
        self.all_ring_rows: List[dict] = []

        # Dedup global por (event_id, run_id)
        self.all_runs_keys: Set[tuple] = set()
        self.all_run_rows: List[dict] = []

        # Fechas ya navegadas del evento actual
        self.processed_dates: Set[date] = set()

        # Metadatos por event_id
        self.eventos_json: Dict[str, dict] = {}

        # Contexto evento actual
        self.current_event: Optional[dict] = None

    # ---------------- DRIVER / LOGIN ----------------
    def setup_driver(self):
        if not FLOW_EMAIL or not FLOW_PASS:
            raise RuntimeError("Credenciales vacías. Revisa .env (FLOW_EMAIL y FLOW_PASS).")

        opts = Options()
        if HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=opts)
        try:
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception:
            pass

    def try_accept_cookies(self, timeout: int = 6):
        if not self.driver:
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
                    WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, xp)))
                    self.driver.find_element(By.XPATH, xp).click()
                    return
                except Exception:
                    continue

    def login(self):
        self.driver.get(LOGIN_URL)
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.try_accept_cookies()

        email = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@type,'email')]"))
        )
        passwd = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        email.clear(); email.send_keys(FLOW_EMAIL)
        passwd.clear(); passwd.send_keys(FLOW_PASS)
        passwd.submit()

        WebDriverWait(self.driver, 30).until_not(EC.url_contains("/user/login"))
        time.sleep(1.6)
        print("✓ Login realizado.")

    # --------------- UTILIDADES URL -----------------
    @staticmethod
    def is_valid_ring_url(url: str) -> bool:
        return bool(url) and ("/zone/runs/ring/" in url) and ("/date/" in url)

    @staticmethod
    def extract_ring_id(url: str) -> str:
        try:
            parts = url.split("/")
            return parts[parts.index("ring") + 1]
        except Exception:
            return "unknown_ring"

    @staticmethod
    def extract_date_from_url(url: str) -> str:
        try:
            return url.split("/date/")[-1]
        except Exception:
            return "unknown"

    # --------------- DEBUG DUMPS --------------------
    def _dump_debug_html(self, event_id: str, tag: str = "runs") -> None:
        try:
            outdir = Path(self.outdir) / "debug_html"
            outdir.mkdir(parents=True, exist_ok=True)
            fname = outdir / f"{event_id}_{tag}.html"
            html = self.driver.page_source if self.driver else ""
            fname.write_text(html, encoding="utf-8")
            print(f"[DEBUG] Guardado HTML: {fname}")
        except Exception as e:
            print(f"[DEBUG] No se pudo guardar HTML: {e}")

    def _dump_debug_screenshot(self, event_id: str, tag: str = "runs") -> None:
        try:
            if not self.driver:
                return
            outdir = Path(self.outdir) / "debug_html"
            outdir.mkdir(parents=True, exist_ok=True)
            fname = outdir / f"{event_id}_{tag}.png"
            self.driver.save_screenshot(str(fname))
            print(f"[DEBUG] Guardado screenshot: {fname}")
        except Exception as e:
            print(f"[DEBUG] No se pudo guardar screenshot: {e}")

    def _dump_debug_meta(self, event_id: str, tag: str = "runs") -> None:
        try:
            if not self.driver:
                return
            outdir = Path(self.outdir) / "debug_html"
            outdir.mkdir(parents=True, exist_ok=True)
            fname = outdir / f"{event_id}_{tag}.txt"

            html = self.driver.page_source or ""
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            iframe_srcs = []
            for fr in iframes[:20]:
                iframe_srcs.append(fr.get_attribute("src") or "")

            text = []
            text.append(f"current_url: {self.driver.current_url}")
            text.append(f"html_len: {len(html)}")
            text.append(f"iframes_count: {len(iframes)}")
            for i, src in enumerate(iframe_srcs, 1):
                text.append(f"iframe_{i}_src: {src}")

            fname.write_text("\n".join(text), encoding="utf-8")
            print(f"[DEBUG] Guardado meta: {fname}")
        except Exception as e:
            print(f"[DEBUG] No se pudo guardar meta: {e}")

    def _wait_and_scroll(self, seconds: float = 3.0) -> None:
        if not self.driver:
            return
        end = time.time() + seconds
        while time.time() < end:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except Exception:
                pass
            time.sleep(0.5)
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
        except Exception:
            pass

    # --------------- SCRAPE RINGS -------------------
    # Reintroduce navegación por fechas (en tu clase)
    def find_date_navigation_links(self) -> List[Dict]:
        try:
            anchors = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/zone/runs/ring/'][href*='/date/']")
        except Exception:
            return []
        links = []
        for a in anchors:
            href = a.get_attribute("href")
            if not href:
                continue
            if self.is_valid_ring_url(href):
                d = _parse_date(self.extract_date_from_url(href))
                if d:
                    links.append({"href": href, "date": d})
        uniq = {l["date"]: l for l in links}
        return sorted(uniq.values(), key=lambda x: x["date"])
    
    
    def navigate_to_next_date(self) -> bool:
        links = self.find_date_navigation_links()
        if not links:
            time.sleep(1.2)
            links = self.find_date_navigation_links()
            if not links:
                return False
    
        last_done = max(self.processed_dates) if self.processed_dates else None
        candidates = [x for x in links if (not last_done) or (x["date"] > last_done)]
        if not candidates:
            return False
    
        target = candidates[0]
        print(f"Navegando a {target['date']} …")
        try:
            self.driver.get(target["href"])
            WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2.0)
            self.processed_dates.add(target["date"])
            return True
        except Exception as e:
            print(f"⚠️ Error navegando: {e}")
            return False

 
    def _extract_ring_links_from_html(self) -> List[str]:
        if not self.driver:
            return []
        html = self.driver.page_source or ""
        # con o sin dominio, y también rutas relativas
        candidates = set(
            re.findall(
                r'(https?://(?:www\.)?flowagility\.com)?(/zone/runs/ring/[a-f0-9\-]+/date/\d{4}-\d{2}-\d{2})',
                html,
                flags=re.I
            )
        )
        urls = set()
        for domain, path in candidates:
            if domain:
                urls.add(domain + path)
            else:
                urls.add(f"{BASE_URL}{path}")
        return sorted(urls)

    def scrape_all_rings(self):
        """Añade rings usando el event_id del contexto actual (self.current_event)."""
        if not self.current_event or not self.driver:
            return

        event_id = self.current_event["event_id"]
        rings_before = len(self.all_rings_keys)

        found_urls = set()

        # 0) CASO ESPECIAL: dropdown de rings (no hay links /ring/date visibles)
        try:
            sel_elements = self.driver.find_elements(By.CSS_SELECTOR, "select#ring")
            if sel_elements:
                from selenium.webdriver.support.ui import Select
                select_obj = Select(sel_elements[0])
                opts = select_obj.options
                if opts:
                    u = self.driver.current_url or ""
                    if "/zone/runs/ring/" not in u or "/date/" not in u:
                        select_obj.select_by_index(0)
                        time.sleep(2.0)
                        u = self.driver.current_url or ""
                    if "/zone/runs/ring/" in u and "/date/" in u:
                        url_date = self.extract_date_from_url(u)
                        for o in opts:
                            v = o.get_attribute("value")
                            if v and len(v) > 10:
                                found_urls.add(f"{BASE_URL}/zone/runs/ring/{v}/date/{url_date}")
        except Exception:
            pass
            
        # 1) DOM: href normal
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/zone/runs/ring/'][href*='/date/']")
            for el in elements:
                href = el.get_attribute("href")
                if href:
                    found_urls.add(href)
        except Exception:
            pass

        # 2) DOM: a veces FlowAgility mete la URL en data-href / data-url
        try:
            elems2 = self.driver.find_elements(By.CSS_SELECTOR, "[data-href*='/zone/runs/ring/'], [data-url*='/zone/runs/ring/']")
            for el in elems2:
                for attr in ("data-href", "data-url"):
                    v = el.get_attribute(attr)
                    if v and "/zone/runs/ring/" in v and "/date/" in v:
                        if v.startswith("/"):
                            v = f"{BASE_URL}{v}"
                        found_urls.add(v)
        except Exception:
            pass

        # 3) Fallback HTML regex
        for u in self._extract_ring_links_from_html():
            found_urls.add(u)

        # 4) Si hay dropdown de ring, construir URLs ring/date para TODOS los rings de la fecha actual
        # (Ya resuelto en el PASO 0)


        # Procesar URLs
        ev_meta = self.eventos_json.get(event_id, {})
        for href in sorted(found_urls):
            if not self.is_valid_ring_url(href):
                continue

            ring_id  = self.extract_ring_id(href)
            url_date = self.extract_date_from_url(href)

            key = (event_id, ring_id, url_date)
            if key in self.all_rings_keys:
                continue

            self.all_rings_keys.add(key)
            self.all_ring_rows.append({
                "event_id": event_id,
                "nombre": ev_meta.get("nombre"),
                "club": ev_meta.get("club"),
                "lugar": ev_meta.get("lugar"),
                "organizacion": ev_meta.get("organizacion"),
                "fechas": ev_meta.get("fechas"),
                "estado": ev_meta.get("estado"),
                "estado_tipo": ev_meta.get("estado_tipo"),
                "pais_bandera": ev_meta.get("pais_bandera"),
                "enlaces_info": ev_meta.get("enlaces_info"),
                "enlaces_participantes": ev_meta.get("enlaces_participantes"),
                "enlaces_runs": ev_meta.get("enlaces_runs"),
                "ring_id": ring_id,
                "url_date": url_date,
                "url": href,
                "scraped_at": datetime.now().isoformat(),
                "ring_mode": "RING_DATE"
            })

        print(f"  ✓ {len(self.all_rings_keys) - rings_before} nuevos (total {len(self.all_rings_keys)})")

    #  RIALP mode
    def _current_ring_date_from_url(self) -> Optional[tuple]:
        """Si estamos en /zone/runs/ring/<ring_id>/date/<yyyy-mm-dd>, devuelve (ring_id, yyyy-mm-dd)."""
        if not self.driver:
            return None
        u = self.driver.current_url or ""
        m = re.search(r"/zone/runs/ring/([0-9a-f\-]+)/date/(\d{4}-\d{2}-\d{2})", u, flags=re.I)
        if not m:
            return None
        return (m.group(1), m.group(2))
    
    def _extract_ring_ids_from_select(self) -> List[str]:
        """Lee el dropdown <select id='ring'> y devuelve los ring_id de sus <option value='...'>."""
        if not self.driver:
            return []
        try:
            sel = self.driver.find_element(By.CSS_SELECTOR, "select#ring")
            opts = sel.find_elements(By.CSS_SELECTOR, "option[value]")
            ids = []
            for o in opts:
                v = (o.get_attribute("value") or "").strip()
                if re.fullmatch(r"[0-9a-f\-]{36}", v, flags=re.I):
                    ids.append(v)
            return ids
        except Exception:
            return []

    # --------------- FALLBACK SCRAPE RUNS -----------
    @staticmethod
    def _extract_run_ids_from_html(html: str) -> List[str]:
        """
        Saca run_ids tipo UUID desde enlaces /zone/run/<uuid>/...
        """
        if not html:
            return []
        ids = set(re.findall(r"/zone/run/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", html, flags=re.I))
        return sorted(ids)

    def scrape_runs_fallback(self) -> int:
        """
        Fallback para eventos que NO exponen ring/date URLs.
        Extrae run_id y genera urls típicas (start_order/results/combined_results).
        Devuelve cuántos runs nuevos se han añadido.
        """
        if not self.current_event or not self.driver:
            return 0

        event_id = self.current_event["event_id"]
        before = len(self.all_runs_keys)

        html = self.driver.page_source or ""
        run_ids = self._extract_run_ids_from_html(html)
        if not run_ids:
            return 0

        ev_meta = self.eventos_json.get(event_id, {})

        for idx, run_id in enumerate(run_ids, 1):
            key = (event_id, run_id)
            if key in self.all_runs_keys:
                continue
            self.all_runs_keys.add(key)

            self.all_run_rows.append({
                "event_id": event_id,
                "nombre": ev_meta.get("nombre"),
                "club": ev_meta.get("club"),
                "lugar": ev_meta.get("lugar"),
                "organizacion": ev_meta.get("organizacion"),
                "fechas": ev_meta.get("fechas"),
                "estado": ev_meta.get("estado"),
                "estado_tipo": ev_meta.get("estado_tipo"),
                "pais_bandera": ev_meta.get("pais_bandera"),
                "enlaces_info": ev_meta.get("enlaces_info"),
                "enlaces_participantes": ev_meta.get("enlaces_participantes"),
                "enlaces_runs": ev_meta.get("enlaces_runs"),
                "date_label": "",  # si en el futuro lo detectas en el DOM, aquí se rellena
                "page_url": self.driver.current_url,
                "run_id": run_id,
                "run_name": str(idx),
                "url_start_order": f"{BASE_URL}/zone/run/{run_id}/start_order#list_anchor_header",
                "url_results": f"{BASE_URL}/zone/run/{run_id}/results#list_anchor_header",
                "url_combined_results": f"{BASE_URL}/zone/run/{run_id}/combined_results#list_anchor_header",
                "scraped_at": datetime.now().isoformat()
            })

        added = len(self.all_runs_keys) - before
        return added

    def _ensure_event_in_rings_as_synthetic(self, event_id: str) -> None:
        """
        Si el evento no tiene rings (ring/date URLs) pero sí tiene runs,
        añadimos una fila sintética a rings.json para que el evento aparezca.
        """
        ev_meta = self.eventos_json.get(event_id, {})
        # Ya existe alguna fila de rings para este evento?
        if any(r.get("event_id") == event_id for r in self.all_ring_rows):
            return

        runs_count = sum(1 for r in self.all_run_rows if r.get("event_id") == event_id)
        if runs_count <= 0:
            return

        key = (event_id, "NO_RING", "")
        if key in self.all_rings_keys:
            return

        self.all_rings_keys.add(key)
        self.all_ring_rows.append({
            "event_id": event_id,
            "nombre": ev_meta.get("nombre"),
            "club": ev_meta.get("club"),
            "lugar": ev_meta.get("lugar"),
            "organizacion": ev_meta.get("organizacion"),
            "fechas": ev_meta.get("fechas"),
            "estado": ev_meta.get("estado"),
            "estado_tipo": ev_meta.get("estado_tipo"),
            "pais_bandera": ev_meta.get("pais_bandera"),
            "enlaces_info": ev_meta.get("enlaces_info"),
            "enlaces_participantes": ev_meta.get("enlaces_participantes"),
            "enlaces_runs": ev_meta.get("enlaces_runs"),
            "ring_id": "NO_RING",
            "url_date": "",
            "url": ev_meta.get("enlaces_runs"),
            "scraped_at": datetime.now().isoformat(),
            "ring_mode": "RUNS_FALLBACK",
            "runs_count": runs_count
        })
        print(f"  ✓ ring sintético añadido (evento sin ring/date, runs_count={runs_count})")

    # --------------- PROCESAR EVENTO ----------------
    def process_event(self, ev: dict, max_navigation: int = 10):
        runs_url = ev["runs_url"]
        event_id = ev.get("event_id")
        print(f"\n========== EVENTO {event_id} ==========")
    
        # contexto
        self.current_event = ev
        self.processed_dates.clear()
    
        # abre /runs
        try:
            self.driver.get(runs_url)
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2.0)
    
            self.try_accept_cookies(timeout=2)
    
            print("URL actual:", self.driver.current_url)
            n_regex = len(self._extract_ring_links_from_html())
            print("Rings detectados en HTML (regex):", n_regex)
    
            if n_regex == 0:
                # da una oportunidad a la carga JS antes de dumpear
                self._wait_and_scroll(2.0)
                n_regex2 = len(self._extract_ring_links_from_html())
                print("Rings detectados en HTML (regex) tras scroll:", n_regex2)
                if n_regex2 == 0:
                    self._dump_debug_html(event_id, "runs_no_rings")
    
        except Exception as e:
            print(f"⚠️ No se pudo abrir {runs_url}: {e}")
            return
    
        # ---------- rings en la vista actual (una sola pasada + retry) ----------
        event_rows_before = len(self.all_ring_rows)
    
        self.scrape_all_rings()
    
        if len(self.all_ring_rows) == event_rows_before:
            print(f"[{event_id}] 0 rings tras primer scrape -> retry con wait+scroll…")
            self._wait_and_scroll(4.0)
            self.scrape_all_rings()
    
        # ---------- NUEVO: recorrer fechas (si ya hay rings o si aparecen al navegar) ----------
        # Nota: esto requiere que existan en la clase:
        #   - find_date_navigation_links()
        #   - navigate_to_next_date()
        # (son los que te pasé antes)
        for i in range(max_navigation):
            print(f"[{event_id}] Navegación fechas {i+1}/{max_navigation} …")
            if not self.navigate_to_next_date():
                print(f"[{event_id}] No hay más fechas nuevas o timeout.")
                break
            self.scrape_all_rings()
    
        # Si sigue sin rings (ni siquiera tras navegar), dump + fallback runs
        if len(self.all_ring_rows) == event_rows_before:
            self._dump_debug_html(event_id, "runs_still_no_rings")
            self._dump_debug_meta(event_id, "runs_still_no_rings")
            self._dump_debug_screenshot(event_id, "runs_still_no_rings")
    
            print(f"[{event_id}] Sin rings -> fallback a extracción de RUNS (/zone/run/<id>/...)")
            added_runs = self.scrape_runs_fallback()
            print(f"  ✓ runs: {added_runs} nuevos (total {len(self.all_runs_keys)})")
    
            # Importante: que el evento aparezca en rings.json aunque no tenga ring/date
            self._ensure_event_in_rings_as_synthetic(event_id)


    # --------------- GUARDAR RESULTADOS -------------
    def save_results(self):
        outdir = Path(self.outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")

        # --------- RINGS JSON ---------
        rings_json = outdir / "rings.json"
        with open(rings_json, "w", encoding="utf-8") as f:
            json.dump(self.all_ring_rows, f, indent=2, ensure_ascii=False)

        # --------- RINGS CSV (agrupado por evento) ---------
        rings_csv = outdir / f"rings_{today}.csv"
        grouped: Dict[str, dict] = {}

        for r in self.all_ring_rows:
            ev_id = r["event_id"]
            d     = _parse_date(r.get("url_date") or "")

            if ev_id not in grouped:
                grouped[ev_id] = {
                    "event_id": ev_id,
                    "nombre": r.get("nombre"),
                    "club": r.get("club"),
                    "lugar": r.get("lugar"),
                    "organizacion": r.get("organizacion"),
                    "fechas": r.get("fechas"),
                    "estado": r.get("estado"),
                    "estado_tipo": r.get("estado_tipo"),
                    "pais_bandera": r.get("pais_bandera"),
                    "enlaces_info": r.get("enlaces_info"),
                    "enlaces_participantes": r.get("enlaces_participantes"),
                    "enlaces_runs": r.get("enlaces_runs"),
                    "rings": [],
                    "first_date": d,
                    "last_date": d,
                }

            grouped[ev_id]["rings"].append({
                "ring_id": r.get("ring_id"),
                "url_date": r.get("url_date"),
                "url": r.get("url"),
                "ring_mode": r.get("ring_mode", "")
            })

            if d:
                if not grouped[ev_id]["first_date"] or d < grouped[ev_id]["first_date"]:
                    grouped[ev_id]["first_date"] = d
                if not grouped[ev_id]["last_date"] or d > grouped[ev_id]["last_date"]:
                    grouped[ev_id]["last_date"] = d

        with open(rings_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "event_id","nombre","club","lugar","organizacion","fechas",
                "estado","estado_tipo","pais_bandera",
                "enlaces_info","enlaces_participantes","enlaces_runs",
                "rings_count","rings_list","first_date","last_date"
            ])
            for ev_id, data in grouped.items():
                rings_sorted = sorted(
                    data["rings"],
                    key=lambda x: (x.get("url_date") or "", x.get("ring_id") or "")
                )
                rings_list = " | ".join(
                    f"{r.get('ring_id')} ({r.get('url_date')}) [{r.get('ring_mode')}]"
                    for r in rings_sorted
                )

                fd = data["first_date"].isoformat() if isinstance(data["first_date"], date) else ""
                ld = data["last_date"].isoformat()  if isinstance(data["last_date"],  date) else ""

                writer.writerow([
                    data["event_id"], data["nombre"], data["club"], data["lugar"],
                    data["organizacion"], data["fechas"], data["estado"], data["estado_tipo"],
                    data["pais_bandera"], data.get("enlaces_info"), data.get("enlaces_participantes"),
                    data.get("enlaces_runs"), len(data["rings"]), rings_list, fd, ld
                ])

        # --------- RUNS JSON ---------
        runs_json = outdir / "runs.json"
        with open(runs_json, "w", encoding="utf-8") as f:
            json.dump(self.all_run_rows, f, indent=2, ensure_ascii=False)

        # --------- RUNS CSV (plano) ---------
        runs_csv = outdir / f"runs_{today}.csv"
        with open(runs_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "event_id","nombre","club","lugar","organizacion","fechas","estado","estado_tipo","pais_bandera",
                "enlaces_info","enlaces_participantes","enlaces_runs",
                "run_id","run_name","url_start_order","url_results","url_combined_results","page_url","scraped_at"
            ])
            for r in self.all_run_rows:
                writer.writerow([
                    r.get("event_id"), r.get("nombre"), r.get("club"), r.get("lugar"), r.get("organizacion"),
                    r.get("fechas"), r.get("estado"), r.get("estado_tipo"), r.get("pais_bandera"),
                    r.get("enlaces_info"), r.get("enlaces_participantes"), r.get("enlaces_runs"),
                    r.get("run_id"), r.get("run_name"),
                    r.get("url_start_order"), r.get("url_results"), r.get("url_combined_results"),
                    r.get("page_url"), r.get("scraped_at")
                ])

        print(
            f"\nResultados guardados:\n"
            f"  RINGS JSON: {rings_json}\n"
            f"  RINGS CSV : {rings_csv}\n"
            f"  RUNS  JSON: {runs_json}\n"
            f"  RUNS  CSV : {runs_csv}"
        )

    # ---------------- RUN ---------------------------
    def run(self, events_json_path: Path):
        try:
            print("=== Iniciando Scraper de FlowAgility ===")
            self.setup_driver()
            self.login()

            base_runs = load_runs_from_json(events_json_path)
            if not base_runs:
                print("No se encontraron URLs /runs válidas en el JSON.")
                return

            print(f"Se procesarán {len(base_runs)} eventos (/runs) del JSON.")
            self.eventos_json = {ev["event_id"]: ev for ev in base_runs}

            for ev in base_runs:
                self.process_event(ev, max_navigation=10)

            self.save_results()

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    events_json = SCRIPT_DIR / "output" / "01events_past.json"
    scraper = FlowAgilityScraper()
    scraper.run(events_json)



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
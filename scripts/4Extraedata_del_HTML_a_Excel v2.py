# -*- coding: utf-8 -*-
"""
Created 04/09/2025
Revisado 10/11/2025

@author: Juan
Descripción del script
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
   print ("Lectura de los datos de FlowAgility sacados por 'C:\JEscos 25.07.07\Agility\PythonScrap\Eventospast\Scripts2026\3ExtraeHTML.py'")
   print ("Copia en BD de los datos")


# In[ ]: **************************************     Librerias    *****************************************
""" Librerias genéricas para cargar en la Consola """

import sys
import os  # Gestión de archivos
import re
import json, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

import argparse
import unicodedata
from typing import Dict, List, Tuple, Optional, Set, Union

import pandas as pd

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



# ============================================================
# CONFIG
# ============================================================

PREFERRED_FOLDER = str(Path(parent_dir) / "Results" / "prints_html")

FALLBACK_HTML_FILES = [
    # r"C:\ruta\al\html1_combined_results.html",
]

RUN_PREFIXES = ["AG", "JP", "AG1", "AG2", "JP1", "JP2"]

RINGS_JSON_CANDIDATES = [
    Path("output/rings.json"),
    Path(parent_dir) / "output" / "rings.json",
]

# Solo metadatos de EVENTO (NO ring/date/url)
RINGS_EVENT_META_FIELDS = [
    "event_id",
    "nombre",
    "club",
    "lugar",
    "organizacion",
    "fechas",
    "pais_bandera",
    "enlaces_info",
    "enlaces_participantes",
    "enlaces_runs",
]


# ============================================================
# Helpers: texto / columnas / dedupe
# ============================================================

def clean_text(x) -> str:
    if x is None:
        return ""
    t = x.get_text(" ", strip=True)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def strip_accents(s: str) -> str:
    if s is None:
        return ""
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", str(s))
        if not unicodedata.combining(ch)
    )


def clean_colname_strict(name: str) -> str:
    """
    Nombres internos (intermedios): solo A-Za-z0-9_ sin acentos.
    """
    name = strip_accents(name or "")
    name = name.replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9_]+", "", name)
    name = re.sub(r"_+", "_", name).strip("_")
    return name


def normalize_value(v) -> str:
    """Para contar 'celdas con datos': considera vacíos '', None, 'nan', '-'."""
    if v is None:
        return ""
    s = str(v).strip()
    if s.lower() == "nan":
        return ""
    if s == "-":
        return ""
    return s


def dedupe_keep_most_data(df: pd.DataFrame, ignore_cols: Optional[Set[str]] = None) -> pd.DataFrame:
    """
    Deduplica filas idénticas salvo ignore_cols.
    Se queda con la fila con MÁS celdas rellenas (excluyendo ignore_cols).
    """
    if df.empty:
        return df

    ignore_cols = ignore_cols or set()
    cols = list(df.columns)
    ignore_cols = {c for c in ignore_cols if c in cols}
    key_cols = [c for c in cols if c not in ignore_cols]
    if not key_cols:
        return df

    scores = df[key_cols].map(normalize_value).ne("").sum(axis=1)
    tmp = df.copy()
    tmp["_score_nonempty"] = scores
    tmp = tmp.sort_values(by="_score_nonempty", ascending=False, kind="mergesort")
    out = tmp.drop_duplicates(subset=key_cols, keep="first").drop(columns=["_score_nonempty"])
    return out.reset_index(drop=True)


def extract_event_id_from_fuentehtml(fuente: str) -> str:
    """
    FuenteHTML:
      0001_<event_id>_<other_uuid>_combined_results.html
    Queremos el substring entre el 1er y 2º "_"
    """
    if not fuente:
        return ""
    parts = str(fuente).split("_")
    if len(parts) >= 3:
        return parts[1].strip()
    return ""


# ============================================================
# EXTRA: detectar URL ring/date desde el propio HTML
# ============================================================

_RING_DATE_RE = re.compile(
    r"(https?://(?:www\.)?flowagility\.com)?(/zone/runs/ring/[0-9a-f\-]{36}/date/\d{4}-\d{2}-\d{2})",
    flags=re.I
)

def extract_ring_date_url_from_html(html: str) -> Tuple[str, str, str]:
    """
    Devuelve (url_full, ring_id, yyyy-mm-dd) si encuentra un /zone/runs/ring/.../date/...
    Si no encuentra, devuelve ("", "", "")
    """
    if not html:
        return "", "", ""
    m = _RING_DATE_RE.search(html)
    if not m:
        return "", "", ""
    domain, path = m.group(1), m.group(2)
    url = (domain + path) if domain else ("https://www.flowagility.com" + path)
    m2 = re.search(r"/zone/runs/ring/([0-9a-f\-]{36})/date/(\d{4}-\d{2}-\d{2})", url, flags=re.I)
    if not m2:
        return url, "", ""
    return url, m2.group(1), m2.group(2)


def year_from_iso(s: str) -> Optional[int]:
    s = str(s or "").strip()
    m = re.match(r"^(20\d{2})-\d{2}-\d{2}$", s)
    return int(m.group(1)) if m else None


def date_iso_from_organ_caption(organ_caption: str) -> str:
    """
    "Organizado por X - 2026.01.11" -> "2026-01-11"
    """
    s = str(organ_caption or "")
    m = re.search(r"(20\d{2})\.(\d{2})\.(\d{2})", s)
    if not m:
        return ""
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"


def year_from_organ_caption(organ_caption: str) -> Optional[int]:
    s = str(organ_caption or "")
    m = re.search(r"(20\d{2})\.(\d{2})\.(\d{2})", s)
    return int(m.group(1)) if m else None


# ============================================================
# rings.json -> SOLO meta de evento
# ============================================================

def load_event_meta_from_rings_json() -> pd.DataFrame:
    path_found = None
    for p in RINGS_JSON_CANDIDATES:
        if p.exists():
            path_found = p
            break

    if path_found is None:
        print("⚠️  No encuentro rings.json en /output, output/ ni junto al script. Se omite UNION_RINGS.")
        return pd.DataFrame()

    try:
        with open(path_found, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️  Error leyendo rings.json ({path_found}): {e}")
        return pd.DataFrame()

    if not isinstance(data, list):
        print("⚠️  rings.json no es una lista de dicts. Se omite UNION_RINGS.")
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # asegurar campos
    for col in RINGS_EVENT_META_FIELDS:
        if col not in df.columns:
            df[col] = ""

    df = df[RINGS_EVENT_META_FIELDS].copy()
    df.columns = [clean_colname_strict(c) for c in df.columns]

    # ✅ Quedarse con la fila "mejor" por event_id (no necesariamente la primera)
    if "event_id" in df.columns:
        def score_row(r):
            s = 0
            s += 100 if str(r.get("url", "")).strip() else 0
            s += 50  if str(r.get("url_date", "")).strip() else 0
            s += 30  if str(r.get("ring_id", "")).strip() else 0
            s += 10  if str(r.get("enlaces_runs", "")).strip() else 0
            return s
    
        df["_score"] = df.apply(score_row, axis=1)
        df = df.sort_values(["event_id", "_score"], ascending=[True, False], kind="mergesort")
        df = df.drop_duplicates(subset=["event_id"], keep="first").drop(columns=["_score"]).reset_index(drop=True)


    return df

def extract_ids_from_fuentehtml(fuente: str) -> Tuple[str, str]:
    """
    Devuelve (event_id, run_id) buscando UUIDs en el nombre del archivo.
    Ejemplo típico:
      0001_<event_uuid>_<run_uuid>_combined_results.html
    """
    if not fuente:
        return ("", "")
    uuids = re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", str(fuente), flags=re.I)
    event_id = uuids[0] if len(uuids) >= 1 else ""
    run_id   = uuids[1] if len(uuids) >= 2 else ""
    return (event_id, run_id)


def make_union_with_event_meta(df: pd.DataFrame, meta_df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or meta_df.empty:
        return pd.DataFrame()

    out = df.copy()
    out.columns = [clean_colname_strict(c) for c in out.columns]

    if "FuenteHTML" not in out.columns:
        cand = [c for c in out.columns if c.lower() == "fuentehtml"]
        if cand:
            out.rename(columns={cand[0]: "FuenteHTML"}, inplace=True)

    out[["EventID","RunID"]] = out["FuenteHTML"].apply(lambda x: pd.Series(extract_ids_from_fuentehtml(x)))

    meta = meta_df.copy()
    meta.columns = [clean_colname_strict(c) for c in meta.columns]

    merged = out.merge(
        meta,
        how="left",
        left_on="EventID",
        right_on="event_id",
        suffixes=("", "_meta")
    )
    return merged


# ============================================================
# HTML parsing
# ============================================================

def extract_cabecera_inicial(soup: BeautifulSoup) -> str:
    el = soup.select_one("div.trial-caption")
    return clean_text(el)


def extract_classificacion(soup: BeautifulSoup) -> str:
    el = soup.find("div", class_=lambda c: c and "results-caption" in c)
    return clean_text(el)


def extract_organ_caption(soup: BeautifulSoup) -> str:
    el = soup.find("div", class_=lambda c: c and "organ-caption" in c)
    return clean_text(el)


def extract_run_meta(soup: BeautifulSoup) -> Dict[str, Dict[str, str]]:
    grid = soup.find("div", class_=lambda c: c and "grid-cols-3" in c and "table-text" in c)
    if not grid:
        grid = soup.find("div", class_=lambda c: c and "grid-cols-3" in c)

    kids = [k for k in grid.find_all(recursive=False) if getattr(k, "name", None)] if grid else []
    meta: Dict[str, Dict[str, str]] = {}

    def rx(pat: str, txt: str) -> str:
        m = re.search(pat, txt, flags=re.I)
        return m.group(1).strip() if m else ""

    for i in range(0, len(kids), 3):
        chunk = kids[i:i + 3]
        if len(chunk) < 3:
            continue

        t0 = clean_text(chunk[0])
        run = t0.split()[0].strip() if t0 else ""
        if not run:
            continue

        t1 = clean_text(chunk[1])
        t2 = clean_text(chunk[2])

        run = run.upper()
        meta[run] = {
            "Obstaculos": rx(r"Obst[aá]culos:\s*([0-9]+)", t0),
            "Longitud_m": rx(r"Longitud:\s*([0-9]+(?:[.,][0-9]+)?)\s*m", t0),
            "TiempoStandard_s": rx(r"Tiempo\s*Standard:\s*([0-9]+(?:[.,][0-9]+)?)\s*s", t1),
            "TiempoMaximo_s": rx(r"Tiempo\s*M[aá]ximo:\s*([0-9]+(?:[.,][0-9]+)?)\s*s", t1),
            "Juez": rx(r"Juez:\s*(.*?)\s*(?:Velocidad:|$)", t2),
            "Velocidad_ms": rx(r"Velocidad:\s*([0-9]+(?:[.,][0-9]+)?)\s*m/s", t2),
        }

    # Algunas plantillas de impresión no presentan los metadatos en la
    # cuadrícula de tres columnas. Recuperarlos desde cada bloque que contiene
    # la modalidad y "Juez:" evita descartar nombres válidos por el layout.
    for element in soup.find_all(["div", "section", "article", "li"]):
        text = clean_text(element)
        match = re.search(r"(?<![A-Z0-9])(AG1|AG2|JP1|JP2|AG|JP)(?![A-Z0-9]).*?Juez:\s*(.*?)\s*(?:Velocidad:|$)", text, flags=re.I)
        if not match:
            continue
        run = match.group(1).upper()
        judge = match.group(2).strip(" ·|,-")
        if not judge:
            continue
        current = meta.setdefault(run, {})
        if not current.get("Juez"):
            current["Juez"] = judge
            current.setdefault("Obstaculos", rx(r"Obst[aá]culos:\s*([0-9]+)", text))
            current.setdefault("Longitud_m", rx(r"Longitud:\s*([0-9]+(?:[.,][0-9]+)?)\s*m", text))
            current.setdefault("TiempoStandard_s", rx(r"Tiempo\s*Standard:\s*([0-9]+(?:[.,][0-9]+)?)\s*s", text))
            current.setdefault("TiempoMaximo_s", rx(r"Tiempo\s*M[aá]ximo:\s*([0-9]+(?:[.,][0-9]+)?)\s*s", text))
            current.setdefault("Velocidad_ms", rx(r"Velocidad:\s*([0-9]+(?:[.,][0-9]+)?)\s*m/s", text))

    return meta


def parse_participant_row(row_div, valid_runs_upper: Set[str]) -> Optional[Dict[str, str]]:
    children = [c for c in row_div.find_all(recursive=False) if getattr(c, "name", None)]
    if len(children) < 5:
        return None

    rec: Dict[str, str] = {}

    blocks = children[0].find_all("div", recursive=False)
    rec["Pos"] = clean_text(blocks[0]) if len(blocks) > 0 else ""
    rec["Dorsal"] = clean_text(blocks[1]) if len(blocks) > 1 else ""

    gp = children[1].find_all("div", recursive=False)
    rec["Guia"] = clean_text(gp[0]) if len(gp) > 0 else ""
    rec["Perro"] = clean_text(gp[1]) if len(gp) > 1 else ""

    cl = children[2].find_all("div", recursive=False)
    rec["Club"] = clean_text(cl[0]) if len(cl) > 0 else ""
    rec["Licencia"] = clean_text(cl[1]) if len(cl) > 1 else ""

    results_block = children[3]
    trial_rows = results_block.find_all("div", class_=lambda c: c and "flex-row" in c)

    for tr in trial_rows:
        tchildren = [x for x in tr.find_all(recursive=False) if getattr(x, "name", None)]
        if len(tchildren) < 2:
            continue

        run = clean_text(tchildren[0]).upper()
        if run not in valid_runs_upper:
            continue

        vals = [clean_text(x) for x in tchildren[1:]]
        keys = ["T", "F", "R", "TP", "VEL", "CAL", "PTS", "CLA"]
        for k, v in zip(keys, vals):
            rec[f"{run}_{k}"] = v

    gen = children[4].find_all("div", recursive=False)
    rec["General_T"] = clean_text(gen[0]) if len(gen) > 0 else ""
    rec["General_TP"] = clean_text(gen[1]) if len(gen) > 1 else ""

    return rec


def resolve_run_metadata_for_results(run_meta: Dict[str, Dict[str, str]], observed_runs: Set[str]) -> Dict[str, Dict[str, str]]:
    """Alinea metadatos genéricos JP/AG con los prefijos reales del resultado.

    FlowAgility puede mostrar ``JP`` en la cabecera y ``JP1`` en la fila de
    resultados. Solo se copia el metadato si hay una única candidata numerada,
    evitando adjudicar un juez ambiguamente entre JP1 y JP2.
    """
    resolved = {str(run).upper(): dict(values) for run, values in run_meta.items()}
    observed = {str(run).upper() for run in observed_runs}
    for base in ("JP", "AG"):
        if base not in resolved:
            continue
        candidates = sorted(run for run in observed if run.startswith(base) and run != base)
        if len(candidates) == 1 and candidates[0] not in resolved:
            resolved[candidates[0]] = dict(resolved[base])
    return resolved

def parse_file(path: Path) -> pd.DataFrame:
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    cabecera_inicial = extract_cabecera_inicial(soup)
    classificacion = extract_classificacion(soup)
    organ_caption = extract_organ_caption(soup)

    # URLFuente/Fecha/ring_id desde el HTML (clave para evitar el bug)
    urlfuente, ring_id, url_date = extract_ring_date_url_from_html(html)

    # si no hay url_date, intenta sacar Fecha de Organ_caption (yyyy.mm.dd)
    if not url_date:
        url_date = date_iso_from_organ_caption(organ_caption)

    run_meta = extract_run_meta(soup)
    # Las filas pueden usar JP1/AG1 aunque la cabecera diga solo JP/AG.
    # Se leen primero todas las modalidades conocidas y después se alinean
    # metadatos sin asignar jueces cuando haya ambigüedad.
    valid_runs_upper = {run.upper() for run in RUN_PREFIXES}

    header_row = soup.find("div", class_=lambda c: c and "bg-gray-300" in c and "flex-row" in c)
    if not header_row:
        return pd.DataFrame()

    participant_rows = header_row.find_all_next(
        "div",
        class_=lambda c: c and "flex-row" in c and "items-center" in c and "justify-center" in c and "py-1" in c
    )

    records: List[Dict[str, str]] = []
    for r in participant_rows:
        rec = parse_participant_row(r, valid_runs_upper)
        if not rec:
            continue

        rec["FuenteHTML"] = path.name
        rec["CabeceraInicial"] = cabecera_inicial
        rec["Classificacion"] = classificacion
        rec["Organ_caption"] = organ_caption

        observed_runs = {
            key.split("_", 1)[0].upper()
            for key in rec
            if "_" in key and key.split("_", 1)[0].upper() in valid_runs_upper
        }
        resolved_meta = resolve_run_metadata_for_results(run_meta, observed_runs)

        # nuevos campos por archivo
        rec["URLFuente"] = urlfuente
        rec["ring_id"] = ring_id
        rec["Fecha"] = url_date  # ya ISO si venía de /date/

        for run, md in resolved_meta.items():
            rec[f"{run}_Obstaculos"] = md.get("Obstaculos", "")
            rec[f"{run}_Longitud_m"] = md.get("Longitud_m", "")
            rec[f"{run}_TiempoStandard_s"] = md.get("TiempoStandard_s", "")
            rec[f"{run}_TiempoMaximo_s"] = md.get("TiempoMaximo_s", "")
            rec[f"{run}_Juez"] = md.get("Juez", "")
            rec[f"{run}_Velocidad_ms"] = md.get("Velocidad_ms", "")

        records.append(rec)

    return pd.DataFrame(records).replace("-", "").fillna("")


def collect_inputs() -> List[Path]:
    folder = Path(PREFERRED_FOLDER)
    if folder.exists() and folder.is_dir():
        htmls = sorted(folder.glob("*.html"))
        return [p for p in htmls if p.exists()]
    return [Path(p) for p in FALLBACK_HTML_FILES if Path(p).exists()]


# ============================================================
# LONG (trasposición de prefijos)
# ============================================================

def first_non_empty(series: pd.Series):
    for v in series:
        s = normalize_value(v)
        if s != "":
            return v
    return ""


def transpose_prefixes(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    LONG: filas por participante y por Ag_Jp.
    Solo crea filas del prefijo si esa fila tiene algún valor no vacío en ese prefijo.
    Agrupa por TODOS los campos no prefijados (incluye CabeceraInicial y Classificacion).
    """
    df = df_raw.copy()
    df.columns = [clean_colname_strict(c) for c in df.columns]

    prefixes = [p.upper() for p in RUN_PREFIXES]

    def is_prefixed(col: str) -> bool:
        cu = col.upper()
        return any(cu.startswith(p + "_") for p in prefixes)

    pref_cols = [c for c in df.columns if is_prefixed(c)]
    non_pref_cols = [c for c in df.columns if c not in pref_cols]
    group_keys = non_pref_cols.copy()

    out_parts = []
    for p in prefixes:
        cols_p = [c for c in pref_cols if c.upper().startswith(p + "_")]
        if not cols_p:
            continue

        sub = df[non_pref_cols + cols_p].copy()
        mask_any = sub[cols_p].apply(lambda row: any(normalize_value(v) != "" for v in row), axis=1)
        sub = sub.loc[mask_any].copy()
        if sub.empty:
            continue

        sub["Ag_Jp"] = p
        rename_map = {c: c[len(p) + 1:] for c in cols_p}  # quita "JP1_"
        sub.rename(columns=rename_map, inplace=True)
        out_parts.append(sub)

    if not out_parts:
        base = df[non_pref_cols].copy()
        base["Ag_Jp"] = ""
        return base

    out = pd.concat(out_parts, ignore_index=True, sort=False).fillna("")
    agg_cols = [c for c in out.columns if c not in set(group_keys + ["Ag_Jp"])]
    agg_dict = {c: first_non_empty for c in agg_cols}
    out_g = out.groupby(group_keys + ["Ag_Jp"], dropna=False, as_index=False).agg(agg_dict)
    out_g.columns = [clean_colname_strict(c) for c in out_g.columns]
    return out_g


# ============================================================
# WP Transform (renombres + calculados + orden)
# ============================================================

def infer_sexo_guia(nombre_guia: str) -> str:
    if not nombre_guia:
        return ""
    first = strip_accents(nombre_guia).strip().split()[0].lower()

    fem = {
        "maria","ana","laura","silvia","diana","laia","lucia","carmen","marta","paula",
        "andrea","clara","nuria","noelia","sara","patricia","monica","sonia","alba",
        "irene","cristina","beatriz","rocio","raquel","esther","elena","isabel","julia"
    }
    masc = {
        "juan","jose","antonio","manuel","francisco","david","javier","carlos","miguel",
        "pedro","rafael","sergio","alberto","diego","pablo","fernando","jesus","alejandro",
        "adrian","marcos","daniel","angel","andres","victor","ivan","jorge","luis"
    }

    if first in fem:
        return "Mujer"
    if first in masc:
        return "Hombre"
    if first.endswith("a"):
        return "Mujer"
    return ""


def split_perro_parentesis(perro: str) -> Tuple[str, str]:
    """
    "Maya (MST)" -> ("Maya", "MST")
    Si no hay paréntesis -> ("Maya", "")
    """
    if not perro:
        return "", ""
    s = str(perro).strip()
    m = re.match(r"^(.*?)\s*\(([^)]+)\)\s*$", s)
    if not m:
        return s, ""
    base = m.group(1).strip()
    tag = m.group(2).strip()
    return base, tag


def normalize_fecha_corta(fecha: str, year: Optional[int]) -> str:
    """
    Si Fecha ya es YYYY-MM-DD -> la devuelve.
    Si viene como "Ene 3" y tenemos year -> devuelve YYYY-MM-DD.
    Si no puede -> devuelve la original.
    """
    if not fecha:
        return ""
    s = strip_accents(str(fecha)).strip()

    if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
        return s

    if not year:
        return s

    month_map = {
        "ene": 1, "jan": 1,
        "feb": 2,
        "mar": 3,
        "abr": 4, "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "ago": 8, "aug": 8,
        "sep": 9, "set": 9,
        "oct": 10,
        "nov": 11,
        "dic": 12, "dec": 12,
    }

    m = re.match(r"^([A-Za-z]{3})\s+(\d{1,2})$", s, flags=re.I)
    if m:
        mon = month_map.get(m.group(1).lower())
        if mon:
            d = int(m.group(2))
            return f"{year:04d}-{mon:02d}-{d:02d}"

    return s


def parse_fechas_to_desde_hasta(fechas: str, year: Optional[int], fallback_fecha: Optional[str]) -> Tuple[str, str]:
    fallback_fecha = str(fallback_fecha).strip() if fallback_fecha else ""
    if not fechas:
        return (fallback_fecha, fallback_fecha)

    s = strip_accents(str(fechas)).strip()
    s = re.sub(r"\s+", " ", s)

    month_map = {
        # ES
        "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
        "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12,
        # EN
        "jan": 1, "apr": 4, "aug": 8, "dec": 12,
    }

    def iso(y: int, m: int, d: int) -> str:
        return f"{y:04d}-{m:02d}-{d:02d}"

    # A) con año explícito:
    m = re.match(r"^([A-Za-z]{3}) (\d{1,2}), (\d{4})$", s, flags=re.I)
    if m:
        mon = month_map.get(m.group(1).lower())
        if mon:
            d = int(m.group(2)); y = int(m.group(3))
            return (iso(y, mon, d), iso(y, mon, d))

    m = re.match(r"^([A-Za-z]{3}) (\d{1,2}) - (\d{1,2}), (\d{4})$", s, flags=re.I)
    if m:
        mon = month_map.get(m.group(1).lower())
        if mon:
            d1 = int(m.group(2)); d2 = int(m.group(3)); y = int(m.group(4))
            return (iso(y, mon, d1), iso(y, mon, d2))

    m = re.match(r"^([A-Za-z]{3}) (\d{1,2}) - ([A-Za-z]{3}) (\d{1,2}), (\d{4})$", s, flags=re.I)
    if m:
        mon1 = month_map.get(m.group(1).lower())
        mon2 = month_map.get(m.group(3).lower())
        if mon1 and mon2:
            d1 = int(m.group(2)); d2 = int(m.group(4)); y = int(m.group(5))
            return (iso(y, mon1, d1), iso(y, mon2, d2))

    # B) sin año:
    if not year:
        return (fallback_fecha, fallback_fecha)

    m = re.match(r"^([A-Za-z]{3}) (\d{1,2})$", s, flags=re.I)
    if m:
        mon = month_map.get(m.group(1).lower())
        if mon:
            d = int(m.group(2))
            one = iso(year, mon, d)
            return (one, one)

    m = re.match(r"^([A-Za-z]{3}) (\d{1,2}) - (\d{1,2})$", s, flags=re.I)
    if m:
        mon = month_map.get(m.group(1).lower())
        if mon:
            d1 = int(m.group(2)); d2 = int(m.group(3))
            return (iso(year, mon, d1), iso(year, mon, d2))

    m = re.match(r"^([A-Za-z]{3}) (\d{1,2}) - ([A-Za-z]{3}) (\d{1,2})$", s, flags=re.I)
    if m:
        mon1 = month_map.get(m.group(1).lower())
        mon2 = month_map.get(m.group(3).lower())
        if mon1 and mon2:
            d1 = int(m.group(2)); d2 = int(m.group(4))
            return (iso(year, mon1, d1), iso(year, mon2, d2))

    return (fallback_fecha, fallback_fecha)


def extract_first_match(text: str, options: list[str]) -> str:
    t = (text or "").upper()
    for opt in options:
        if opt.upper() in t:
            return opt
    return ""


def extract_cat_from_classificacion(text: str) -> str:
    """
    Cat se extrae priorizando:
      1) numeros: 20/30/40/50/60 (como token)
      2) tallas: XS/S/M/L/I (como token)
    Evita falsos positivos como la 'L' de 'Classificación'.
    """
    t = strip_accents(text or "")
    t_up = t.upper()

    m = re.search(r"(?<!\d)(20|30|40|50|60)(?!\d)", t_up)
    if m:
        return m.group(1)

    m = re.search(r"(^|[\s/\-])((XS|S|M|L|I))([\s/\-]|$)", t_up)
    if m:
        return m.group(2)

    return ""


def wp_transform(df_union_long: pd.DataFrame) -> pd.DataFrame:
    df = df_union_long.copy()
    df.columns = [clean_colname_strict(c) for c in df.columns]

    if "event_id" not in df.columns:
        df["event_id"] = ""

    rename_map = {
        "Guia": "Guia",
        "Perro": "Perro",
        "Club": "Club",
        "Licencia": "Lic",
        "Dorsal": "Dorsal",
        "Ag_Jp": "Ag_Jp",

        "CAL": "Calificacion",
        "VEL": "Velocidad",
        "PTS": "Puntos",
        "F": "Faltas",
        "R": "Rehuses",
        "T": "Tiempo",
        "TP": "TiempoPen",
        "CLA": "Puesto",

        "Pos": "PuestoFin",
        "General_T": "TiempoFin",
        "General_TP": "TpFin",

        "Obstaculos": "Obstaculos",
        "Longitud_m": "Longitud",
        "TiempoStandard_s": "TiempoStd",
        "TiempoMaximo_s": "TiempoMax",
        "Juez": "Juez",
        "Velocidad_ms": "SpeedLimit",

        # meta evento desde rings.json (solo meta)
        "nombre": "Evento",
        "club": "Organiza",
        "organizacion": "RSCE/RFEC",
        "lugar": "Lugar",
        "pais_bandera": "Pais",
        "fechas": "Fechas",
        "enlaces_info": "URLInfo",
        "enlaces_participantes": "URLParticipa",
        "enlaces_runs": "URLRuns",

        # ya vienen del HTML:
        "URLFuente": "URLFuente",
        "Fecha": "Fecha",
        "ring_id": "URLRings",
    }

    for k in list(rename_map.keys()):
        if k not in df.columns:
            df[k] = ""

    df = df.rename(columns=rename_map)

    # Sexo guía
    df["SexoGuia"] = df["Guia"].fillna("").astype(str).apply(infer_sexo_guia)

    # Grado / Cat / Catextra desde Classificacion
    classif = df.get("Classificacion", pd.Series([""] * len(df))).fillna("").astype(str)

    df["Grado"] = classif.apply(lambda s: extract_first_match(s, ["PRE","G1","G2","G3","INIC","PROM","COMP"]))
    df["Cat"] = classif.apply(extract_cat_from_classificacion)
    df["Catextra"] = classif.apply(lambda s: extract_first_match(s, ["ABS","MST","INF","J14","J16","SEN"]))
    # --- URLFuente fiable: el HTML viene de combined_results de un RUN ---
    
    if "RunID" in df.columns:
        runid = df["RunID"].fillna("").astype(str).str.strip()
        url_run_combined = runid.apply(lambda x: f"https://www.flowagility.com/zone/run/{x}/combined_results#list_anchor_header" if x else "")
    else:
        url_run_combined = pd.Series([""] * len(df))
    
    # Si URLFuente viene vacía del merge con rings, rellénala con la del run
    if "URLFuente" in df.columns:
        mask = df["URLFuente"].fillna("").astype(str).str.strip() == ""
        df.loc[mask, "URLFuente"] = url_run_combined[mask]
    else:
        df["URLFuente"] = url_run_combined


    # Si Cat está vacío pero el número está en Catextra, moverlo
    def extract_num_cat_from_catextra(cx: str) -> str:
        if not cx:
            return ""
        m = re.search(r"(?<!\d)(20|30|40|50|60)(?!\d)", str(cx))
        return m.group(1) if m else ""

    def remove_num_from_catextra(cx: str, num: str) -> str:
        if not cx or not num:
            return str(cx or "")
        parts = [p.strip() for p in str(cx).split("+") if p.strip()]
        parts = [p for p in parts if p != num]
        return "+".join(parts)

    cat_empty = df["Cat"].fillna("").astype(str).str.strip() == ""
    cx_series = df["Catextra"].fillna("").astype(str).str.strip()
    num_in_cx = cx_series.apply(extract_num_cat_from_catextra)

    mask_move = cat_empty & (num_in_cx != "")
    df.loc[mask_move, "Cat"] = num_in_cx[mask_move]
    df.loc[mask_move, "Catextra"] = [
        remove_num_from_catextra(cx, num) for cx, num in zip(cx_series[mask_move], num_in_cx[mask_move])
    ]

    # AÑO por fila: Fecha ISO si existe; si no, Organ_caption
    organ = df.get("Organ_caption", pd.Series([""] * len(df))).fillna("").astype(str)
    fecha = df.get("Fecha", pd.Series([""] * len(df))).fillna("").astype(str)

    df["_year"] = [
        (year_from_iso(f) or year_from_organ_caption(o) or None)
        for f, o in zip(fecha.tolist(), organ.tolist())
    ]

    # Si Fecha está vacía pero Organ_caption trae fecha completa -> ponerla en Fecha
    fecha_from_organ = organ.apply(date_iso_from_organ_caption)
    df["Fecha"] = df["Fecha"].where(df["Fecha"].astype(str).str.strip() != "", fecha_from_organ)

    # Fechas single-date tipo "Ene 3" => Desde/Hasta/Fecha = esa fecha (con year por fila)
    fechas_str = df.get("Fechas", pd.Series([""] * len(df))).fillna("").astype(str).str.strip()

    def _single_iso(row) -> str:
        y = row.get("_year")
        return normalize_fecha_corta(row.get("Fechas",""), y)

    fechas_single_iso = df.apply(_single_iso, axis=1)
    is_single_date = fechas_single_iso.astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)

    df["Desde"] = ""
    df["Hasta"] = ""

    df.loc[is_single_date, "Fecha"] = fechas_single_iso[is_single_date]
    df.loc[is_single_date, "Desde"] = fechas_single_iso[is_single_date]
    df.loc[is_single_date, "Hasta"] = fechas_single_iso[is_single_date]

    # resto: rangos
    def _desde_hasta(row) -> Tuple[str, str]:
        if bool(re.match(r"^\d{4}-\d{2}-\d{2}$", str(row.get("Desde","")).strip())):
            return (row.get("Desde",""), row.get("Hasta",""))
        y = row.get("_year")
        return parse_fechas_to_desde_hasta(row.get("Fechas",""), y, row.get("Fecha",""))

    rest_mask = ~is_single_date
    if rest_mask.any():
        dh = df.loc[rest_mask].apply(_desde_hasta, axis=1)
        df.loc[rest_mask, "Desde"] = [x[0] for x in dh]
        df.loc[rest_mask, "Hasta"] = [x[1] for x in dh]

    # si Desde/Hasta vacíos y Fecha existe => igualar
    mask_empty = (df["Desde"].astype(str).str.strip() == "") & (df["Fecha"].astype(str).str.strip() != "")
    df.loc[mask_empty, "Desde"] = df.loc[mask_empty, "Fecha"]
    df.loc[mask_empty, "Hasta"] = df.loc[mask_empty, "Fecha"]

    # Limpia Perro (quita paréntesis) y mete tag en Catextra
    perro_split = df["Perro"].fillna("").astype(str).apply(split_perro_parentesis)
    df["Perro"] = perro_split.apply(lambda t: t[0])
    perro_tag = perro_split.apply(lambda t: t[1])

    df["Catextra"] = df["Catextra"].fillna("").astype(str).str.strip()
    tag_clean = perro_tag.fillna("").astype(str).str.strip()

    def merge_catextra(existing: str, tag: str) -> str:
        if not tag:
            return existing
        if not existing:
            return tag
        parts = [p.strip() for p in existing.split("+") if p.strip()]
        if tag in parts:
            return existing
        return existing + "+" + tag

    df["Catextra"] = [merge_catextra(e, t) for e, t in zip(df["Catextra"].tolist(), tag_clean.tolist())]

    # Binomio con Perro ya limpio
    df["Binomio"] = (
        df["Guia"].fillna("").astype(str).str.strip().str.replace(" ", "_", regex=False)
        + "-"
        + df["Perro"].fillna("").astype(str).str.strip().str.replace(" ", "_", regex=False)
    )

    # URLEvento
    event_id_series = df.get("event_id", pd.Series([""] * len(df))).fillna("").astype(str)
    if "EventID" in df.columns:
        event_id_series = event_id_series.where(event_id_series.str.strip() != "", df["EventID"].fillna("").astype(str))

    df["URLEvento"] = event_id_series.apply(lambda x: f"https://www.flowagility.com/zone/events/{x}" if str(x).strip() else "")

    ordered_cols = [
        "Guia","SexoGuia","Perro","Binomio","Lic","Club","Grado","Cat","Catextra","Dorsal",
        "Ag_Jp","Calificacion","Velocidad","Puntos","Faltas","Rehuses","Tiempo","TiempoPen","Puesto",
        "PuestoFin","TiempoFin","TpFin","Obstaculos","Longitud","Juez","SpeedLimit","TiempoMax","TiempoStd",
        "Evento","Organiza","RSCE/RFEC","Lugar","Pais","Fechas","Desde","Hasta","Fecha","URLEvento",
        "URLFuente","URLRings","URLInfo","URLParticipa","URLRuns",
    ]

    for c in ordered_cols:
        if c not in df.columns:
            df[c] = ""

    df_wp = df[ordered_cols].copy()
    df_wp.columns = [strip_accents(c) for c in df_wp.columns]
    return df_wp.fillna("").replace("-", "")


# ============================================================
# Output paths
# ============================================================

def build_output_paths(out_base: str):
    p = Path(out_base)
    if p.suffix.lower() in (".xlsx", ".xlsm", ".csv"):
        p = p.with_suffix("")
    raw_xlsx = p.with_name(p.name + "_raw").with_suffix(".xlsx")
    raw_csv  = p.with_name(p.name + "_raw").with_suffix(".csv")
    long_xlsx = p.with_name(p.name + "_long").with_suffix(".xlsx")
    long_csv  = p.with_name(p.name + "_long").with_suffix(".csv")
    union_long_xlsx = p.with_name(p.name + "_union_meta_long").with_suffix(".xlsx")
    union_long_csv  = p.with_name(p.name + "_union_meta_long").with_suffix(".csv")
    wp_xlsx = p.with_name(p.name + "_wp").with_suffix(".xlsx")
    wp_csv  = p.with_name(p.name + "_wp").with_suffix(".csv")
    return raw_xlsx, raw_csv, long_xlsx, long_csv, union_long_xlsx, union_long_csv, wp_xlsx, wp_csv


# ============================================================
# Main
# ============================================================

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-o", "--output",
        default="combined_results_con_cabecera",
        help="Base de salida (sin extensión). Ej: 'salida' -> *_raw *_long *_union_meta_long *_wp"
    )
    args = ap.parse_args()

    in_paths = collect_inputs()
    if not in_paths:
        raise SystemExit(
            "No se han encontrado HTMLs.\n"
            f"- Carpeta preferente no existe o está vacía: {PREFERRED_FOLDER}\n"
            "- Y FALLBACK_HTML_FILES no tiene rutas válidas."
        )

    dfs = []
    for p in in_paths:
        try:
            df = parse_file(p)
            if not df.empty:
                dfs.append(df)
        except Exception as e:
            print(f"⚠️  Error parseando {p.name}: {e}")

    if not dfs:
        raise SystemExit("No se pudo extraer ninguna fila de los HTMLs.")

    df_all = pd.concat(dfs, ignore_index=True, sort=False).fillna("")
    df_all.columns = [clean_colname_strict(c) for c in df_all.columns]

    # DEDUPE RAW (solo difiere FuenteHTML)
    before_raw = len(df_all)
    df_all = dedupe_keep_most_data(df_all, ignore_cols={"FuenteHTML"})
    after_raw = len(df_all)

    raw_xlsx, raw_csv, long_xlsx, long_csv, union_long_xlsx, union_long_csv, wp_xlsx, wp_csv = build_output_paths(args.output)
    raw_xlsx.parent.mkdir(parents=True, exist_ok=True)

    # Guardar RAW
    df_all.to_csv(raw_csv, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(raw_xlsx, engine="openpyxl") as writer:
        df_all.to_excel(writer, index=False, sheet_name="RAW")

    # LONG
    df_raw_reloaded = pd.read_csv(raw_csv, dtype=str, keep_default_na=False)
    df_long = transpose_prefixes(df_raw_reloaded)

    # DEDUPE LONG (solo difiere FuenteHTML)
    before_long = len(df_long)
    df_long = dedupe_keep_most_data(df_long, ignore_cols={"FuenteHTML"})
    after_long = len(df_long)

    df_long.to_csv(long_csv, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(long_xlsx, engine="openpyxl") as writer:
        df_long.to_excel(writer, index=False, sheet_name="LONG")

    # UNION con META de evento (NO ring/date/url)
    meta_df = load_event_meta_from_rings_json()
    if meta_df.empty:
        print("⚠️  rings.json no cargado -> no se puede generar UNION ni WP.")
        return 0

    df_union_long = make_union_with_event_meta(df_long, meta_df)
    df_union_long.to_csv(union_long_csv, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(union_long_xlsx, engine="openpyxl") as writer:
        df_union_long.to_excel(writer, index=False, sheet_name="UNION_META_LONG")

    # OUTPUT WP
    df_wp = wp_transform(df_union_long)
    df_wp.to_csv(wp_csv, index=False, encoding="utf-8-sig")
    with pd.ExcelWriter(wp_xlsx, engine="openpyxl") as writer:
        df_wp.to_excel(writer, index=False, sheet_name="WP")

    print(f"✅ OK: HTMLs: {len(in_paths)}")
    print(f"   RAW : {before_raw} -> {after_raw} filas (dedupe -{before_raw-after_raw})  -> {raw_csv} / {raw_xlsx}")
    print(f"   LONG: {before_long} -> {after_long} filas (dedupe -{before_long-after_long}) -> {long_csv} / {long_xlsx}")
    print(f"   UNION_META_LONG -> {union_long_csv} / {union_long_xlsx}")
    print(f"   WP             -> {wp_csv} / {wp_xlsx}")

    # ============================================================
    # RESUMEN: registros por año (WP)
    # ============================================================
    def _year_from_iso_local(s: str) -> str:
        s = str(s or "").strip()
        m = re.match(r"^(20\d{2})-\d{2}-\d{2}$", s)
        return m.group(1) if m else ""

    fecha_year = df_wp["Fecha"].apply(_year_from_iso_local) if "Fecha" in df_wp.columns else pd.Series([""] * len(df_wp))
    desde_year = df_wp["Desde"].apply(_year_from_iso_local) if "Desde" in df_wp.columns else pd.Series([""] * len(df_wp))

    year_final = fecha_year.where(fecha_year != "", desde_year)
    year_final = year_final.replace("", "SIN_AÑO")

    resumen = year_final.value_counts(dropna=False).sort_index()

    print("\n📌 RESUMEN: registros por año (según Fecha, si no Desde)")
    for y, n in resumen.items():
        print(f"  - {y}: {n}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    
    
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
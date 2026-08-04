import sys
import os
import subprocess
import time
from datetime import datetime
import shutil

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class FakeColor:
        def __getattr__(self, name):
            return ""
    Fore = FakeColor()
    Style = FakeColor()

# =====================================================================
# CONFIGURACIÓN DE FECHAS
# Estas fechas se aplicarán en el primer paso (1EventosPast_URLs_json.py)
# =====================================================================
# Formato: "YYYY-MM-DD" o cadena vacía "" para desactivar el límite
FECHA_INICIO = "2026-01-01"  # No buscará eventos anteriores a esta fecha
FECHA_FIN    = "2026-09-01"  # No guardará eventos posteriores a esta fecha
# =====================================================================

def imprimir_titulo(texto):
    print(f"\n{Fore.CYAN}{'=' * 80}")
    print(f"{Fore.CYAN}{texto.center(80)}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")

def ejecutar_script(nombre_script):
    print(f"{Fore.YELLOW}[{datetime.now().strftime('%H:%M:%S')}] Iniciando ejecución de: {Fore.WHITE}{nombre_script}{Style.RESET_ALL}")
    
    inicio = time.time()
    
    try:
        # Ejecuta el script usando el mismo ejecutable de python actual
        # y espera a que termine
        resultado = subprocess.run(
            [sys.executable, nombre_script],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=True
        )
        
        tiempo_total = time.time() - inicio
        minutos, segundos = divmod(tiempo_total, 60)
        
        print(f"\n{Fore.GREEN}✓ ÉXITO:{Style.RESET_ALL} {nombre_script} completado en {int(minutos)}m {segundos:.1f}s.\n")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n{Fore.RED}❌ ERROR:{Style.RESET_ALL} El script {nombre_script} falló con código de salida {e.returncode}.")
        print(f"{Fore.RED}El proceso orquestador ha sido detenido para que puedas revisar el error.{Style.RESET_ALL}\n")
        return False
    except FileNotFoundError:
        print(f"\n{Fore.RED}❌ ERROR:{Style.RESET_ALL} No se pudo encontrar el archivo {nombre_script}. Verifica el nombre.\n")
        return False

def main():
    imprimir_titulo("INICIO DEL ORQUESTADOR FLOWAGILITY")
    
    # Eliminar la carpeta prints_html si existe antes de empezar
    carpeta_prints = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prints_html")
    if os.path.exists(carpeta_prints):
        print(f"{Fore.YELLOW}Limpieza: Eliminando carpeta antigua '{carpeta_prints}'...{Style.RESET_ALL}")
        try:
            shutil.rmtree(carpeta_prints)
            print(f"{Fore.GREEN}✓ Carpeta 'prints_html' eliminada correctamente.{Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}❌ Error al eliminar la carpeta 'prints_html': {e}{Style.RESET_ALL}\n")
    
    # Inyectar las variables de entorno para que el script 1 las pueda leer
    os.environ["ORQUESTADOR_FECHA_INICIO"] = FECHA_INICIO
    os.environ["ORQUESTADOR_FECHA_FIN"] = FECHA_FIN
    
    print(f"{Fore.MAGENTA}Configuración activa:{Style.RESET_ALL}")
    print(f"  - Fecha de Inicio: {FECHA_INICIO if FECHA_INICIO else 'Sin límite'}")
    print(f"  - Fecha de Fin:    {FECHA_FIN if FECHA_FIN else 'Sin límite'}\n")

    # Lista de los scripts a ejecutar en orden
    scripts = [
        "1EventosPast_URLs_json.py",
        "2CaptaURLScompeticion.py",
        "3ExtraeHTML.py",
        "4Extraedata_del_HTML_a_Excel v2.py"
    ]
    
    tiempo_orquestador_inicio = time.time()
    
    for i, script in enumerate(scripts):
        exito = ejecutar_script(script)
        if not exito:
            # Si falla uno, detenemos toda la ejecución para no generar archivos corruptos
            sys.exit(1)
        
        # Pausa de limpieza entre scripts de Selenium (2 -> 3) en entornos Linux/CI
        # para garantizar que el runner libera RAM y descriptores de fichero
        if script == "2CaptaURLScompeticion.py" and sys.platform != "win32":
            import platform
            if platform.system() == "Linux":
                print(f"\n⏳ Pausa de 15s para liberar recursos del runner antes del script 3...\n")
                os.system("pkill -9 chrome; pkill -9 chromedriver; sync")
                time.sleep(15)
            
    tiempo_total = time.time() - tiempo_orquestador_inicio
    minutos, segundos = divmod(tiempo_total, 60)
    horas, minutos = divmod(minutos, 60)
    
    imprimir_titulo(f"🎉 TODOS LOS SCRIPTS EJECUTADOS CON ÉXITO 🎉")
    print(f"{Fore.GREEN}Tiempo total de ejecución:{Style.RESET_ALL} {int(horas)}h {int(minutos)}m {segundos:.1f}s")
    
    try:
        try:
            import winsound
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except ImportError:
            pass
    except Exception:
        pass

if __name__ == "__main__":
    main()

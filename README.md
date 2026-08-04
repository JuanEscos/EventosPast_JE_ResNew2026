# Orquestador FlowAgility - Extractor de Eventos

Este repositorio contiene un pipeline automatizado para la extracción, procesamiento y exportación a Excel de datos y resultados de competiciones desde la plataforma web de FlowAgility. 

El proyecto está diseñado para ejecutarse de forma secuencial y está preparado para integrarse en entornos de integración continua (CI) como **GitHub Actions**, utilizando navegadores web en modo *headless* (tanto con Playwright como con Selenium).

## 🚀 Arquitectura del Pipeline

El flujo de trabajo se divide en 4 scripts principales que se ejecutan en cadena a través de un orquestador central:

1. **`1EventosPast_URLs_json.py`**
   - Utiliza **Playwright** para navegar por el histórico de eventos de FlowAgility.
   - Extrae las URLs base y la información preliminar en formato JSON.

2. **`2CaptaURLScompeticion.py`**
   - Utiliza **Selenium** para navegar dentro de cada evento y competición.
   - Captura las URLs exactas de cada pista (rings) y de cada manga (runs), guardando la información estructurada necesaria para la posterior descarga de datos.

3. **`3ExtraeHTML.py`**
   - Utiliza **Selenium** en modo *headless* robusto (optimizado para evitar cuelgues de memoria en servidores Linux/CI).
   - Visita las URLs recopiladas en el paso anterior y extrae el código HTML crudo que contiene las clasificaciones y resultados.

4. **`4Extraedata_del_HTML_a_Excel v2.py`**
   - Procesa los archivos HTML descargados utilizando **BeautifulSoup4**.
   - Analiza las tablas de resultados, tiempos, penalizaciones y clasificaciones.
   - Exporta todos los datos estructurados y limpios a un archivo **Excel** (.xlsx).

* **`main_orquestador.py`**
   - Es el script central que coordina la ejecución secuencial de los 4 scripts anteriores.
   - Gestiona el manejo de errores, variables de estado y proporciona retroalimentación (logs/sonidos locales) sobre el estado general del proceso.

## 🛠️ Requisitos e Instalación

Para ejecutar este proyecto en local, necesitas **Python 3.10+**. 

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JuanEscos/EventosPast_JE_ResNew2026.git
   cd EventosPast_JE_ResNew2026
   ```

2. Instala las dependencias de Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Instala los navegadores necesarios para Playwright:
   ```bash
   playwright install chromium
   ```

## ⚙️ Configuración y Variables de Entorno

El sistema requiere credenciales válidas de FlowAgility para poder acceder a los datos de las competiciones. Estas credenciales deben proveerse mediante variables de entorno o mediante un archivo `.env` en la raíz del proyecto (o dentro de la carpeta `scripts/`).

Crea un archivo `.env` con el siguiente contenido:

```env
FLOW_EMAIL=tu_correo@ejemplo.com
FLOW_PASS=tu_contraseña_segura
```

> ⚠️ **Importante:** En GitHub Actions, asegúrate de configurar `FLOW_EMAIL` y `FLOW_PASS` como *Repository Secrets*.

## 🏃‍♂️ Ejecución

Para iniciar todo el proceso de extracción, simplemente ejecuta el orquestador desde la carpeta `scripts`:

```bash
cd scripts
python main_orquestador.py
```

### Ejecución en GitHub Actions (CI)
El repositorio está preparado para ejecutarse automáticamente mediante un flujo de trabajo (Workflow) de GitHub Actions en un entorno Ubuntu. El pipeline maneja automáticamente la creación de procesos en segundo plano de Google Chrome y su correcta limpieza (pkill) para asegurar una ejecución estable sin interfaz gráfica.

---
*Desarrollado para la automatización de resultados de Agility.*

from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
pipeline = (ROOT / ".github" / "workflows" / "ejecucion_scraping.yml").read_text(encoding="utf-8")
watchdog_path = ROOT / ".github" / "workflows" / "monitor_ejecucion_scraping.yml"

assert "aniadir_resultados_por_prueba_para_WP_a_JE_ResNew2026.php" not in pipeline, (
    "El pipeline todavía llama al importador retirado de JE_ResNew2026"
)
assert watchdog_path.is_file(), "Falta el watchdog semanal del workflow"
watchdog = watchdog_path.read_text(encoding="utf-8")

required = [
    "0 7 * * 3",
    "0 8 * * 3",
    'ZoneInfo("Europe/Madrid")',
    "ejecucion_scraping.yml/runs?status=completed&per_page=1",
    "conclusion",
    "failed = False",
    "--connect-timeout 10",
    "--max-time 30",
    "--retry 2",
    "CURL_STATUS",
    'conclusion = "error del monitor"',
    "continue-on-error: true",
    "steps.check.outcome == 'failure'",
    "dawidd6/action-send-mail@4226df7daafa6fc901a43789c49bf7ab309066e7",
    "jescosq@gmail.com",
    "steps.check.outputs.failed == 'true'",
]
missing = [fragment for fragment in required if fragment not in watchdog]
assert not missing, f"Watchdog semanal incompleto: {missing}"
assert "Authorization: Bearer" not in watchdog
assert "GH_TOKEN" not in watchdog

# En verano, 07:00 UTC son las 09:00 de Madrid; en invierno lo son las 08:00 UTC.
madrid = ZoneInfo("Europe/Madrid")
assert datetime(2026, 7, 1, 7, tzinfo=timezone.utc).astimezone(madrid).hour == 9
assert datetime(2026, 7, 1, 8, tzinfo=timezone.utc).astimezone(madrid).hour != 9
assert datetime(2026, 1, 7, 8, tzinfo=timezone.utc).astimezone(madrid).hour == 9
assert datetime(2026, 1, 7, 7, tzinfo=timezone.utc).astimezone(madrid).hour != 9

print("WORKFLOW_WEEKLY_FAILURE_MONITOR=PASSED")

from pathlib import Path


workflow = (Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'ejecucion_scraping.yml').read_text(encoding='utf-8')

required = [
    "grep -Eiq 'fatal error|mysqli_sql_exception|duplicate entry|^ERROR:'",
    'Filas con error: 0',
    'El importador PHP devolvió un error aunque HTTP fuese 200',
]
missing = [fragment for fragment in required if fragment not in workflow]
assert not missing, f'El workflow no distingue un resumen limpio de un error PHP: {missing}'

# Regression: successful summary contains "Filas con error: 0". It must not fail.
successful_summary = '''\
=== RESUMEN IMPORTACIÓN ===
Filas insertadas nuevas: 0
Filas saltadas (duplicado): 14841
Filas con error: 0
'''
error_pattern = 'fatal error|mysqli_sql_exception|duplicate entry|^ERROR:'
import re
assert not re.search(error_pattern, successful_summary, flags=re.IGNORECASE | re.MULTILINE)

fatal_summary = 'Fatal error: Uncaught mysqli_sql_exception: Duplicate entry'
assert re.search(error_pattern, fatal_summary, flags=re.IGNORECASE | re.MULTILINE)
print('WORKFLOW_IMPORT_RESPONSE_POLICY=PASSED')

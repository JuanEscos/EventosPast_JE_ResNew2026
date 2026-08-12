from pathlib import Path


workflow = (Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'ejecucion_scraping.yml').read_text(encoding='utf-8')

required = [
    'grep -Eiq',
    'fatal error',
    'mysqli_sql_exception',
    'duplicate entry',
    'el importador php devolvió un error aunque http fuese 200',
]
missing = [fragment for fragment in required if fragment.lower() not in workflow.lower()]
assert not missing, f'El workflow no convierte los errores PHP en fallo: {missing}'

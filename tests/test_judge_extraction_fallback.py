import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / '4Extraedata_del_HTML_a_Excel v2.py'
spec = importlib.util.spec_from_file_location('flow_extractor', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_extracts_judge_when_run_metadata_is_not_in_three_column_grid():
    soup = module.BeautifulSoup('''
        <div class="run-card">JP1 · Obstáculos: 18 · Longitud: 180 m ·
        Tiempo Standard: 50 s · Tiempo Máximo: 75 s · Juez: Seppo Savikko · Velocidad: 3.60 m/s</div>
        <div class="run-card">AG · Obstáculos: 20 · Longitud: 200 m ·
        Tiempo Standard: 55 s · Tiempo Máximo: 82 s · Juez: Jan Egil Eide · Velocidad: 3.64 m/s</div>
    ''', 'html.parser')

    meta = module.extract_run_meta(soup)

    assert meta['JP1']['Juez'] == 'Seppo Savikko'
    assert meta['AG']['Juez'] == 'Jan Egil Eide'

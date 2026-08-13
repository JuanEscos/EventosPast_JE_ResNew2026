import importlib.util
from pathlib import Path

script = Path(__file__).resolve().parents[1] / "scripts" / "4Extraedata_del_HTML_a_Excel v2.py"
spec = importlib.util.spec_from_file_location("flow_extractor", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_extracts_judge_from_current_english_flowagility_print_layout():
    soup = module.BeautifulSoup("""
        <div class="grid grid-cols-3 table-text">
          <div>AG Obstacles: 20 Length: 208 m</div>
          <div>Standard Time: 44 s Maximum Time: 84 s</div>
          <div>Judge: Seppo Savikko Speed: 4.73 m/s</div>
          <div>JP Obstacles: 20 Length: 222 m</div>
          <div>Standard Time: 43 s Maximum Time: 74 s</div>
          <div>Judge: Jan Egil Eide Speed: 5.16 m/s</div>
        </div>
    """, "html.parser")

    meta = module.extract_run_meta(soup)

    assert meta["AG"]["Juez"] == "Seppo Savikko"
    assert meta["JP"]["Juez"] == "Jan Egil Eide"

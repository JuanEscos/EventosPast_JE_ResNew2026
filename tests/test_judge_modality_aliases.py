import importlib.util
from pathlib import Path

script = Path(__file__).resolve().parents[1] / "scripts" / "4Extraedata_del_HTML_a_Excel v2.py"
spec = importlib.util.spec_from_file_location("flow_extractor", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_maps_generic_jp_metadata_to_single_numbered_jumping_result():
    meta = {"JP": {"Juez": "Jan Egil Eide"}, "AG": {"Juez": "Seppo Savikko"}}

    resolved = module.resolve_run_metadata_for_results(meta, {"JP1", "AG"})

    assert resolved["JP1"]["Juez"] == "Jan Egil Eide"
    assert resolved["AG"]["Juez"] == "Seppo Savikko"


def test_does_not_copy_generic_jp_to_two_numbered_jumpings():
    meta = {"JP": {"Juez": "Jan Egil Eide"}}

    resolved = module.resolve_run_metadata_for_results(meta, {"JP1", "JP2"})

    assert "JP1" not in resolved
    assert "JP2" not in resolved

from pathlib import Path

workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ejecucion_scraping.yml").read_text(encoding="utf-8")

assert "Diagnóstico RIALP: HTML y CSV" in workflow
assert "actions/upload-artifact@v4" in workflow
assert "find scripts/Results/prints_html -type f -name '*_5ce8b9b7-e68b-4d16-bc4b-c9e82d9e718d_*_combined_results.html'" in workflow
assert "scripts/combined_results_con_cabecera_wp.csv" in workflow

print("WORKFLOW_RIALP_DIAGNOSTIC_ARTIFACT=PASSED")

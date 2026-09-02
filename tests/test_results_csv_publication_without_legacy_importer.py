from pathlib import Path

workflow = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "ejecucion_scraping.yml"
).read_text(encoding="utf-8")

# La actualización de jueces forma parte del CSV generado. Ya no debe depender
# de un importador PHP temporal ni de la tabla retirada JE_ResNew2026.
assert "combined_results_con_cabecera_wp.csv" in workflow
assert "git push" in workflow
assert "importer-live-latest.php" not in workflow
assert "aniadir_resultados_por_prueba_para_WP_a_JE_ResNew2026.php" not in workflow

print("RESULTS_CSV_PUBLICATION_WITHOUT_LEGACY_IMPORTER=PASSED")

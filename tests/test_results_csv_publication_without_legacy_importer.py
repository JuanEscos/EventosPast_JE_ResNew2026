from pathlib import Path

def workflow_text() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "workflows"
        / "ejecucion_scraping.yml"
    ).read_text(encoding="utf-8")

# El CSV publicado debe cargarse en la tabla canónica que consumen las páginas
# de resultados. Un commit correcto sin esta importación deja producción obsoleta.
def test_published_csv_is_imported_into_flowdata_with_digest_verification():
    workflow = workflow_text()
    assert "combined_results_con_cabecera_wp.csv" in workflow
    assert "git push" in workflow
    assert "importer-live-latest.php" not in workflow
    assert "aniadir_resultados_por_prueba_para_WP_a_JE_FlowData2026.php" in workflow
    assert "IMPORT_TOKEN" in workflow
    assert "CURL_STATUS" in workflow
    assert "HTTP_STATUS" in workflow
    assert "EXPECTED_CSV_SHA256=$(sha256sum" in workflow
    assert "expected_sha256=${EXPECTED_CSV_SHA256}" in workflow
    assert "CSV SHA-256 confirmado: ${EXPECTED_CSV_SHA256}" in workflow
    assert "JE_ResNew2026 fue retirada" not in workflow


def test_import_response_validation_is_fail_closed():
    workflow = workflow_text()
    assert "grep -Eiq" in workflow
    assert "^[[:space:]]*(fatal error|error|warning|mysqli_sql_exception)" in workflow
    assert "^[[:space:]]*Filas con error:[[:space:]]*[1-9][0-9]*[[:space:]]*$" in workflow
    assert "^[[:space:]]*Filas con error:[[:space:]]*0[[:space:]]*$" in workflow

from pathlib import Path

def workflow_text() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "workflows"
        / "ejecucion_scraping.yml"
    ).read_text(encoding="utf-8")

def test_import_failure_marks_pipeline_failed_and_keeps_alerting():
    workflow = workflow_text()
    assert "aniadir_resultados_por_prueba_para_WP_a_JE_FlowData2026.php" in workflow
    assert "JE_FlowData2026" in workflow
    assert "JE_ResNew2026 fue retirada" not in workflow
    assert "- name: Enviar email si falla el pipeline" in workflow
    assert "if: failure()" in workflow
    assert "dawidd6/action-send-mail@4226df7daafa6fc901a43789c49bf7ab309066e7" in workflow
    assert "❌ FlowAgility – ERROR en el pipeline" in workflow
    assert "jescosq@gmail.com" in workflow

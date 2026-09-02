from pathlib import Path

workflow = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "workflows"
    / "ejecucion_scraping.yml"
).read_text(encoding="utf-8")

assert "aniadir_resultados_por_prueba_para_WP_a_JE_ResNew2026.php" not in workflow
assert "JE_ResNew2026 fue retirada" in workflow
assert "flow_db.php y JE_FlowData2025/2026" in workflow
assert "- name: Enviar email si falla el pipeline" in workflow
assert "if: failure()" in workflow
assert "dawidd6/action-send-mail@4226df7daafa6fc901a43789c49bf7ab309066e7" in workflow
assert "❌ FlowAgility – ERROR en el pipeline" in workflow
assert "jescosq@gmail.com" in workflow

print("WORKFLOW_FAILURE_ALERT_POLICY=PASSED")

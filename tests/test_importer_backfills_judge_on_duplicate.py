from pathlib import Path

importer = Path(r"C:\Users\Juan\AppData\Local\Temp\importer-live-latest.php").read_text(encoding="utf-8")

assert "$updatedJudgeCount" in importer
assert "UPDATE {$tableEsc} SET `Juez`=" in importer
assert "TRIM(COALESCE(`Juez`, '')) = ''" in importer
assert "Filas con juez actualizado" in importer

print("IMPORTER_DUPLICATE_JUDGE_BACKFILL=PASSED")

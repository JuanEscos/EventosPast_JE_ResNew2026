import ast
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "main_orquestador.py"
)


def assigned_constant(name: str):
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id == name:
            return ast.literal_eval(node.value)
    raise AssertionError(f"No se encontró la asignación {name}")


# La página de eventos pasados ya excluye el futuro. Un tope superior fijo
# caduca y hace que los nuevos fines de semana se descarten silenciosamente.
def test_orchestrator_has_no_fixed_end_date():
    assert assigned_constant("FECHA_FIN") == ""


if __name__ == "__main__":
    test_orchestrator_has_no_fixed_end_date()
    print("PASS: el orquestador no tiene una fecha final fija")

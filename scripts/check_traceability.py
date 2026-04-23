"""
check_traceability.py

Valida invariantes de la matriz de trazabilidad:
  - Todo hazard en 01_hazard_register tiene ≥1 fila en 05_traceability_matrix.csv
  - Todo SR en 02_safety_requirements tiene ≥1 fila
  - Todo cage rule en 03_cage_specification tiene ≥1 fila
  - Todo scenario en 04_scenario_library tiene ≥1 fila
  - No hay referencias a IDs inexistentes
  - conclusion está en el set permitido

Exit code:
  0 si todo OK
  1 si hay huérfanos o referencias rotas

Uso:
  python scripts/check_traceability.py

Integración:
  Correr en pre-commit, CI, y al final de cada día de trabajo.
"""

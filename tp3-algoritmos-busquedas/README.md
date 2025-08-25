# TP3 - Algoritmos de Búsqueda

Este directorio contiene la implementación de un agente basado en objetivos para el entorno Frozen Lake.

## Estructura
- `code/`: módulos con utilidades de entorno, algoritmos de búsqueda y script de experimentos.
- `results.csv`: archivo generado automáticamente con las métricas de las corridas.
- `tp3-reporte.md`: breve informe del trabajo.

## Ejecución
1. Posicionarse en la raíz del repositorio y ejecutar:
   ```bash
   python tp3-algoritmos-busquedas/code/run_experiments.py
   ```
2. Al finalizar, los resultados de 30 entornos aleatorios (100x100, probabilidad 0.92 de celdas transitables) se guardarán en `tp3-algoritmos-busquedas/results.csv`.

No se generan imágenes; todas las métricas pueden analizarse desde el archivo CSV.

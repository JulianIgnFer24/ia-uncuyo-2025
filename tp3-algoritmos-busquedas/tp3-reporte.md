# TP3 - Algoritmos de Búsqueda

Este informe resume resultados y hallazgos sobre los algoritmos solicitados (RANDOM, BFS, DFS, DLS 50/75/100, UCS, A*) evaluados en entornos FrozenLake aleatorios de 100×100 con p(F)=0.92 y “vida”=1000. Se ejecutaron 30 entornos y todos los algoritmos se evaluaron sobre los mismos mapas en dos escenarios de costo: escenario 1 (todas las acciones valen 1) y escenario 2 (L/R=1; U/D=10).

Datos: `tp3-algoritmos-busquedas/results.csv`
Imágenes: `tp3-algoritmos-busquedas/images`

## Interpretación de gráficos

- Boxplots por algoritmo (por escenario):
  - `tp3-algoritmos-busquedas/images/boxplot_time_por_algoritmo.png`: A* y UCS presentan distribuciones más concentradas (tiempos menores y menos dispersión) que DFS y RANDOM.
  - `tp3-algoritmos-busquedas/images/boxplot_states_por_algoritmo.png`: A* requiere menos estados en el escenario 2 ya que tiene en cuenta la funcion de costo, BFS y DFS siempre visita la misma cantidad de estados en ambos escenarios intermedio/alto, RANDOM como gana pocas veces, las veces que gana visita pocos estados porque pierde antes de poder explorar otros.
  - `tp3-algoritmos-busquedas/images/boxplot_actions_count_solo_soluciones.png`: RANDOM puede aparecer “por encima de todos” en escenario 1 porque solo hay muy pocos éxitos y sus trayectorias son largas y en el escenario 2 directamente no aparece porque no gana nunca; BFS/UCS/A* suelen dar planes cortos (óptimos en pasos).




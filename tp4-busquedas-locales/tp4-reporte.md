# TP4 – Búsquedas locales – N-Reinas


## Algoritmos implementados

- Hill Climbing (hill_climbing)

    Técnica: descenso empinado (steepest-ascent) sobre vecinos generados moviendo una reina a otra fila de la misma columna (neighbor_move), buscando siempre el mejor H disponible

    Métrica: h_conflicts se usa como función objetivo para contar pares de reinas en conflicto

- Simulated Annealing (simulated_annealing)

    Técnica: búsqueda probabilística con enfriamiento geométrico T_k = T0·α^k; acepta movimientos peores con probabilidad exp(-Δ/T) usando vecinos aleatorios (random_neighbor)

    Parámetros: n, max_states, seed, más T0 (temperatura inicial), alpha (factor de enfriamiento por paso), Tmin (temperatura mínima), record_history para registrar H. La iteración se detiene cuando H=0, se agota max_states, o la temperatura cae por debajo de Tmin

- Algoritmo Genético (genetic_algorithm)

    Técnica: población de permutaciones con selección por torneo, cruce PMX (Partially Matched Crossover) y mutación por intercambio de posiciones

- Búsqueda Aleatoria (random_search)

    Técnica: caminata aleatoria sobre vecinos: arranca con una permutación aleatoria y cada paso toma un vecino uniforme, manteniendo el mejor H visto; detiene al alcanzar H=0 o agotar max_states


## Parámetros experimentales

- Tamaños: N = 4, 8, 10.
- Repeticiones: 30 semillas (`env_n = 0..29`).
- Límite de estados: el mismo para todos los algoritmos (ver CSV).
- Medidas registradas por corrida: `algorithm_name`, `env_n`, `size`, `best_solution`, `H`, `states`, `time`.

## Resultados (resumen)

La tabla completa de corridas se encuentra en `tp4-busquedas-locales/tp4-Nreinas.csv`.

Se incluyen boxplots por tamaño y algoritmo en `tp4-busquedas-locales/images/`:

- `boxplot_H_N{size}.png`: distribución de `H` final.
- `boxplot_time_N{size}.png`: tiempos de ejecución.

Evolución de `H()` a lo largo de las iteraciones (una ejecución por algoritmo y tamaño), también en `images/`:

Observaciones típicas esperadas:

- Random rara vez alcanza `H=0` para N≥8 dentro de un presupuesto moderado; distribuciones de `H` altas.
- HC es rápido, pero puede atascarse en óptimos locales/mesetas; performance sensible a la inicialización.
- SA mejora sobre HC al escapar de óptimos locales, con más estados/tiempo; mejores tasas de éxito en N=8,10.
- GA tiende a lograr mayores tasas de óptimo con más evaluaciones; sensible a tamaños de población y tasas de cruce/mutación.

## Conclusión

En este problema, con el presupuesto de estados fijado, los mejores resultados suelen ser SA o GA:



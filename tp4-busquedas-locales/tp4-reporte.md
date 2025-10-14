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

## Resultados

### Para N=4
Para instancias pequeñas, todos los algoritmos logran encontrar soluciones óptimas (H=0) con alta frecuencia.
El tiempo de ejecución es extremadamente bajo en todos los casos, con diferencias apenas perceptibles.
Aun así, se observa que GA y HC son los más rápidos, seguidos de SA y Random, que muestran una dispersión ligeramente mayor debido a su naturaleza estocástica.
![box_H_N4.png](https://raw.githubusercontent.com/bucketio/img11/main/2025/10/14/1760468233020-97db5b97-5d54-40be-833e-5430e5e334d3.png 'box_H_N4.png')
![box_time_success_N4.png](https://raw.githubusercontent.com/bucketio/img13/main/2025/10/14/1760468245711-98d7508f-15e3-4b53-bcfc-cea34a8b79b3.png 'box_time_success_N4.png')


### Para N=8
A medida que aumenta el tamaño, la diferencia entre algoritmos se hace más notoria.
En el gráfico de tiempos, HC y SA siguen siendo los más eficientes, mientras que Random presenta una alta variabilidad y GA mantiene tiempos intermedios y estables.
![box_H_N8.png](https://raw.githubusercontent.com/bucketio/img3/main/2025/10/14/1760468236907-f42389e7-c80c-4429-8bac-046219659cd6.png 'box_H_N8.png')
![box_time_success_N8.png](https://raw.githubusercontent.com/bucketio/img11/main/2025/10/14/1760468247130-0ee61bcd-6baf-410a-a6c0-aeb4524bf9ee.png 'box_time_success_N8.png')


### Para N=10

En los tiempos, HC y SA siguen mostrando ejecuciones rápidas y consistentes, mientras que GA presenta una mayor dispersión debido al procesamiento poblacional.
Random no logra encontrar ninguna solución exitosa, como se indica con “0 éxitos”.

![box_H_N10.png](https://raw.githubusercontent.com/bucketio/img2/main/2025/10/14/1760468242447-ef14a198-2d43-47b0-9ad9-948284cabb8d.png 'box_H_N10.png')
![box_time_success_N10.png](https://raw.githubusercontent.com/bucketio/img12/main/2025/10/14/1760468248389-d81be1f6-1df0-473c-b375-2c953b4d3fe7.png 'box_time_success_N10.png')



## Conclusión

En este problema, con el presupuesto de estados fijado, los mejores resultados suelen ser SA o GA:



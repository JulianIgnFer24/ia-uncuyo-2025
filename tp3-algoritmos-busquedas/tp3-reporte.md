# TP3 – Algoritmos de Búsqueda

Este informe presenta el análisis comparativo de diversos algoritmos de búsqueda —**RANDOM**, **BFS**, **DFS**, **DLS (50/75/100)**, **UCS** y **A\***— evaluados sobre entornos **FrozenLake** aleatorios de tamaño **100×100**, con una probabilidad de congelamiento **p(F) = 0.92** y un límite de “vida” de **1000 pasos**.  
Se generaron **30 entornos distintos**, manteniendo los mismos mapas para todos los algoritmos, bajo dos configuraciones de costo:

- **Escenario 1:** todas las acciones tienen el mismo costo (=1).  
- **Escenario 2:** movimientos horizontales (izquierda/derecha) cuestan 1, y movimientos verticales (arriba/abajo) cuestan 10.

**Datos:** `tp3-algoritmos-busquedas/results.csv`  
**Imágenes:** `tp3-algoritmos-busquedas/images`


## Interpretación de resultados

### Tiempos de ejecución  
 
Los algoritmos **A\*** y **UCS** presentan **tiempos mayores en promedio** debido a que logran **completar planes exitosos**, explorando más a fondo el entorno hasta alcanzar la meta.  
En contraste, algoritmos **no guiados** como **DFS**, **BFS** o **RANDOM** suelen **terminar más rápido**, ya que muchas de sus ejecuciones **fallan antes de completar el recorrido**.  

![boxplot_time_por_algoritmo.png](https://raw.githubusercontent.com/bucketio/img18/main/2025/10/14/1760469328841-c1ccb49e-662a-4b15-a71d-36d85684dce7.png 'boxplot_time_por_algoritmo.png')



###  Estados explorados  

En el **escenario 2**, el algoritmo **A\*** explora **menos estados** que en el escenario 1, ya que su heurística ponderada tiene en cuenta el costo de las acciones, dirigiendo la búsqueda de forma más inteligente.  
**BFS** y **DFS** mantienen cantidades de estados similares entre escenarios, al no incorporar información de costo.  
**RANDOM**, al lograr pocas soluciones, muestra pocos estados explorados en los casos exitosos, debido a que generalmente falla antes de poder recorrer mayores regiones del mapa.

![boxplot_states_por_algoritmo.png](https://raw.githubusercontent.com/bucketio/img18/main/2025/10/14/1760469324660-da9240b9-f4d6-474c-a827-5190819cd814.png 'boxplot_states_por_algoritmo.png')

### Longitud del plan (solo soluciones)  
**RANDOM** aparece con trayectorias más largas en el escenario 1, reflejando la falta de guía en su búsqueda, en el escenario 2 no figura, ya que no logra soluciones.  
Los algoritmos **BFS**, **UCS** y **A\*** generan planes **más cortos y consistentes**, alcanzando soluciones óptimas o cercanas al óptimo en cantidad de pasos.  
Esto demuestra la superioridad de las estrategias sistemáticas y guiadas frente a la aleatoriedad.

![boxplot_actions_count_solo_soluciones.png](https://raw.githubusercontent.com/bucketio/img17/main/2025/10/14/1760469321075-9e665ea7-3b2c-4edb-8e30-ee649a707963.png 'boxplot_actions_count_solo_soluciones.png')


## Heurística utilizada por A\*

El algoritmo **A\*** emplea una **distancia de Manhattan ponderada** para el escenario 2, adaptada a los costos diferenciales del entorno:

\[
h(n) = 10 \times |y_{\text{actual}} - y_{\text{meta}}| + 1 \times |x_{\text{actual}} - x_{\text{meta}}|
\]

Donde:
- Los **movimientos verticales** (arriba/abajo) tienen un costo de **10**, por lo que su contribución a la distancia se multiplica por 10.  
- Los **movimientos horizontales** (izquierda/derecha) tienen un costo de **1**, reflejando un desplazamiento menos costoso.

Esta ponderación hace que la heurística priorice rutas que minimicen desplazamientos verticales, adaptándose de manera eficiente a las condiciones del **escenario 2**, lo que se traduce en **menor exploración y tiempos más bajos**.


## Conclusiones generales

- **A\*** y **UCS** son los algoritmos más eficientes y consistentes en ambos escenarios.  
- **BFS** y **DFS** presentan resultados correctos, pero con mayor tiempo y exploración innecesaria.  
- **RANDOM** es el menos eficiente, con alta variabilidad y baja tasa de éxito.  
- La heurística ponderada de **A\*** mejora significativamente su desempeño en el escenario 2, reduciendo la cantidad de estados explorados sin comprometer la calidad de la solución.




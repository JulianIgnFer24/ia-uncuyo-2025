# Ejercicios 2.10 y 2.11

## 2.10
Considera una versión modificada del entorno de la aspiradora en el Ejercicio 2.8, en el que  
al agente se le penaliza con un punto por cada movimiento.

**a. ¿Puede un agente reflejo simple ser perfectamente racional para este entorno? Explica.**

No, un agente reflejo simple no puede ser perfectamente racional en este entorno. La razón es que un agente racional busca maximizar su desempeño total. En este caso, dado que el agente no tiene información sobre el tamaño del entorno ni sobre la distribución de la suciedad, cualquier movimiento tiene un costo (penalización de un punto). Por lo tanto, para actuar de manera racional, el agente necesitaría planificar sus movimientos de manera eficiente, considerando la penalización por cada acción y la probabilidad de limpiar más suciedad con menos pasos. Un agente reflejo simple, que solo reacciona al estado actual sin memoria ni planificación, no puede optimizar este balance, por lo que no alcanzaría un comportamiento perfectamente racional.

**b. ¿Qué hay de un agente reflejo con estado? Diseña dicho agente.**

Un agente reflejo con estado sí puede aproximarse a un comportamiento racional en este entorno, porque mantiene información sobre lo que ha ocurrido previamente y puede usarla para tomar decisiones más informadas. A diferencia de un agente reflejo simple, este agente recuerda qué casillas ya fueron limpiadas y puede planificar sus movimientos para minimizar la penalización por cada acción.

**c. ¿Cómo cambian tus respuestas de los apartados a y b si las percepciones del agente le dan el estado limpio/sucio de *todas* las casillas del entorno?**

En este caso podriamos hacer una planificaion previa de como hacer el recorrido, por lo tanto podriamos decir que es perfectamente racional.

---

## 2.11
Considera una versión modificada del entorno de la aspiradora en el Ejercicio 2.8, en la que  
la geografía del entorno —su extensión, límites y obstáculos— es desconocida, al igual que la configuración inicial de suciedad. (El agente puede ir Arriba y Abajo además de Izquierda y Derecha).

**a. ¿Puede un agente reflejo simple ser perfectamente racional para este entorno? Explica.**

En este caso si, ya que al no existir la penalización solo debo enfocarme en recorrer la matriz de manera eficiente, por ejemplo haciendo un espiral.

**b. ¿Puede un agente reflejo simple pero con una función agente aleatoria superar a un agente reflejo simple? Diseña dicho agente y mide su desempeño en varios entornos.**

Al usar un agente aleatorio, siempre existe la posibilidad de que ocasionalmente supere al agente reflejo simple. Sin embargo, la mayoría de las veces el agente reflejo simple será más eficiente. Por ejemplo, si comparamos dos agentes aleatorios, pero uno de ellos verifica si la casilla está sucia o limpia antes de decidir limpiar, este agente será más eficiente que el que actúa de manera completamente aleatoria, porque evita acciones innecesarias y reduce el costo por movimientos.

En otras palabras, incorporar información del estado incluso de forma mínima permite que el agente tome decisiones más racionales y mejore su desempeño frente a un comportamiento puramente aleatorio.

**c. ¿Puedes diseñar un entorno en el que tu agente aleatorizado tenga un rendimiento pobre? Muestra tus resultados.**

En este caso, el entorno debería ser grande, por ejemplo de 128×128 casillas, y con un alto porcentaje de suciedad. En un escenario así, un agente aleatorio tendría que visitar la mayoría de las posiciones del entorno, y en ciertos casos podría decidir no actuar al llegar a una casilla sucia. Como resultado, no hay garantía de que cada vez que llegue a una posición sucia el agente limpie, lo que hará que su rendimiento sea muy bajo en promedio.

**d. ¿Puede un agente reflejo con estado superar a un agente reflejo simple? Diseña dicho agente y mide su desempeño en varios entornos. ¿Puedes diseñar un agente racional de este tipo?**

Sí, un agente reflejo con estado puede superar a un agente reflejo simple, ya que mantiene información sobre lo que ha hecho y puede planificar movimientos más eficientes. Mientras que un agente reflejo simple solo reacciona a la percepción inmediata, un agente con estado puede evitar acciones redundantes, priorizar casillas sucias y minimizar movimientos innecesarios, mejorando su desempeño general.
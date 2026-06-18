# Agente Benigno Basado en LLM para Simulación de Comportamiento de Usuario en Entornos Contenerizados

**Materia:** Inteligencia Artificial  
**Facultad de Ingeniería – Universidad Nacional de Cuyo**  
**Año:** 2025
**Alumnos:** Julian Ignacio Fernandez, Rocio Baggio 

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Marco Teórico](#2-marco-teórico)
3. [Diseño Experimental](#3-diseño-experimental)
4. [Análisis y Discusión de Resultados](#4-análisis-y-discusión-de-resultados)
5. [Conclusiones Finales](#5-conclusiones-finales)
6. [Bibliografía](#6-bibliografía)

---

## 1. Introducción

### 1.1 Contexto y Motivación

La simulación de comportamiento humano en entornos digitales es una problemática central en múltiples áreas de la informática, especialmente en ciberseguridad. Los entornos de prueba conocidos como *cyber ranges*, infraestructuras controladas diseñadas para simular redes y sistemas reales, requieren la presencia de actividad legítima y creíble para que su utilidad sea real. Sin esta simulación, los experimentos de detección de intrusiones, análisis de tráfico de red o evaluación de sistemas de defensa carecen del contexto necesario para validarse correctamente [1].

Históricamente, la generación de tráfico benigno se ha abordado mediante scripts predefinidos o mediante la intervención directa de operadores humanos. Ambos enfoques presentan limitaciones significativas: los scripts son rígidos, predecibles y no logran capturar la variabilidad natural del comportamiento humano, mientras que la operación manual no escala y está sujeta a errores de reproducibilidad. Esta rigidez hace que los sistemas de detección entrenados o evaluados sobre tráfico sintético de baja calidad presenten resultados que no se corresponden con el rendimiento real en producción [2].

La irrupción de los Modelos de Lenguaje de Gran Escala (LLMs, por sus siglas en inglés) ha abierto una alternativa prometedora. Estos modelos, entrenados sobre vastas colecciones de texto y código, han demostrado capacidad para razonar sobre tareas complejas, generar secuencias de comandos válidos, adaptarse ante errores y operar de manera autónoma en entornos interactivos [3]. La posibilidad de equipar a un agente de software con un LLM como motor de razonamiento permite así construir un simulador de usuario que no sigue un guión fijo, sino que interpreta objetivos en lenguaje natural y decide cómo alcanzarlos mediante comandos reales ejecutados en un sistema operativo.

### 1.2 Problema a Resolver

El problema abordado en este trabajo consiste en desarrollar y evaluar un **agente benigno autónomo** que simule el comportamiento de un usuario humano realizando tareas de administración de bases de datos en un entorno Linux contenerizado. El agente debe recibir objetivos expresados en lenguaje natural y ejecutarlos a través de una terminal, generando patrones de actividad realistas que incluyan tanto comandos SQL como operaciones de sistema, consultas web y pausas naturales.

La pregunta central del trabajo es: **¿En qué medida un agente de código impulsado por un LLM es capaz de simular de forma confiable y autónoma las acciones de un administrador de bases de datos real?** Para responder esta pregunta, se diseñaron y ejecutaron experimentos sistemáticos evaluando el comportamiento del agente a través de métricas objetivas como tasas de éxito por tipo de comando y distribución de códigos de salida.

### 1.3 Relevancia de la Inteligencia Artificial en esta Problemática

La aplicación de técnicas de inteligencia artificial, en particular agentes basados en LLMs, resulta una solución viable por varias razones:

- **Generalización a partir del lenguaje natural:** Los LLMs pueden interpretar instrucciones ambiguas o incompletas y derivar un plan de acción coherente sin necesidad de reglas explícitas.
- **Adaptación dinámica:** A diferencia de un script, un agente LLM puede detectar que una estrategia falla y modificar su enfoque en tiempo real.
- **Variabilidad emergente:** El comportamiento varía de ejecución en ejecución, lo que produce patrones de tráfico más naturales y menos predecibles.
- **Escalabilidad:** Una vez definida la arquitectura, el agente puede ser reconfigurado para distintos perfiles de usuario simplemente cambiando su instrucción de sistema (*system prompt*).


---

## 2. Marco Teórico

### 2.1 Modelos de Lenguaje de Gran Escala (LLMs)

Los Modelos de Lenguaje de Gran Escala son sistemas de aprendizaje automático basados en arquitecturas de tipo *Transformer* [4], entrenados sobre enormes corpus de texto con el objetivo de predecir la siguiente palabra (o *token*) en una secuencia dada. Esta tarea aparentemente simple da lugar, a escala suficiente de parámetros y datos, a capacidades emergentes sorprendentes: razonamiento lógico, generación de código, resolución de problemas matemáticos y seguimiento de instrucciones complejas [3].

El proceso de entrenamiento de un LLM moderno comprende típicamente dos grandes etapas:

1. **Preentrenamiento:** El modelo aprende una representación estadística del lenguaje a partir de miles de millones de documentos de texto (páginas web, libros, repositorios de código, artículos científicos). El objetivo es minimizar la entropía cruzada sobre la predicción del siguiente token.

2. **Alineamiento mediante retroalimentación humana (RLHF):** Tras el preentrenamiento, el modelo es ajustado mediante *fine-tuning* supervisado y aprendizaje por refuerzo con retroalimentación humana (*Reinforcement Learning from Human Feedback*) para que sus respuestas sean útiles, inofensivas y honestas [5].

Los modelos resultantes son capaces de recibir una instrucción en lenguaje natural y generar una respuesta textual que puede incluir razonamiento paso a paso, fragmentos de código, comandos de terminal o planes de acción.

### 2.2 Agentes Autónomos Basados en LLM

Un **agente** en el contexto de la inteligencia artificial es un sistema que percibe su entorno y toma acciones con el objetivo de maximizar alguna noción de recompensa u objetivo [6]. Un agente LLM extiende este concepto al utilizar un modelo de lenguaje como mecanismo de decisión central. En lugar de programar explícitamente las respuestas ante cada situación, el agente formula su siguiente acción mediante el razonamiento del LLM.

La arquitectura típica de un agente LLM incluye [7]:

- **Módulo de percepción:** Toma la observación del entorno (por ejemplo, la salida de un comando de terminal) y la incorpora al contexto del LLM.
- **Módulo de razonamiento:** El LLM procesa el contexto acumulado y genera la siguiente acción, que puede incluir una reflexión interna (*chain-of-thought*) seguida de una acción concreta.
- **Módulo de ejecución:** La acción generada por el LLM se ejecuta en el entorno (por ejemplo, se corre un comando en la terminal), y el resultado se devuelve al módulo de percepción.

Este ciclo percepción–razonamiento–acción permite al agente operar de forma iterativa, corrigiendo errores y ajustando su estrategia en función de la retroalimentación del entorno.


### 2.3 Agentes de Código y Herramientas de Ejecución

Una subclase particularmente relevante de agentes LLM son los **agentes de código** (*coding agents*): sistemas diseñados específicamente para generar y ejecutar código de manera iterativa. Estos agentes tienen acceso a un conjunto de herramientas, como la ejecución de comandos de shell, la lectura y escritura de archivos, y la búsqueda en la web, y pueden llamarlas como parte de su proceso de razonamiento.

Los agentes de código han demostrado capacidades notables en tareas de ingeniería de software: corrección automática de bugs, generación de test cases, refactorización de código y resolución de desafíos de programación competitiva [8]. Estas mismas capacidades los hacen apropiados para simular a un usuario técnico interactuando con un sistema mediante una terminal.

### 2.4 OpenCode: Framework de Agente de Código

**OpenCode** es un framework de código abierto diseñado para construir agentes de código que interactúan con entornos reales a través de herramientas de terminal. A diferencia de entornos de benchmarking puramente sintéticos, OpenCode está concebido para ejecutar comandos reales en sistemas operativos reales, lo que lo hace particularmente apto para la simulación de usuarios en entornos contenerizados.

El framework expone al modelo de lenguaje subyacente un conjunto de herramientas entre las que se incluyen: ejecución de comandos de bash, lectura y escritura de archivos, y solicitudes web. El LLM recibe un objetivo en lenguaje natural como parte de su *system prompt*, junto con el historial de acciones y observaciones previas, y genera la siguiente acción a tomar.

### 2.5 Modelo de Lenguaje Utilizado: Qwen3-Coder

Para este trabajo se utilizó **Qwen3-Coder** como motor de razonamiento del agente. Qwen3-Coder es un modelo de lenguaje de gran escala desarrollado por el equipo de Qwen de Alibaba Cloud, especializado en tareas de generación y comprensión de código [9]. El modelo se distingue por su fuerte rendimiento en benchmarks de programación y su capacidad para razonar sobre entornos de terminal, incluyendo la interpretación de mensajes de error, la depuración de comandos fallidos y la ejecución de secuencias multi-paso.

La elección de Qwen3-Coder se fundamenta en su orientación explícita hacia tareas de código e interacción con sistemas, lo que lo convierte en un candidato adecuado para la simulación de un administrador de bases de datos que trabaja principalmente a través de una terminal Linux.

### 2.6 Cyber Ranges y Simulación de Comportamiento Benigno

Un **cyber range** es una infraestructura controlada que replica entornos de red y sistemas reales con el propósito de llevar a cabo entrenamiento en ciberseguridad, desarrollo y prueba de herramientas de defensa, e investigación sobre técnicas de ataque y detección [1]. A diferencia de los laboratorios físicos o los entornos de producción, los cyber ranges ofrecen un espacio seguro donde es posible ejecutar ataques reales sin riesgo para sistemas productivos.

Para que un cyber range sea útil en el contexto de la detección de intrusiones, es imprescindible que el tráfico de red y la actividad del sistema sean realistas. Un sistema de detección de intrusiones (IDS) entrenado o evaluado únicamente sobre tráfico de ataque —sin actividad benigna de fondo— aprenderá clasificadores trivialmente sesgados que no generalizan al mundo real [2]. De igual modo, la evaluación de la tasa de falsos positivos de un IDS requiere disponer de actividad benigna convincente que el sistema pueda confundir con actividad maliciosa.

Esta necesidad de actividad benigna realista es la motivación directa de este trabajo. Históricamente, la generación de dicha actividad ha dependido de scripts predefinidos o de la participación activa de personas. Los scripts son rígidos: ejecutan siempre la misma secuencia de acciones, en el mismo orden, con la misma temporización, lo que los hace trivialmente distinguibles del comportamiento humano por cualquier clasificador con algo de sofisticación. La participación humana, en cambio, no escala ni es reproducible. Los agentes LLM ofrecen una tercera vía: comportamiento autónomo, variable y coherente con el rol asignado, generado de manera completamente automatizada.

### 2.7 PostgreSQL como Entorno de Trabajo

**PostgreSQL** es un sistema de gestión de bases de datos relacionales (RDBMS) de código abierto, ampliamente utilizado en entornos empresariales y académicos. Su elección como sistema objetivo del agente responde a varios factores: es uno de los sistemas de bases de datos más documentados en el corpus de entrenamiento de los LLMs (lo que maximiza la competencia del agente en esta área), es de código abierto (lo que facilita su integración en el entorno Docker), y es representativo de los sistemas que un DBA real administraría en un entorno corporativo.

Las operaciones típicas que el agente realiza sobre PostgreSQL incluyen consultas de lectura (`SELECT`), operaciones de escritura (`INSERT`, `UPDATE`, `DELETE`), creación y modificación de esquemas (`CREATE TABLE`, `ALTER TABLE`), operaciones de mantenimiento (`VACUUM`, `ANALYZE`), y verificación de estado del servidor mediante vistas del sistema (`pg_stat_activity`, `pg_stat_user_tables`, etc.).

### 2.8 Contenerización con Docker

Los experimentos se realizaron en un entorno contenerizado utilizando **Docker** [10]. La contenerización ofrece varias ventajas fundamentales para este tipo de experimentos:

- **Aislamiento:** Cada ejecución del agente opera en un entorno limpio y reproducible, eliminando efectos secundarios entre experimentos.
- **Reproducibilidad:** La imagen de Docker captura el estado exacto del sistema (sistema operativo, dependencias, configuración de red) garantizando que los resultados sean comparables entre ejecuciones.
- **Escalabilidad:** Es posible ejecutar múltiples instancias del agente en paralelo sin interferencia mutua.
- **Seguridad:** El aislamiento del contenedor limita el impacto de las acciones del agente sobre el sistema anfitrión.

### 2.9 Métricas de Evaluación de Agentes

La evaluación del rendimiento de un agente autónomo es un problema no trivial. En ausencia de una función de recompensa escalar bien definida, es necesario recurrir a métricas proxy que aproximen la calidad del comportamiento. Para este trabajo, se adoptan las siguientes métricas principales:

- **Tasa de éxito por tipo de comando:** Proporción de veces que un determinado tipo de comando (e.g., `SELECT`, `curl`) se ejecuta exitosamente.
- **Distribución de códigos de salida:** Análisis de los códigos de retorno de los procesos ejecutados por el agente, donde el código 0 indica éxito y los códigos distintos indican diferentes categorías de error.
- **Frecuencia de comandos:** Conteo promedio de comandos de cada tipo emitidos por el agente por ejecución.
- **Evolución temporal del comportamiento:** Análisis de cómo varía la tasa de errores a lo largo de la ejecución del agente.

Estas métricas permiten caracterizar tanto la **eficacia** del agente (¿logra completar las tareas?) como su **estilo de comportamiento** (¿cómo las afronta?).

---

## 3. Diseño Experimental

### 3.1 Arquitectura del Sistema

El sistema implementado consta de los siguientes componentes:

```
┌─────────────────────────────────────────────┐
│              Entorno Docker                  │
│                                             │
│   ┌──────────────┐    ┌──────────────────┐  │
│   │  Agente      │    │  PostgreSQL       │  │
│   │  OpenCode    │◄──►│  (remoto/local)   │  │
│   │  (LLM:       │    └──────────────────┘  │
│   │  Qwen3-Coder)│                          │
│   └──────┬───────┘                          │
│          │ comandos de terminal              │
│          ▼                                  │
│   ┌──────────────┐                          │
│   │  Shell Linux │                          │
│   └──────────────┘                          │
└─────────────────────────────────────────────┘
```

**Figura 1:** Arquitectura general del sistema.

El agente recibe un objetivo de alto nivel en lenguaje natural y lo ejecuta íntegramente mediante comandos de terminal. No se provee al agente de ningún script predefinido: toda la secuencia de acciones es generada autónomamente por el LLM.

### 3.2 Perfil del Agente: Administrador de Bases de Datos

El agente fue configurado para asumir el rol de un **administrador de bases de datos** (DBA). Este perfil fue elegido porque:

1. Las tareas de administración de bases de datos son rutinarias, bien definidas y verificables objetivamente.
2. El conjunto de comandos involucrados (SQL, herramientas de sistema, consultas web) es diverso, lo que permite evaluar múltiples dimensiones del comportamiento del agente.
3. La administración de bases de datos es un perfil realista en contextos empresariales, lo que otorga validez a la simulación.

Los **objetivos primarios** asignados al agente son:

1. **Trabajo administrativo continuo:** Realizar tareas regulares de administración de bases de datos, incluyendo verificaciones de salud del sistema, mantenimiento de datos y evolución incremental del esquema, así como consulta de referencias técnicas externas mediante solicitudes web.

2. **Dinámica temporal humana:** Intercalar trabajo activo con pausas y cambios de tarea que imiten el ritmo natural de un empleado real.

El agente fue provisto de la dirección IP de un servidor PostgreSQL remoto (`172.31.0.10`) como punto de conexión inicial.

### 3.3 Configuración de los Experimentos

Se realizaron un total de **100 ejecuciones independientes**. Cada ejecución tuvo una duración de **2.700 segundos (45 minutos)**, una extensión seleccionada por aproximar la duración de una sesión de trabajo realista.

La decisión de ejecutar 100 instancias independientes responde a la necesidad de obtener estimaciones estadísticamente robustas del comportamiento del agente, ya que la naturaleza estocástica del LLM introduce variabilidad entre ejecuciones. Con 100 repeticiones es posible calcular medias y distribuciones confiables para cada métrica.

Las condiciones de cada ejecución son idénticas al inicio: misma imagen de Docker, mismo *system prompt*, misma dirección del servidor objetivo. Sin embargo, como el LLM introduce variabilidad en cada generación, el comportamiento concreto del agente difiere de ejecución en ejecución, lo que es precisamente lo que se busca para simular la variabilidad de un usuario real.

### 3.4 Métricas y Herramientas de Medición

#### 3.4.1 Categorización de Comandos

Los comandos ejecutados por el agente fueron agrupados en las siguientes categorías:

| Categoría | Comandos incluidos |
|---|---|
| Operaciones SQL de lectura | `SELECT` |
| Operaciones SQL de escritura | `INSERT`, `UPDATE`, `DELETE` |
| Tareas administrativas SQL | `CREATE TABLE`, `ALTER TABLE`, `GRANT`, `VACUUM`, etc. |
| Solicitudes web | `curl` |
| Gestión del sistema de archivos | `ls`, `grep`, `cat`, y variantes |
| Consultas de información del sistema | `ps`, `top`, `netstat`, `df`, etc. |
| Pausas de ejecución | `sleep` |
| Otros | Comandos diagnósticos, reinicio de servicios, escalada de privilegios, sondeos de red |

#### 3.4.2 Análisis de Códigos de Salida

Los procesos ejecutados en Linux retornan un código de salida (*exit code*) que indica el resultado de la ejecución. Los códigos más relevantes para este análisis son:

| Código | Significado |
|---|---|
| `0` | Éxito |
| `1` | Error genérico |
| `2` | Uso incorrecto del comando |
| `127` | Comando no encontrado (binario ausente) |
| Otros | Códigos específicos de cada programa |

La distribución de estos códigos a lo largo de las ejecuciones sirve como métrica de "limpieza operacional" del agente: una predominancia de `exit 0` indica alta confiabilidad, mientras que una presencia significativa de `exit 1` o `exit 2` señala errores frecuentes de sintaxis o lógica.

#### 3.4.3 Evolución Temporal del Comportamiento

Para analizar si el agente aprende o adapta su comportamiento a lo largo de la ejecución, se calculó la tasa de errores (proporción de comandos con `exit != 0`) para cada segmento de la línea temporal normalizada de cada ejecución. Esto permite detectar si existe una fase inicial de exploración/descubrimiento del entorno, seguida de una fase de estabilización.

### 3.5 Herramientas Utilizadas

- **OpenCode:** Framework de agente de código (open source) utilizado como base del agente benigno.
- **Qwen3-Coder:** Modelo de lenguaje de gran escala utilizado como motor de razonamiento.
- **Docker:** Sistema de contenerización para el entorno de ejecución aislado.
- **PostgreSQL:** Sistema de gestión de bases de datos objetivo.
- **Python + Pandas + Matplotlib:** Utilizados para el procesamiento y visualización de los logs de ejecución.

### 3.6 Recolección y Procesamiento de Datos

Los logs de cada ejecución registraron, para cada comando ejecutado:

- El texto exacto del comando.
- El código de salida retornado.
- La salida estándar y la salida de error.
- El timestamp relativo dentro de la ejecución.

A partir de estos logs se construyeron las métricas descritas anteriormente. La categorización de los comandos se realizó mediante análisis del texto del comando (identificando el binario o instrucción SQL inicial). Los logs de 100 ejecuciones de 45 minutos cada una representan un volumen considerable de datos, procesado de manera automatizada.

### 3.7 Resultados de los Experimentos

#### 3.7.1 Distribución de Comandos por Tipo

El análisis de los comandos ejecutados a lo largo de las 100 ejecuciones revela un perfil de uso coherente con el rol asignado.

**Figura 2:** *Conteo promedio de comandos por ejecución, discriminado por categoría.*

Los hallazgos principales son los siguientes:

- **Alta frecuencia de `SELECT`:** Las consultas de lectura son, por amplio margen, las operaciones más frecuentes. Esto es consistente con un perfil de administrador de bases de datos cuya tarea principal en este contexto es la generación de reportes sobre el estado del sistema y los datos almacenados.
- **Uso significativo de `curl`:** Las solicitudes web aparecen con frecuencia considerable, reflejando el objetivo del agente de consultar referencias técnicas externas durante su trabajo. Esto es un comportamiento esperable: un DBA real consulta documentación, foros de soporte o APIs externas durante sus tareas.
- **Presencia de `sleep`:** Los comandos de pausa aparecen regularmente, lo que indica que el agente cumple con el objetivo de simular dinámicas temporales humanas intercalando trabajo con esperas.
- **Operaciones de escritura (`INSERT`, `UPDATE`, `DELETE`):** Presentes en proporciones menores que `SELECT`, lo cual es también consistente con el perfil: un DBA genera muchos más reportes que modificaciones directas de datos en una sesión típica.

#### 3.7.2 Tasa de Éxito por Tipo de Comando

La tasa de éxito de los comandos varía según la categoría:

**Figura 3:** *Tasa de éxito vs. tasa de error para las 10 acciones más frecuentes.*

| Categoría de comando | Tasa de éxito aproximada |
|---|---|
| `SELECT` | 95–100% |
| `INSERT` | 92–100% |
| `UPDATE` | 92–100% |
| `DELETE` | 92–100% |
| `curl` (solicitudes web) | ~85–90% |
| `sleep` | ~100% |
| Gestión de archivos (`ls`, `grep`, `cat`) | ~90–95% |
| Otros (diagnóstico, red, escalada) | ~38% |

Las operaciones SQL fundamentales (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) alcanzan tasas de éxito de entre el 92% y el 100%, lo que demuestra una alta confiabilidad del agente en su dominio principal de operación.

La categoría `otros` presenta la tasa de error más elevada (~62%). Esta categoría agrupa comandos diagnósticos para reinicio de servicios, intentos de escalada de privilegios, llamadas directas a la CLI de la base de datos y sondeos de red. El elevado error en esta categoría revela el **comportamiento de resolución de problemas** del agente: cuando sus herramientas principales fallan, el agente experimenta con comandos alternativos, muchos de los cuales no están disponibles o requieren permisos que el agente no posee. Cabe señalar que parte de esta tasa de error se explica por la inclusión de comandos `webfetch` —una herramienta nativa de OpenCode— que registraron un 100% de fallos durante los experimentos debido a problemas a nivel de herramienta ajenos al razonamiento del agente.

#### 3.7.3 Distribución de Códigos de Salida

**Figura 4:** *Distribución promedio de códigos de salida a lo largo de las ejecuciones.*

La distribución de códigos de salida muestra una clara predominancia de `exit 0` (éxito), lo que confirma la alta confiabilidad general del agente. La presencia de `exit 1` y `exit 2` es menor y concentrada en las categorías de comandos menos dominadas por el agente (especialmente la categoría `otros`). Los casos de `exit 127` (binario no encontrado) son infrecuentes pero significativos: ocurren cuando el agente intenta utilizar herramientas que no están instaladas en el entorno del contenedor, lo que refleja una brecha entre el conocimiento del modelo (entrenado sobre documentación de sistemas generales) y el entorno específico de ejecución.

#### 3.7.4 Evolución Temporal de la Tasa de Errores

**Figura 5:** *Tasa de errores (exit code ≠ 0) en función de la posición relativa en la ejecución.*

El análisis de la evolución temporal revela un patrón consistente a través de las 100 ejecuciones:

- **Fase inicial (0–40% de la ejecución):** La tasa de errores es más elevada. El agente se encuentra en una fase de exploración del entorno, intentando establecer conexión con el servidor remoto, verificando herramientas disponibles e intentando diferentes estrategias.
- **Fase de estabilización (60% en adelante):** La tasa de errores se estabiliza por debajo del 9%. Una vez que el agente ha establecido una estrategia funcional, opera con alta confiabilidad.

Este patrón es análogo a la curva de aprendizaje de un empleado humano que comienza un trabajo nuevo: los primeros momentos son de orientación y prueba, mientras que una vez asentado el workflow, la eficiencia aumenta.

#### 3.7.5 Acción Destacada: Fallo de Conexión y Cambio de Estrategia

El comportamiento más notable observado durante los experimentos fue la respuesta del agente ante el fallo de conexión al servidor PostgreSQL remoto. Este caso ilustra con claridad la capacidad de adaptación emergente del agente:

**Situación inicial:** El agente recibe la instrucción de conectarse al servidor PostgreSQL en `172.31.0.10` para realizar tareas de administración rutinaria.

**Secuencia de acciones observada:**

1. El agente intenta conectarse directamente mediante el cliente `psql`. La conexión es rechazada inmediatamente.
2. Realiza verificaciones básicas de conectividad (ping, `telnet`, `nc`) para confirmar que el servidor no es alcanzable desde su entorno.
3. Intenta establecer un túnel SSH para acceder a la base de datos de manera indirecta. Estos intentos fallan por problemas de autenticación y permisos.
4. El agente concluye que no tiene ninguna vía viable para alcanzar la base de datos remota, y que tampoco existe una instancia local de PostgreSQL en su entorno.
5. **Cambio de estrategia:** En lugar de continuar intentando resolver la conectividad remota, el agente instala una instancia local de PostgreSQL en su entorno de ejecución.
6. Una vez instalada y configurada la instancia local, el agente se conecta localmente, crea un esquema básico con tablas (`employee`, `salary`), inserta datos iniciales y verifica la estructura.
7. Procede a ejecutar operaciones regulares de base de datos (consultas, inserciones, actualizaciones) íntegramente sobre la base de datos local provisionada por él mismo.

Este comportamiento no fue explícitamente programado ni anticipado en el diseño del agente. Emerge del razonamiento autónomo del LLM ante un entorno hostil. El agente interpreta su objetivo de alto nivel (realizar administración de bases de datos) de manera flexible, priorizando la completitud de la tarea sobre el cumplimiento estricto del método original.

**Pseudo-código del proceso de decisión observado:**

```
objetivo = "administrar base de datos en 172.31.0.10"

intentar conectar_psql(172.31.0.10)
si falla:
    verificar_conectividad(172.31.0.10)  // ping, telnet
    intentar_ssh_tunnel(172.31.0.10)
    si falla:
        // No hay camino al objetivo original
        instalar_postgresql_local()
        configurar_base_datos_local()
        crear_schema_local()       // tablas: employee, salary
        ejecutar_tareas_normales_en_local()
```

**Figura 6:** *Diagrama de flujo de decisiones del agente ante el fallo de conexión remota.*

---

## 4. Análisis y Discusión de Resultados

### 4.1 Efectividad General del Agente

Los resultados obtenidos permiten afirmar que el agente benigno basado en Qwen3-Coder es, en términos generales, un simulador efectivo de comportamiento de usuario técnico. La alta tasa de éxito en operaciones SQL (92–100%) confirma que el modelo tiene un dominio sólido de la sintaxis y semántica de las operaciones de base de datos más comunes. Esta competencia es esperable dado que los modelos de la familia Qwen3-Coder han sido entrenados extensamente sobre código y documentación técnica, incluyendo SQL [9].

La distribución de tipos de comandos es también consistente con el perfil asignado: la predominancia de `SELECT` sobre otras operaciones refleja el énfasis en la generación de reportes, mientras que la presencia de `curl` confirma el comportamiento de consulta a referencias externas. En conjunto, estos patrones constituirían tráfico benigno creíble para sistemas de detección de intrusiones que analicen comportamiento de usuario.

### 4.2 Comportamiento en Fases: Exploración y Estabilización

La evolución temporal de la tasa de errores revela un comportamiento bifásico que tiene una interpretación clara: el agente dedica la parte inicial de la ejecución a construir un modelo del entorno en el que opera. Durante esta fase de exploración, experimenta con comandos que pueden no estar disponibles, intenta conexiones que pueden fallar y prueba estrategias alternativas. Una vez que ha establecido qué herramientas están disponibles y cuáles no, su comportamiento se vuelve más eficiente y confiable.

Este patrón tiene implicaciones directas para la utilidad del agente como simulador: si bien la fase inicial produce tráfico con una proporción mayor de errores, esto es en sí mismo realista. Un administrador humano que comienza a trabajar en un sistema nuevo también comete más errores inicialmente. La curva de aprendizaje del agente imita, de forma emergente y no programada, este aspecto del comportamiento humano.

Desde la perspectiva del diseño del agente, este hallazgo también sugiere una posible mejora: si el agente fuera provisto de información inicial sobre el entorno (herramientas disponibles, estado de los servicios, configuración de red), la fase de exploración podría acortarse o eliminarse, resultando en un comportamiento más eficiente desde el primer momento. Sin embargo, esta información inicial también reduciría el realismo de la simulación, ya que un usuario humano real también necesitaría cierto tiempo de orientación en un sistema desconocido. El equilibrio entre eficiencia y realismo en esta dimensión es una cuestión de diseño que depende del caso de uso específico.

### 4.3 Capacidad de Adaptación: El Caso de la Base de Datos Local

El comportamiento observado ante el fallo de conexión remota es el resultado más notable del trabajo y merece un análisis detallado.

El agente no fue instruido explícitamente sobre qué hacer si el servidor remoto no estaba disponible. Su respuesta —instalar una instancia local de PostgreSQL— emerge del razonamiento del LLM sobre el objetivo de alto nivel. Esto ilustra una propiedad fundamental de los agentes LLM: la capacidad de **replanificación dinámica** ante obstáculos no previstos.

Desde una perspectiva positiva, esta capacidad es altamente deseable para un simulador de usuario: un administrador humano real probablemente tomaría una decisión similar si se encontrara con que el servidor remoto no está disponible y su tarea es urgente. Sin embargo, desde una perspectiva de seguridad, este comportamiento también revela un aspecto potencialmente problemático: el agente modifica el entorno de formas no previstas (instalando software). En un contexto de cyber range, estas acciones imprevistas podrían interferir con los experimentos o producir señales de red que no deberían estar presentes.

### 4.4 Limitaciones Identificadas

#### 4.4.1 Conocimiento del Entorno vs. Entorno Real

El LLM fue entrenado sobre documentación general de Linux y PostgreSQL, pero el entorno de Docker en el que opera el agente puede diferir de este conocimiento general. Esto explica los casos de `exit 127` (binario no encontrado): el agente intenta usar herramientas que son comunes en sistemas Linux generales pero que no están instaladas en la imagen de Docker. Esta brecha entre el conocimiento del modelo y el entorno real es una limitación fundamental de los agentes LLM en entornos controlados.

#### 4.4.2 Errores en la Herramienta `webfetch`

El 100% de fallos registrado para la herramienta `webfetch` no es atribuible al razonamiento del agente sino a un problema técnico a nivel del framework. Si bien esto infló artificialmente la tasa de error en la categoría `otros`, en trabajos futuros debería corregirse esta incompatibilidad o reemplazarse la herramienta por una alternativa funcional.

#### 4.4.3 Variabilidad entre Ejecuciones

La naturaleza estocástica del LLM introduce variabilidad entre ejecuciones que, aunque deseable para simular comportamiento humano, también dificulta la caracterización precisa del agente. Ejecuciones individuales pueden diferir considerablemente en la secuencia de acciones tomadas, aunque las métricas agregadas sobre 100 ejecuciones revelan patrones estables.

#### 4.4.4 Ausencia de Retroalimentación de Objetivos Completados

El sistema actual no dispone de un mecanismo que permita al agente reportar si consideró que completó su objetivo. La evaluación se basa enteramente en métricas de comportamiento observado (tipos de comandos, tasas de éxito) pero no hay una medida directa de si el agente logró o no el objetivo de alto nivel. Definir y medir esta métrica es una tarea pendiente importante.

#### 4.4.5 Profundidad del Perfil Simulado

Si bien el agente simula convincentemente varias dimensiones del comportamiento de un DBA (tipos de comandos, pausas, consultas web), otros aspectos del comportamiento humano no son capturados: patrones de horario (el agente no tiene noción de jornada laboral), interacciones con otros usuarios del sistema, o la evolución de hábitos a lo largo de días o semanas.

### 4.5 Reflexión sobre la Idoneidad del Enfoque

Los resultados sugieren que los agentes LLM representan una alternativa genuinamente superior a los scripts predefinidos para la simulación de comportamiento de usuario. La variabilidad emergente, la capacidad de adaptación y la coherencia semántica de las acciones del agente son cualidades que no pueden replicarse con reglas estáticas. Al mismo tiempo, los experimentos ponen en evidencia que el uso de LLMs como motor de simulación introduce nuevos desafíos: comportamientos inesperados (como la instalación del PostgreSQL local), dependencia de la calidad del prompt inicial y sensibilidad a las herramientas disponibles en el entorno.

Un aspecto particularmente valioso desde la perspectiva de la inteligencia artificial es la **generalización que exhibe el agente**. El modelo no fue entrenado específicamente para este entorno ni para este rol: simplemente fue instruido en lenguaje natural y respondió de manera coherente con el contexto. Esto contrasta con los enfoques clásicos basados en reglas, que requieren una ingeniería detallada y explícita de cada comportamiento deseado. La reducción del esfuerzo de programación a cambio de una menor predictibilidad es un trade-off que, para el dominio de la simulación de usuarios, parece favorable.

Finalmente, vale destacar que los resultados de este trabajo son relevantes no solo para el dominio de los cyber ranges, sino también para áreas como la generación automática de datos de entrenamiento para IDS, la evaluación de herramientas de monitoreo de sistemas, y el desarrollo de agentes de asistencia para administración de sistemas. En todos estos contextos, la capacidad de un agente LLM para simular comportamiento técnico humano de manera autónoma y variable tiene un valor potencial considerable.

---

## 5. Conclusiones Finales

### 5.1 Síntesis de Resultados

Este trabajo presentó el diseño, implementación y evaluación experimental de un agente benigno autónomo que simula el comportamiento de un administrador de bases de datos en un entorno Linux contenerizado. El agente, construido sobre el framework OpenCode con Qwen3-Coder como motor de razonamiento, fue evaluado a través de 100 ejecuciones independientes de 45 minutos cada una.

Los principales hallazgos son:

1. **Alta confiabilidad en tareas SQL:** Las operaciones de base de datos fundamentales (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) se ejecutan exitosamente en el 92–100% de los casos, confirmando la competencia del modelo en su dominio principal.

2. **Comportamiento bifásico:** El agente presenta una fase inicial de exploración con mayor tasa de errores, seguida de una fase de estabilización donde opera por debajo del 9% de errores. Este patrón imita, de forma emergente, la curva de aprendizaje de un usuario humano.

3. **Distribución realista de comandos:** El perfil de uso de comandos (predominancia de `SELECT`, presencia significativa de `curl` y `sleep`) es coherente con el rol de DBA asignado.

4. **Capacidad de replanificación dinámica:** Ante el fallo del servidor remoto, el agente adaptó su estrategia de manera autónoma, instalando una base de datos local y completando sus tareas en el nuevo entorno. Este comportamiento, si bien no previsto, ilustra la flexibilidad emergente de los agentes LLM.

5. **Limitaciones identificadas:** La brecha entre el conocimiento del modelo y el entorno específico de Docker, los problemas con la herramienta `webfetch`, y la ausencia de una métrica directa de completitud del objetivo son las principales áreas de mejora.

### 5.2 Contribuciones

El trabajo demuestra la viabilidad de utilizar agentes LLM como generadores de tráfico benigno realista en entornos de cyber range. La metodología experimental diseñada (100 ejecuciones independientes, categorización de comandos, análisis de exit codes, análisis temporal) constituye un framework de evaluación replicable para futuros trabajos en esta área.

### 5.3 Trabajo Futuro

Varios experimentos y mejoras quedaron fuera del alcance de este trabajo y constituyen líneas de investigación futuras de alta relevancia:

1. **Comparación entre múltiples modelos LLM:** Evaluar el mismo agente con distintos modelos (e.g., modelos de la familia Llama, Mistral, o modelos orientados a código como DeepSeek-Coder) permitiría determinar cuál ofrece el mejor equilibrio entre autonomía, confiabilidad y comportamiento realista para esta tarea específica.

2. **Implementación de métricas de completitud de objetivos:** Diseñar un mecanismo que permita evaluar si el agente logró o no su objetivo de alto nivel, más allá de las métricas de comportamiento observado.

3. **Simulación de múltiples perfiles de usuario:** Extender el sistema para simular perfiles distintos (desarrollador web, analista de datos, operador de red), evaluando si el framework generaliza bien a diferentes roles.

4. **Análisis de la calidad del tráfico simulado:** Evaluar si el tráfico generado por el agente puede efectivamente engañar a clasificadores de tráfico (IDS/IPS), midiendo métricas como la distancia estadística entre el tráfico del agente y tráfico humano real.

5. **Experimentos de larga duración:** Extender la duración de las ejecuciones para evaluar si el agente mantiene su comportamiento coherente en sesiones de trabajo más largas (varias horas), y si emergen comportamientos adicionales en horizontes temporales mayores.

6. **Mejora del entorno de ejecución:** Resolver el problema de la herramienta `webfetch` y asegurar que el entorno Docker cuente con las herramientas habituales que un agente LLM espera encontrar, reduciendo así los errores por binarios ausentes.

7. **Coordinación entre múltiples agentes:** Evaluar la posibilidad de ejecutar simultáneamente múltiples instancias del agente benigno junto con agentes de otros perfiles (atacante, usuario casual) para generar un entorno de cyber range con tráfico mixto más realista.

---

## 6. Bibliografía

[1] Yamin, M. M., Ullah, M., Ullah, H., & Katt, B. (2021). Cyber ranges: A systematic literature review. *Computers & Security, 107*, 102358. https://doi.org/10.1016/j.cose.2021.102358

[2] Sommer, R., & Paxson, V. (2010). Outside the closed world: On using machine learning for network intrusion detection. En *2010 IEEE Symposium on Security and Privacy* (pp. 305–316). IEEE. https://doi.org/10.1109/SP.2010.25

[3] Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., ... & Fedus, W. (2022). Emergent abilities of large language models. *Transactions on Machine Learning Research*. https://arxiv.org/abs/2206.07682

[4] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems, 30*. https://arxiv.org/abs/1706.03762

[5] Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., ... & Lowe, R. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems, 35*, 27730–27744. https://arxiv.org/abs/2203.02155

[6] Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.

[7] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing reasoning and acting in language models. En *International Conference on Learning Representations (ICLR) 2023*. https://arxiv.org/abs/2210.03629

[8] Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., & Press, O. (2024). SWE-agent: Agent-computer interfaces enable automated software engineering. *Advances in Neural Information Processing Systems, 37*. https://arxiv.org/abs/2405.15793

[9] Qwen Team. (2025). *Qwen3-Coder: Technical Report*. Alibaba Cloud. https://huggingface.co/Qwen/Qwen3-Coder

[10] Merkel, D. (2014). Docker: Lightweight Linux containers for consistent development and deployment. *Linux Journal, 2014*(239), 2.

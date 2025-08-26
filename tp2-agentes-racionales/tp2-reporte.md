# Reporte de Resultados — Agentes de Vacuum Cleaner

Este informe presenta los resultados de la evaluación de dos agentes (`random` y `simple_reflex`) en distintos tamaños de entorno y niveles de suciedad.  
Se incluyen tres gráficos principales, cuyos archivos se encuentran en la carpeta de resultados.

---

## 1. Acciones realizadas vs Nivel de suciedad (Agente Random)

Archivo: **actions_vs_dirt_random.png**

**Descripción:**  
El gráfico muestra la relación entre la cantidad de acciones tomadas y el nivel de suciedad en diferentes tamaños de entorno para el agente **Random**.

**Observaciones:**
- A medida que aumenta el nivel de suciedad, el agente requiere más acciones.  
- En tableros más grandes, el número de acciones crece de manera significativa, llegando al máximo de pasos permitidos en `128x128`.

---

## 2. Acciones realizadas vs Nivel de suciedad (Agente Simple Reflex)

Archivo: **actions_vs_dirt_simple_reflex.png**

**Descripción:**  
El gráfico muestra el comportamiento del agente **Simple Reflex** bajo las mismas condiciones.

**Observaciones:**
- El agente reflexivo también incrementa el número de acciones al aumentar la suciedad.  
- Muestra una tendencia más estable en entornos pequeños y medianos.  
- En entornos grandes (`128x128`), alcanza igualmente el límite de acciones posibles.

---

## 3. Comparación de Performance con rango de variación

Archivo: **performance_lines_band.png**

**Descripción:**  
El gráfico presenta la performance promedio de ambos agentes según el nivel de suciedad, incluyendo el rango de variación observado.

**Observaciones:**
- El agente **Simple Reflex** mantiene consistentemente un rendimiento superior al agente **Random**.  
- Ambos agentes ven reducida su performance a medida que aumenta la suciedad, aunque la caída es menos pronunciada en el agente reflexivo.  
- La banda de variación refleja que, en algunos escenarios, la diferencia puede ampliarse dependiendo del tamaño del entorno.

---

## Conclusiones

- El agente **Random** muestra un comportamiento ineficiente en entornos grandes y con alta suciedad, llegando al máximo de acciones sin lograr una limpieza completa.  
- El agente **Simple Reflex** ofrece un mejor desempeño global, adaptándose mejor a distintos niveles de suciedad y tamaños de entorno.  
- La comparación de performance evidencia que el enfoque reflexivo es más robusto y consistente, lo que lo hace más adecuado para el problema de Vacuum Cleaner.

---


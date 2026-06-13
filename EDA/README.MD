# 📊 Análisis Exploratorio de Datos (EDA)

## Descripción

En esta etapa se realizó un análisis exploratorio del conjunto de características generado previamente, con el objetivo de comprender la distribución de las variables, identificar posibles relaciones con las variables objetivo y detectar patrones relevantes para el modelado.

---

## Datos de entrada

- `data/features.csv`

---

## Objetivos

- Analizar la distribución de las variables.
- Evaluar la presencia de sesgos y valores extremos.
- Examinar la distribución de los goles anotados.
- Estudiar el comportamiento de las puntuaciones Elo.
- Analizar la correlación entre las características y las variables objetivo.
- Obtener información que permita orientar la selección de variables y la construcción de modelos.

---

## Análisis realizados

### Estadísticas descriptivas

Se calcularon medidas de tendencia central y dispersión para todas las variables numéricas.

### Distribución de las variables objetivo

Se analizaron:

- `home_score`
- `away_score`

mediante histogramas.

### Distribución del sistema Elo

Se evaluó la distribución de:

- `home_elo`
- `away_elo`
- `elo_diff`

### Matriz de correlación

Se construyó una matriz de correlación entre todas las variables numéricas con el fin de identificar relaciones lineales y posibles dependencias.

---

## Principales hallazgos

### Distribución de los goles

Los goles anotados por los equipos locales y visitantes presentan una distribución sesgada hacia la derecha.

La mayoría de los partidos registran entre 0 y 3 goles, mientras que marcadores muy elevados representan eventos poco frecuentes.

Esto indica que las variables objetivo no siguen una distribución normal y poseen una larga cola asociada a resultados excepcionales.

---

### Ventaja del equipo local

En promedio:

- Goles del local: **1.64**
- Goles del visitante: **1.11**

Lo anterior sugiere la existencia de una ventaja asociada al equipo que juega como local.

---

### Sistema Elo

Las distribuciones de:

- `home_elo`
- `away_elo`
- `elo_diff`

presentan una forma aproximadamente normal.

La mayoría de las selecciones poseen puntuaciones cercanas al promedio, mientras que únicamente unas pocas corresponden a equipos extremadamente fuertes o débiles.

---

### Rendimiento reciente de las selecciones

Los promedios de goles a favor y en contra durante las últimas cinco y diez jornadas se concentran alrededor de:

- 1.3 goles anotados por partido.
- 1.3 goles recibidos por partido.

Lo anterior refleja un comportamiento relativamente equilibrado entre las selecciones internacionales.

---

### Historial entre equipos

La mediana del número de enfrentamientos directos es de dos partidos.

Por tanto, para una gran cantidad de encuentros existe poca información histórica entre ambas selecciones, por lo que otras variables como el rendimiento reciente y el Elo podrían tener mayor relevancia.

---

### Variables con mayor relación con los goles del equipo local

Las variables con mayor correlación positiva con `home_score` fueron:

| Variable | Correlación |
|------------|-----------|
| elo_diff | 0.370 |
| away_GA10 | 0.337 |
| away_GA5 | 0.315 |
| home_GF10 | 0.172 |
| home_elo | 0.162 |
| home_GF5 | 0.156 |

Esto sugiere que el número de goles del equipo local depende principalmente de:

- La diferencia de nivel entre ambas selecciones.
- La capacidad defensiva reciente del rival.
- El potencial ofensivo del propio equipo.

---

### Variables con mayor relación con los goles del equipo visitante

Las variables más relacionadas con `away_score` fueron:

| Variable | Correlación |
|------------|-----------|
| home_GA10 | 0.345 |
| home_GA5 | 0.325 |
| away_elo | 0.175 |
| away_GF10 | 0.161 |
| away_GF5 | 0.149 |
| away_points10 | 0.146 |

Los goles del visitante parecen estar influenciados principalmente por:

- La solidez defensiva reciente del equipo local.
- El nivel competitivo del visitante.
- Su capacidad ofensiva reciente.

---

### Importancia de la diferencia Elo

La variable `elo_diff` presentó la mayor correlación con el número de goles anotados por el equipo local y una fuerte correlación negativa con los goles del visitante.

Esto sugiere que la diferencia de calidad entre ambas selecciones constituye uno de los factores más relevantes para la predicción del marcador.

---

### Ausencia de correlaciones extremadamente altas

No se observaron correlaciones lineales superiores a 0.4 con respecto a las variables objetivo.

Esto indica que el problema de predicción del marcador es altamente complejo y probablemente requiera modelos capaces de capturar relaciones no lineales entre las variables.

---

## Conclusiones

El análisis exploratorio permitió identificar que:

- Los goles presentan distribuciones sesgadas hacia la derecha.
- Existe una ventaja promedio del equipo local.
- Las puntuaciones Elo muestran una distribución aproximadamente normal.
- La diferencia Elo constituye una de las variables más influyentes.
- La capacidad ofensiva propia y la fortaleza defensiva del rival son factores determinantes en la cantidad de goles anotados.
- Ninguna variable individual explica por sí sola el marcador final, lo que justifica el empleo de modelos de aprendizaje automático capaces de capturar interacciones complejas entre las características.

---

## Archivo generado

```text
data/features_processed.csv
```

Este conjunto de datos procesado será utilizado en las etapas posteriores de selección de variables y entrenamiento de modelos.
```
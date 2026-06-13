# 🤖 Entrenamiento y Comparación de Modelos de Predicción de Marcadores

## Descripción

En esta etapa se entrenaron modelos de regresión basados en XGBoost con el objetivo de predecir los goles anotados por el equipo local y el equipo visitante.

Adicionalmente, se evaluaron diferentes configuraciones de variables para determinar cuáles aportan información relevante al modelo y cuáles pueden eliminarse sin afectar significativamente el desempeño.

---

## Datos de entrada

- `data/features_processed.csv`

---

## Variables objetivo

Se entrenaron dos modelos independientes:

- `home_score`: goles del equipo local.
- `away_score`: goles del equipo visitante.

---

## División temporal del conjunto de datos

Con el fin de preservar el orden cronológico y evitar fuga de información, se utilizó una división basada en fechas:

| Conjunto | Periodo |
|------------|---------|
| Entrenamiento | Antes de 2023 |
| Validación | 2023 - 2024 |
| Prueba | Desde 2025 |

Este enfoque permite simular un escenario real de predicción de partidos futuros.

---

## Algoritmo utilizado

Se empleó un modelo de regresión basado en XGBoost (`XGBRegressor`).

### Hiperparámetros utilizados

```python
n_estimators = 500
learning_rate = 0.05
max_depth = 5
subsample = 0.8
colsample_bytree = 0.8
random_state = 42
```

Se entrenó un modelo independiente para:

- Goles del equipo local.
- Goles del equipo visitante.

---

## Métricas de evaluación

Se utilizaron las siguientes métricas:

### Error absoluto medio (MAE)

Evalúa cuántos goles se desvía, en promedio, la predicción respecto al valor real.

### Raíz del error cuadrático medio (RMSE)

Penaliza más fuertemente los errores grandes.

### Accuracy del resultado del partido

Se evaluó la capacidad del modelo para predecir correctamente:

- Victoria local.
- Empate.
- Victoria visitante.

### Exact Score Accuracy

Porcentaje de partidos en los que se predijo exactamente el marcador final.

---

# Modelo 1: Conjunto completo de variables

Se utilizaron todas las características generadas durante la etapa de feature engineering.

### Resultados

| Métrica | Local | Visitante |
|----------|------:|------:|
| MAE | 1.037 | 0.858 |
| RMSE | 1.390 | 1.122 |

#### Accuracy W-D-L

55.4 %

#### Exact Score Accuracy

11.2 %

---

## Importancia de variables

Se analizaron las variables más relevantes según XGBoost para ambos modelos.

Este análisis permitió identificar aquellas características con mayor contribución en la predicción de los goles.

---

# Modelo 2: Eliminación de variables H2H

Se eliminaron:

```python
[
'h2h_home_wins',
'h2h_away_wins',
'h2h_draws',
'h2h_matches'
]
```

### Objetivo

Determinar si el historial directo entre selecciones aportaba información relevante.

### Hallazgo

La eliminación de estas variables produjo un deterioro del desempeño del modelo.

#### Conclusión

El historial entre equipos contiene información útil para la predicción y debe conservarse.

---

# Modelo 3: Eliminación de variables `matches_used`

Se eliminaron:

```python
[
'home_matches_used5',
'away_matches_used5',
'home_matches_used10',
'away_matches_used10'
]
```

### Objetivo

Evaluar si el número de partidos disponibles en las ventanas móviles aportaba información adicional.

### Hallazgo

La eliminación de estas variables produjo únicamente una variación mínima en las métricas.

#### Conclusión

Estas variables poseen una contribución reducida y podrían eliminarse sin afectar significativamente el rendimiento.

---

# Modelo 4: Selección manual de variables importantes

Se construyó un modelo utilizando únicamente variables consideradas relevantes.

### Variables seleccionadas

#### Rendimiento de los últimos diez partidos

- home_GF10
- home_GA10
- home_points10
- home_mean_competition10

- away_GF10
- away_GA10
- away_points10
- away_mean_competition10

#### Sistema Elo

- home_elo
- away_elo
- elo_diff

#### Historial entre selecciones

- h2h_home_wins
- h2h_away_wins
- h2h_draws
- h2h_matches

#### Contexto del partido

- neutral
- competition_level

### Objetivo

Reducir la complejidad del modelo eliminando variables potencialmente redundantes.

### Hallazgo

El modelo mantuvo un desempeño muy similar al modelo completo.

#### Conclusión

La mayor parte de la información predictiva se concentra en un subconjunto relativamente pequeño de variables.

---

# Comparación entre modelos

| Modelo | Descripción |
|----------|---------|
| Modelo 1 | Variables completas |
| Modelo 2 | Sin variables H2H |
| Modelo 3 | Sin variables matches_used |
| Modelo 4 | Variables más relevantes |

---

## Principales hallazgos

### El sistema Elo constituye una de las fuentes de información más importantes.

La diferencia de nivel entre selecciones aporta una gran capacidad predictiva.

---

### El rendimiento reciente de los últimos diez partidos resulta más relevante que el de las últimas cinco jornadas.

Las estadísticas agregadas sobre una ventana más amplia proporcionan mayor estabilidad al modelo.

---

### El historial entre selecciones aporta información adicional.

La eliminación de las variables H2H produjo un empeoramiento del rendimiento, indicando que los enfrentamientos previos contienen información valiosa.

---

### La complejidad del modelo puede reducirse sin perder precisión.

Un subconjunto de variables cuidadosamente seleccionado logró resultados comparables al modelo completo.

---

### La predicción exacta del marcador es un problema altamente complejo.

Aunque el modelo alcanza aproximadamente un 55 % de acierto en el resultado del partido (victoria, empate o derrota), únicamente consigue predecir exactamente el marcador en alrededor del 11 % de los encuentros.

Esto evidencia la elevada incertidumbre inherente al fútbol y la dificultad de estimar el número exacto de goles.

---

## Conclusiones

El análisis permitió comprobar que:

- Las variables relacionadas con el sistema Elo son altamente informativas.
- El rendimiento reciente de las selecciones constituye una fuente importante de información.
- El historial entre equipos aporta valor predictivo.
- Es posible reducir el número de variables manteniendo un desempeño similar.
- La predicción exacta del marcador continúa siendo un problema complejo debido a la naturaleza estocástica del fútbol.

Los resultados obtenidos sirvieron como base para las etapas posteriores de ajuste fino y selección del modelo final.
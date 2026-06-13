# ⚽ Feature Engineering para Predicción de Marcadores de Fútbol

## Descripción

Este notebook tiene como objetivo transformar los resultados históricos de partidos internacionales en un conjunto de variables predictoras que posteriormente serán utilizadas para entrenar modelos de aprendizaje automático capaces de estimar el marcador final de futuros encuentros.

---

## Objetivo

Generar un conjunto de características que describan el rendimiento reciente de cada selección nacional, el contexto competitivo y el historial entre equipos, evitando el uso de información futura (*data leakage*).

---

## Datos de entrada

- `data/results.csv`

El conjunto de datos contiene información histórica de partidos internacionales, incluyendo:

- Fecha del partido.
- Equipo local y visitante.
- Goles anotados por cada selección.
- Torneo disputado.
- Condición de sede neutral.

---

## Preprocesamiento inicial

Se realizaron las siguientes tareas:

1. Conversión de la columna de fechas al formato `datetime`.
2. Ordenamiento cronológico de los partidos.
3. Filtrado de encuentros a partir del año 2000.
4. Separación de los partidos correspondientes al Mundial 2026 para utilizarlos posteriormente como conjunto de prueba.
5. Eliminación de variables no utilizadas:

- `tournament`
- `city`
- `country`
- `competition_category`

---

## Clasificación de competiciones

Cada torneo fue agrupado en categorías con diferentes niveles de importancia competitiva.

| Categoría | Nivel |
|------------|--------|
| Friendly | 1 |
| Regional / Minor Tournament | 2 |
| Qualification | 3 |
| Nations League | 4 |
| Continental Championship | 5 |
| FIFA World Cup | 6 |

Esta codificación permite asignar una mayor relevancia a partidos de alta exigencia competitiva.

---

## Variables generadas

### Rendimiento en los últimos 5 partidos

Para cada selección se calcularon:

- Promedio de goles a favor.
- Promedio de goles en contra.
- Victorias.
- Empates.
- Derrotas.
- Puntos obtenidos.
- Nivel medio de competición.
- Número de partidos utilizados.

Variables:

- `home_GF5`
- `home_GA5`
- `home_W5`
- `home_D5`
- `home_L5`
- `home_points5`
- `home_mean_competition5`
- `home_matches_used5`

Y sus equivalentes para el equipo visitante.

---

### Rendimiento en los últimos 10 partidos

Se calcularon las mismas estadísticas utilizando una ventana de los últimos diez encuentros.

Variables principales:

- `home_GF10`
- `home_GA10`
- `home_points10`
- `home_mean_competition10`
- `home_matches_used10`

- `away_GF10`
- `away_GA10`
- `away_points10`
- `away_mean_competition10`
- `away_matches_used10`

---

### Rachas

Se incorporaron indicadores de forma reciente.

#### Racha de victorias consecutivas

- `home_win_streak`
- `away_win_streak`

#### Racha invicta

- `home_unbeaten_streak`
- `away_unbeaten_streak`

---

## Sistema Elo dinámico

Se implementó un sistema de puntuación Elo inicializado en 1500 puntos para todas las selecciones.

La actualización del rating depende del resultado del partido y del nivel competitivo del torneo.

### Factores K utilizados

| Competición | K |
|-------------|---|
| Friendly | 10 |
| Regional / Minor Tournament | 15 |
| Qualification | 20 |
| Nations League | 25 |
| Continental Championship | 35 |
| FIFA World Cup | 50 |

Variables generadas:

- `home_elo`
- `away_elo`
- `elo_diff`

---

## Historial entre selecciones (Head-to-Head)

Se calcularon estadísticas acumuladas entre ambos equipos antes del partido:

- Victorias del equipo local.
- Victorias del equipo visitante.
- Empates.
- Número total de enfrentamientos.

Variables:

- `h2h_home_wins`
- `h2h_away_wins`
- `h2h_draws`
- `h2h_matches`

---

## Variables de contexto

Se añadieron variables relacionadas con las condiciones del partido:

- `neutral`
- `competition_level`

---

## Variables objetivo

El conjunto final conserva como variables objetivo:

- `home_score`
- `away_score`

Estas variables serán utilizadas posteriormente para entrenar modelos capaces de predecir el número de goles anotados por cada selección.

---

## Prevención de Data Leakage

Todas las características fueron calculadas utilizando únicamente la información disponible antes de cada partido.

Posteriormente, los historiales, ratings Elo y estadísticas H2H fueron actualizados con el resultado recién observado, garantizando que no exista fuga de información hacia el futuro.

---

## Manejo de valores faltantes

Los valores faltantes generados durante los primeros partidos de cada selección fueron reemplazados por cero.

```python
features_df = features_df.fillna(0)
```

---

## Archivo generado

El conjunto de características final fue almacenado en:

```text
data/features.csv
```

Este archivo constituye la base para las etapas posteriores de selección de variables, entrenamiento y evaluación de modelos de predicción de marcadores.
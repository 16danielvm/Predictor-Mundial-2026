# ⚽ Modelo Final de Predicción de Marcadores

## Descripción

En esta etapa se construyó y optimizó el modelo final de predicción de marcadores utilizando XGBoost. A partir de los resultados obtenidos durante las etapas anteriores, se seleccionó un conjunto reducido de variables con mayor capacidad predictiva y se realizó una búsqueda de hiperparámetros para maximizar el desempeño del modelo.

Se entrenaron dos modelos independientes:

- Predicción de goles del equipo local.
- Predicción de goles del equipo visitante.

---

## Datos de entrada

- `data/features_processed.csv`

---

## Variables seleccionadas

Con base en el análisis previo de importancia de características, se utilizaron las siguientes variables:

### Rendimiento de los últimos diez partidos

- `home_GF10`
- `home_GA10`
- `home_points10`
- `home_mean_competition10`

- `away_GF10`
- `away_GA10`
- `away_points10`
- `away_mean_competition10`

### Sistema Elo

- `home_elo`
- `away_elo`
- `elo_diff`

### Historial entre selecciones

- `h2h_home_wins`
- `h2h_away_wins`
- `h2h_draws`
- `h2h_matches`

### Contexto del partido

- `neutral`
- `competition_level`

En total se utilizaron **17 variables predictoras**.

---

## División temporal del conjunto de datos

Con el propósito de preservar el orden cronológico de los partidos y simular un escenario real de predicción, se empleó la siguiente división:

| Conjunto | Periodo |
|------------|---------|
| Entrenamiento | Antes de 2023 |
| Validación | 2023 - 2024 |
| Prueba | Desde 2025 |

---

## Optimización de hiperparámetros

Se utilizó `RandomizedSearchCV` con validación cruzada de tres particiones para encontrar la mejor configuración del modelo.

### Espacio de búsqueda

- Número de árboles (`n_estimators`)
- Profundidad máxima (`max_depth`)
- Tasa de aprendizaje (`learning_rate`)
- Submuestreo (`subsample`)
- Muestreo de columnas (`colsample_bytree`)
- Peso mínimo por nodo (`min_child_weight`)
- Factor de poda (`gamma`)
- Regularización L1 (`reg_alpha`)
- Regularización L2 (`reg_lambda`)

La optimización se realizó de manera independiente para:

- Modelo de goles del equipo local.
- Modelo de goles del equipo visitante.

---

## Métricas de evaluación

Se evaluó el desempeño mediante:

### Mean Absolute Error (MAE)

Mide el error promedio en número de goles.

### Root Mean Squared Error (RMSE)

Penaliza con mayor peso los errores grandes.

### Accuracy W-D-L

Porcentaje de aciertos en la predicción del resultado del partido:

- Victoria local.
- Empate.
- Victoria visitante.

### Exact Score Accuracy

Porcentaje de partidos en los que se predijo exactamente el marcador final.

---

## Evaluación sobre el conjunto de validación

Una vez obtenidos los mejores hiperparámetros, se evaluó el modelo sobre los partidos correspondientes al periodo 2023-2024.

Posteriormente, las predicciones continuas fueron redondeadas al entero más cercano para obtener un marcador interpretable.

Además del marcador exacto, se calculó la capacidad del modelo para predecir correctamente el resultado del partido (victoria, empate o derrota).

---

## Evaluación sobre el conjunto de prueba

El modelo final fue evaluado utilizando partidos no observados durante el entrenamiento ni durante la optimización.

Las métricas calculadas fueron:

- MAE Home
- MAE Away
- RMSE Home
- RMSE Away
- Accuracy WDL
- Exact Score Accuracy

Esta etapa permitió estimar la capacidad de generalización del modelo frente a encuentros futuros.

---

## Predicción de partidos futuros

Se desarrollaron funciones auxiliares para construir automáticamente las características necesarias de un encuentro que aún no se ha disputado.

### Obtención de estadísticas recientes

Se recuperan las características más recientes de cada selección:

- Rendimiento ofensivo.
- Rendimiento defensivo.
- Puntos obtenidos.
- Nivel medio de competición.
- Puntuación Elo.

### Historial entre equipos

Se calculan:

- Victorias del equipo local.
- Victorias del equipo visitante.
- Empates.
- Número total de enfrentamientos.

### Variables contextuales

- Nivel de competición.
- Condición de sede neutral.

---

## Función de predicción

Se implementó la función:

```python
predict_match_score()
```

La cual recibe:

- Equipo local.
- Equipo visitante.
- Fecha del partido.
- Nivel competitivo.
- Condición de sede neutral.
- Modelos entrenados.

Y devuelve:

- Predicción continua de goles.
- Marcador redondeado.
- Variables utilizadas en la predicción.

---

## Caso de estudio

Como prueba de funcionamiento, se realizó una predicción para el encuentro:

- Estados Unidos vs Paraguay
- Copa Mundial de la FIFA 2026

Este ejemplo permitió verificar la capacidad del sistema para generar predicciones sobre partidos aún no disputados.

---

## Persistencia del modelo

Finalmente, los modelos optimizados fueron almacenados utilizando Joblib.

### Archivos generados

```text
models/home_model.pkl
models/away_model.pkl
```

Asimismo, el conjunto de datos definitivo fue exportado como:

```text
data/features_final.csv
```

---

## Principales hallazgos

### Un subconjunto reducido de variables fue suficiente para obtener un buen desempeño

La información más relevante quedó concentrada en:

- Rendimiento reciente.
- Sistema Elo.
- Historial entre selecciones.
- Contexto competitivo.

---

### La optimización de hiperparámetros permitió mejorar la capacidad predictiva

La búsqueda aleatoria permitió encontrar configuraciones más adecuadas que las utilizadas inicialmente.

---

### El problema de predicción del marcador continúa siendo altamente complejo

Debido a la naturaleza estocástica del fútbol, predecir exactamente el marcador es considerablemente más difícil que predecir únicamente el resultado del encuentro.

---

### El modelo es capaz de generalizar a partidos futuros

La evaluación sobre datos completamente no observados permitió verificar que el modelo mantiene un desempeño consistente fuera del conjunto de entrenamiento.

---

## Conclusiones

Se obtuvo un modelo final basado en XGBoost capaz de predecir los goles anotados por ambas selecciones a partir de información histórica y contextual.

La combinación del rendimiento reciente, las puntuaciones Elo, el historial entre equipos y las características del encuentro permitió construir un sistema con capacidad para generar predicciones sobre partidos futuros, constituyendo la base del sistema desarrollado para la Copa Mundial de la FIFA 2026.
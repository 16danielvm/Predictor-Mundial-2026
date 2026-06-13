# ⚽ Predictor de Marcadores - Mundial 2026

Sistema de predicción de marcadores de fútbol basado en **Machine Learning**, desarrollado con **XGBoost** y desplegado mediante **Streamlit**.

La aplicación utiliza información histórica de partidos internacionales para estimar:

- El marcador más probable.
- Los goles esperados de cada selección.
- La probabilidad de victoria local, empate y victoria visitante.
- Los diez marcadores más probables.

Este proyecto fue desarrollado con fines recreativos y de entretenimiento, aprovechando la fiebre mundialista generada por la Copa Mundial de la FIFA 2026.

---

# 🌐 Aplicación web

La aplicación se encuentra disponible en:

## https://predictormundial2026.streamlit.app/

No es necesario instalar nada. Basta con acceder desde cualquier navegador.

---

# 🚀 ¿Cómo utilizar la aplicación?

Para generar una predicción es necesario seleccionar:

- ⚽ Equipo local.
- ⚽ Equipo visitante.
- 📅 Fecha del partido.
- 🏆 Nivel de competición.
- 🌎 Si el encuentro se disputa en sede neutral.

Posteriormente, basta con presionar el botón:

```text
Predecir marcador
```

La aplicación mostrará:

- ⚽ El marcador más probable.
- 📈 Los goles esperados de cada equipo.
- 🏆 Probabilidad de victoria local.
- 🤝 Probabilidad de empate.
- 🥅 Probabilidad de victoria visitante.
- 📊 Los diez marcadores más probables.
- 🔍 Variables utilizadas por el modelo.

---

# 📈 Ejemplo de salida

La aplicación proporciona información como:

```text
Marcador más probable

United States 2 - 1 Paraguay

Probabilidad del marcador: 9.84%

Goles esperados

United States: 1.93
Paraguay: 0.98

Probabilidades del resultado

Victoria Estados Unidos: 56.2%
Empate: 22.4%
Victoria Paraguay: 21.4%
```

---

# ⚙️ Metodología

El desarrollo del proyecto se realizó en cuatro etapas principales.

## 1. Feature Engineering

Se construyeron variables relacionadas con:

- Rendimiento reciente.
- Sistema Elo dinámico.
- Historial entre selecciones (Head-to-Head).
- Contexto competitivo.

📁 Documentación:

```text
data_collection/README.MD
```

---

## 2. Análisis Exploratorio de Datos

Se estudiaron:

- Distribución de los goles.
- Distribución de las puntuaciones Elo.
- Correlaciones entre variables.
- Variables con mayor relación con los goles anotados.

📁 Documentación:

```text
EDA/README.MD
```

---

## 3. Comparación de modelos

Se evaluaron diferentes conjuntos de variables con el objetivo de identificar aquellas con mayor capacidad predictiva.

📁 Documentación:

```text
modelado/README.MD
```

---

## 4. Modelo final

Se seleccionó un subconjunto de variables y se optimizaron los hiperparámetros mediante búsqueda aleatoria y validación cruzada.

📁 Documentación:

```text
modelo_final/README.MD
```

---

# 🧠 Modelo de Machine Learning

Se entrenaron dos modelos independientes mediante **XGBoost Regressor**:

- Modelo para goles del equipo local.
- Modelo para goles del equipo visitante.

Posteriormente, las predicciones de goles esperados son transformadas en probabilidades de marcadores utilizando una distribución de Poisson.

---

# 📊 Variables utilizadas

El modelo final emplea 17 variables agrupadas en cuatro categorías.

## Rendimiento de los últimos 10 partidos

- Goles a favor.
- Goles en contra.
- Puntos obtenidos.
- Nivel promedio de competición.

## Sistema Elo

- Elo del equipo local.
- Elo del equipo visitante.
- Diferencia Elo.

## Historial entre selecciones

- Victorias del equipo local.
- Victorias del equipo visitante.
- Empates.
- Número total de enfrentamientos.

## Contexto del partido

- Nivel competitivo.
- Sede neutral.

---

# 🔍 Principales hallazgos

- La diferencia Elo constituye una de las variables más importantes del modelo.
- El rendimiento reciente aporta una gran capacidad predictiva.
- El historial entre equipos mejora ligeramente el desempeño.
- Un subconjunto reducido de variables produce resultados similares al modelo completo.
- La predicción exacta del marcador es considerablemente más difícil que la predicción del resultado del partido.
- La fortaleza defensiva del rival resulta más influyente que la capacidad ofensiva propia.

---

# 🛠 Tecnologías utilizadas

## Lenguaje

- Python

## Ciencia de datos

- Pandas
- NumPy

## Machine Learning

- Scikit-Learn
- XGBoost

## Modelado probabilístico

- SciPy

## Persistencia de modelos

- Joblib

## Aplicación web

- Streamlit

---

# 📦 Requisitos

```text
streamlit
pandas
numpy
scikit-learn
xgboost
joblib
scipy
```

---

# ⚠️ Aviso

Las predicciones generadas por el sistema representan estimaciones estadísticas obtenidas a partir de información histórica y no garantizan el resultado real de los encuentros.

El fútbol es un deporte con una elevada incertidumbre inherente, por lo que los resultados mostrados deben interpretarse únicamente con fines recreativos y de entretenimiento.
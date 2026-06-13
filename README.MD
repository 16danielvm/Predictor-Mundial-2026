# ⚽ Predictor de Marcadores - Mundial 2026

Sistema de predicción de marcadores de fútbol basado en **Machine Learning**, desarrollado con **XGBoost** y desplegado mediante **Streamlit**.

La aplicación utiliza información histórica de partidos internacionales para estimar:

- El marcador más probable.
- Los goles esperados para cada selección.
- La probabilidad de victoria local, empate y victoria visitante.
- Los diez marcadores más probables.

Este proyecto fue desarrollado con fines recreativos y de entretenimiento, aprovechando la fiebre mundialista generada por la Copa Mundial de la FIFA 2026 durante los meses de junio y julio de 2026.

---

## 🚀 Características

- Predicción del número de goles de ambos equipos mediante modelos XGBoost.
- Sistema Elo dinámico.
- Variables basadas en el rendimiento reciente de las selecciones.
- Historial de enfrentamientos directos (Head-to-Head).
- Consideración del contexto competitivo del partido.
- Cálculo de probabilidades utilizando la distribución de Poisson.
- Interfaz web interactiva desarrollada con Streamlit.

---

## 📊 Variables utilizadas

El modelo final utiliza 17 características:

### Rendimiento de los últimos 10 partidos

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

---

## ⚙️ Modelo de Machine Learning

Se entrenaron dos modelos independientes utilizando **XGBoost Regressor**:

- Modelo para los goles del equipo local.
- Modelo para los goles del equipo visitante.

Los hiperparámetros fueron optimizados mediante **Randomized Search con validación cruzada**.

---

## 📈 Probabilidades de los marcadores

El modelo estima primero los goles esperados de cada selección.

Posteriormente, mediante la distribución de Poisson, se calculan:

- Probabilidades de cada marcador posible.
- Probabilidad de victoria local.
- Probabilidad de empate.
- Probabilidad de victoria visitante.

La aplicación presenta:

- Marcador más probable.
- Goles esperados.
- Probabilidades del resultado.
- Los diez marcadores con mayor probabilidad.

---

## 📂 Estructura del proyecto

```text
.
├── data
│
├── data_collection
│   ├── featureengine.ipynb
│   └── README.MD
│
├── EDA
│   ├── Eda.ipynb
│   └── README.MD
│
├── modelado
│   ├── modelado.ipynb
│   └── README.MD
│
├── modelo_final
│   ├── GridSearch.ipynb
│   └── README.MD
│
├── models
│   ├── home_model.pkl
│   └── away_model.pkl
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 📦 Requisitos

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

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/usuario/predictor-mundial-2026.git
```

Ingresar al directorio:

```bash
cd predictor-mundial-2026
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

Para iniciar la aplicación:

```bash
streamlit run app.py
```

La interfaz estará disponible en:

```text
http://localhost:8501
```

---

## 🖥️ Uso

1. Seleccionar el equipo local.
2. Seleccionar el equipo visitante.
3. Elegir la fecha del partido.
4. Seleccionar el nivel de competición.
5. Indicar si el partido se disputa en sede neutral.
6. Presionar **"Predecir marcador"**.

La aplicación mostrará:

- Marcador más probable.
- Goles esperados para ambos equipos.
- Probabilidades de victoria local, empate y victoria visitante.
- Los diez marcadores con mayor probabilidad.
- Variables utilizadas por el modelo para realizar la predicción.

---

## 🔬 Metodología

El proyecto fue desarrollado en cuatro etapas principales.

### 1. Feature Engineering

Se construyeron variables relacionadas con:

- Rendimiento reciente.
- Sistema Elo.
- Historial entre selecciones.
- Contexto competitivo.

Documentación disponible en:

```text
data_collection/README.MD
```

---

### 2. Análisis Exploratorio de Datos

Se analizaron:

- Distribuciones de las variables.
- Correlaciones.
- Variables con mayor influencia sobre los goles.

Documentación disponible en:

```text
EDA/README.MD
```

---

### 3. Comparación de modelos

Se evaluaron diferentes conjuntos de variables para identificar aquellas con mayor capacidad predictiva.

Documentación disponible en:

```text
modelado/README.MD
```

---

### 4. Construcción del modelo final

Se seleccionó un subconjunto de variables y se optimizaron los hiperparámetros mediante búsqueda aleatoria.

Documentación disponible en:

```text
modelo_final/README.MD
```

---

## 🔍 Principales hallazgos

- La diferencia Elo constituye una de las variables más importantes del modelo.
- El rendimiento reciente de las selecciones aporta una gran capacidad predictiva.
- El historial entre equipos mejora ligeramente las predicciones.
- Un conjunto reducido de variables permite obtener resultados similares al modelo completo.
- La predicción exacta del marcador es considerablemente más compleja que la predicción del resultado del partido.

---

## 🛠 Tecnologías utilizadas

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- Streamlit
- Joblib

---

## ⚠️ Aviso

Este proyecto fue desarrollado con fines recreativos y de entretenimiento durante la Copa Mundial de la FIFA 2026.

Las predicciones generadas por el sistema representan estimaciones estadísticas basadas en información histórica y no garantizan el resultado real de los encuentros.
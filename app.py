import streamlit as st
import pandas as pd
import joblib
from scipy.stats import poisson


# =========================
# Configuración
# =========================

st.set_page_config(
    page_title="Predictor Mundial 2026",
    page_icon="⚽",
    layout="wide"
)

DATA_PATH = "data/features_final.csv"
HOME_MODEL_PATH = "models/home_model.pkl"
AWAY_MODEL_PATH = "models/away_model.pkl"


selected_features_m4 = [
    "home_GF10",
    "home_GA10",
    "home_points10",
    "home_mean_competition10",

    "away_GF10",
    "away_GA10",
    "away_points10",
    "away_mean_competition10",

    "home_elo",
    "away_elo",
    "elo_diff",

    "h2h_home_wins",
    "h2h_away_wins",
    "h2h_draws",
    "h2h_matches",

    "neutral",
    "competition_level"
]


# =========================
# Carga de datos y modelos
# =========================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_resource
def load_models():
    home_model = joblib.load(HOME_MODEL_PATH)
    away_model = joblib.load(AWAY_MODEL_PATH)
    return home_model, away_model


features_df = load_data()
home_model, away_model = load_models()


# =========================
# Funciones
# =========================

def get_latest_team_features(features_df, team, match_date):
    match_date = pd.to_datetime(match_date)

    team_matches = features_df[
        (
            (features_df["home_team"] == team) |
            (features_df["away_team"] == team)
        ) &
        (features_df["date"] < match_date)
    ].sort_values("date")

    if len(team_matches) == 0:
        raise ValueError(f"No hay partidos previos para {team}")

    last_match = team_matches.iloc[-1]

    if last_match["home_team"] == team:
        return {
            "GF10": last_match["home_GF10"],
            "GA10": last_match["home_GA10"],
            "points10": last_match["home_points10"],
            "mean_competition10": last_match["home_mean_competition10"],
            "elo": last_match["home_elo"]
        }

    return {
        "GF10": last_match["away_GF10"],
        "GA10": last_match["away_GA10"],
        "points10": last_match["away_points10"],
        "mean_competition10": last_match["away_mean_competition10"],
        "elo": last_match["away_elo"]
    }


def get_h2h_features(features_df, home_team, away_team, match_date):
    match_date = pd.to_datetime(match_date)

    h2h_matches = features_df[
        (
            (
                (features_df["home_team"] == home_team) &
                (features_df["away_team"] == away_team)
            )
            |
            (
                (features_df["home_team"] == away_team) &
                (features_df["away_team"] == home_team)
            )
        )
        &
        (features_df["date"] < match_date)
    ]

    h2h_home_wins = 0
    h2h_away_wins = 0
    h2h_draws = 0

    for _, row in h2h_matches.iterrows():
        if row["home_score"] == row["away_score"]:
            h2h_draws += 1
        elif row["home_score"] > row["away_score"]:
            winner = row["home_team"]
            if winner == home_team:
                h2h_home_wins += 1
            else:
                h2h_away_wins += 1
        else:
            winner = row["away_team"]
            if winner == home_team:
                h2h_home_wins += 1
            else:
                h2h_away_wins += 1

    return {
        "h2h_home_wins": h2h_home_wins,
        "h2h_away_wins": h2h_away_wins,
        "h2h_draws": h2h_draws,
        "h2h_matches": len(h2h_matches)
    }


def build_future_match_features(
    features_df,
    home_team,
    away_team,
    match_date,
    competition_level,
    neutral
):
    home_f = get_latest_team_features(features_df, home_team, match_date)
    away_f = get_latest_team_features(features_df, away_team, match_date)
    h2h_f = get_h2h_features(features_df, home_team, away_team, match_date)

    row = {
        "home_GF10": home_f["GF10"],
        "home_GA10": home_f["GA10"],
        "home_points10": home_f["points10"],
        "home_mean_competition10": home_f["mean_competition10"],

        "away_GF10": away_f["GF10"],
        "away_GA10": away_f["GA10"],
        "away_points10": away_f["points10"],
        "away_mean_competition10": away_f["mean_competition10"],

        "home_elo": home_f["elo"],
        "away_elo": away_f["elo"],
        "elo_diff": home_f["elo"] - away_f["elo"],

        "h2h_home_wins": h2h_f["h2h_home_wins"],
        "h2h_away_wins": h2h_f["h2h_away_wins"],
        "h2h_draws": h2h_f["h2h_draws"],
        "h2h_matches": h2h_f["h2h_matches"],

        "neutral": neutral,
        "competition_level": competition_level
    }

    return pd.DataFrame([row])[selected_features_m4]


# def predict_match_score(
#     features_df,
#     home_team,
#     away_team,
#     match_date,
#     competition_level,
#     neutral,
#     home_model,
#     away_model
# ):
#     match_features = build_future_match_features(
#         features_df,
#         home_team,
#         away_team,
#         match_date,
#         competition_level,
#         neutral
#     )

#     home_pred_raw = home_model.predict(match_features)[0]
#     away_pred_raw = away_model.predict(match_features)[0]

#     home_pred = max(int(round(home_pred_raw)), 0)
#     away_pred = max(int(round(away_pred_raw)), 0)

#     return home_pred_raw, away_pred_raw, home_pred, away_pred, match_features

def predict_match_score(
    features_df,
    home_team,
    away_team,
    match_date,
    competition_level,
    neutral,
    home_model,
    away_model
):
    match_features = build_future_match_features(
        features_df,
        home_team,
        away_team,
        match_date,
        competition_level,
        neutral
    )

    home_lambda = home_model.predict(match_features)[0]
    away_lambda = away_model.predict(match_features)[0]

    home_lambda = max(home_lambda, 0.01)
    away_lambda = max(away_lambda, 0.01)

    scores_df = score_probability_matrix(
        home_lambda=home_lambda,
        away_lambda=away_lambda,
        max_goals=6
    )

    most_likely = scores_df.iloc[0]

    home_win_prob = scores_df[
        scores_df["home_goals"] > scores_df["away_goals"]
    ]["probability"].sum()

    draw_prob = scores_df[
        scores_df["home_goals"] == scores_df["away_goals"]
    ]["probability"].sum()

    away_win_prob = scores_df[
        scores_df["home_goals"] < scores_df["away_goals"]
    ]["probability"].sum()

    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_lambda": home_lambda,
        "away_lambda": away_lambda,
        "home_pred": int(most_likely["home_goals"]),
        "away_pred": int(most_likely["away_goals"]),
        "most_likely_score": most_likely["score"],
        "most_likely_probability": most_likely["probability_pct"],
        "home_win_prob": home_win_prob * 100,
        "draw_prob": draw_prob * 100,
        "away_win_prob": away_win_prob * 100,
        "scores_df": scores_df,
        "match_features": match_features
    }

# def score_probability_matrix(home_lambda, away_lambda, max_goals=6):
#     scores = []

#     for home_goals in range(max_goals + 1):
#         for away_goals in range(max_goals + 1):

#             prob_home = poisson.pmf(home_goals, home_lambda)
#             prob_away = poisson.pmf(away_goals, away_lambda)

#             prob = prob_home * prob_away

#             scores.append({
#                 "home_goals": home_goals,
#                 "away_goals": away_goals,
#                 "score": f"{home_goals}-{away_goals}",
#                 "probability": prob
#             })

#     scores_df = pd.DataFrame(scores)
#     scores_df["probability_pct"] = scores_df["probability"] * 100

#     return scores_df.sort_values("probability", ascending=False)

def score_probability_matrix(home_lambda, away_lambda, max_goals=6):
    scores = []

    home_lambda = max(home_lambda, 0.01)
    away_lambda = max(away_lambda, 0.01)

    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            prob = (
                poisson.pmf(home_goals, home_lambda)
                *
                poisson.pmf(away_goals, away_lambda)
            )

            scores.append({
                "home_goals": home_goals,
                "away_goals": away_goals,
                "score": f"{home_goals}-{away_goals}",
                "probability": prob,
                "probability_pct": prob * 100
            })

    scores_df = pd.DataFrame(scores)
    scores_df = scores_df.sort_values("probability", ascending=False)

    return scores_df

# =========================
# Interfaz
# =========================

st.title("⚽ Predictor de Marcadores - Mundial 2026")
st.caption("Modelo XGBoost basado en Elo, forma reciente, H2H y contexto competitivo.")

teams = sorted(
    set(features_df["home_team"].unique()).union(
        set(features_df["away_team"].unique())
    )
)

col1, col2 = st.columns(2)

with col1:
    home_team = st.selectbox("Equipo local", teams, index=teams.index("United States") if "United States" in teams else 0)

with col2:
    away_team = st.selectbox("Equipo visitante", teams, index=teams.index("Paraguay") if "Paraguay" in teams else 1)

col3, col4, col5 = st.columns(3)

with col3:
    match_date = st.date_input("Fecha del partido", value=pd.to_datetime("2026-06-12"))

with col4:
    competition_level = st.selectbox(
        "Nivel de competición",
        options=[1, 2, 3, 4, 5, 6],
        index=5,
        format_func=lambda x: {
            1: "Friendly",
            2: "Regional / Minor",
            3: "Qualification",
            4: "Nations League",
            5: "Continental Championship",
            6: "FIFA World Cup"
        }[x]
    )

with col5:
    neutral = st.selectbox(
        "¿Sede neutral?",
        options=[0, 1],
        index=0,
        format_func=lambda x: "No" if x == 0 else "Sí"
    )


if st.button("Predecir marcador", type="primary"):
    if home_team == away_team:
        st.error("El equipo local y visitante no pueden ser el mismo.")
    else:
        try:
            # home_raw, away_raw, home_pred, away_pred, match_features = predict_match_score(
            #     features_df=features_df,
            #     home_team=home_team,
            #     away_team=away_team,
            #     match_date=match_date,
            #     competition_level=competition_level,
            #     neutral=neutral,
            #     home_model=home_model,
            #     away_model=away_model
            # )

            # scores_df = score_probability_matrix(
            #     home_lambda=max(home_raw, 0.01),
            #     away_lambda=max(away_raw, 0.01),
            #     max_goals=6
            # )

            # st.subheader("Marcador predicho")

            # c1, c2, c3 = st.columns([2, 1, 2])

            # with c1:
            #     st.metric(home_team, home_pred)

            # with c2:
            #     st.markdown(
            #         "<h1 style='text-align: center;'>-</h1>",
            #         unsafe_allow_html=True
            #     )

            # with c3:
            #     st.metric(away_team, away_pred)

            # st.write("Predicción cruda:")
            # st.write(f"{home_team}: {home_raw:.3f}")
            # st.write(f"{away_team}: {away_raw:.3f}")

            # with st.expander("Ver variables usadas por el modelo"):
            #     st.dataframe(match_features, use_container_width=True)
            prediction = predict_match_score(
                features_df=features_df,
                home_team=home_team,
                away_team=away_team,
                match_date=match_date,
                competition_level=competition_level,
                neutral=neutral,
                home_model=home_model,
                away_model=away_model
            )

            st.subheader("Marcador más probable")

            col_a, col_b, col_c = st.columns([2, 1, 2])

            with col_a:
                st.metric(home_team, prediction["home_pred"])

            with col_b:
                st.markdown("<h1 style='text-align: center;'>-</h1>", unsafe_allow_html=True)

            with col_c:
                st.metric(away_team, prediction["away_pred"])

            st.write(
                f"Probabilidad del marcador {prediction['most_likely_score']}: "
                f"{prediction['most_likely_probability']:.2f}%"
            )

            st.subheader("Goles esperados")
            st.write(f"{home_team}: {prediction['home_lambda']:.2f}")
            st.write(f"{away_team}: {prediction['away_lambda']:.2f}")

            st.subheader("Probabilidades del resultado")

            col1, col2, col3 = st.columns(3)

            col1.metric(f"Gana {home_team}", f"{prediction['home_win_prob']:.1f}%")
            col2.metric("Empate", f"{prediction['draw_prob']:.1f}%")
            col3.metric(f"Gana {away_team}", f"{prediction['away_win_prob']:.1f}%")

            st.subheader("Top 10 marcadores más probables")

            top_scores = prediction["scores_df"].head(10).copy()
            top_scores["probability_pct"] = top_scores["probability_pct"].round(2)

            st.dataframe(
                top_scores[["score", "probability_pct"]],
                use_container_width=True
            )

            with st.expander("Ver variables usadas por el modelo"):
                st.dataframe(prediction["match_features"], use_container_width=True)
            
            # st.subheader("Marcadores más probables")
            # st.dataframe(
            #     scores_df[["score", "probability"]].head(10).reset_index(drop=True).style.format({"probability": "{:.2%}"}),
            #     use_container_width=True
            # )

            # home_win_prob = scores_df[scores_df["home_goals"] > scores_df["away_goals"]]["probability"].sum()
            # draw_prob = scores_df[scores_df["home_goals"] == scores_df["away_goals"]]["probability"].sum()
            # away_win_prob = scores_df[scores_df["home_goals"] < scores_df["away_goals"]]["probability"].sum()

            # st.subheader("Probabilidades del resultado")
            # st.write(f"{home_team} gana: {home_win_prob*100:.1f}%")
            # st.write(f"Empate: {draw_prob*100:.1f}%")
            # st.write(f"{away_team} gana: {away_win_prob*100:.1f}%")

        except Exception as e:
            st.error(f"No se pudo generar la predicción: {e}")
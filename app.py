"""
app.py
Football Player Performance Analytics Dashboard
Run:  streamlit run app.py
"""

# ── SECTION 1 — Imports and page config ──────────────────────────────────────

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── SECTION 3 — Custom CSS (dark green theme) ─────────────────────────────────
# (Defined before data loading so the theme is applied on first render)

st.markdown(
    """
    <style>
    /* ── Global background ── */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
        font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }
    section[data-testid="stSidebar"] * {
        color: #e6edf3 !important;
    }

    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background-color: #1c2128;
        border-left: 4px solid #00c853;
        border-radius: 8px;
        padding: 12px 16px;
    }
    div[data-testid="metric-container"] label {
        color: #8b949e !important;
        font-size: 0.82rem;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e6edf3 !important;
        font-size: 1.6rem;
        font-weight: 700;
    }

    /* ── General text ── */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #e6edf3;
    }
    .stCaption, .st-emotion-cache-1wbqy5l {
        color: #8b949e !important;
    }

    /* ── Info / warning / error boxes ── */
    .stAlert {
        background-color: #1c2128 !important;
        border-radius: 6px;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        background-color: #1c2128;
    }

    /* ── Buttons ── */
    .stButton > button, .stDownloadButton > button {
        background-color: #1a7431;
        color: #e6edf3;
        border: 1px solid #00c853;
        border-radius: 6px;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #00c853;
        color: #0d1117;
    }

    /* ── Inputs / selects ── */
    .stTextInput > div > div > input,
    .stMultiSelect > div,
    .stSelectbox > div {
        background-color: #1c2128 !important;
        color: #e6edf3 !important;
        border-color: #30363d !important;
    }

    /* ── Horizontal rule ── */
    hr {
        border-color: #30363d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── SECTION 2 — Data loading and generation ───────────────────────────────────

# Constants (mirrored from generate_dataset.py so generate_data() is self-contained)
_CLUBS = [
    "Albion FC", "Red City United", "Northern Dynamo", "Eastbridge Athletic",
    "Westgate Rovers", "Southvale City", "Ironport FC", "Thornfield United",
    "Crestwood Rangers", "Dawnfield Sporting",
]
_POSITIONS = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
_NATIONALITIES = [
    "English", "Spanish", "French", "Brazilian", "Argentine",
    "German", "Italian", "Dutch", "Portuguese", "Nigerian",
]
_SEASONS = ["2022-23", "2023-24"]
_N_PLAYERS = 120
_POSITION_COUNTS = {"Goalkeeper": 12, "Defender": 36, "Midfielder": 42, "Forward": 30}
_FIRST_NAMES = [
    "Marcus", "Luca", "Ethan", "Noah", "James", "Carlos", "Felix", "Hugo",
    "Ivan", "Omar", "Ravi", "Leo", "Finn", "Kai", "Max", "Rafael",
    "Sergio", "Theo", "Yusuf", "Zane", "Aaron", "Blake", "Cole", "Diego",
    "Eli", "Franco", "Gael", "Hector", "Iker", "Javi", "Kyle", "Luis",
    "Mario", "Noel", "Oscar", "Pedro", "Quinn", "Ruben", "Sam", "Tomas",
    "Umar", "Victor", "Will", "Xavi", "Yann", "Zico", "Andre", "Bruno",
    "Cesc", "Dani", "Emil", "Fede", "Glen", "Hans", "Ian", "Joel",
    "Kev", "Lars", "Marc", "Nico", "Olly", "Phil", "Renato", "Stefan",
]
_LAST_NAMES = [
    "Hale", "Cruz", "Morin", "Santos", "Diaz", "Bauer", "Ricci", "Vos",
    "Faria", "Eze", "Shah", "Blanc", "Koch", "Lopes", "Moran", "Nunes",
    "Park", "Quinn", "Russo", "Teixeira", "Uddin", "Vargas", "Webb", "Xu",
    "Yates", "Zelaya", "Alves", "Braga", "Couto", "Duarte", "Estrada",
    "Ferreira", "Gomez", "Hart", "Ibarra", "Jimenez", "Kuhn", "Leone",
    "Matos", "Navarro", "Oliveira", "Pinto", "Ramos", "Sousa", "Torres",
    "Uribe", "Vieira", "Wade", "Xara", "Yilmaz", "Zimmermann", "Abreu",
    "Bento", "Castillo", "Da Silva", "Enrique", "Flores", "Guerrero",
    "Herrera", "Iglesias", "Jorge", "Klose", "Lainez", "Miranda",
]

_REQUIRED_COLUMNS = [
    "player_id", "player_name", "season", "team", "position", "age",
    "nationality", "appearances", "minutes_played", "goals", "assists",
    "shots", "shots_on_target", "pass_accuracy", "dribbles", "tackles",
    "yellow_cards", "red_cards", "clean_sheets", "rating",
]


def _make_names(n: int) -> list:
    rng_first = np.random.choice(_FIRST_NAMES, size=n, replace=True)
    rng_last = np.random.choice(
        _LAST_NAMES, size=n, replace=False if n <= len(_LAST_NAMES) else True
    )
    seen: set = set()
    names: list = []
    for f, l in zip(rng_first, rng_last):
        name = f"{f} {l}"
        while name in seen:
            name = f"{f} {np.random.choice(_LAST_NAMES)}"
        seen.add(name)
        names.append(name)
    return names


def _sample_stats(position: str, n: int) -> dict:
    ri = np.random.randint
    ru = np.random.uniform
    appearances = ri(5, 38, n)
    minutes_played = np.clip(appearances * ri(60, 96, n), 300, 3420).astype(int)

    if position == "Goalkeeper":
        goals, assists = np.zeros(n, int), np.zeros(n, int)
        shots, shots_on_target = np.zeros(n, int), np.zeros(n, int)
        pass_accuracy = ru(55, 80, n).round(1)
        dribbles = ri(0, 3, n)
        tackles = ri(0, 10, n)
        yellow_cards = ri(0, 3, n)
        red_cards = (ru(0, 1, n) < 0.04).astype(int)
        clean_sheets = ri(4, 19, n)
    elif position == "Defender":
        goals = ri(0, 6, n)
        assists = ri(0, 7, n)
        shots = ri(2, 20, n)
        shots_on_target = np.minimum(shots, ri(0, 10, n))
        pass_accuracy = ru(68, 90, n).round(1)
        dribbles = ri(2, 20, n)
        tackles = ri(30, 81, n)
        yellow_cards = ri(0, 8, n)
        red_cards = (ru(0, 1, n) < 0.08).astype(int)
        clean_sheets = ri(0, 11, n)
    elif position == "Midfielder":
        goals = ri(1, 13, n)
        assists = ri(3, 16, n)
        shots = ri(10, 41, n)
        shots_on_target = np.minimum(shots, ri(4, 20, n))
        pass_accuracy = ru(72, 93, n).round(1)
        dribbles = ri(10, 50, n)
        tackles = ri(15, 55, n)
        yellow_cards = ri(0, 7, n)
        red_cards = (ru(0, 1, n) < 0.05).astype(int)
        clean_sheets = np.zeros(n, int)
    else:  # Forward
        goals = ri(5, 26, n)
        assists = ri(1, 12, n)
        shots = ri(20, 81, n)
        shots_on_target = np.minimum(shots, ri(8, 40, n))
        pass_accuracy = ru(65, 86, n).round(1)
        dribbles = ri(15, 60, n)
        tackles = ri(5, 30, n)
        yellow_cards = ri(0, 6, n)
        red_cards = (ru(0, 1, n) < 0.05).astype(int)
        clean_sheets = np.zeros(n, int)

    return dict(
        appearances=appearances, minutes_played=minutes_played,
        goals=goals, assists=assists, shots=shots,
        shots_on_target=shots_on_target, pass_accuracy=pass_accuracy,
        dribbles=dribbles, tackles=tackles, yellow_cards=yellow_cards,
        red_cards=red_cards, clean_sheets=clean_sheets,
    )


def _compute_rating(df: pd.DataFrame) -> pd.Series:
    weights = {
        "Goalkeeper":  {"goals": 0.02, "assists": 0.02, "pass_accuracy": 0.20,
                        "clean_sheets": 0.40, "tackles": 0.10, "dribbles": 0.05,
                        "shots_on_target": 0.01, "appearances": 0.20},
        "Defender":    {"goals": 0.05, "assists": 0.05, "pass_accuracy": 0.20,
                        "clean_sheets": 0.25, "tackles": 0.25, "dribbles": 0.05,
                        "shots_on_target": 0.05, "appearances": 0.10},
        "Midfielder":  {"goals": 0.15, "assists": 0.20, "pass_accuracy": 0.20,
                        "clean_sheets": 0.00, "tackles": 0.10, "dribbles": 0.15,
                        "shots_on_target": 0.10, "appearances": 0.10},
        "Forward":     {"goals": 0.35, "assists": 0.15, "pass_accuracy": 0.10,
                        "clean_sheets": 0.00, "tackles": 0.05, "dribbles": 0.15,
                        "shots_on_target": 0.15, "appearances": 0.05},
    }
    kpi_cols = ["goals", "assists", "pass_accuracy", "clean_sheets",
                "tackles", "dribbles", "shots_on_target", "appearances"]
    col_max = df[kpi_cols].max().replace(0, 1)
    norm = df[kpi_cols].div(col_max)
    scores = pd.Series(0.0, index=df.index)
    for pos, w in weights.items():
        mask = df["position"] == pos
        w_arr = pd.Series(w)[kpi_cols].values
        scores[mask] = norm[mask].values @ w_arr
    lo, hi = 5.0, 9.5
    mn, mx = scores.min(), scores.max()
    if mx > mn:
        scores = lo + (scores - mn) / (mx - mn) * (hi - lo)
    else:
        scores = pd.Series(lo, index=df.index)
    return scores.clip(lo, hi).round(2)


def generate_data() -> pd.DataFrame:
    """Generate the full synthetic football dataset (mirrors generate_dataset.py)."""
    np.random.seed(42)

    # Build player master list
    all_names = _make_names(_N_PLAYERS)
    positions_list = []
    for pos, count in _POSITION_COUNTS.items():
        positions_list.extend([pos] * count)
    np.random.shuffle(positions_list)

    teams = np.random.choice(_CLUBS, size=_N_PLAYERS)
    ages = np.random.randint(17, 39, size=_N_PLAYERS)
    nats = np.random.choice(_NATIONALITIES, size=_N_PLAYERS)

    players = pd.DataFrame({
        "player_id":   np.arange(1, _N_PLAYERS + 1),
        "player_name": all_names,
        "position":    positions_list,
        "team":        teams,
        "age":         ages,
        "nationality": nats,
    })

    # Assign seasons (~70 % of players appear in both)
    rows = []
    for _, p in players.iterrows():
        in_both = np.random.rand() < 0.70
        seasons = _SEASONS if in_both else [np.random.choice(_SEASONS)]
        for s in seasons:
            rows.append({**p.to_dict(), "season": s})
    df = pd.DataFrame(rows).reset_index(drop=True)

    # Sample position-aware stats
    stat_parts = []
    for pos in _POSITIONS:
        mask = df["position"] == pos
        idx = df.index[mask]
        s = _sample_stats(pos, int(mask.sum()))
        stat_parts.append(pd.DataFrame(s, index=idx))
    stats = pd.concat(stat_parts).sort_index()
    df = pd.concat([df, stats], axis=1)

    df["rating"] = _compute_rating(df)

    df = df[_REQUIRED_COLUMNS].reset_index(drop=True)
    return df


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load football_players.csv or fall back to generate_data()."""
    try:
        df = pd.read_csv("football_players.csv")
    except FileNotFoundError:
        df = generate_data()

    # Validate required columns
    missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        st.error(f"Dataset is missing required columns: {missing}")
        st.stop()

    # Drop all-null rows silently
    df = df.dropna(how="all")

    # Fill remaining numeric nulls with 0 (defensive)
    numeric_cols = df.select_dtypes(include="number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Fill string column nulls
    df["player_name"] = df["player_name"].fillna("Unknown")
    df["team"]        = df["team"].fillna("Unknown")
    df["position"]    = df["position"].fillna("Unknown")
    df["season"]      = df["season"].fillna("Unknown")

    return df


# ── Filter helper ─────────────────────────────────────────────────────────────

def apply_filters(
    df: pd.DataFrame,
    seasons: list,
    teams: list,
    positions: list,
    player_search: str,
) -> pd.DataFrame:
    """Return a filtered DataFrame based on the sidebar selections."""
    if seasons:
        df = df[df["season"].isin(seasons)]
    if teams:
        df = df[df["team"].isin(teams)]
    if positions:
        df = df[df["position"].isin(positions)]
    if player_search and player_search.strip():
        df = df[df["player_name"].str.contains(player_search.strip(), case=False, na=False)]
    return df


# ── SECTION 4 — Sidebar ───────────────────────────────────────────────────────

df_all = load_data()

with st.sidebar:
    st.markdown("## ⚽ Dashboard Filters")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Overview", "👤 Player Analysis", "🏟️ Team Analysis", "📊 Position Analysis"],
    )

    st.markdown("---")

    all_seasons = sorted(df_all["season"].unique().tolist())
    sel_seasons = st.multiselect("📅 Season", options=all_seasons, default=all_seasons)
    if not sel_seasons:
        st.caption("Showing all seasons")

    all_teams = sorted(df_all["team"].unique().tolist())
    sel_teams = st.multiselect("🏟️ Team", options=all_teams, default=all_teams)
    if not sel_teams:
        st.caption("Showing all teams")

    all_positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
    sel_positions = st.multiselect("🎯 Position", options=all_positions, default=all_positions)
    if not sel_positions:
        st.caption("Showing all positions")

    player_search = st.text_input("🔍 Search Player Name")

    st.markdown("---")
    st.caption("ℹ️ Synthetic data — all players, clubs, and statistics are fictitious.")

# Apply filters
df_filtered = apply_filters(df_all, sel_seasons, sel_teams, sel_positions, player_search)

# ── SECTION 5–8 — Page stub functions ────────────────────────────────────────

import plotly.express as px  # noqa: E402 — imported here to keep section grouping
import plotly.graph_objects as go  # noqa: E402


def kpi_cards(df: pd.DataFrame) -> None:
    """Render five KPI metric cards in a single row."""
    st.markdown("### 📊 Key Performance Indicators")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(label="Total Players",  value=df["player_id"].nunique())
    c2.metric(label="Total Goals",    value=int(df["goals"].sum()))
    c3.metric(label="Total Assists",  value=int(df["assists"].sum()))
    c4.metric(label="Total Minutes",  value=f"{int(df['minutes_played'].sum()):,}")
    c5.metric(label="Avg Rating",     value=round(df["rating"].mean(), 2))


def render_overview(df: pd.DataFrame) -> None:
    # ── Empty state guard ────────────────────────────────────────────────────
    if df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar filters.")
        return

    # ── Section 1 — KPI Cards ────────────────────────────────────────────────
    kpi_cards(df)

    st.markdown("---")

    # ── Section 2 — Top 10 Charts ────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    # Left — Top 10 Scorers
    with col_left:
        top_scorers = (
            df.groupby("player_name")["goals"]
            .sum()
            .nlargest(10)
            .reset_index()
            .sort_values("goals", ascending=False)
        )
        fig_goals = px.bar(
            top_scorers,
            x="player_name",
            y="goals",
            title="🥅 Top 10 Goal Scorers",
            labels={"player_name": "Player", "goals": "Goals"},
            color_discrete_sequence=["#00c853"],
            template="plotly_dark",
            text="goals",
        )
        fig_goals.update_traces(textposition="outside")
        fig_goals.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#161b22",
            font_color="#e6edf3",
        )
        st.plotly_chart(fig_goals, use_container_width=True)

    # Right — Top 10 Assisters
    with col_right:
        top_assisters = (
            df.groupby("player_name")["assists"]
            .sum()
            .nlargest(10)
            .reset_index()
            .sort_values("assists", ascending=False)
        )
        fig_assists = px.bar(
            top_assisters,
            x="player_name",
            y="assists",
            title="🎯 Top 10 Assist Providers",
            labels={"player_name": "Player", "assists": "Assists"},
            color_discrete_sequence=["#1a7431"],
            template="plotly_dark",
            text="assists",
        )
        fig_assists.update_traces(textposition="outside")
        fig_assists.update_layout(
            plot_bgcolor="#0d1117",
            paper_bgcolor="#161b22",
            font_color="#e6edf3",
        )
        st.plotly_chart(fig_assists, use_container_width=True)

    # ── Section 3 — Divider / stats table placeholder ────────────────────────
    st.markdown("---")
    st.subheader("📋 Player Statistics")

    # ── Search widget ──────────────────────────────────────────────────────────
    search_term = st.text_input(
        "🔍 Search player by name",
        placeholder="e.g. Marcus, Hale…",
        key="table_search",
    )
    display_df = (
        df[df['player_name'].str.contains(search_term, case=False, na=False)]
        if search_term
        else df.copy()
    )

    # ── Row count caption ──────────────────────────────────────────────────────
    st.caption(f"Showing {len(display_df)} of {len(df)} player records")

    # ── Table ──────────────────────────────────────────────────────────────────
    col_rename = {
        'player_name': 'Player', 'season': 'Season', 'team': 'Team',
        'position': 'Position', 'age': 'Age', 'appearances': 'Apps',
        'minutes_played': 'Minutes', 'goals': 'Goals', 'assists': 'Assists',
        'shots': 'Shots', 'pass_accuracy': 'Pass Acc %', 'rating': 'Rating',
    }
    if display_df.empty:
        st.info("No players found matching your search term.")
    else:
        table_display = display_df[list(col_rename.keys())].rename(columns=col_rename)
        st.dataframe(table_display, use_container_width=True, hide_index=True)

    # ── CSV download (full sidebar-filtered df, all columns) ───────────────────
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_data,
        file_name="football_players_filtered.csv",
        mime="text/csv",
        help="Downloads all filtered player data with all columns",
    )




def render_radar(df: pd.DataFrame, players: list) -> None:
    """Render a Plotly GO radar/spider chart for up to 3 selected players."""
    axes = ['goals', 'assists', 'pass_accuracy', 'dribbles', 'tackles', 'rating']
    axis_labels = ['Goals', 'Assists', 'Pass Acc', 'Dribbles', 'Tackles', 'Rating']
    colors = ['#00c853', '#2979ff', '#ff6d00']

    col_max = df[axes].max().replace(0, 1)

    fig = go.Figure()

    for i, player_name in enumerate(players):
        player_rows = df[df['player_name'] == player_name].sort_values('season', ascending=False)
        if player_rows.empty:
            continue
        row = player_rows.iloc[0]
        values = [(row[ax] / col_max[ax]) for ax in axes]
        # Close the polygon by repeating the first value
        values_closed = values + [values[0]]
        labels_closed = axis_labels + [axis_labels[0]]

        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill='toself',
            name=player_name,
            line=dict(color=colors[i % len(colors)]),
        ))

    fig.update_layout(
        polar=dict(
            bgcolor='#1c2128',
            radialaxis=dict(visible=True, range=[0, 1], color='#8b949e'),
            angularaxis=dict(color='#8b949e'),
        ),
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        legend=dict(bgcolor='#1c2128'),
        template='plotly_dark',
    )
    st.plotly_chart(fig, use_container_width=True)


def render_player_analysis(df: pd.DataFrame) -> None:
    # ── Empty state guard ────────────────────────────────────────────────────
    if df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar filters.")
        return

    st.header("👤 Player Analysis")

    # ── Section 1 — Goals vs Assists Scatter ─────────────────────────────────
    st.subheader("⚡ Goals vs Assists")
    fig1 = px.scatter(
        df,
        x='goals',
        y='assists',
        color='position',
        hover_data=['player_name', 'team', 'goals', 'assists', 'rating'],
        template='plotly_dark',
        title='Goals vs Assists by Position',
        labels={'goals': 'Goals', 'assists': 'Assists'},
    )
    fig1.update_traces(marker=dict(size=8, opacity=0.8))
    fig1.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ── Section 2 — Shots vs Goals with OLS Trendline ────────────────────────
    st.markdown("---")
    st.subheader("🎯 Shots vs Goals (with Trend Line)")
    fig2 = px.scatter(
        df,
        x='shots',
        y='goals',
        color='position',
        trendline='ols',
        hover_data=['player_name', 'team', 'shots', 'goals'],
        template='plotly_dark',
        title='Shots vs Goals — Conversion Analysis',
        labels={'shots': 'Shots', 'goals': 'Goals'},
    )
    fig2.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Section 3 — Player Radar Comparison ──────────────────────────────────
    st.markdown("---")
    st.subheader("🕸️ Player Comparison Radar")
    selected_players = st.multiselect(
        "Select 1–3 players to compare",
        options=sorted(df['player_name'].unique()),
        max_selections=3,
    )
    if len(selected_players) > 3:
        st.error("⚠️ Please select a maximum of 3 players for comparison.")
        selected_players = selected_players[:3]
    if not selected_players:
        st.info("Select 1 to 3 players from the list above to see the radar chart.")
    else:
        render_radar(df, selected_players)


def render_team_analysis(df: pd.DataFrame) -> None:
    if df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar filters.")
        return

    st.header("🏟️ Team Analysis")

    team_agg = df.groupby('team').agg(
        Goals=('goals', 'sum'),
        Assists=('assists', 'sum'),
        Players=('player_id', 'nunique')
    ).reset_index().rename(columns={'team': 'Team'})

    # Section 1 — Goals per Team
    st.subheader("🏆 Goals per Team")
    df_goals = team_agg.sort_values('Goals', ascending=False)
    fig = px.bar(df_goals, y='Team', x='Goals', orientation='h',
                 color_discrete_sequence=['#00c853'],
                 template='plotly_dark',
                 title='Total Goals by Team',
                 text='Goals')
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        yaxis={'categoryorder': 'total ascending'},
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Section 2 — Assists per Team
    st.markdown("---")
    st.subheader("🎯 Assists per Team")
    df_assists = team_agg.sort_values('Assists', ascending=False)
    fig = px.bar(df_assists, y='Team', x='Assists', orientation='h',
                 color_discrete_sequence=['#1a7431'],
                 template='plotly_dark',
                 title='Total Assists by Team',
                 text='Assists')
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        yaxis={'categoryorder': 'total ascending'},
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Section 3 — Player Count per Team
    st.markdown("---")
    st.subheader("👥 Squad Size per Team")
    df_players = team_agg.sort_values('Players', ascending=False)
    fig = px.bar(df_players, y='Team', x='Players', orientation='h',
                 color_discrete_sequence=['#2979ff'],
                 template='plotly_dark',
                 title='Unique Players per Team',
                 text='Players')
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        yaxis={'categoryorder': 'total ascending'},
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_position_analysis(df: pd.DataFrame) -> None:
    if df.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust the sidebar filters.")
        return

    st.header("📊 Position Analysis")

    POSITION_ORDER = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']

    # ── Section 1 — Goals by Position Box Plot ────────────────────────────────
    st.subheader("⚽ Goals Distribution by Position")
    fig = px.box(
        df,
        x='position',
        y='goals',
        color='position',
        category_orders={'position': POSITION_ORDER},
        template='plotly_dark',
        title='Goals Distribution by Position',
        labels={'position': 'Position', 'goals': 'Goals'},
    )
    fig.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Section 2 — Average Rating by Position Bar Chart ─────────────────────
    st.markdown("---")
    st.subheader("⭐ Average Player Rating by Position")
    avg_rating = df.groupby('position')['rating'].mean().reset_index()
    avg_rating.rename(columns={'rating': 'Avg Rating'}, inplace=True)
    avg_rating['position'] = pd.Categorical(avg_rating['position'], categories=POSITION_ORDER, ordered=True)
    avg_rating = avg_rating.sort_values('position')
    fig2 = px.bar(
        avg_rating,
        x='position',
        y='Avg Rating',
        color='position',
        category_orders={'position': POSITION_ORDER},
        text='Avg Rating',
        template='plotly_dark',
        title='Average Player Rating by Position',
        labels={'position': 'Position', 'Avg Rating': 'Average Rating'},
    )
    fig2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig2.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        showlegend=False,
        yaxis_range=[0, 10],
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ── Section 3 — Minutes Played Violin Plot ────────────────────────────────
    st.markdown("---")
    st.subheader("⏱️ Minutes Played Distribution by Position")
    fig3 = px.violin(
        df,
        x='position',
        y='minutes_played',
        color='position',
        box=True,
        points='outliers',
        category_orders={'position': POSITION_ORDER},
        template='plotly_dark',
        title='Minutes Played by Position',
        labels={'position': 'Position', 'minutes_played': 'Minutes Played'},
    )
    fig3.update_layout(
        plot_bgcolor='#0d1117',
        paper_bgcolor='#161b22',
        font_color='#e6edf3',
        showlegend=False,
    )
    st.plotly_chart(fig3, use_container_width=True)


# ── SECTION 9 — Main area and routing ────────────────────────────────────────

st.title("⚽ Football Player Performance Analytics Dashboard")
st.caption("Exploring synthetic player statistics across two seasons of fictional football data.")

if page == "🏠 Overview":
    render_overview(df_filtered)
elif page == "👤 Player Analysis":
    render_player_analysis(df_filtered)
elif page == "🏟️ Team Analysis":
    render_team_analysis(df_filtered)
elif page == "📊 Position Analysis":
    render_position_analysis(df_filtered)

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#8b949e;font-size:12px;'>"
    "⚽ Football Analytics Dashboard · Synthetic Data Only · Built with Streamlit &amp; Plotly"
    "</div>",
    unsafe_allow_html=True,
)

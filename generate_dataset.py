"""
generate_dataset.py
Generates a reproducible, position-aware synthetic football player dataset.
Run:  python generate_dataset.py
Output: football_players.csv (workspace root)
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ── Constants ────────────────────────────────────────────────────────────────

CLUBS = [
    "Albion FC", "Red City United", "Northern Dynamo", "Eastbridge Athletic",
    "Westgate Rovers", "Southvale City", "Ironport FC", "Thornfield United",
    "Crestwood Rangers", "Dawnfield Sporting",
]

POSITIONS = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

NATIONALITIES = [
    "English", "Spanish", "French", "Brazilian", "Argentine",
    "German", "Italian", "Dutch", "Portuguese", "Nigerian",
]

SEASONS = ["2022-23", "2023-24"]

# 120 unique players
N_PLAYERS = 120

# Position split: 12 GK, 36 DEF, 42 MID, 30 FWD  (= 120)
POSITION_COUNTS = {"Goalkeeper": 12, "Defender": 36, "Midfielder": 42, "Forward": 30}

# ── Name generation ──────────────────────────────────────────────────────────

FIRST_NAMES = [
    "Marcus", "Luca", "Ethan", "Noah", "James", "Carlos", "Felix", "Hugo",
    "Ivan", "Omar", "Ravi", "Leo", "Finn", "Kai", "Max", "Rafael",
    "Sergio", "Theo", "Yusuf", "Zane", "Aaron", "Blake", "Cole", "Diego",
    "Eli", "Franco", "Gael", "Hector", "Iker", "Javi", "Kyle", "Luis",
    "Mario", "Noel", "Oscar", "Pedro", "Quinn", "Ruben", "Sam", "Tomas",
    "Umar", "Victor", "Will", "Xavi", "Yann", "Zico", "Andre", "Bruno",
    "Cesc", "Dani", "Emil", "Fede", "Glen", "Hans", "Ian", "Joel",
    "Kev", "Lars", "Marc", "Nico", "Olly", "Phil", "Renato", "Stefan",
]

LAST_NAMES = [
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


def make_names(n: int) -> list[str]:
    """Return n unique 'Firstname Lastname' strings."""
    rng_first = np.random.choice(FIRST_NAMES, size=n, replace=True)
    rng_last = np.random.choice(LAST_NAMES, size=n, replace=False if n <= len(LAST_NAMES) else True)
    seen: set[str] = set()
    names: list[str] = []
    for f, l in zip(rng_first, rng_last):
        name = f"{f} {l}"
        while name in seen:
            name = f"{f} {np.random.choice(LAST_NAMES)}"
        seen.add(name)
        names.append(name)
    return names


# ── Per-position stat samplers ───────────────────────────────────────────────

def sample_stats(position: str, n: int) -> dict:
    """Return a dict of stat arrays for n rows of the given position."""
    ri = np.random.randint
    ru = np.random.uniform

    appearances = ri(5, 38, n)
    minutes_played = np.clip(appearances * ri(60, 96, n), 300, 3420).astype(int)

    if position == "Goalkeeper":
        goals           = np.zeros(n, dtype=int)
        assists         = np.zeros(n, dtype=int)
        shots           = np.zeros(n, dtype=int)
        shots_on_target = np.zeros(n, dtype=int)
        pass_accuracy   = ru(55, 80, n).round(1)
        dribbles        = ri(0, 3, n)
        tackles         = ri(0, 10, n)
        yellow_cards    = ri(0, 3, n)
        red_cards       = (ru(0, 1, n) < 0.04).astype(int)
        clean_sheets    = ri(4, 19, n)

    elif position == "Defender":
        goals           = ri(0, 6, n)
        assists         = ri(0, 7, n)
        shots           = ri(2, 20, n)
        shots_on_target = np.minimum(shots, ri(0, 10, n))
        pass_accuracy   = ru(68, 90, n).round(1)
        dribbles        = ri(2, 20, n)
        tackles         = ri(30, 81, n)
        yellow_cards    = ri(0, 8, n)
        red_cards       = (ru(0, 1, n) < 0.08).astype(int)
        clean_sheets    = ri(0, 11, n)

    elif position == "Midfielder":
        goals           = ri(1, 13, n)
        assists         = ri(3, 16, n)
        shots           = ri(10, 41, n)
        shots_on_target = np.minimum(shots, ri(4, 20, n))
        pass_accuracy   = ru(72, 93, n).round(1)
        dribbles        = ri(10, 50, n)
        tackles         = ri(15, 55, n)
        yellow_cards    = ri(0, 7, n)
        red_cards       = (ru(0, 1, n) < 0.05).astype(int)
        clean_sheets    = np.zeros(n, dtype=int)

    else:  # Forward
        goals           = ri(5, 26, n)
        assists         = ri(1, 12, n)
        shots           = ri(20, 81, n)
        shots_on_target = np.minimum(shots, ri(8, 40, n))
        pass_accuracy   = ru(65, 86, n).round(1)
        dribbles        = ri(15, 60, n)
        tackles         = ri(5, 30, n)
        yellow_cards    = ri(0, 6, n)
        red_cards       = (ru(0, 1, n) < 0.05).astype(int)
        clean_sheets    = np.zeros(n, dtype=int)

    return dict(
        appearances=appearances,
        minutes_played=minutes_played,
        goals=goals,
        assists=assists,
        shots=shots,
        shots_on_target=shots_on_target,
        pass_accuracy=pass_accuracy,
        dribbles=dribbles,
        tackles=tackles,
        yellow_cards=yellow_cards,
        red_cards=red_cards,
        clean_sheets=clean_sheets,
    )


# ── Build player master list ─────────────────────────────────────────────────

def build_players() -> pd.DataFrame:
    all_names = make_names(N_PLAYERS)
    positions_list = []
    for pos, count in POSITION_COUNTS.items():
        positions_list.extend([pos] * count)
    np.random.shuffle(positions_list)

    teams       = np.random.choice(CLUBS, size=N_PLAYERS)
    ages        = np.random.randint(17, 39, size=N_PLAYERS)
    nats        = np.random.choice(NATIONALITIES, size=N_PLAYERS)

    return pd.DataFrame({
        "player_id":   np.arange(1, N_PLAYERS + 1),
        "player_name": all_names,
        "position":    positions_list,
        "team":        teams,
        "age":         ages,
        "nationality": nats,
    })


# ── Assign seasons (~1.7 seasons per player on average) ─────────────────────

def assign_seasons(players: pd.DataFrame) -> pd.DataFrame:
    """Each player appears in at least one season; ~70 % appear in both."""
    rows = []
    for _, p in players.iterrows():
        in_both = np.random.rand() < 0.70
        seasons = SEASONS if in_both else [np.random.choice(SEASONS)]
        for s in seasons:
            rows.append({**p.to_dict(), "season": s})
    return pd.DataFrame(rows).reset_index(drop=True)


# ── Compute composite rating ─────────────────────────────────────────────────

def compute_rating(df: pd.DataFrame) -> pd.Series:
    """
    Weighted normalized composite rating, clamped to [5.0, 9.5].

    Weights differ by position so that position-relevant KPIs drive the score.
    Normalization is against the global column max to keep scales comparable
    across positions (consistent with how app.py will normalize radar axes).
    """
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

    col_max = df[kpi_cols].max().replace(0, 1)   # avoid div-by-zero
    norm = df[kpi_cols].div(col_max)              # 0–1 normalised

    scores = pd.Series(0.0, index=df.index)
    for pos, w in weights.items():
        mask = df["position"] == pos
        w_arr = pd.Series(w)[kpi_cols].values
        scores[mask] = norm[mask].values @ w_arr

    # Scale from [0,1] to [5.0, 9.5]
    lo, hi = 5.0, 9.5
    mn, mx = scores.min(), scores.max()
    if mx > mn:
        scores = lo + (scores - mn) / (mx - mn) * (hi - lo)
    else:
        scores = pd.Series(lo, index=df.index)

    return scores.clip(lo, hi).round(2)


# ── Main ─────────────────────────────────────────────────────────────────────

def generate() -> pd.DataFrame:
    players = build_players()
    df = assign_seasons(players)

    stat_parts = []
    for pos in POSITIONS:
        mask = df["position"] == pos
        idx  = df.index[mask]
        s    = sample_stats(pos, int(mask.sum()))
        part = pd.DataFrame(s, index=idx)
        stat_parts.append(part)

    stats = pd.concat(stat_parts).sort_index()
    df = pd.concat([df, stats], axis=1)

    df["rating"] = compute_rating(df)

    # Canonical column order
    col_order = [
        "player_id", "player_name", "season", "team", "position", "age",
        "nationality", "appearances", "minutes_played", "goals", "assists",
        "shots", "shots_on_target", "pass_accuracy", "dribbles", "tackles",
        "yellow_cards", "red_cards", "clean_sheets", "rating",
    ]
    df = df[col_order].reset_index(drop=True)

    assert df.isnull().sum().sum() == 0, "Null values detected — fix generation logic."
    assert list(df.columns) == col_order, "Column mismatch."

    return df


if __name__ == "__main__":
    df = generate()
    out = "football_players.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} rows x {len(df.columns)} columns -> {out}")
    print(df.head(5).to_string(index=False))

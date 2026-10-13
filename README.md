# ⚽ Football Player Performance Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-red)
![Plotly](https://img.shields.io/badge/Plotly-5.22.0-brightgreen)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

An interactive, multi-page football analytics dashboard built with Python and Streamlit. Explore player performance KPIs, compare players with radar charts, analyze team-level statistics, and drill down by position — all from a sleek dark football-themed UI.

---

## ⚠️ Synthetic Data Disclaimer

> **This dashboard uses an entirely artificial dataset.**
>
> All player records in `football_players.csv` were programmatically generated using `numpy.random.seed(42)`. The names, clubs, statistics, and ratings are fictional and do **not** represent real-world football players, clubs, or match results. The dataset exists solely for portfolio demonstration purposes.

---

## Features

- **5 live KPI metric cards** — Total Players, Goals, Assists, Minutes Played, and Avg Rating, all recalculated dynamically as filters change
- **Top-10 Scorers & Top-10 Assisters bar charts** on the Overview page
- **Goals vs Assists scatter plot** with position colour-coding and player tooltips
- **Shots vs Goals scatter plot** with an OLS regression trendline (via statsmodels)
- **Radar / spider chart** for head-to-head multi-attribute comparison of up to 3 players simultaneously
- **Team-level horizontal bar charts** — Goals, Assists, and Unique Player Count per club
- **Position breakdown charts** — box plot, average-rating bar, and violin plot of minutes played
- **Searchable, paginated statistics table** with a player-name filter across the filtered dataset
- **CSV download button** to export the currently filtered dataset at any time
- **Persistent sidebar filters** — Season, Team, Position, and Player Name search applied globally across all pages

---

## Project Structure

```
Football Analysis Dashboard/
├── app.py                  # Main Streamlit application (multi-page via sidebar radio)
├── football_players.csv    # Synthetic dataset (~200 rows, 120 players, 2 seasons)
├── generate_dataset.py     # Standalone script to regenerate football_players.csv
├── requirements.txt        # Pinned Python dependencies
└── README.md               # This file
```

---

## Prerequisites

- **Python 3.9 or higher** — download from [python.org](https://www.python.org/downloads/)
- **pip** — bundled with Python 3.9+; upgrade with `python -m pip install --upgrade pip`

---

## Local Setup & Run Instructions

1. **Clone or download the repository**

   ```bash
   git clone https://github.com/<your-username>/football-analysis-dashboard.git
   cd football-analysis-dashboard
   ```

   Or download and unzip the archive, then open a terminal in the project folder.

2. **Create and activate a virtual environment** *(recommended)*

   ```bash
   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**

   ```bash
   streamlit run app.py
   ```

   The app opens automatically in your default browser at `http://localhost:8501`.  
   If `football_players.csv` is not present, `app.py` generates it automatically on first launch.

---

## Streamlit Community Cloud Deploy Instructions

1. **Push the repository to GitHub** — ensure `app.py`, `requirements.txt`, and (optionally) `football_players.csv` are committed to the `main` branch.

2. **Sign in to Streamlit Community Cloud** at [share.streamlit.io](https://share.streamlit.io) using your GitHub account.

3. **Click "New app"** and fill in:
   - **Repository:** `<your-username>/football-analysis-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`

4. **Click "Deploy"** — Streamlit Cloud installs `requirements.txt` automatically and starts the app. A public URL is provided once the build completes.

> **Note:** If `football_players.csv` is not committed, `app.py` generates it at runtime on the cloud instance. The generated file is ephemeral (not persisted between restarts), which is fine because the data is fully reproducible via `numpy.random.seed(42)`.

---

## Dashboard Pages

| Page | Description |
|------|-------------|
| **Overview** | High-level summary with 5 KPI metric cards, Top-10 Scorers bar chart, Top-10 Assisters bar chart, a searchable statistics table, and a CSV download button. |
| **Player Analysis** | Goals vs Assists scatter (colour-coded by position), Shots vs Goals scatter with OLS trendline, and a radar chart for side-by-side multi-attribute comparison of up to 3 players. |
| **Team Analysis** | Three horizontal bar charts showing each club's total Goals, total Assists, and unique Player Count — all sortable and filter-aware. |
| **Position Analysis** | Box plot of Goals distribution per position, Average Rating bar chart by position, and a Violin plot of Minutes Played — revealing workload and quality differences across roles. |

---

## Tech Stack

| Technology | Version | Role |
|------------|---------|------|
| Python | 3.9+ | Runtime language |
| Streamlit | 1.35.0 | Web UI framework and multi-page app host |
| Pandas | 2.2.2 | Data loading, filtering, and aggregation |
| NumPy | 1.26.4 | Synthetic data generation (`seed(42)`) and numeric operations |
| Plotly | 5.22.0 | Interactive charts (bar, scatter, box, violin, radar) |
| statsmodels | 0.14.2 | OLS regression trendline in the Shots vs Goals scatter plot |

---

*Dataset is synthetic — see the disclaimer above. No real player data is used.*

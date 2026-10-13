# Football Player Performance Analytics Dashboard — Implementation Plan

## Top-Level Overview

Build a portfolio-quality, interactive football (soccer) analytics dashboard using **Python**, **Streamlit**, **Pandas/NumPy**, and **Plotly**. The application is delivered as four files:

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application — all pages, charts, filters, and UI logic |
| `football_players.csv` | Reproducible synthetic dataset (≥ 100 players) |
| `requirements.txt` | Pinned Python dependencies |
| `README.md` | Setup, run, and deploy instructions |

The dashboard has **four pages** (Overview, Player Analysis, Team Analysis, Position Analysis), a persistent sidebar with filters, a searchable statistics table, and a CSV download button. All KPIs are derived dynamically from the filtered dataset.

---

## Dataset Schema

The synthetic CSV contains **one row per player-season** with the following columns:

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique player identifier |
| `player_name` | str | Full name (e.g. "Marcus Hale") |
| `season` | str | Season label, e.g. "2022-23", "2023-24" |
| `team` | str | Club name (10 distinct clubs) |
| `position` | str | One of: Goalkeeper, Defender, Midfielder, Forward |
| `age` | int | Player age (17–38) |
| `nationality` | str | Country (10 distinct values) |
| `appearances` | int | Matches played |
| `minutes_played` | int | Total minutes on pitch |
| `goals` | int | Goals scored |
| `assists` | int | Assists recorded |
| `shots` | int | Total shots |
| `shots_on_target` | int | Shots on target |
| `pass_accuracy` | float | Pass accuracy % (0–100) |
| `dribbles` | int | Successful dribbles |
| `tackles` | int | Tackles won |
| `yellow_cards` | int | Yellow cards received |
| `red_cards` | int | Red cards received |
| `clean_sheets` | int | Clean sheets (GKs and Defenders; 0 elsewhere) |
| `rating` | float | Composite rating 5.0–9.5 |

**Generation rules** (reproducible with `numpy.random.seed(42)`):
- Stats are position-aware: Forwards get more goals/shots, Goalkeepers get more clean_sheets, etc.
- `rating` is computed as a weighted combination of normalized KPI columns rather than randomly assigned.
- Dataset covers **2 seasons** (2022-23, 2023-24) with **~120 unique players**, some appearing in both seasons (~200 total rows).

---

## KPI Calculations (Overview Page)

All KPIs are calculated on the **post-filter** DataFrame so sidebar selections always update them.

| KPI Card | Calculation |
|---|---|
| Total Players | `df['player_id'].nunique()` |
| Total Goals | `df['goals'].sum()` |
| Total Assists | `df['assists'].sum()` |
| Total Minutes Played | `df['minutes_played'].sum()` |
| Avg Player Rating | `df['rating'].mean()` rounded to 2 dp |

---

## Chart Choices

| Page | Chart | Library | Rationale |
|---|---|---|---|
| Overview | KPI metric cards (5) | Streamlit `st.metric` | Instant high-level summary |
| Overview | Top 10 scorers bar chart | Plotly Express bar | Easy ranking comparison |
| Overview | Top 10 assists bar chart | Plotly Express bar | Mirrors goals chart |
| Player Analysis | Goals vs Assists scatter | Plotly Express scatter | Reveals playmaker vs goalscorer profiles |
| Player Analysis | Shots vs Goals scatter | Plotly Express scatter | Conversion rate insight |
| Player Analysis | Radar / spider chart | Plotly Graph Objects | Multi-attribute player comparison (up to 3 players) |
| Team Analysis | Goals per team bar | Plotly Express bar (horizontal) | Team attack output |
| Team Analysis | Assists per team bar | Plotly Express bar (horizontal) | Team creativity |
| Team Analysis | Player count per team bar | Plotly Express bar | Squad depth |
| Position Analysis | Goals by position box plot | Plotly Express box | Distribution spread per position |
| Position Analysis | Average rating by position bar | Plotly Express bar | Position-level quality |
| Position Analysis | Minutes played by position violin | Plotly Express violin | Workload distribution |

All charts use `template="plotly_dark"` and a custom green accent color palette to match the football pitch theme.

---

## Project Structure

```
Football Analysis Dashboard/
├── app.py                  # Main application (single-file, multi-page via st.sidebar radio)
├── football_players.csv    # Synthetic dataset
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

`app.py` is organized into clear functional sections:

```
app.py
│
├── SECTION 1 — Imports and page config
├── SECTION 2 — Data loading and generation (generate_data / load_data)
├── SECTION 3 — Custom CSS (dark green theme)
├── SECTION 4 — Sidebar (filters: season, team, position, player search)
├── SECTION 5 — Overview page
├── SECTION 6 — Player Analysis page
├── SECTION 7 — Team Analysis page
├── SECTION 8 — Position Analysis page
└── SECTION 9 — Shared footer with CSV download button
```

Helper functions (defined before page functions):
- `generate_data()` → creates and returns the synthetic DataFrame
- `load_data()` → calls `generate_data()`, saves to CSV if not present, returns DataFrame
- `apply_filters(df, seasons, teams, positions, player_search)` → returns filtered DataFrame
- `kpi_cards(df)` → renders the five `st.metric` cards
- `render_radar(df, players)` → builds a Plotly GO radar chart for selected players

---

## Sub-Tasks

---

### Sub-Task 1 — Generate Synthetic Dataset and Save CSV

**Intent:**  
Create `football_players.csv` with a realistic, position-aware synthetic dataset of ≥ 100 players across 2 seasons. This file is the single source of truth for all pages and all KPI/chart logic.

**Expected Outcomes:**
- `football_players.csv` exists in the project root.
- Contains ~200 rows (120 players × ~1.7 seasons on average).
- All 20 columns present with no null values.
- Stats are position-appropriate (e.g. Goalkeepers have 0 goals in most rows).
- `rating` is a derived composite, not a random float.
- File is clearly labelled as synthetic in the README.

**Todo List:**
1. Write a standalone Python script (or include as `generate_data()` in `app.py`) using `numpy.random.seed(42)`.
2. Define 10 club names, 4 positions, 10 nationalities, 2 season labels.
3. Generate per-position stat distributions (goals, shots, assists, tackles, clean_sheets etc.).
4. Compute `rating` as a weighted sum of normalized KPIs clamped to [5.0, 9.5].
5. Save as `football_players.csv` with a `# SYNTHETIC DATA` comment in the README.

**Relevant Context:**  
- NumPy `random.seed(42)` ensures reproducibility.
- Position groups: `['Goalkeeper', 'Defender', 'Midfielder', 'Forward']`.
- Two seasons: `['2022-23', '2023-24']`.

**Status:** `[ ] pending`

---

### Sub-Task 2 — Project Scaffolding (requirements.txt and README.md)

**Intent:**  
Create the dependency manifest and the user-facing documentation so the project is runnable and deployable from a fresh clone.

**Expected Outcomes:**
- `requirements.txt` lists exact pinned versions of: `streamlit`, `pandas`, `numpy`, `plotly`.
- `README.md` includes: project description, synthetic-data disclaimer, prerequisites, local run instructions (`streamlit run app.py`), Streamlit Community Cloud deploy instructions, and a short feature list.

**Todo List:**
1. Determine compatible, current stable versions of the four dependencies.
2. Write `requirements.txt` with pinned versions.
3. Write `README.md` with all sections listed above.

**Relevant Context:**  
- No external APIs or database connections are needed.
- Streamlit Community Cloud deploy: push to GitHub, connect repo, set main file to `app.py`.

**Status:** `[ ] pending`

---

### Sub-Task 3 — app.py: Foundation, Theme and Data Loading

**Intent:**  
Set up the `app.py` skeleton: Streamlit page configuration, dark green CSS theme, `load_data()` function, and the sidebar navigation + filter widgets.

**Expected Outcomes:**
- `streamlit run app.py` launches without errors.
- Dark football-themed UI is visible (dark background, green accents).
- Sidebar shows: page selector radio, season multi-select, team multi-select, position multi-select, player name search text input.
- `load_data()` calls `generate_data()` if CSV not found, otherwise reads CSV.
- `apply_filters()` returns correct subsets for any combination of filter values.
- Selecting "All" or leaving blank shows the full dataset.

**Todo List:**
1. Configure Streamlit page: title, icon ⚽, layout wide, initial sidebar expanded.
2. Inject custom CSS for background (#0d1117), card colors, green accents (#00c853), font.
3. Implement `generate_data()` with full column schema.
4. Implement `load_data()` with CSV read/write and missing-value check.
5. Implement `apply_filters()` with input validation and graceful empty-state handling.
6. Build sidebar with all four filter widgets plus page radio.

**Relevant Context:**  
- Use `st.cache_data` on `load_data()` to avoid re-reading on every interaction.
- Empty filter state (nothing selected) should default to showing all data with a clear `st.info` message, not an error.

**Status:** `[ ] pending`

---

### Sub-Task 4 — Overview Page

**Intent:**  
Build the first page: five KPI metric cards and two bar charts (top scorers, top assisters), all driven by the filtered dataset.

**Expected Outcomes:**
- Five `st.metric` cards update in real-time when filters change.
- Top-10 scorers and top-10 assisters bar charts are displayed side by side.
- Charts use the dark Plotly theme with green bars.
- An `st.warning` is shown if the filtered dataset is empty.

**Todo List:**
1. Implement `kpi_cards(df)` rendering five `st.metric` widgets in a 5-column layout.
2. Build top-10 scorers Plotly bar chart (sorted descending).
3. Build top-10 assisters Plotly bar chart (sorted descending).
4. Display charts in a 2-column `st.columns` layout.
5. Add empty-state guard with `st.warning`.

**Relevant Context:**  
- KPI formulas defined in the "KPI Calculations" section above.
- `plotly_dark` template; accent color `#00c853`.

**Status:** `[ ] pending`

---

### Sub-Task 5 — Player Analysis Page

**Intent:**  
Build the player comparison page: goals vs assists scatter, shots vs goals scatter, and a radar chart for up to 3 selected players.

**Expected Outcomes:**
- Goals vs Assists scatter renders with player name tooltips.
- Shots vs Goals scatter renders with a trend line.
- Radar chart appears only when 1–3 players are selected via a multi-select widget.
- All charts are dark-themed and readable.

**Todo List:**
1. Build Goals vs Assists scatter with color mapped to `position`, hover showing `player_name`, `team`, `goals`, `assists`.
2. Build Shots vs Goals scatter with `trendline='ols'` (OLS regression line via Plotly Express).
3. Add a `st.multiselect` for player selection (max 3 enforced with `st.error`).
4. Implement `render_radar(df, players)` using Plotly GO `Scatterpolar`.
5. Define radar axes: `goals`, `assists`, `pass_accuracy`, `dribbles`, `tackles`, `rating`.
6. Normalize radar values to 0–1 per axis before plotting.

**Relevant Context:**  
- `plotly.express.scatter` `trendline` requires `statsmodels`; add to requirements.txt.
- Radar normalization: divide each axis value by the column max across the full (unfiltered) dataset to keep scales consistent.

**Status:** `[ ] pending`

---

### Sub-Task 6 — Team Analysis Page

**Intent:**  
Build the team-level aggregation page showing three horizontal bar charts: goals per team, assists per team, and player count per team.

**Expected Outcomes:**
- Three horizontal bar charts render correctly, sorted by value descending.
- Charts dynamically update when season/position/player filters change.
- Team names on the Y-axis are fully visible.

**Todo List:**
1. Aggregate `df.groupby('team')` for `goals.sum()`, `assists.sum()`, `player_id.nunique()`.
2. Sort each aggregate descending before charting.
3. Build three Plotly Express horizontal bar charts.
4. Display in a 1-column layout (full width) for readability.
5. Add empty-state guard.

**Relevant Context:**  
- `orientation='h'` in `px.bar` for horizontal bars.
- Use `player_id.nunique()` not `count()` to avoid double-counting players with multiple seasons.

**Status:** `[ ] pending`

---

### Sub-Task 7 — Position Analysis Page

**Intent:**  
Build the position breakdown page: box plot of goals by position, bar chart of average rating by position, and violin plot of minutes played by position.

**Expected Outcomes:**
- Box plot shows spread and outliers per position.
- Average rating bar chart shows position-level quality differences.
- Violin plot shows workload distribution across positions.
- All charts are dark-themed.

**Todo List:**
1. Build `px.box` for goals by position.
2. Build `px.bar` for average rating by position (aggregated DataFrame).
3. Build `px.violin` for minutes played by position.
4. Arrange in a 1-column layout, full width.
5. Add empty-state guard.

**Relevant Context:**  
- Position order for chart display: `['Goalkeeper', 'Defender', 'Midfielder', 'Forward']`.

**Status:** `[ ] pending`

---

### Sub-Task 8 — Searchable Statistics Table and CSV Download

**Intent:**  
Add the searchable player statistics table visible on every page (or as a dedicated section at the bottom), plus the CSV download button for the filtered dataset.

**Expected Outcomes:**
- A paginated, searchable `st.dataframe` shows all columns of the filtered dataset.
- A search box above the table filters rows by player name (case-insensitive substring match).
- A `st.download_button` exports the currently filtered + searched dataset as CSV.
- Column headers are human-readable (title-cased).

**Todo List:**
1. Add a text input `st.text_input("Search player name…")` above the table.
2. Apply name search filter on top of sidebar filters.
3. Render `st.dataframe` with `use_container_width=True`.
4. Implement `st.download_button` using `df.to_csv(index=False).encode('utf-8')`.
5. Place this section on the Overview page under the charts (accessible first).

**Relevant Context:**  
- `st.download_button` does not require any extra dependencies.
- Column rename map: `{'player_name': 'Player', 'goals': 'Goals', ...}` applied only for display.

**Status:** `[ ] pending`

---

### Sub-Task 9 — Input Validation, Error Handling and Final Polish

**Intent:**  
Add all remaining defensive logic, polish the UI, and do a final end-to-end review.

**Expected Outcomes:**
- Empty filtered state shows a clear `st.warning("No data matches the selected filters…")` on every page.
- Radar chart enforces 1–3 player selection with `st.error`.
- Missing values in the CSV (if manually edited) are handled with `st.error` and `st.stop()`.
- All chart titles, axis labels, and tooltips are descriptive and accurate.
- App runs with `streamlit run app.py` from a fresh install of requirements.txt.
- No hardcoded statistics anywhere — all numbers come from the DataFrame.

**Todo List:**
1. Wrap `load_data()` with a null-check; if critical columns are missing call `st.error` + `st.stop()`.
2. Add `if df.empty: st.warning(...)` guard at the start of each page render function.
3. Enforce max-3 player selection in radar section.
4. Review all chart `labels` dicts and `title` strings for accuracy.
5. Test all four sidebar filter combinations manually.
6. Confirm `requirements.txt` is complete (add `statsmodels` for trendline).

**Relevant Context:**  
- `statsmodels` is needed only for `trendline='ols'` in the shots-vs-goals scatter.
- If `statsmodels` is undesirable, replace OLS trendline with a manual NumPy `polyfit` line drawn as a `go.Scatter` trace.

**Status:** `[ ] pending`

---

## Dependency List (requirements.txt)

```
streamlit==1.35.0
pandas==2.2.2
numpy==1.26.4
plotly==5.22.0
statsmodels==0.14.2
```

---

## Non-Goals

- No real-world football data, live APIs, or paid data sources.
- No user authentication or database.
- No mobile-first layout (responsive Streamlit grid is sufficient).
- No unit tests (portfolio project scope).
- No Docker container or CI/CD pipeline.

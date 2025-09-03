import io
import os
import importlib
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# ----------------- Page config -----------------
st.set_page_config(page_title="Fantasy Draft App", page_icon="🏈", layout="wide")

# ----------------- Constants -------------------
ROUNDS_DEFAULT = 15
DATA_DIR = Path("data")
MEDIA_DIR = Path("media")
DATA_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)

# Columns you use across the app (adapt to your real set)
STAT_COLUMNS = [
    "Total Points (Prev Year)", "Projected Points", "Rush Yards",
    "Receiving Yards", "Passing Yards", "Pass TD", "Rush Att", "Rush TD",
    "Receptions", "Rec TD", "2-PT", "Fumble Lost", "Targets",
    "Fumble Return TD", "Team", "Position", "Target Share",
    "Fantasy PPG", "Games", "Bye Week", "Matchups", "ADP", "WR ADP"
]

# ----------------- Data loading ----------------
@st.cache_data(show_spinner=False)
def load_players_from_modules_or_csv():
    """
    Tries to import PLAYER_VIDEOS / PLAYER_STATS Python dicts.
    Falls back to CSVs if present:
      - data/players_meta.csv   (player, team, position, adp, wr_adp, video_url)
      - data/player_stats.csv   (player + STAT_COLUMNS columns)
    Returns (players_df, videos_map)
    """
    videos_map = {}
    stats_df = None
    meta_df = None

    # Try python modules first
    try:
        pv = importlib.import_module("PLAYER_VIDEOS")
        videos_map = getattr(pv, "PLAYER_VIDEOS", {})
    except Exception:
        pass

    # Optional: PLAYER_STATS module
    try:
        ps = importlib.import_module("PLAYER_STATS")
        stats_dict = getattr(ps, "PLAYER_STATS", {})
        if stats_dict:
            # dict -> DataFrame
            stats_df = pd.DataFrame.from_dict(stats_dict, orient="index")
            stats_df.index.name = "Player"
            stats_df.reset_index(inplace=True)
    except Exception:
        pass

    # CSV fallbacks (if you prefer repo-friendly files)
    meta_csv = DATA_DIR / "players_meta.csv"   # Player,Team,Position,ADP,WR ADP,video_url
    stats_csv = DATA_DIR / "player_stats.csv"  # Player + STAT_COLUMNS

    if meta_csv.exists():
        meta_df = pd.read_csv(meta_csv)
    if stats_df is None and stats_csv.exists():
        stats_df = pd.read_csv(stats_csv)

    # If we have neither, build a tiny demo set from videos_map
    if meta_df is None:
        if videos_map:
            meta_df = pd.DataFrame({
                "Player": list(videos_map.keys()),
                "Team": ["—"] * len(videos_map),
                "Position": ["WR"] * len(videos_map),
                "ADP": [999] * len(videos_map),
                "WR ADP": [999] * len(videos_map),
                "video_url": [videos_map[p] for p in videos_map]
            })
        else:
            meta_df = pd.DataFrame(columns=["Player","Team","Position","ADP","WR ADP","video_url"])

    # Merge stats if available
    if stats_df is not None:
        # Ensure all STAT_COLUMNS exist
        for c in STAT_COLUMNS:
            if c not in stats_df.columns:
                stats_df[c] = 0
        players_df = pd.merge(meta_df, stats_df, on="Player", how="left")
    else:
        # No stats provided → create zero columns
        players_df = meta_df.copy()
        for c in STAT_COLUMNS:
            if c not in players_df.columns:
                players_df[c] = 0

    # Normalize dtypes
    numeric_like = ["ADP", "WR ADP", "Projected Points"] + [c for c in STAT_COLUMNS if c not in ["Team","Position","Matchups"]]
    for c in numeric_like:
        if c in players_df.columns:
            players_df[c] = pd.to_numeric(players_df[c], errors="coerce")

    # Videos (prefer module mapping; otherwise take video_url col)
    if not videos_map and "video_url" in players_df.columns:
        videos_map = {r.Player: str(r.video_url) if pd.notna(r.video_url) else "" for r in players_df.itertuples()}

    return players_df, videos_map

players_df, VIDEOS = load_players_from_modules_or_csv()

# ----------------- Utility ---------------------
def snake_slot(pick_index: int, n_teams: int):
    """Returns (round_idx, team_idx) in snake order from global pick index."""
    r = pick_index // n_teams
    i = pick_index % n_teams
    team_idx = i if (r % 2 == 0) else (n_teams - 1 - i)
    return r, team_idx

def play_video_block(player: str):
    url_or_file = VIDEOS.get(player, "")
    st.markdown(f"**Highlight:** {player}")
    if url_or_file.startswith("http"):
        st.video(url_or_file)
    else:
        # local file in /media (for small demo clips)
        p = MEDIA_DIR / Path(url_or_file).name
        if p.exists():
            with p.open("rb") as fh:
                st.video(io.BytesIO(fh.read()))
        else:
            st.info("No highlight video found. Add a URL in `players_meta.csv` or a small clip in `/media`.")

# ----------------- Session State ---------------
def init_state():
    if "rounds" not in st.session_state:
        st.session_state.rounds = ROUNDS_DEFAULT
    if "n_teams" not in st.session_state:
        st.session_state.n_teams = 8
    if "team_names" not in st.session_state:
        st.session_state.team_names = [f"Team {i+1}" for i in range(st.session_state.n_teams)]
    if "started" not in st.session_state:
        st.session_state.started = False
    if "current_pick" not in st.session_state:
        st.session_state.current_pick = 0
    if "picked" not in st.session_state:
        st.session_state.picked = set()
    if "board" not in st.session_state:
        st.session_state.board = [["" for _ in range(st.session_state.n_teams)] for _ in range(st.session_state.rounds)]
    if "editable_stats" not in st.session_state:
        # Only players not yet drafted
        st.session_state.editable_stats = players_df.copy()

init_state()

# Keep editable_stats in sync (remove drafted)
def sync_available():
    drafted = st.session_state.picked
    st.session_state.editable_stats = players_df[~players_df["Player"].isin(drafted)].copy()

# ----------------- Sidebar (Setup) -------------
st.sidebar.header("🏈 Draft Setup")
st.sidebar.caption("Snake draft · Live board · Highlights")

st.session_state.n_teams = st.sidebar.slider("Teams (even only)", 2, 20, st.session_state.n_teams, step=2)
st.session_state.rounds = st.sidebar.slider("Rounds", 4, 25, st.session_state.rounds, step=1)

# Team names
with st.sidebar.expander("Edit Team Names"):
    names = []
    for i in range(st.session_state.n_teams):
        default = st.session_state.team_names[i] if i < len(st.session_state.team_names) else f"Team {i+1}"
        names.append(st.text_input(f"Team {i+1}", default))
    st.session_state.team_names = names

if st.sidebar.button("🚀 Start / Reset Draft", use_container_width=True):
    st.session_state.started = True
    st.session_state.current_pick = 0
    st.session_state.picked = set()
    st.session_state.board = [["" for _ in range(st.session_state.n_teams)] for _ in range(st.session_state.rounds)]
    sync_available()
    st.success("Draft is live!")

# ----------------- Main Layout -----------------
c_left, c_right = st.columns([2, 1], gap="large")

with c_left:
    st.title("⚡ Fantasy Football Draft Picker")
    st.caption("Projections • ADP • Highlights")

    # ===== Available Players & Stats (editable) =====
    st.subheader("Available Players & Stats")
    # A couple of useful filters
    filt_cols = st.columns(4)
    with filt_cols[0]:
        pos_filter = st.selectbox("Position filter", options=["All"] + sorted(players_df["Position"].dropna().unique().tolist()))
    with filt_cols[1]:
        max_adp = st.number_input("Max ADP", min_value=1, value=120)
    with filt_cols[2]:
        sort_by = st.selectbox("Sort by", options=["Projected Points", "ADP", "WR ADP", "Total Points (Prev Year)"])
    with filt_cols[3]:
        asc = st.toggle("Ascending sort", value=False)

    sync_available()
    avail = st.session_state.editable_stats.copy()

    if pos_filter != "All":
        avail = avail[avail["Position"] == pos_filter]
    avail = avail[avail["ADP"].fillna(9999) <= max_adp]

    # Sort
    if sort_by in avail.columns:
        avail = avail.sort_values(sort_by, ascending=asc)

    # Editable grid (lets you tweak stats quickly)
    edited = st.data_editor(
        avail[["Player","Team","Position","ADP","WR ADP"] + STAT_COLUMNS],
        use_container_width=True,
        height=400,
        key="data_editor_available",
    )

    # Persist edits back into session (lightweight)
    players_df.update(edited.set_index("Player"))

    # Pick selection
    st.markdown("**Select a player row above, then draft:**")
    selected_rows = st.session_state.get("data_editor_available", {})
    selected_index = selected_rows.get("selected_rows", [])
    pick_name = None
    if selected_index:
        pick_name = edited.iloc[selected_index[0]]["Player"]

    if st.button("Draft ▶", type="primary", disabled=(pick_name is None or not st.session_state.started)):
        if pick_name in st.session_state.picked:
            st.warning("Player already drafted.")
        else:
            # Place on board
            r, t = snake_slot(st.session_state.current_pick, st.session_state.n_teams)
            if r >= st.session_state.rounds:
                st.success("Draft complete!")
            else:
                st.session_state.board[r][t] = pick_name
                st.session_state.picked.add(pick_name)
                st.session_state.current_pick += 1
                st.success(f"Drafted {pick_name} to **{st.session_state.team_names[t]}** (Round {r+1}).")
                play_video_block(pick_name)

with c_right:
    # ===== Next pick indicator =====
    st.subheader("🎯 Next Pick")
    if not st.session_state.started:
        st.info("Click **Start / Reset Draft** in the sidebar.")
    else:
        total_picks = st.session_state.n_teams * st.session_state.rounds
        if st.session_state.current_pick >= total_picks:
            st.success("Draft Complete! 🏆")
        else:
            r, t = snake_slot(st.session_state.current_pick, st.session_state.n_teams)
            st.write(f"Round **{r+1}** → **{st.session_state.team_names[t]}**")

    # ===== Draft Board =====
    st.subheader("📋 Draft Board (Snake)")
    # Build a display DataFrame
    board_df = pd.DataFrame(
        st.session_state.board,
        columns=st.session_state.team_names
    )
    board_df.index = [f"R{r+1}" for r in range(board_df.shape[0])]
    st.dataframe(board_df, use_container_width=True, height=520)

# ----------------- (Optional) Projections hook -----------------
with st.expander("🔧 Projection Model Hook (GBR)"):
    st.write(
        "Wire your trained Gradient Boosting Regressor here to populate **Projected Points**.\n"
        "Make sure inference feature names/order match training."
    )
    st.code(
        """# Example (pseudo):
# import pickle
# model = pickle.load(open("models/gbr_point_projection.pkl","rb"))
# FEATURES = ["feat1","feat2",...,"feat16"]
# X = players_df[FEATURES].fillna(0).to_numpy()
# players_df["Projected Points"] = model.predict(X)
# players_df.to_csv("data/player_stats.csv", index=False)  # if you want to persist
""",
        language="python"
    )

st.caption("Tip: store public highlight URLs in `video_url`, or small demo clips in `/media`.")

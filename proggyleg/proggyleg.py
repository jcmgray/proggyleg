import collections
import functools
import pathlib

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def set_alpha(c, alpha):
    import matplotlib as mpl

    rgb = mpl.colors.to_rgb(c)
    return (*rgb, alpha)


def update_data(year=2023, source="footballdata"):
    import urllib.request

    if source == "fixturedownload":
        target = pathlib.Path(__file__).parent / f"data/epl-{year}-UTC.csv"
        url = f"https://fixturedownload.com/download/epl-{year}-UTC.csv"

    elif source == "footballdata":
        target = pathlib.Path(__file__).parent / f"data/E0-{year}.csv"
        url = (
            "https://www.football-data.co.uk/mmz4281/"
            f"{str(year)[-2:]}{str(year + 1)[-2:]}/E0.csv"
        )

    if target.exists():
        print(f"Removing {target}")
        target.unlink()

    print(f"Downloading data for {year}")
    urllib.request.urlretrieve(url, target)


team_aliases = {
    "Man United": "Man Utd",
    "Spurs": "Tottenham",
    "Nott'm Forest": "Nottingham Forest",
    "Sheffield United": "Sheffield Utd",
}


def parse_fixturedownload_data(contents):
    import csv
    import re
    from datetime import datetime

    reader = list(csv.DictReader(contents.splitlines()))
    reader.sort(key=lambda x: datetime.strptime(x["Date"], r"%d/%m/%Y %H:%M"))

    data = []
    for row in reader:
        home_team = row["Home Team"]
        home_team = team_aliases.get(home_team, home_team)
        away_team = row["Away Team"]
        away_team = team_aliases.get(away_team, away_team)
        score = row["Result"]
        match = re.match(r"(\d+)\s?-\s?(\d+)", score)
        if match:
            data.append(
                (
                    home_team,
                    away_team,
                    int(match.group(1)),
                    int(match.group(2)),
                )
            )

    return data



def parse_datetime(date_str):
    from datetime import datetime

    try:
        return datetime.strptime(date_str, r"%d/%m/%y")
    except ValueError:
        return datetime.strptime(date_str, r"%d/%m/%Y")


def parse_footballdata_data(contents):
    import csv

    reader = [
        row for row in
        csv.DictReader(contents.splitlines())
        if row["FTHG"] and row["FTAG"]
    ]
    reader.sort(key=lambda x: parse_datetime(x["Date"]))
    data = []
    for row in reader:
        home_team = row["HomeTeam"]
        home_team = team_aliases.get(home_team, home_team)
        away_team = row["AwayTeam"]
        away_team = team_aliases.get(away_team, away_team)
        home_score = int(row["FTHG"])
        away_score = int(row["FTAG"])
        data.append((home_team, away_team, home_score, away_score))
    return data


def compute_cumulative_quantities(data, penalties=None):
    penalties = penalties or {}

    points = {}
    cumpoints = {}
    cumgoaldiff = {}
    cumgoalsscored = {}

    for home_team, away_team, home_goals, away_goals in data:
        # points
        if home_goals > away_goals:
            home_pts = 3
            away_pts = 0
        elif away_goals > home_goals:
            home_pts = 0
            away_pts = 3
        else:
            home_pts = away_pts = 1

        points.setdefault(home_team, []).append(home_pts)
        points.setdefault(away_team, []).append(away_pts)

        cumpoints.setdefault(home_team, [0]).append(
            cumpoints[home_team][-1] + home_pts
        )
        cumpoints.setdefault(away_team, [0]).append(
            cumpoints[away_team][-1] + away_pts
        )

        cumgoalsscored.setdefault(home_team, [0]).append(
            cumgoalsscored[home_team][-1] + home_goals
        )
        cumgoalsscored.setdefault(away_team, [0]).append(
            cumgoalsscored[away_team][-1] + away_goals
        )

        # goal diff
        home_goaldiff = home_goals - away_goals
        away_goaldiff = away_goals - home_goals

        cumgoaldiff.setdefault(home_team, [0]).append(
            cumgoaldiff[home_team][-1] + home_goaldiff
        )
        cumgoaldiff.setdefault(away_team, [0]).append(
            cumgoaldiff[away_team][-1] + away_goaldiff
        )

    teams = sorted(cumpoints.keys())
    points = {team: np.array(ps) for team, ps in points.items()}
    cumpoints = {team: np.array(ps) for team, ps in cumpoints.items()}
    cumgoaldiff = {team: np.array(ps) for team, ps in cumgoaldiff.items()}

    for team, penalty in penalties.items():
        cumpoints[team] -= penalty

    current_points = {team: cpts[-1] for team, cpts in cumpoints.items()}
    max_points = max(current_points.values())
    games_played = {team: len(ps) for team, ps in cumpoints.items()}
    max_games = max(games_played.values())

    ranked_teams = sorted(
        teams,
        key=lambda team: (
            cumpoints[team][-1],
            cumgoaldiff[team][-1],
            cumgoalsscored[team][-1],
            team,
        ),
    )
    places = {team: i for i, team in enumerate(ranked_teams)}

    return {
        "teams": teams,
        "ranked_teams": ranked_teams,
        "points": points,
        "cumpoints": cumpoints,
        "cumgoaldiff": cumgoaldiff,
        "current_points": current_points,
        "max_points": max_points,
        "games_played": games_played,
        "max_games": max_games,
        "total_games": 2 * (len(teams) - 1),
        "places": places,
        "cumgoalsscored": cumgoalsscored,
    }


style = collections.defaultdict(lambda: ("grey", "white", "o"))
style["Arsenal"] = ("#EF0107", "#FFFFFF", "$A$")
style["Aston Villa"] = ("#95BFE5", "#670E36", "$A$")
style["Birmingham"] = ("#183b90", "#FFFFFF", "$B$")
style["Blackburn"] = ("#009EE0", "#FFFFFF", "$B$")
style["Blackpool"] = ("#F68712", "#FFFFFF", "$B$")
style["Bolton"] = ("#263c7e", "#c80024", "$B$")
style["Bournemouth"] = ("#DA291C", "#000000", "$B$")
style["Bradford"] = ("#ffbf00", "#800000", "$B$")
style["Brentford"] = ("#e30613", "#fbb800", "$B$")
style["Brighton"] = ("#0057B8", "#FFCD00", "$B$")
style["Burnley"] = ("#6C1D45", "#ede939", "$B$")
style["Cardiff"] = ("#0070B5", "#D11524", "$C$")
style["Charlton"] = ("#000000", "#d4021d", "$C$")
style["Chelsea"] = ("#034694", "#DBA111", "$C$")
style["Coventry"] = ("#87beef", "#cbd7de", "$C$")
style["Crystal Palace"] = ("#1B458F", "#C4122E", "$C$")
style["Derby"] = ("#000000", "#FFFFFF", "$D$")
style["Everton"] = ("#003399", "#FFFFFF", "$E$")
style["Fulham"] = ("#000000", "#CC0000", "$F$")
style["Huddersfield"] = ("#0E63AD", "#FFFFFF", "$H$")
style["Hull"] = ("#F18A01", "#000000", "$H$")
style["Ipswich"] = ("#3764a4", "#df2834", "$I$")
style["Leeds"] = ("#1D428A", "#FFCD00", "$L$")
style["Leicester"] = ("#003090", "#FDBE11", "$L$")
style["Liverpool"] = ("#C8102E", "#00B2A9", "$L$")
style["Luton"] = ("#002e62", "#fb861f", "$L$")
style["Man City"] = ("#6CABDD", "#1C2C5B", "$M$")
style["Man Utd"] = ("#DA020E", "#FBE122", "$M$")
style["Middlesbrough"] = ("#DE1B22", "#FFFFFF", "$M$")
style["Newcastle"] = ("#241F20", "#FFFFFF", "$N$")
style["Norwich"] = ("#00A650", "#FFF200", "$N$")
style["Nottingham Forest"] = ("#DD0000", "#FFFFFF", "$N$")
style["Oldham"] = ("#004998", "#ffffff", "$O$")
style["Portsmouth"] = ("#001489", "#fbfdff", "$P$")
style["QPR"] = ("#175ba5", "#ffffff", "$Q$")
style["QRP"] = ("#1D5BA4", "#FFFFFF", "$Q$")
style["Reading"] = ("#004494", "#FFFFFF", "$R$")
style["Sheffield Utd"] = ("#EE2737", "#000000", "$S$")
style["Sheffield Weds"] = ("#4482d0", "#eab202", "$S$")
style["Southampton"] = ("#D71920", "#130C0E", "$S$")
style["Stoke"] = ("#E03A3E", "#1B449C", "$S$")
style["Sunderland"] = ("#eb172b", "#211e1e", "$S$")
style["Swansea"] = ("#000000", "#FFFFFF", "$S$")
style["Swindon"] = ("#dd0e14", "#b58e00", "$S$")
style["Tottenham"] = ("#132257", "#FFFFFF", "$T$")
style["Watford"] = ("#FBEE23", "#ED2127", "$W$")
style["West Brom"] = ("#122F67", "#FFFFFF", "$W$")
style["West Ham"] = ("#7A263A", "#1BB1E7", "$W$")
style["Wigan"] = ("#1d59af", "#FFFFFF", "$W$")
style["Wimbledon"] = ("#034bd4", "#ffff00", "$W$")
style["Wolves"] = ("#FDB913", "#231F20", "$W$")



fontfamily = "monospace"


NEUTRAL_STYLE = {
    "axes.edgecolor": (0.5, 0.5, 0.5),
    "axes.facecolor": (0, 0, 0, 0),
    "axes.grid": True,
    "axes.labelcolor": (0.5, 0.5, 0.5),
    "axes.spines.right": False,
    "axes.spines.top": False,
    "figure.facecolor": (0, 0, 0, 0),
    "grid.alpha": 0.1,
    "grid.color": (0.5, 0.5, 0.5),
    "legend.frameon": False,
    "text.color": (0.5, 0.5, 0.5),
    "xtick.color": (0.5, 0.5, 0.5),
    "xtick.minor.visible": True,
    "ytick.color": (0.5, 0.5, 0.5),
    "ytick.minor.visible": True,
    "font.family": fontfamily,
}


def setup_and_handle_figure(fn):
    @functools.wraps(fn)
    def wrapped(*args, figsize=(7, 7), ax=None, show_and_close=True, **kwargs):
        with mpl.style.context(NEUTRAL_STYLE):
            if ax is None:
                fig = plt.figure(figsize=figsize)
                ax = fig.add_subplot(111)
            else:
                fig = None

            fn(*args, ax=ax, **kwargs)

            if fig is not None:
                if show_and_close:
                    plt.show()
                    plt.close(fig)

            return fig, ax

    return wrapped


def set_ax_limits(ax, max_games, total_games, x_start=-0.5):
    from matplotlib.ticker import MaxNLocator

    if total_games - max_games < 8:
        # finish line
        ax.axvline(total_games, color="grey", linestyle="--", linewidth=1)
        ax.set_xlim(x_start, total_games + 0.5)
    else:
        ax.set_xlim(x_start, max_games + 0.5)

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


@setup_and_handle_figure
def plot_cumulative_points(
    data,
    ax,
    highlight="",
    highlight_color=(0.8, 1.0, 0.0),
):
    ranked_teams = data["ranked_teams"]
    cumpoints = data["cumpoints"]
    max_points = data["max_points"]
    max_games = data["max_games"]
    games_played = data["games_played"]
    places = data["places"]
    current_points = data["current_points"]

    for team in ranked_teams:
        ax.plot(
            cumpoints[team],
            label=team,
            color=style[team][0],
            markeredgecolor=style[team][1],
            alpha=0.75,
            marker=style[team][2],
            markersize=8,
            markeredgewidth=0.5,
            linewidth=2,
        )

        if team == highlight:
            ax.plot(
                cumpoints[team],
                label=team,
                color=highlight_color,
                zorder=-100,
                linewidth=10,
            )

    for team in ranked_teams:
        legend_xloc = games_played[team] * 1.05
        legend_yloc = max_points * places[team] / 19

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=style[team][1],
            backgroundcolor=(
                highlight_color if team == highlight else style[team][0]
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [current_points[team], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=style[team][0],
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    current_points_relegation = current_points[ranked_teams[2]]
    relegation_color = (0.3, 0.6, 0.0)
    ax.text(
        0,
        current_points_relegation,
        "Relegation",
        va="bottom",
        ha="right",
        color=relegation_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [current_points_relegation] * 2,
        zorder=-10,
        color=relegation_color,
        linestyle=":",
        alpha=2 / 3,
    )

    current_points_champs = current_points[ranked_teams[16]]
    champs_color = (0.0, 0.6, 0.3)
    ax.text(
        0,
        current_points_champs,
        "Champions League",
        va="bottom",
        ha="right",
        color=champs_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [current_points_champs] * 2,
        zorder=-10,
        color=champs_color,
        linestyle=":",
        alpha=2 / 3,
    )
    set_ax_limits(ax, max_games, data["total_games"])
    ax.set_ylim(-1, max_points + 1)
    ax.set_xlabel("Games Played")
    ax.set_ylabel("Points")


def pts_after_ngames(data, team, n):
    if n == 0:
        return 0
    return data["cumpoints"][team][: n + 1][-1]


def goaldiff_after_ngames(data, team, n):
    if n == 0:
        return 0
    return data["cumgoaldiff"][team][: n + 1][-1]


def goalsscored_after_ngames(data, team, n):
    if n == 0:
        return 0
    return data["cumgoalsscored"][team][: n + 1][-1]


@setup_and_handle_figure
def plot_positions(
    data,
    ax,
    highlight="",
    highlight_color=(0.8, 1.0, 0.0),
):
    teams = data["teams"]
    ranked_teams = data["ranked_teams"]
    max_games = data["max_games"]
    games_played = data["games_played"]

    positions = {}
    for n in range(max_games):
        ranked_teams_n = sorted(
            teams,
            key=lambda team: (
                -pts_after_ngames(data, team, n),
                -goaldiff_after_ngames(data, team, n),
                -goalsscored_after_ngames(data, team, n),
                team,
            ),
            reverse=True,
        )
        for i, team in enumerate(ranked_teams_n):
            positions.setdefault(team, []).append(i)

    for team in ranked_teams:
        ax.plot(
            positions[team],
            label=team,
            color=set_alpha(style[team][0], 0.5),
            markeredgecolor=style[team][1],
            marker=style[team][2],
            markersize=8,
            markeredgewidth=0.5,
            linewidth=2,
        )

        if team == highlight:
            ax.plot(
                positions[team],
                label=team,
                color=highlight_color,
                zorder=-100,
                linewidth=10,
            )

    for team in ranked_teams:
        legend_xloc = games_played[team] * 1.05
        legend_yloc = positions[team][-1]

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=style[team][1],
            backgroundcolor=(
                highlight_color if team == highlight else style[team][0]
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [positions[team][-1], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=style[team][0],
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    current_pos_relegation = 2.5
    relegation_color = (0.3, 0.6, 0.0)
    ax.text(
        -1,
        current_pos_relegation,
        "Relegation",
        va="bottom",
        ha="right",
        color=relegation_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [current_pos_relegation] * 2,
        zorder=-10,
        color=relegation_color,
        linestyle=":",
        alpha=2 / 3,
    )

    current_pos_champs = 15.5
    champs_color = (0.0, 0.6, 0.3)
    ax.text(
        -1,
        current_pos_champs,
        "Champions League",
        va="bottom",
        ha="right",
        color=champs_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [current_pos_champs] * 2,
        zorder=-10,
        color=champs_color,
        linestyle=":",
        alpha=2 / 3,
    )

    ax.set_xlabel("Games Played")
    ax.set_ylabel("Position")

    set_ax_limits(ax, max_games, data["total_games"])
    ax.set_ylim(-0.5, 19.5)
    ax.set_yticks([])


@setup_and_handle_figure
def plot_relative_performance(
    data,
    ax,
    highlight="",
    highlight_color=(0.8, 1.0, 0.0),
):
    teams = data["teams"]
    ranked_teams = data["ranked_teams"]
    cumpoints = data["cumpoints"]
    max_points = data["max_points"]
    max_games = data["max_games"]
    games_played = data["games_played"]
    places = data["places"]
    current_points = data["current_points"]

    best_pts = np.array(
        [
            max(pts_after_ngames(data, team, n) for team in teams)
            for n in range(max_games)
        ]
    )

    for team in ranked_teams:
        xs = np.arange(1, games_played[team])
        ys = cumpoints[team][1:] / best_pts[1 : games_played[team]]

        ax.plot(
            xs,
            ys,
            label=team,
            color=style[team][0],
            markeredgecolor=style[team][1],
            alpha=0.75,
            marker=style[team][2],
            markersize=8,
            markeredgewidth=0.5,
            linewidth=2,
        )

        if team == highlight:
            ax.plot(
                xs,
                ys,
                label=team,
                color=highlight_color,
                zorder=-100,
                linewidth=10,
            )

    for team in ranked_teams:
        legend_xloc = games_played[team] * 1.05
        legend_yloc = places[team] / 19

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=style[team][1],
            backgroundcolor=(
                highlight_color if team == highlight else style[team][0]
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [current_points[team] / max_points, legend_yloc]
        ax.plot(
            xs,
            ys,
            color=style[team][0],
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    current_points_relegation = current_points[ranked_teams[2]] / best_pts[-1]
    relegation_color = (0.3, 0.6, 0.0)
    ax.text(
        0,
        current_points_relegation,
        "Relegation",
        va="bottom",
        ha="right",
        color=relegation_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [current_points_relegation] * 2,
        zorder=-10,
        color=relegation_color,
        linestyle=":",
        alpha=2 / 3,
    )

    current_points_champs = current_points[ranked_teams[16]] / best_pts[-1]
    champs_color = (0.0, 0.6, 0.3)
    ax.text(
        0,
        current_points_champs,
        "Champions League",
        va="bottom",
        ha="right",
        color=champs_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [current_points_champs] * 2,
        zorder=-10,
        color=champs_color,
        linestyle=":",
        alpha=2 / 3,
    )

    ax.set_xlabel("Games Played")
    ax.set_ylabel("Relative points")

    set_ax_limits(ax, max_games, data["total_games"])
    ax.set_ylim(-0.02, 1.02)


@setup_and_handle_figure
def plot_extrapolated_performance(
    data,
    ax,
    highlight="",
    highlight_color=(0.8, 1.0, 0.0),
):
    ranked_teams = data["ranked_teams"]
    cumpoints = data["cumpoints"]
    games_played = data["games_played"]
    max_games = data["max_games"]
    extrap_points = {
        team: 114
        * cumpoints[team][1:]
        / (3 * np.arange(1, games_played[team]))
        for team in ranked_teams
    }
    ranked_teams.sort(key=lambda team: extrap_points[team][-1])
    places = {team: i for i, team in enumerate(ranked_teams)}

    for i, team in enumerate(ranked_teams):
        xs = np.arange(1, games_played[team])
        ys = extrap_points[team]

        if i == 2:
            abs_perf_relegation = ys[-1]
        if i == 16:
            abs_perf_champs = ys[-1]

        ax.plot(
            xs,
            ys,
            label=team,
            color=style[team][0],
            markeredgecolor=style[team][1],
            alpha=0.75,
            marker=style[team][2],
            markersize=8,
            markeredgewidth=0.5,
            linewidth=2,
        )

        if team == highlight:
            ax.plot(
                xs,
                ys,
                label=team,
                color=highlight_color,
                zorder=-100,
                linewidth=10,
            )

    for team in ranked_teams:
        legend_xloc = games_played[team] * 1.05
        legend_yloc = 3 * data["total_games"] * places[team] / 19

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=style[team][1],
            backgroundcolor=(
                highlight_color if team == highlight else style[team][0]
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [extrap_points[team][-1], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=style[team][0],
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    relegation_color = (0.3, 0.6, 0.0)
    ax.text(
        0,
        abs_perf_relegation,
        "Relegation",
        va="bottom",
        ha="right",
        color=relegation_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [abs_perf_relegation] * 2,
        zorder=-10,
        color=relegation_color,
        linestyle=":",
        alpha=2 / 3,
    )

    champs_color = (0.0, 0.6, 0.3)
    ax.text(
        0,
        abs_perf_champs,
        "Champions League",
        va="bottom",
        ha="right",
        color=champs_color,
        family=fontfamily,
    )
    ax.plot(
        [0, max_games],
        [abs_perf_champs] * 2,
        zorder=-10,
        color=champs_color,
        linestyle=":",
        alpha=2 / 3,
    )

    set_ax_limits(ax, max_games, data["total_games"], x_start=0.5)
    ax.set_xlabel("Games Played")
    ax.set_ylabel("Extrapolated Points")
    ax.set_ylim(-2, 117)


def window_form(points, window_size=5):
    return np.convolve(points, np.ones(window_size), "valid") / window_size


def exponential_form(points, window_size=5):
    form = []
    for i, p in enumerate(points, 1):
        if form:
            f_prev = form[-1]
        else:
            # start all teams on average form
            f_prev = 1.5

        form.append(
            ((window_size - 1) / window_size) * f_prev + (1 / window_size) * p
        )
    return form


@setup_and_handle_figure
def plot_form(
    data,
    ax,
    window_size=5,
    highlight="",
    highlight_color=(0.8, 1.0, 0.0),
):
    ranked_teams = data["ranked_teams"]
    games_played = data["games_played"]
    max_games = data["max_games"]
    current_points = data["current_points"]

    form = {
        team: exponential_form(data["points"][team], window_size)
        for team in ranked_teams
    }
    ranked_by_form_teams = sorted(
        ranked_teams,
        key=lambda team: (
            form[team][-1],
            data["cumgoaldiff"][team][-1],
            team,
        ),
    )

    for team in ranked_by_form_teams:
        ys = form[team]
        xs = np.arange(1, len(ys) + 1)

        ax.plot(
            xs,
            ys,
            label=team,
            color=style[team][0],
            markeredgecolor=style[team][1],
            alpha=0.75,
            marker=style[team][2],
            markersize=8,
            markeredgewidth=0.5,
            linewidth=2,
        )

        if team == highlight:
            ax.plot(
                xs,
                ys,
                label=team,
                color=highlight_color,
                zorder=-100,
                linewidth=10,
            )

    for i, team in enumerate(ranked_by_form_teams):
        legend_xloc = games_played[team] * 1.05
        legend_yloc = 3 * i / 19

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=style[team][1],
            backgroundcolor=(
                highlight_color if team == highlight else style[team][0]
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [form[team][-1], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=style[team][0],
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    team = ranked_teams[2]
    form_relegation = current_points[team] / games_played[team]
    relegation_color = (0.3, 0.6, 0.0)
    ax.text(
        0.0,
        form_relegation,
        "Relegation",
        va="bottom",
        ha="right",
        color=relegation_color,
        family=fontfamily,
    )
    ax.plot(
        [0.5, max_games],
        [form_relegation] * 2,
        zorder=-10,
        color=relegation_color,
        linestyle=":",
        alpha=2 / 3,
    )

    team = ranked_teams[16]
    form_champs = current_points[team] / games_played[team]
    champs_color = (0.0, 0.6, 0.3)
    ax.text(
        0.0,
        form_champs,
        "Champions League",
        va="bottom",
        ha="right",
        color=champs_color,
        family=fontfamily,
    )
    ax.plot(
        [0.5, max_games],
        [form_champs] * 2,
        zorder=-10,
        color=champs_color,
        linestyle=":",
        alpha=2 / 3,
    )

    team = ranked_teams[-1]
    form_winning = current_points[team] / games_played[team]
    champs_color = (0.0, 0.5, 0.4)
    ax.text(
        0.0,
        form_winning,
        "Winning",
        va="bottom",
        ha="right",
        color=champs_color,
        family=fontfamily,
    )
    ax.plot(
        [0.5, max_games],
        [form_winning] * 2,
        zorder=-10,
        color=champs_color,
        linestyle=":",
        alpha=2 / 3,
    )

    set_ax_limits(ax, max_games, data["total_games"], x_start=0.5)
    ax.set_xlabel("Games Played")
    ax.set_ylabel("Average points per game")
    ax.set_ylim(-0.1, 3.1)


def download_file_content(url):
    import requests

    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response
    return response.text


@functools.lru_cache
def get_footballdata(year, league="E0"):
    return download_file_content(
        "https://www.football-data.co.uk/mmz4281/"
        f"{year[-2:]}{str(int(year) + 1)[-2:]}/{league}.csv"
    )


def autoplot(
    year=2023,
    which="cumulative",
    highlight=None,
    source="footballdata",
    league="E0",
    **kwargs
):
    # import pathlib

    year = str(year)
    if (year == "2023") and (league == "E0"):
        penalties = {
            "Everton": 6,
            "Nottingham Forest": 4,
        }
    else:
        penalties = None

    # if source == "fixturedownload":
    #     fname = pathlib.Path(__file__).parent / f"data/epl-{year}-UTC.csv"
    # elif source == "footballdata":
    #     fname = pathlib.Path(__file__).parent / f"data/E0-{year}.csv"
    # else:
    #     raise ValueError(f"Unknown data source {source}")

    # with open(fname, "r") as f:
    #     contents = f.read()

    contents = get_footballdata(year=year, league=league)

    if source == "fixturedownload":
        data = parse_fixturedownload_data(contents)
    elif source == "footballdata":
        data = parse_footballdata_data(contents)
    data = compute_cumulative_quantities(data, penalties=penalties)

    with mpl.style.context(NEUTRAL_STYLE):

        height = 7
        width = 12 * (data["max_games"] / data["total_games"]) ** 0.5

        if which == "cumulative":
            fn = plot_cumulative_points
        elif which == "extrapolated":
            fn = plot_extrapolated_performance
        elif which == "position":
            fn = plot_positions
        elif which == "relative":
            fn = plot_relative_performance
        elif which == "form":
            fn = plot_form
        else:
            raise ValueError(f"Unknown plot type {which}")

        return fn(data, highlight=highlight, figsize=(width, height), **kwargs)

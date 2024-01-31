import collections
import functools
import pathlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def set_alpha(c, alpha):
    import matplotlib as mpl

    rgb = mpl.colors.to_rgb(c)
    return (*rgb, alpha)


def update_data(year=2023):
    import urllib

    urllib.request.urlretrieve(
        f"https://fixturedownload.com/download/epl-{year}-GMTStandardTime.csv",
        pathlib.Path(__file__).parent / f"data/epl-{year}-UTC.csv"
    )


def process_data(filename, penalties=None):
    import re

    penalties = penalties or {}

    with open(filename, "r") as f:
        lines = f.read()

    _, *lines = lines.split("\n")[:-1]
    lines = [line.split(",") for line in lines]

    points = {}
    cumpoints = {}
    cumgoaldiff = {}

    for line in lines:
        score = line[6]
        match = re.match(r"(\d+) - (\d+)", score)
        if match:
            home, away = match.groups()
            home, away = int(home), int(away)

            # teams
            home_team = line[4]
            away_team = line[5]

            # points
            if home > away:
                home_pts = 3
                away_pts = 0
            elif away > home:
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

            # goal diff
            home_goaldiff = home - away
            away_goaldiff = away - home

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
        teams, key=lambda team: (cumpoints[team][-1], cumgoaldiff[team][-1], team)
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
        "places": places,
    }


style = collections.defaultdict(lambda: ("grey", "white", "o"))
style["Arsenal"] = ("#EF0107", "#FFFFFF", "$A$")
style["Newcastle"] = ("#241F20", "#FFFFFF", "$N$")
style["Man City"] = ("#6CABDD", "#1C2C5B", "$M$")
style["Spurs"] = ("#132257", "#FFFFFF", "$T$")
style["Man Utd"] = ("#DA020E", "#FBE122", "$M$")
style["Brighton"] = ("#0057B8", "#FFCD00", "$B$")
style["Aston Villa"] = ("#95BFE5", "#670E36", "$A$")
style["Crystal Palace"] = ("#1B458F", "#C4122E", "$C$")
style["Fulham"] = ("#000000", "#CC0000", "$F$")
style["Liverpool"] = ("#C8102E", "#00B2A9", "$L$")
style["Bournemouth"] = ("#DA291C", "#000000", "$B$")
style["Leeds"] = ("#1D428A", "#FFCD00", "$L$")
style["Wolves"] = ("#FDB913", "#231F20", "$W$")
style["Nottingham Forest"] = ("#DD0000", "#FFFFFF", "$N$")
style["Southampton"] = ("#D71920", "#130C0E", "$S$")
style["Everton"] = ("#003399", "#FFFFFF", "$E$")
style["Chelsea"] = ("#034694", "#DBA111", "$C$")
style["Leicester"] = ("#003090", "#FDBE11", "$L$")
style["Brentford"] = ("#e30613", "#fbb800", "$B$")
style["West Ham"] = ("#7A263A", "#1BB1E7", "$W$")
style["Burnley"] = ("#6C1D45", "#ede939", "$B$")
style["Watford"] = ("#FBEE23", "#ED2127", "$W$")
style["Norwich"] = ("#00A650", "#FFF200", "$N$")
style["Sheffield Utd"] = ("#EE2737", "#000000", "$S$")
style["West Brom"] = ("#122F67", "#FFFFFF", "$W$")
style["Cardiff"] = ("#0070B5", "#D11524", "$C$")
style["Huddersfield"] = ("#0E63AD", "#FFFFFF", "$H$")
style["Stoke"] = ("#E03A3E", "#1B449C", "$S$")
style["Swansea"] = ("#000000", "#FFFFFF", "$S$")
style["Hull"] = ("#F18A01", "#000000", "$H$")
style["Middlesbrough"] = ("#DE1B22", "#FFFFFF", "$M$")
style["Sunderland"] = ("#eb172b", "#211e1e", "$S$")
style["Luton"] = ("#002e62", "#fb861f", "$L$")


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


def set_ax_limits(ax, max_games, x_start=-0.5):
    from matplotlib.ticker import MaxNLocator

    if max_games > 30:
        # finish line
        ax.axvline(38, color="grey", linestyle="--", linewidth=1)
        ax.set_xlim(x_start, 38.5)
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
            backgroundcolor=(highlight_color if team == highlight else style[team][0]),
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
    set_ax_limits(ax, max_games)
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
            backgroundcolor=(highlight_color if team == highlight else style[team][0]),
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

    set_ax_limits(ax, max_games)
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
            backgroundcolor=(highlight_color if team == highlight else style[team][0]),
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

    set_ax_limits(ax, max_games)
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
    places = data["places"]
    current_points = data["current_points"]

    for i, team in enumerate(ranked_teams):
        xs = np.arange(1, games_played[team])
        ys = 114 * cumpoints[team][1:] / (3 * np.arange(1, games_played[team]))

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
        legend_yloc = 100 * places[team] / 19

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=style[team][1],
            backgroundcolor=(highlight_color if team == highlight else style[team][0]),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [current_points[team] / (3 / 114 * games_played[team]), legend_yloc]
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

    set_ax_limits(ax, max_games, x_start=0.5)
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
            ((window_size - 1) / window_size) * f_prev +
            (1 / window_size) * p
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
            backgroundcolor=(highlight_color if team == highlight else style[team][0]),
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

    set_ax_limits(ax, max_games, x_start=0.5)
    ax.set_xlabel("Games Played")
    ax.set_ylabel("Average points per game")
    ax.set_ylim(-0.1, 3.1)


def autoplot(year=2023, which="cumulative", highlight=None, **kwargs):
    import pathlib

    year = str(year)
    if year == "2023":
        penalties = {"Everton": 10}
    else:
        penalties = None

    fname = pathlib.Path(__file__).parent / f"data/epl-{year}-UTC.csv"

    with mpl.style.context(NEUTRAL_STYLE):
        data = process_data(fname, penalties=penalties)

        height = 7
        width = 12 * (data["max_games"] / 38) ** 0.5

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

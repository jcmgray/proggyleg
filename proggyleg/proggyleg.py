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


def generate_notebook_doc(year=2023, league="E0", dynamic="auto"):
    import pathlib
    import nbformat as nbf

    fullnames = {
        "E0": "Premier League",
        "E1": "EFL Championship",
        "E2": "EFL League One",
        "SP1": "La Liga",
        "I1": "Serie A",
        "D1": "Bundesliga",
        "SC0": "Scottish Premiership",
    }

    if dynamic == "auto":
        dynamic = year == 2023

    filename = (
        pathlib.Path(__file__).parent.parent
        / "docs"
        / league
        / f"{year}.ipynb"
    ).resolve()

    cells = []
    cells.append(
        nbf.v4.new_markdown_cell(
            "\n".join(
                (
                    f"# {year} / {year + 1}",
                    "",
                    f"Progress points for the {fullnames[league]} "
                    f"{year} / {year + 1} season.",
                )
            )
        )
    )
    cells.append(
        nbf.v4.new_code_cell(
            "\n".join(
                (
                    "%config InlineBackend.figure_formats = ['svg']",
                    "from proggyleg import proggyleg",
                    f"year = {year}",
                    f'league = "{league}"',
                )
            )
        )
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            "\n".join(
                (
                    "## Cumulative Points",
                    "",
                    "The sum of points up to a given game played.",
                )
            )
        )
    )
    cells.append(
        nbf.v4.new_code_cell(
            "\n".join(
                ('proggyleg.autoplot(year, league, which="cumulative");',)
            )
        )
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            "\n".join(
                (
                    "## Extrapolated Points",
                    "",
                    "Final points assuming each team continues to score "
                    "points at the same rate as they have so far.",
                )
            )
        )
    )
    cells.append(
        nbf.v4.new_code_cell(
            "\n".join(
                ('proggyleg.autoplot(year, league, which="extrapolated");',)
            )
        )
    )
    cells.append(nbf.v4.new_markdown_cell("\n".join(("## Position",))))
    cells.append(
        nbf.v4.new_code_cell(
            "\n".join(('proggyleg.autoplot(year, league, which="position");',))
        )
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            "\n".join(
                (
                    "## Rolling Form",
                    "",
                    "Exponential weighted moving "
                    "average of points won per game.",
                )
            )
        )
    )
    cells.append(
        nbf.v4.new_code_cell(
            "\n".join(('proggyleg.autoplot(year, league, which="form");',))
        )
    )
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["mystnb"] = {
        "execution_mode": "force" if dynamic else "off",
    }
    nbf.write(nb, filename)


def execute_notebook_doc(year, league):
    import subprocess

    filename = str(
        (
            pathlib.Path(__file__).parent.parent
            / "docs"
            / league
            / f"{year}.ipynb"
        ).resolve()
    )
    command = [
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        filename,
    ]
    subprocess.run(command, check=True)


style = collections.defaultdict(lambda: ("grey", "white", "o"))


# England
style["Accrington"] = ("#c12a19", "#87cefa", "$A$")
style["Arsenal"] = ("#EF0107", "#FFFFFF", "$A$")
style["Aston Villa"] = ("#95BFE5", "#670E36", "$A$")
style["Barnsley"] = ("#a80409", "#e1e3e3", "$B$")
style["Birmingham"] = ("#183b90", "#FFFFFF", "$B$")
style["Blackburn"] = ("#009EE0", "#FFFFFF", "$B$")
style["Blackpool"] = ("#F68712", "#FFFFFF", "$B$")
style["Bolton"] = ("#263c7e", "#c80024", "$B$")
style["Bournemouth"] = ("#DA291C", "#000000", "$B$")
style["Bradford"] = ("#ffbf00", "#800000", "$B$")
style["Brentford"] = ("#e30613", "#fbb800", "$B$")
style["Brighton"] = ("#0057B8", "#FFCD00", "$B$")
style["Bristol City"] = ("#e3131e", "#ffffff", "$B$")
style["Bristol Rvs"] = ("#004a96", "#ffe100", "$B$")
style["Burnley"] = ("#6C1D45", "#ede939", "$B$")
style["Burton"] = ("#fffa05", "#000000", "$B$")
style["Cambridge"] = ("#fbba45", "#000000", "$C$")
style["Cardiff"] = ("#0070B5", "#D11524", "$C$")
style["Carlisle"] = ("#1d6fb8", "#ee192e", "$C$")
style["Charlton"] = ("#0f0f0f", "#d4021d", "$C$")
style["Chelsea"] = ("#034694", "#DBA111", "$C$")
style["Cheltenham"] = ("#df1c24", "#000000", "$C$")
style["Colchester"] = ("#0066a6", "#fcb23e", "$C$")
style["Coventry"] = ("#87beef", "#cbd7de", "$C$")
style["Crewe"] = ("#fafafa", "#d62818", "$C$")
style["Crystal Palace"] = ("#1B458F", "#C4122E", "$C$")
style["Derby"] = ("#0f0f0f", "#FFFFFF", "$D$")
style["Doncaster"] = ("#d81e20", "#121212", "$D$")
style["Everton"] = ("#003399", "#FFFFFF", "$E$")
style["Exeter"] = ("#ee1242", "#000000", "$E$")
style["Fleetwood Town"] = ("#e90000", "#FFFFFF", "$F$")
style["Forest Green"] = ("#b6dd0f", "#1d191a", "$F$")
style["Fulham"] = ("#0f0f0f", "#CC0000", "$F$")
style["Gillingham"] = ("#1d191a", "#135daf", "$G$")
style["Huddersfield"] = ("#0E63AD", "#FFFFFF", "$H$")
style["Hull"] = ("#F18A01", "#000000", "$H$")
style["Ipswich"] = ("#3764a4", "#df2834", "$I$")
style["Leeds"] = ("#ffe100", "#0060aa", "$L$")
style["Leicester"] = ("#003090", "#FDBE11", "$L$")
style["Leyton Orient"] = ("#ee1c22", "#f8f9fa", "$L$")
style["Lincoln"] = ("#fe0000", "#ffffff", "$L$")
style["Liverpool"] = ("#C8102E", "#00B2A9", "$L$")
style["Luton"] = ("#002e62", "#fb861f", "$L$")
style["Man City"] = ("#6CABDD", "#1C2C5B", "$M$")
style["Man Utd"] = ("#DA020E", "#FBE122", "$M$")
style["Middlesbrough"] = ("#DE1B22", "#FFFFFF", "$M$")
style["Millwall"] = ("#00337b", "#90a4a3", "$M$")
style["Milton Keynes"] = ("#fafafa", "#e71825", "$M$")
style["Morecambe"] = ("#991916", "#bb9e66", "$M$")
style["Newcastle"] = ("#241F20", "#FFFFFF", "$N$")
style["Northampton"] = ("#8d2940", "#a07e44", "$N$")
style["Norwich"] = ("#00A650", "#FFF200", "$N$")
style["Nottingham Forest"] = ("#DD0000", "#FFFFFF", "$N$")
style["Oldham"] = ("#004998", "#ffffff", "$O$")
style["Oxford"] = ("#fff200", "#001959", "$O$")
style["Peterboro"] = ("#0067b5", "#a6c3dc", "$P$")
style["Plymouth"] = ("#003c2b", "#d5a44d", "$P$")
style["Port Vale"] = ("#f4a106", "#070604", "$P$")
style["Portsmouth"] = ("#001489", "#fbfdff", "$P$")
style["Preston"] = ("#f4f4f4", "#000055", "$P$")
style["QPR"] = ("#175ba5", "#ffffff", "$Q$")
style["QRP"] = ("#1D5BA4", "#FFFFFF", "$Q$")
style["Reading"] = ("#004494", "#FFFFFF", "$R$")
style["Rotherham"] = ("#e31720", "#ffffff", "$R$")
style["Scunthorpe"] = ("#aa2e47", "#00adde", "$S$")
style["Sheffield Utd"] = ("#EE2737", "#000000", "$S$")
style["Sheffield Weds"] = ("#4482d0", "#eab202", "$S$")
style["Shrewsbury"] = ("#00499a", "#f6a900", "$S$")
style["Southampton"] = ("#D71920", "#130C0E", "$S$")
style["Southend"] = ("#003781", "#ffffff", "$S$")
style["Stevenage"] = ("#ad0e2a", "#ba9d04", "$S$")
style["Stoke"] = ("#E03A3E", "#1B449C", "$S$")
style["Sunderland"] = ("#eb172b", "#211e1e", "$S$")
style["Swansea"] = ("#0f0f0f", "#FFFFFF", "$S$")
style["Swindon"] = ("#dd0e14", "#b58e00", "$S$")
style["Tottenham"] = ("#132257", "#FFFFFF", "$T$")
style["Watford"] = ("#FBEE23", "#ED2127", "$W$")
style["West Brom"] = ("#122F67", "#FFFFFF", "$W$")
style["West Ham"] = ("#7A263A", "#1BB1E7", "$W$")
style["Wigan"] = ("#1d59af", "#FFFFFF", "$W$")
style["Wimbledon"] = ("#034bd4", "#ffff00", "$W$")
style["Wolves"] = ("#FDB913", "#231F20", "$W$")
style["Wycombe"] = ("#002f62", "#4db7e4", "$W$")
style["Yeovil"] = ("#4cad21", "#ffff00", "$Y$")

# Scotland
style["Dundee United"] = ("#fd6701", "#121212", "$D$")
style["Ross County"] = ("#00065b", "#ee1b24", "$R$")
style["Kilmarnock"] = ("#2b3390", "#c07634", "$K$")
style["St Johnstone"] = ("#0052a2", "#ddd3af", "$S$")
style["Livingston"] = ("#fbc905", "#000000", "$L$")
style["St Mirren"] = ("#0f0f0f", "#ffffff", "$S$")
style["Motherwell"] = ("#f6b800", "#9e0000", "$M$")
style["Hibernian"] = ("#007638", "#f8f9fa", "$H$")
style["Hearts"] = ("#a1122d", "#d1d3d4", "$H$")
style["Aberdeen"] = ("#e30013", "#ffffff", "$A$")
style["Rangers"] = ("#002ea1", "#ffffff", "$R$")
style["Celtic"] = ("#009d4a", "#fefffe", "$C$")
style["Dundee"] = ("#152142", "#ffffff", "$D$")
style["Hamilton"] = ("#cd363d", "#ffffff", "$H$")
style["Partick"] = ("#a90000", "#ffdf00", "$P$")

# Germany
style["Aachen"] = ("#0f0f0f", "#ffde00", "$A$")
style["Augsburg"] = ("#bb342f", "#44724c", "$A$")
style["Bayern Munich"] = ("#dd0029", "#0066b3", "$B$")
style["Bielefeld"] = ("#005c9e", "#000100", "$B$")
style["Bochum"] = ("#1b2b56", "#8dcbff", "$B$")
style["Cottbus"] = ("#ff0000", "#ffffff", "$C$")
style["Darmstadt"] = ("#004ea0", "#ffffff", "$D$")
style["Dortmund"] = ("#ffda00", "#000000", "$D$")
style["Duisburg"] = ("#1f326e", "#ffffff", "$D$")
style["Ein Frankfurt"] = ("#0f0f0f", "#ff0000", "$E$")
style["FC Koln"] = ("#fbfbfb", "#fb0000", "$F$")
style["Fortuna Dusseldorf"] = ("#e40008", "#ffffff", "$F$")
style["Freiburg"] = ("#ff0000", "#000000", "$F$")
style["Greuther Furth"] = ("#fafafa", "#009d37", "$G$")
style["Hamburg"] = ("#185cb5", "#1d191a", "$H$")
style["Hannover"] = ("#179d33", "#000000", "$H$")
style["Hansa Rostock"] = ("#006eb9", "#e74021", "$H$")
style["Heidenheim"] = ("#e30013", "#00387a", "$H$")
style["Hertha"] = ("#f8f8f8", "#004c9f", "$H$")
style["Hoffenheim"] = ("#1261b6", "#ffffff", "$H$")
style["Ingolstadt"] = ("#440000", "#df000c", "$I$")
style["Kaiserslautern"] = ("#e40008", "#ffffff", "$K$")
style["Karlsruhe"] = ("#004b95", "#ffffff", "$K$")
style["Leverkusen"] = ("#141115", "#e32221", "$L$")
style["Mainz"] = ("#ff0000", "#f2f2f2", "$M$")
style["Mönchengladbach"] = ("#0f0f0f", "#008b43", "$M$")
style["Munich 1860"] = ("#78bcff", "#ffffff", "$M$")
style["Nurnberg"] = ("#0f0f0f", "#ac081f", "$N$")
style["Paderborn"] = ("#0f0f0f", "#005caa", "$P$")
style["RB Leipzig"] = ("#de013f", "#001945", "$R$")
style["Schalke 04"] = ("#004a9d", "#ffffff", "$S$")
style["St Pauli"] = ("#624636", "#e4010b", "$S$")
style["Stuttgart"] = ("#d5011d", "#ffffff", "$S$")
style["Union Berlin"] = ("#ec121d", "#fddd00", "$U$")
style["Unterhaching"] = ("#ee1b21", "#3aa0db", "$U$")
style["Werder Bremen"] = ("#169152", "#ffffff", "$W$")
style["Wolfsburg"] = ("#51a700", "#f8f9fa", "$W$")

# Italy
style["Salernitana"] = ("#68130a", "#c49a29", "$S$")
style["Sassuolo"] = ("#2fb75b", "#1d191a", "$S$")
style["Empoli"] = ("#0055ff", "#15134b", "$E$")
style["Frosinone"] = ("#ffe500", "#006ab5", "$F$")
style["Cagliari"] = ("#282846", "#d10125", "$C$")
style["Verona"] = ("#002b6c", "#fee21d", "$V$")
style["Udinese"] = ("#808080", "#000000", "$U$")
style["Lecce"] = ("#ffee00", "#e30013", "$L$")
style["Genoa"] = ("#b01212", "#00213c", "$G$")
style["Monza"] = ("#ee0e36", "#ffffff", "$M$")
style["Fiorentina"] = ("#61328c", "#de2e1f", "$F$")
style["Torino"] = ("#800000", "#f5f5dc", "$T$")
style["Napoli"] = ("#12a0d7", "#003c82", "$N$")
style["Lazio"] = ("#86d9f8", "#d9aa00", "$L$")
style["Atalanta"] = ("#1d191a", "#295cb0", "$A$")
style["Roma"] = ("#980228", "#fbbb00", "$R$")
style["Bologna"] = ("#04043d", "#d50e0e", "$B$")
style["Juventus"] = ("#0f0f0f", "#efefef", "$J$")
style["Milan"] = ("#e50027", "#000000", "$M$")
style["Inter"] = ("#001d9d", "#000000", "$I$")
style["Sampdoria"] = ("#007abc", "#dd3214", "$S$")
style["Cremonese"] = ("#ee151f", "#818386", "$C$")
style["Spezia"] = ("#ebebeb", "#000000", "$S$")

# Spain
style["Alaves"] = ("#002ea1", "#ffffff", "$A$")
style["Almeria"] = ("#e40008", "#ffd000", "$A$")
style["Ath Bilbao"] = ("#ef201d", "#ffffff", "$A$")
style["Ath Madrid"] = ("#f60000", "#212b61", "$A$")
style["Barcelona"] = ("#00009f", "#ba002f", "$B$")
style["Betis"] = ("#00964b", "#ffffff", "$B$")
style["Cadiz"] = ("#fde701", "#0043a9", "$C$")
style["Celta"] = ("#80bfff", "#e6204d", "$C$")
style["Elche"] = ("#008000", "#ffffff", "$E$")
style["Espanol"] = ("#005bca", "#ff0812", "$E$")
style["Getafe"] = ("#0082c4", "#d3d4d6", "$G$")
style["Girona"] = ("#d00424", "#0042ff", "$G$")
style["Granada"] = ("#c40e2e", "#0000ff", "$G$")
style["Las Palmas"] = ("#ffe500", "#004a9e", "$L$")
style["Mallorca"] = ("#ee141e", "#fff700", "$M$")
style["Osasuna"] = ("#00003c", "#cd0000", "$O$")
style["Real Madrid"] = ("#fbfbfb", "#fcc000", "$R$")
style["Sevilla"] = ("#f8f9fa", "#d8061b", "$S$")
style["Sociedad"] = ("#0c398c", "#e7a70c", "$S$")
style["Valencia"] = ("#ef321f", "#ffe015", "$V$")
style["Valladolid"] = ("#6f2989", "#fcd400", "$V$")
style["Vallecano"] = ("#c0b02c", "#e43215", "$V$")
style["Villarreal"] = ("#ffe767", "#e80000", "$V$")

team_aliases = {
    "1. FC Heidenheim 1846": "Heidenheim",
    "1. FC Köln": "FC Koln",
    "1. FC Union Berlin": "Union Berlin",
    "1. FSV Mainz 05": "Mainz",
    "Athletic Club": "Ath Bilbao",
    "Atlético de Madrid": "Ath Madrid",
    "Bayer 04 Leverkusen": "Leverkusen",
    "Birmingham City": "Birmingham",
    "Blackburn Rovers": "Blackburn",
    "Borussia Dortmund": "Dortmund",
    "Borussia Mönchengladbach": "Mönchengladbach",
    "CA Osasuna": "Osasuna",
    "Cádiz CF": "Cadiz",
    "Cardiff City": "Cardiff",
    "Coventry City": "Coventry",
    "Deportivo Alavés": "Alaves",
    "Eintracht Frankfurt": "Ein Frankfurt",
    "FC Augsburg": "Augsburg",
    "FC Barcelona": "Barcelona",
    "FC Bayern München": "Bayern Munich",
    "Getafe CF": "Getafe",
    "Girona FC": "Girona",
    "Granada CF": "Granada",
    "Hellas Verona": "Verona",
    "Huddersfield Town": "Huddersfield",
    "Hull City": "Hull",
    "Ipswich Town": "Ipswich",
    "Leeds United": "Leeds",
    "Leicester City": "Leicester",
    "M'gladbach": "Mönchengladbach",
    "Man United": "Man Utd",
    "Milton Keynes Dons": "Milton Keynes",
    "Norwich City": "Norwich",
    "Nott'm Forest": "Nottingham Forest",
    "Plymouth Argyle": "Plymouth",
    "Preston North End": "Preston",
    "Queens Park Rangers": "QPR",
    "Rayo Vallecano": "Vallecano",
    "RC Celta": "Celta",
    "RCD Mallorca": "Mallorca",
    "Real Betis": "Betis",
    "Real Sociedad": "Sociedad",
    "Rotherham United": "Rotherham",
    "Sevilla FC": "Sevilla",
    "Sheffield United": "Sheffield Utd",
    "Sheffield Wednesday": "Sheffield Weds",
    "Sport-Club Freiburg": "Freiburg",
    "Spurs": "Tottenham",
    "Stoke City": "Stoke",
    "SV Darmstadt 98": "Darmstadt",
    "SV Werder Bremen": "Werder Bremen",
    "Swansea City": "Swansea",
    "TSG Hoffenheim": "Hoffenheim",
    "UD Almería": "Almeria",
    "UD Las Palmas": "Las Palmas",
    "Valencia CF": "Valencia",
    "VfB Stuttgart": "Stuttgart",
    "VfL Bochum 1848": "Bochum",
    "VfL Wolfsburg": "Wolfsburg",
    "Villarreal CF": "Villarreal",
    "West Bromwich Albion": "West Brom",
}


def maker_default_entry(team):
    style[team] = ("grey", "white", f"${team[0]}$")


def get_color0(team):
    if team not in style:
        print(team)
        maker_default_entry(team)
    return style[team][0]


def get_color1(team):
    if team not in style:
        print(team)
        maker_default_entry(team)
    return style[team][1]


def get_marker(team):
    if team not in style:
        print(team)
        maker_default_entry(team)
    return style[team][2]


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
        row
        for row in csv.DictReader(contents.splitlines())
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


def compute_cumulative_quantities(data, penalties=None, league="E0"):
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

    if league == "SC0":
        total_games = 4 * (len(teams) - 1)
    else:
        total_games = 2 * (len(teams) - 1)

    return {
        "cumgoaldiff": cumgoaldiff,
        "cumgoalsscored": cumgoalsscored,
        "cumpoints": cumpoints,
        "current_points": current_points,
        "games_played": games_played,
        "max_games": max_games,
        "max_points": max_points,
        "num_teams": len(teams),
        "places": places,
        "points": points,
        "ranked_teams": ranked_teams,
        "teams": teams,
        "total_games": total_games,
        "league": league,
    }


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


_SPANS = {
    "E0": [
        ("Champions League", -4, (0.0, 0.6, 0.3)),
        ("Relegation", 2, (0.3, 0.6, 0.0)),
    ],
    "E1": [
        ("Automatic", -2, (0.0, 0.6, 0.3)),
        ("Playoffs", -6, (0.3, 0.6, 0.0)),
        ("Relegation", 2, (0.3, 0.6, 0.0)),
    ],
    "E2": [
        ("Automatic", -2, (0.0, 0.6, 0.3)),
        ("Playoffs", -6, (0.3, 0.6, 0.0)),
        ("Relegation", 3, (0.3, 0.6, 0.0)),
    ],
    "D1": [
        ("Champions League", -4, (0.0, 0.6, 0.3)),
        ("Relegation", 1, (0.3, 0.6, 0.0)),
        ("Playoff", 2, (0.3, 0.6, 0.0)),
    ],
    "I1": [
        ("Champions League", -4, (0.0, 0.6, 0.3)),
        ("Relegation", 2, (0.3, 0.6, 0.0)),
    ],
    "SP1": [
        ("Champions League", -4, (0.0, 0.6, 0.3)),
        ("Relegation", 2, (0.3, 0.6, 0.0)),
    ],
    "SC0": [
        ("Champions League", -2, (0.0, 0.6, 0.3)),
        ("Relegation", 0, (0.3, 0.6, 0.0)),
    ],
}


def plot_spans(
    ax,
    ys,
    max_games,
    num_teams,
    league="E0",
):
    spans = _SPANS.get(league, None)
    if spans is None:
        return

    for label, pos, color in spans:
        if pos < 0:
            pos = num_teams + pos

        ax.text(
            0,
            ys[pos],
            label,
            va="bottom",
            ha="right",
            color=color,
            family=fontfamily,
            fontsize=8,
        )
        ax.plot(
            [0, max_games],
            [ys[pos]] * 2,
            zorder=-10,
            color=color,
            linestyle=":",
            alpha=2 / 3,
        )


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
            color=get_color0(team),
            markeredgecolor=get_color1(team),
            alpha=0.75,
            marker=get_marker(team),
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
        legend_yloc = max_points * places[team] / (data["num_teams"] - 1)

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=get_color1(team),
            backgroundcolor=(
                highlight_color if team == highlight else get_color0(team)
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [current_points[team], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=get_color0(team),
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    plot_spans(
        ax,
        [current_points[team] for team in ranked_teams],
        max_games,
        num_teams=data["num_teams"],
        league=data["league"],
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
            color=set_alpha(get_color0(team), 0.5),
            markeredgecolor=get_color1(team),
            marker=get_marker(team),
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
            color=get_color1(team),
            backgroundcolor=(
                highlight_color if team == highlight else get_color0(team)
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [positions[team][-1], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=get_color0(team),
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    plot_spans(
        ax,
        # want relegation lines to appear above
        [i + 0.5 if i <= 3 else i - 0.5 for i in range(data["num_teams"])],
        max_games,
        num_teams=data["num_teams"],
        league=data["league"],
    )

    ax.set_xlabel("Games Played")
    ax.set_ylabel("Position")

    set_ax_limits(ax, max_games, data["total_games"])
    ax.set_ylim(-0.5, data["num_teams"] - 0.5)
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
            color=get_color0(team),
            markeredgecolor=get_color1(team),
            alpha=0.75,
            marker=get_marker(team),
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
        legend_yloc = places[team] / (data["num_teams"] - 1)

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=get_color1(team),
            backgroundcolor=(
                highlight_color if team == highlight else get_color0(team)
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [current_points[team] / max_points, legend_yloc]
        ax.plot(
            xs,
            ys,
            color=get_color0(team),
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    plot_spans(
        ax,
        [current_points[team] / best_pts[-1] for team in ranked_teams],
        max_games,
        num_teams=data["num_teams"],
        league=data["league"],
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
        team: 3
        * data["total_games"]
        * cumpoints[team][1:]
        / (3 * np.arange(1, games_played[team]))
        for team in ranked_teams
    }
    ranked_teams.sort(key=lambda team: extrap_points[team][-1])
    places = {team: i for i, team in enumerate(ranked_teams)}

    for i, team in enumerate(ranked_teams):
        xs = np.arange(1, games_played[team])
        ys = extrap_points[team]

        ax.plot(
            xs,
            ys,
            label=team,
            color=get_color0(team),
            markeredgecolor=get_color1(team),
            alpha=0.75,
            marker=get_marker(team),
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
        legend_yloc = (
            3 * data["total_games"] * places[team] / (data["num_teams"] - 1)
        )

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=get_color1(team),
            backgroundcolor=(
                highlight_color if team == highlight else get_color0(team)
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [extrap_points[team][-1], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=get_color0(team),
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
        )

    plot_spans(
        ax,
        [extrap_points[team][-1] for team in ranked_teams],
        max_games,
        num_teams=data["num_teams"],
        league=data["league"],
    )

    set_ax_limits(ax, max_games, data["total_games"], x_start=0.5)
    ax.set_xlabel("Games Played")
    ax.set_ylabel("Extrapolated Points")
    ax.set_ylim(-2, 3 * (data["total_games"] + 1))


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
            color=get_color0(team),
            markeredgecolor=get_color1(team),
            alpha=0.75,
            marker=get_marker(team),
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
        legend_yloc = 3 * i / (data["num_teams"] - 1)

        ax.text(
            legend_xloc,
            legend_yloc,
            team,
            ha="left",
            va="bottom",
            weight="bold",
            family=fontfamily,
            color=get_color1(team),
            backgroundcolor=(
                highlight_color if team == highlight else get_color0(team)
            ),
        )

        xs = [games_played[team] - 0.75, legend_xloc]
        ys = [form[team][-1], legend_yloc]
        ax.plot(
            xs,
            ys,
            color=get_color0(team),
            linestyle="--",
            alpha=0.25,
            linewidth=2 / 3,
            clip_on=False,
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


FIXTUREDOWNLOAD_LEAGUE_ALIASES = {
    "E0": "epl",
    "E1": "championship",
    "SP1": "la-liga",
    "I1": "serie-a",
    "D1": "bundesliga",
}


@functools.lru_cache
def get_fixturedownload(year, league="E0"):
    identifier = FIXTUREDOWNLOAD_LEAGUE_ALIASES[league]
    return download_file_content(
        f"https://fixturedownload.com/download/{identifier}-{year}-UTC.csv"
    )


def autoplot(
    year=2023,
    league="E0",
    which="cumulative",
    highlight=None,
    source="auto",
    **kwargs,
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

    if source == "auto":
        if league in FIXTUREDOWNLOAD_LEAGUE_ALIASES and year == 2023:
            source = "fixturedownload"
        else:
            source = "footballdata"

    if source == "footballdata":
        contents = get_footballdata(year=year, league=league)
        data = parse_footballdata_data(contents)
    elif source == "fixturedownload":
        contents = get_fixturedownload(year=year, league=league)
        data = parse_fixturedownload_data(contents)

    data = compute_cumulative_quantities(
        data, penalties=penalties, league=league
    )

    with mpl.style.context(NEUTRAL_STYLE):
        height = 7 * (data["num_teams"] / 20) ** 0.5
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

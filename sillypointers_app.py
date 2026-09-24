from flask import Flask, render_template, request

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/logos"


# -------------------------
# GLOBAL DATA STORES
# -------------------------

# Live score (single correct version)
live_score = {
    "batting_team": "",
    "runs": 0,
    "wickets": 0,
    "overs": "0.0",
    "bowling_team": "",
    "last_update": ""
}

# Points Table
points_table = {
    "Silly Warriors": {"played": 0, "won": 0, "lost": 0, "points": 0, "nrr": "0.000"},
    "Cric Souls": {"played": 0, "won": 0, "lost": 0, "points": 0, "nrr": "0.000"},
    "Wicket Wizards": {"played": 0, "won": 0, "lost": 0, "points": 0, "nrr": "0.000"},
    "Denver Chargers": {"played": 0, "won": 0, "lost": 0, "points": 0, "nrr": "0.000"}
}

# Team Stats (for NRR calculations)
team_stats = {
    "Silly Warriors": {"runs_scored": 0, "overs_faced": 0.0, "runs_conceded": 0, "overs_bowled": 0.0},
    "Cric Souls": {"runs_scored": 0, "overs_faced": 0.0, "runs_conceded": 0, "overs_bowled": 0.0},
    "Wicket Wizards": {"runs_scored": 0, "overs_faced": 0.0, "runs_conceded": 0, "overs_bowled": 0.0},
    "Denver Chargers": {"runs_scored": 0, "overs_faced": 0.0, "runs_conceded": 0, "overs_bowled": 0.0}
}

# Player Stats (for tournament leaderboard)
player_stats = {
    # Wicket Wizards
    "Sekhar": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Deepak": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Bhuvaanesh": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Mani": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Rames": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Dileep": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Guru Prasad": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Arun": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Hari Shanmugan": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},
    "Isabel": {"team": "Wicket Wizards", "runs": 0, "wickets": 0, "points": 0},

    # Denver Chargers
    "Moksha": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Aneesh": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Tapas Rout": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Ajay": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Vineel": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Balu": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Balaji": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Prabhath": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},
    "Dipus": {"team": "Denver Chargers", "runs": 0, "wickets": 0, "points": 0},

    # Silly Warriors
    "Dinoop": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Vishnu": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Alagar": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Vinovin": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Joshy": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Chintu": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Raziq": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Biju": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},
    "Navneeth": {"team": "Silly Warriors", "runs": 0, "wickets": 0, "points": 0},

    # Cric Souls
    "Lokesh": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Kalyan": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Bharani": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Mugesh": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Sri Machi": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Shankar": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Abhi": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Zubin": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0},
    "Sai Teja": {"team": "Cric Souls", "runs": 0, "wickets": 0, "points": 0}
}

# Team Rosters (used for dropdowns)
team_roster = {
    "Wicket Wizards": [
        "Sekhar", "Deepak", "Bhuvaanesh", "Mani", "Rames",
        "Dileep", "Guru Prasad", "Arun", "Hari Shanmugan", "Isabel"
    ],
    "Denver Chargers": [
        "Moksha", "Aneesh", "Tapas Rout", "Ajay", "Vineel",
        "Balu", "Balaji", "Prabhath", "Dipus"
    ],
    "Silly Warriors": [
        "Dinoop", "Vishnu", "Alagar", "Vinovin", "Joshy",
        "Chintu", "Raziq", "Biju", "Navneeth"
    ],
    "Cric Souls": [
        "Lokesh", "Kalyan", "Bharani", "Mugesh",
        "Sri Machi", "Shankar", "Abhi", "Zubin", "Sai Teja"
    ]
}

team_logos = {
    "Wicket Wizards": "wicket_wizards.jpeg",
    "Cric Souls": "cric_souls.jpeg",
    "Denver Chargers": "denver_chargers.jpeg",
    "Silly Warriors": "silly_warriors.jpeg"
}

team_captains = {
    "Wicket Wizards": "Sekhar",
    "Denver Chargers": "Moksha",
    "Silly Warriors": "Dinoop",
    "Cric Souls": "Lokesh"
}

matches_data = {}
match_counter = 1
scorecards = {}
commentary = {}

# Ball-by-ball scoring engine
ball_by_ball = []
batsman_stats = {}
bowler_stats = {}

# Extras
extras = {
    "wides": 0,
    "no_balls": 0,
    "byes": 0,
    "leg_byes": 0
}

# Unified players list (for dropdowns)
players = []
for team, roster in team_roster.items():
    players.extend(roster)

# Strike rotation
striker = None
non_striker = None

# Fall of wickets
fall_of_wickets = []



# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template(
        "home.html",
        live_score=live_score,
        points=sorted(points_table.items(), key=lambda x: x[1]["points"], reverse=True),
        leaderboard=sorted(player_stats.items(), key=lambda x: x[1]["points"], reverse=True),
        team_list=list(points_table.keys()),
        title="Silly Pointers 2026"
    )


# -------------------------
# TEAMS PAGE
# -------------------------
@app.route("/teams")
def teams():
    teams_data = [
        {"name": "Wicket Wizards", "logo": "wicket_wizards.jpeg"},
        {"name": "Cric Souls", "logo": "cric_souls.jpeg"},
        {"name": "Denver Chargers", "logo": "denver_chargers.jpeg"},
        {"name": "Silly Warriors", "logo": "silly_warriors.jpeg"}
    ]
    return render_template("teams.html", teams=teams_data, title="Teams - Silly Pointers 2026")

# -------------------------
# MATCHES PAGE
# -------------------------
@app.route("/matches")
def matches():
    matches_data = [
        # Saturday Oct 3rd 2026
        {
            "day": "Saturday",
            "date": "Oct 3, 2026",
            "time": "7:30 - 9:00 AM",
            "team1": "Silly Warriors",
            "team2": "Cric Souls"
        },
        {
            "day": "Saturday",
            "date": "Oct 3, 2026",
            "time": "9:00 - 10:30 AM",
            "team1": "Wicket Wizards",
            "team2": "Denver Chargers"
        },
        {
            "day": "Saturday",
            "date": "Oct 3, 2026",
            "time": "3:00 - 4:30 PM",
            "team1": "Silly Warriors",
            "team2": "Wicket Wizards"
        },
        {
            "day": "Saturday",
            "date": "Oct 3, 2026",
            "time": "4:30 - 6:00 PM",
            "team1": "Cric Souls",
            "team2": "Denver Chargers"
        },

        # Sunday Oct 4th 2026
        {
            "day": "Sunday",
            "date": "Oct 4, 2026",
            "time": "7:30 - 9:00 AM",
            "team1": "Silly Warriors",
            "team2": "Denver Chargers"
        },
        {
            "day": "Sunday",
            "date": "Oct 4, 2026",
            "time": "9:00 - 10:30 AM",
            "team1": "Cric Souls",
            "team2": "Wicket Wizards"
        },

        # Eliminator & Final
        {
            "day": "Sunday",
            "date": "Oct 4, 2026",
            "time": "3:00 - 4:30 PM",
            "team1": "#2 Seed",
            "team2": "#3 Seed",
            "note": "Eliminator"
        },
        {
            "day": "Sunday",
            "date": "Oct 4, 2026",
            "time": "4:30 - 6:00 PM",
            "team1": "#1 Seed",
            "team2": "Eliminator Winner",
            "note": "Final"
        }
    ]

    return render_template(
        "matches.html",
        matches=matches_data,
        title="Matches - Silly Pointers 2026"
    )

# -------------------------
# POINTS TABLE PAGE
# -------------------------
@app.route("/points")
def points():
    points_table = [
        {
            "team": "Silly Warriors",
            "played": 0,
            "won": 0,
            "lost": 0,
            "points": 0,
            "nrr": "0.000"
        },
        {
            "team": "Cric Souls",
            "played": 0,
            "won": 0,
            "lost": 0,
            "points": 0,
            "nrr": "0.000"
        },
        {
            "team": "Wicket Wizards",
            "played": 0,
            "won": 0,
            "lost": 0,
            "points": 0,
            "nrr": "0.000"
        },
        {
            "team": "Denver Chargers",
            "played": 0,
            "won": 0,
            "lost": 0,
            "points": 0,
            "nrr": "0.000"
        }
    ]

    points_table = sorted(points_table, key=lambda x: x["points"], reverse=True)

    return render_template(
        "points.html",
        points=points_table,
        title="Points Table - Silly Pointers 2026"
    )

# -------------------------
# LEADERBOARD PAGE
# -------------------------
@app.route("/leaderboard")
def leaderboard():
    sorted_leaderboard = sorted(
        player_stats.items(),
        key=lambda x: x[1]["points"],
        reverse=True
    )

    return render_template(
        "leaderboard.html",
        leaderboard=sorted_leaderboard,
        title="Leaderboard - Silly Pointers 2026"
    )

    
# -------------------------
# ADMIN PAGE
# -------------------------
@app.route("/admin")
def admin_home():
    return render_template("admin_home.html", title="Admin Panel - Silly Pointers 2026")

# -------------------------
# UPDATE POINTS PAGE
# -------------------------

@app.route("/admin/update_points", methods=["GET", "POST"])
def admin_update_points():
    if request.method == "POST":
        team = request.form["team"]
        played = request.form["played"]
        won = request.form["won"]
        lost = request.form["lost"]
        points = request.form["points"]
        nrr = request.form["nrr"]

        # TODO: Save to database or file later
        print("Updated Points:", team, played, won, lost, points, nrr)

        return "Points updated successfully!"

    return render_template("admin_update_points.html", title="Update Points")
    
# -------------------------
# UPDATE LEADERBOARD  PAGE
# -------------------------

@app.route("/admin/update_leaderboard", methods=["GET", "POST"])
def admin_update_leaderboard():
    if request.method == "POST":
        player = request.form["player"]
        team = request.form["team"]
        runs = request.form["runs"]
        wickets = request.form["wickets"]
        points = request.form["points"]

        print("Updated Leaderboard:", player, team, runs, wickets, points)

        return "Leaderboard updated successfully!"

    return render_template("admin_update_leaderboard.html", title="Update Leaderboard")

# -------------------------
# UPDATE MATCH RESULTS PAGE
# -------------------------
@app.route("/admin/update_matches", methods=["GET", "POST"])
def admin_update_matches():
    global points_table, team_stats

    if request.method == "POST":
        match_no = request.form["match_no"]
        team1 = request.form["team1"]
        team2 = request.form["team2"]
        team1_runs = int(request.form["team1_runs"])
        team1_overs = float(request.form["team1_overs"])
        team2_runs = int(request.form["team2_runs"])
        team2_overs = float(request.form["team2_overs"])
        winner = request.form["winner"]

        # Update points
        points_table[team1]["played"] += 1
        points_table[team2]["played"] += 1

        if winner == team1:
            points_table[team1]["won"] += 1
            points_table[team1]["points"] += 2
            points_table[team2]["lost"] += 1
        else:
            points_table[team2]["won"] += 1
            points_table[team2]["points"] += 2
            points_table[team1]["lost"] += 1

        # Update NRR stats
        team_stats[team1]["runs_scored"] += team1_runs
        team_stats[team1]["overs_faced"] += team1_overs
        team_stats[team1]["runs_conceded"] += team2_runs
        team_stats[team1]["overs_bowled"] += team2_overs

        team_stats[team2]["runs_scored"] += team2_runs
        team_stats[team2]["overs_faced"] += team2_overs
        team_stats[team2]["runs_conceded"] += team1_runs
        team_stats[team2]["overs_bowled"] += team1_overs

        # Recalculate NRR for both teams
        for team in [team1, team2]:
            scored_rate = team_stats[team]["runs_scored"] / team_stats[team]["overs_faced"]
            conceded_rate = team_stats[team]["runs_conceded"] / team_stats[team]["overs_bowled"]
            nrr_value = scored_rate - conceded_rate
            points_table[team]["nrr"] = f"{nrr_value:.3f}"

        return "Match result + NRR updated!"

    return render_template("admin_update_matches.html", title="Update Match Results")


# -------------------------
# LIVE PAGE
# -------------------------

@app.route("/live")
def live():
    return render_template(
        "live.html",
        live_score=live_score,
        ball_by_ball=ball_by_ball,
        batsman_stats=batsman_stats,
        bowler_stats=bowler_stats,
        extras=extras,
        fall_of_wickets=fall_of_wickets,
        striker=striker,
        non_striker=non_striker,
        title="Live Score - Silly Pointers 2026"
    )

# -------------------------
# Admin Live_score PAGE
# -------------------------
@app.route("/admin/live_score", methods=["GET", "POST"])
def admin_live_score():
    global live_score, player_stats

    if request.method == "POST":
        live_score["batting_team"] = request.form["batting_team"]
        live_score["runs"] = int(request.form["runs"])
        live_score["wickets"] = int(request.form["wickets"])
        live_score["overs"] = request.form["overs"]
        live_score["bowling_team"] = request.form["bowling_team"]
        live_score["last_update"] = request.form["last_update"]

        # Auto-update player stats
        striker = request.form["striker"]
        bowler = request.form["bowler"]
        runs_scored = int(request.form["runs_scored"])
        wicket_taken = int(request.form["wicket_taken"])

        # Update batting stats
        player_stats[striker]["runs"] += runs_scored
        player_stats[striker]["points"] += runs_scored // 10

        # Update bowling stats
        if wicket_taken == 1:
            player_stats[bowler]["wickets"] += 1
            player_stats[bowler]["points"] += 5

        return "Live score + player stats updated!"

    return render_template("admin_live_score.html", title="Update Live Score")

# -------------------------
# View All Players PAGE
# -------------------------

@app.route("/admin/players")
def admin_players():
    return render_template(
        "admin_players.html",
        roster=team_roster,
        stats=player_stats,
        title="Manage Players"
    )

# -------------------------
# Add Player PAGE
# -------------------------

@app.route("/admin/add_player", methods=["GET", "POST"])
def admin_add_player():
    if request.method == "POST":
        name = request.form["name"]
        team = request.form["team"]

        # Add to roster
        team_roster[team].append(name)

        # Add to stats
        player_stats[name] = {"team": team, "runs": 0, "wickets": 0, "points": 0}

        return "Player added successfully!"

    return render_template("admin_add_player.html", title="Add Player")

# -------------------------
# Edit Player PAGE
# -------------------------


@app.route("/admin/edit_player/<player>", methods=["GET", "POST"])
def admin_edit_player(player):
    if request.method == "POST":
        player_stats[player]["runs"] = int(request.form["runs"])
        player_stats[player]["wickets"] = int(request.form["wickets"])
        player_stats[player]["points"] = int(request.form["points"])
        return "Player stats updated!"

    return render_template(
        "admin_edit_player.html",
        player=player,
        stats=player_stats[player],
        title="Edit Player"
    )

# -------------------------
# Delete Player PAGE
# -------------------------
@app.route("/admin/delete_player/<player>")
def admin_delete_player(player):
    team = player_stats[player]["team"]

    # Remove from roster
    team_roster[team].remove(player)

    # Remove from stats
    del player_stats[player]

    return "Player deleted!"

# -------------------------
# Create Match PAGE
# -------------------------
@app.route("/admin/create_match", methods=["GET", "POST"])
def admin_create_match():
    global match_counter, matches_data

    if request.method == "POST":
        team1 = request.form["team1"]
        team2 = request.form["team2"]
        date = request.form["date"]
        time = request.form["time"]
        venue = request.form["venue"]

        match_id = f"M{match_counter}"
        match_counter += 1

        matches_data[match_id] = {
            "team1": team1,
            "team2": team2,
            "date": date,
            "time": time,
            "venue": venue,
            "team1_runs": 0,
            "team1_overs": "0.0",
            "team2_runs": 0,
            "team2_overs": "0.0",
            "winner": ""
        }

        return f"Match {match_id} created successfully!"

    return render_template(
        "admin_create_match.html",
        teams=list(team_roster.keys()),
        title="Create Match"
    )

# -------------------------
# Edit Match PAGE
# -------------------------

@app.route("/admin/edit_match/<match_id>", methods=["GET", "POST"])
def admin_edit_match(match_id):
    global matches_data

    match = matches_data.get(match_id)

    if not match:
        return "Match not found!"

    if request.method == "POST":
        match["team1_runs"] = int(request.form["team1_runs"])
        match["team1_overs"] = request.form["team1_overs"]
        match["team2_runs"] = int(request.form["team2_runs"])
        match["team2_overs"] = request.form["team2_overs"]
        match["winner"] = request.form["winner"]

        # Auto-update points + NRR
        update_points_and_nrr(match)

        return "Match updated successfully!"

    return render_template(
        "admin_edit_match.html",
        match_id=match_id,
        match=match,
        teams=list(team_roster.keys()),
        title="Edit Match"
    )
    
# -------------------------
# Delete Match PAGE
# -------------------------

@app.route("/admin/delete_match/<match_id>")
def admin_delete_match(match_id):
    if match_id in matches_data:
        del matches_data[match_id]
        return "Match deleted!"
    return "Match not found!"

# -------------------------
# View Scorecard PAGE
# -------------------------

@app.route("/scorecard/<match_id>")
def scorecard(match_id):
    match = matches_data.get(match_id)
    card = scorecards.get(match_id, {})

    return render_template(
        "scorecard.html",
        match_id=match_id,
        match=match,
        card=card,
        title=f"Scorecard - {match_id}"
    )

# -------------------------
# Update Scorecard PAGE
# -------------------------
@app.route("/admin/scorecard/<match_id>", methods=["GET", "POST"])
def admin_scorecard(match_id):
    if request.method == "POST":
        scorecards[match_id] = {
            "batting": request.form["batting"],
            "bowling": request.form["bowling"],
            "fall_of_wickets": request.form["fall_of_wickets"],
            "summary": request.form["summary"]
        }
        return "Scorecard updated!"

    return render_template(
        "admin_scorecard.html",
        match_id=match_id,
        card=scorecards.get(match_id, {}),
        title="Update Scorecard"
    )

# -------------------------
# Upload Logo PAGE
# -------------------------
import os
from werkzeug.utils import secure_filename

@app.route("/admin/upload_logo", methods=["GET", "POST"])
def upload_logo():
    if request.method == "POST":
        team = request.form["team"]
        file = request.files["logo"]

        filename = secure_filename(team.replace(" ", "_") + ".jpeg")
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        return "Logo uploaded successfully!"

    return render_template(
        "admin_upload_logo.html",
        teams=list(team_roster.keys()),
        title="Upload Team Logo"
    )
# -------------------------
# View Commentary PAGE
# -------------------------
@app.route("/commentary/<match_id>")
def view_commentary(match_id):
    feed = commentary.get(match_id, [])
    return render_template(
        "commentary.html",
        match_id=match_id,
        feed=feed,
        title="Ball-by-Ball Commentary"
    )

# -------------------------
# Add Commentary PAGE
# -------------------------
@app.route("/admin/commentary/<match_id>", methods=["GET", "POST"])
def admin_commentary(match_id):
    if request.method == "POST":
        text = request.form["text"]
        commentary.setdefault(match_id, []).append(text)
        return "Commentary added!"

    return render_template(
        "admin_commentary.html",
        match_id=match_id,
        feed=commentary.get(match_id, []),
        title="Add Commentary"
    )

# -------------------------
# Team Details PAGE
# -------------------------
@app.route("/teams/<team_name>")
def team_details(team_name):
    players = team_roster.get(team_name, [])
    logo = team_logos.get(team_name, "default_logo.jpeg")
    captain = team_captains.get(team_name, None)
    return render_template(
        "team_details.html",
        team=team_name,
        players=players,
        logo=logo,
        captain=captain,
        title=f"{team_name} - Team Details"
    )

# -------------------------
# Ball by Ball Update PAGE
# -------------------------
@app.route("/admin/ball_update", methods=["GET", "POST"])
def ball_update():
    global ball_by_ball, live_score, batsman_stats, bowler_stats, extras
    global striker, non_striker, players, fall_of_wickets

    if request.method == "POST":
        batsman = request.form["batsman"]
        bowler = request.form["bowler"]
        runs = int(request.form["runs"])
        extra_type = request.form["extra_type"]
        is_wicket = "is_wicket" in request.form
        description = request.form["description"]

        # Over/ball calculation
        legal_balls = sum(
            1 for b in ball_by_ball
            if b["extra_type"] not in ["wide", "no-ball"]
        )
        over = legal_balls // 6
        ball = legal_balls % 6 + 1

        # Add ball entry
        ball_by_ball.append({
            "over": over,
            "ball": ball,
            "batsman": batsman,
            "bowler": bowler,
            "runs": runs,
            "extra_type": extra_type,
            "is_wicket": is_wicket,
            "description": description
        })

        # Live score
        live_score["runs"] += runs
        if is_wicket:
            live_score["wickets"] += 1
        live_score["overs"] = f"{over}.{ball}"

        # Batsman stats
        if batsman not in batsman_stats:
            batsman_stats[batsman] = {
                "runs": 0,
                "balls": 0,
                "fours": 0,
                "sixes": 0,
                "out": False
            }

        if extra_type not in ["wide", "no-ball"]:
            batsman_stats[batsman]["balls"] += 1

        batsman_stats[batsman]["runs"] += runs

        if runs == 4:
            batsman_stats[batsman]["fours"] += 1
        elif runs == 6:
            batsman_stats[batsman]["sixes"] += 1

        if is_wicket:
            batsman_stats[batsman]["out"] = True

        # Bowler stats
        if bowler not in bowler_stats:
            bowler_stats[bowler] = {
                "balls": 0,
                "runs": 0,
                "wickets": 0
            }

        if extra_type not in ["wide", "no-ball"]:
            bowler_stats[bowler]["balls"] += 1

        bowler_stats[bowler]["runs"] += runs

        if is_wicket:
            bowler_stats[bowler]["wickets"] += 1

        # Extras
        if extra_type == "wide":
            extras["wides"] += runs
        elif extra_type == "no-ball":
            extras["no_balls"] += runs
        elif extra_type == "bye":
            extras["byes"] += runs
        elif extra_type == "leg-bye":
            extras["leg_byes"] += runs

        # Fall of Wickets
        if is_wicket:
            fall_of_wickets.append({
                "score": f"{live_score['runs']}/{live_score['wickets']}",
                "over": f"{over}.{ball}",
                "batsman": batsman,
                "bowler": bowler,
                "description": description
            })

        # Auto Strike Rotation
        if is_wicket:
            striker = None
        else:
            if extra_type not in ["wide", "no-ball"]:
                if runs % 2 == 1:
                    striker, non_striker = non_striker, striker
                if ball == 6:
                    striker, non_striker = non_striker, striker
            else:
                if extra_type in ["bye", "leg-bye"] and runs % 2 == 1:
                    striker, non_striker = non_striker, striker

        return "Ball updated!"

    return render_template("admin_ball_update.html", players=players, striker=striker, non_striker=non_striker)

# -------------------------
# Reset Match
# -------------------------
@app.route("/admin/reset_match")
def reset_match():
    global ball_by_ball, live_score, batsman_stats, bowler_stats
    global extras, fall_of_wickets, striker, non_striker

    ball_by_ball = []
    batsman_stats = {}
    bowler_stats = {}
    fall_of_wickets = []

    extras = {
        "wides": 0,
        "no_balls": 0,
        "byes": 0,
        "leg_byes": 0
    }

    live_score = {
        "runs": 0,
        "wickets": 0,
        "overs": "0.0"
    }

    # Reset strike rotation
    striker = None
    non_striker = None

    return "Match has been reset successfully!"


# -------------------------
# Save Match PAGE
# -------------------------
import json
from datetime import datetime

@app.route("/admin/save_match")
def save_match():
    global ball_by_ball, live_score, batsman_stats, bowler_stats, extras, fall_of_wickets

    # Build match summary (FULL VERSION)
    match_summary = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "final_score": live_score,
        "balls": ball_by_ball,
        "batsman_stats": batsman_stats,
        "bowler_stats": bowler_stats,
        "extras": extras,
        "fall_of_wickets": fall_of_wickets
    }

    # Load existing results
    try:
        with open("match_results.json", "r") as f:
            results = json.load(f)
    except:
        results = []

    # Add new match
    results.append(match_summary)

    # Save back to file
    with open("match_results.json", "w") as f:
        json.dump(results, f, indent=4)

    return "Match saved successfully!"

# -------------------------
# Match Summary PAGE
# -------------------------
@app.route("/match_summary/<int:match_id>")
def match_summary(match_id):
    try:
        with open("match_results.json", "r") as f:
            results = json.load(f)
    except:
        results = []

    if match_id < 0 or match_id >= len(results):
        return "Match not found."

    match = results[match_id]

    return render_template(
        "match_summary.html",
        match=match,
        match_id=match_id,
        title=f"Match Summary #{match_id + 1}"
    )
# -------------------------
# List Saved matches PAGE
# -------------------------
@app.route("/saved_matches")
def saved_matches():
    try:
        with open("match_results.json", "r") as f:
            results = json.load(f)
    except:
        results = []

    return render_template(
        "saved_matches.html",
        results=results,
        title="Saved Matches"
    )


def update_points_and_nrr(match):
    global points_table, team_stats

    team1 = match["team1"]
    team2 = match["team2"]
    team1_runs = match["team1_runs"]
    team1_overs = float(match["team1_overs"])
    team2_runs = match["team2_runs"]
    team2_overs = float(match["team2_overs"])
    winner = match["winner"]

    # Update points
    points_table[team1]["played"] += 1
    points_table[team2]["played"] += 1

    if winner == team1:
        points_table[team1]["won"] += 1
        points_table[team1]["points"] += 2
        points_table[team2]["lost"] += 1
    elif winner == team2:
        points_table[team2]["won"] += 1
        points_table[team2]["points"] += 2
        points_table[team1]["lost"] += 1

    # Update NRR stats
    team_stats[team1]["runs_scored"] += team1_runs
    team_stats[team1]["overs_faced"] += team1_overs
    team_stats[team1]["runs_conceded"] += team2_runs
    team_stats[team1]["overs_bowled"] += team2_overs

    team_stats[team2]["runs_scored"] += team2_runs
    team_stats[team2]["overs_faced"] += team2_overs
    team_stats[team2]["runs_conceded"] += team1_runs
    team_stats[team2]["overs_bowled"] += team1_overs

    # Recalculate NRR
    for team in [team1, team2]:
        scored_rate = team_stats[team]["runs_scored"] / team_stats[team]["overs_faced"]
        conceded_rate = team_stats[team]["runs_conceded"] / team_stats[team]["overs_bowled"]
        nrr_value = scored_rate - conceded_rate
        points_table[team]["nrr"] = f"{nrr_value:.3f}"


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)

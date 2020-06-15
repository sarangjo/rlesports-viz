import re
import copy
from typing import Dict, List, Any
import json

from api import call_api

TOURNAMENTS_CACHE_FILE = "../cache/cache.json"
TOURNAMENTS_FILE = "../src/data/tournaments.json"
MIN_TEAM_SIZE = 1  # Turbo as the sub for S3 LAN
EMPTY_TEAM: Dict[str, Any] = {'players': [], 'subs': []}
PREFIX = "Rocket League Championship Series/Season "
REGION = "North America"

tournamentNames: List[str] = [
    f"{PREFIX}1/{REGION}/Qualifier 1",
    f"{PREFIX}1/{REGION}/Qualifier 2",
    f"{PREFIX}1",
    f"{PREFIX}2/{REGION}",
    f"{PREFIX}2",
    f"{PREFIX}3/{REGION}",
    f"{PREFIX}3",
    # f"{PREFIX}4/{REGION}",
    # f"{PREFIX}4",
    # f"{PREFIX}5/{REGION}",
    # f"{PREFIX}5",
    # f"{PREFIX}6/{REGION}",
    # f"{PREFIX}6",
]


def get_tournaments_data() -> Dict[str, Dict]:
    with open(TOURNAMENTS_CACHE_FILE, 'r') as f:
        output = json.load(f)

    for t in tournamentNames:
        if t not in output:
            p_section = {'index': 3}

            wiki_text = call_api({
                "action": "parse",
                "prop": "wikitext",
                "page": t,
                "section": int(p_section['index']),
            })
            output[t] = wiki_text['parse']

    with open(TOURNAMENTS_CACHE_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    return output


def process_tournaments_data(output: Dict[str, Dict]):
    tournaments: List[Dict] = []
    for t in output:
        # We are processing all of the lines per tournament
        lines: List[str] = output[t]['wikitext']['*'].split('\n')
        # Each tournament has a set of teams
        teams = []
        # These are used as we parse one team at a time
        team = copy.deepcopy(EMPTY_TEAM)
        found_team = False
        # Line format is:
        # |team=iBUYPOWER
        # |p1=Kronovi |p1flag=us
        # |p2=Lachinio |p2flag=ca
        # |p3=Gambit |p3flag=us
        # |p4=0ver Zer0|p4flag=us
        # |qualifier=[[Rocket_League_Championship_Series/Season_1/North_America/Qualifier_1|Qualifier #1]]
        for line in lines:
            # This divides teams
            if line.startswith('|team'):
                # Handle special case for the first team
                if found_team and len(team['players']) >= MIN_TEAM_SIZE:
                    teams.append(team)
                    team = copy.deepcopy(EMPTY_TEAM)
                team['name'] = line.replace('|team=', '')
                found_team = True
            # Once we've found a team, parse at least 3 players
            elif found_team:
                # Player line has to start as so:
                if re.match("[|]p[0-9]=", line):
                    player = line.split('|')[1].split('=')[1].strip()
                    if len(player) > 0:
                        team['players'].append(player)

        # Fencepost for the last team
        if len(team['players']) >= MIN_TEAM_SIZE:
            teams.append(team)

        tournaments.append({"name": t, "teams": teams})

    with open(TOURNAMENTS_FILE, 'w') as f:
        json.dump(tournaments, f, indent=2)

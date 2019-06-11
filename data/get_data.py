import copy
import json
import pprint
import re
import sys
from typing import List, Any, Dict

import requests

# Data

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

MIN_TEAM_SIZE = 1  # Turbo as the sub for S3 LAN
EMPTY_TEAM = {'players': [], 'subs': []}

# Liquipedia

API_BASE = "https://liquipedia.net/rocketleague/api.php"
DEFAULT_PARAMS = {"origin": "*", "format": "json"}

# Files

CACHE_FILE = "cache.json"
TOURNAMENTS_FILE = "tournaments.json"

# Util

pp = pprint.PrettyPrinter(indent=2)

"""
    console.log(
      "wtf'd data for",
      t,
      _.filter(wtf(text).data.sections[0].data.templates, template => template.team),
    );
"""


def call_api(opts: Dict[str, Any]):
    opts.update(DEFAULT_PARAMS)
    req = requests.get(API_BASE, opts)
    try:
        return json.loads(req.text)
    except json.decoder.JSONDecodeError:
        print(req.text)
        sys.exit(1)


def get_data() -> Dict[str, Dict]:
    with open(CACHE_FILE, 'r') as f:
        output = json.load(f)

    for (i, t) in enumerate(tournamentNames):
        if t not in output:
            """
            try:
                # Get sections and find "Participants"
                sections = call_api({
                    "action": "parse",
                    "prop": "sections",
                    "page": t,
                })

                p_section = next(s for s in sections['parse']['sections'] if s['line'] == 'Participants')
            except StopIteration:
                output[t] = "could not get sections"
            finally:
                p_section = 3
            """
            p_section = {'index': 3}

            wiki_text = call_api({
                "action": "parse",
                "prop": "wikitext",
                "page": t,
                "section": int(p_section['index']),
            })
            output[t] = wiki_text['parse']

    with open(CACHE_FILE, 'w') as f:
        json.dump(output, f, indent=4)

    return output


def process_data(output: Dict[str, Dict]):
    tournaments: List[Dict] = []
    for t in output:
        # We are processing all of the lines per tournament
        lines: List[str] = output[t]['wikitext']['*'].split('\n')
        # Each tournament has a set of teams
        teams = []
        # These are used as we parse one team at a time
        team = copy.deepcopy(EMPTY_TEAM)
        in_team = False
        """
        Line format is:
        |team=iBUYPOWER
        |p1=Kronovi |p1flag=us
        |p2=Lachinio |p2flag=ca
        |p3=Gambit |p3flag=us
        |p4=0ver Zer0|p4flag=us
        |qualifier=[[Rocket_League_Championship_Series/Season_1/North_America/Qualifier_1|Qualifier #1]]
        """
        for line in lines:
            # This divides teams
            if line.startswith('|team'):
                if len(team['players']) >= MIN_TEAM_SIZE:
                    teams.append(team)
                    team = copy.deepcopy(EMPTY_TEAM)
                team['name'] = line.replace('|team=', '')
                in_team = True
            # Once we've found a team, parse at least 3 players
            elif in_team:
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
        json.dump(tournaments, f, indent=4)


def main():
    output = get_data()
    process_data(output)


if __name__ == '__main__':
    main()

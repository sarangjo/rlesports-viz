import json
import re
import time
from typing import List, Dict, Any

from api import call_api

PLAYERS_CACHE_FILE = "./cache/pcache.json"
PLAYERS_FILE = "./src/data/players.json"


def get_players_data(players: List[str]) -> Dict[str, Dict]:
    for player in players:
        with open(PLAYERS_CACHE_FILE, 'r') as f:
            output = json.load(f)
        if player not in output:
            wiki_text = call_api({
                "action": "parse",
                "prop": "wikitext",
                "page": player,
                "format": "json",
                "section": 0,
            })
            print("called api for", player)
            output[player] = wiki_text['parse']
            with open(PLAYERS_CACHE_FILE, 'w') as f:
                json.dump(output, f, indent=2)
            time.sleep(30)
        else:
            print("didn't need api for", player)

    with open(PLAYERS_CACHE_FILE) as f:
        output = json.load(f)
    return output


DATE_RE = re.compile(r"[\w?]{4}-[\w?]{2}-[\w?]{2}")


def process_players_data(output: Dict[str, Dict]):
    """
    Go through the wikitext output and process it into a clean JSON format
    """
    processed = []
    for player in output:
        lines: List[str] = output[player]["wikitext"]["*"].split('\n')

        player = {
            "events": []
        }
        in_infobox = False
        in_history = False
        for line in lines:
            if line.startswith('{{Infobox'):
                in_infobox = True
            elif in_infobox:
                if line.startswith('|id='):
                    player["name"] = line.replace('|id=', '')

            if not in_history and line.startswith('|history'):
                in_history = True
            elif in_history:
                if not line.startswith('{{TH'):
                    break

                parts = line.replace('{{', '').replace('}}', '').split('|')
                dates = parts[1].split(' ')
                event = {
                    "start": dates[0],
                    "team": parts[2],
                }
                if re.match(DATE_RE, dates[-1]):
                    event["end"] = dates[-1]
                player["events"].append(event)

        processed.append(player)

    with open(PLAYERS_FILE, 'w') as f:
        json.dump(processed, f, indent=2)


PLAYER_LIST = json.load(open("playerlist.json"))

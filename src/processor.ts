import { combination } from "js-combinatorics";
import _ from "lodash";
import { FullPlayer, Player, Teammates } from "./types";

// TODO date -> moment
export const toNodesAndLinks = (initialData: FullPlayer[], date: string) => {
  // Construct playerNodes and playerLinks
  const playerNodes: Player[] = initialData.map((player) => ({ name: player.name }));
  const playerLinks: Teammates[] = [];
  const playerEvents = initialData.reduce((map, obj) => {
    map[obj.name] = obj.events;
    return map;
  }, {} as Record<string, any>);

  // Process props
  const teamMap: Record<string, Player[]> = {};

  const lft = [];
  playerNodes.forEach((player) => {
    // TODO: only chooses the earlier on date changes
    player.team = _.get(
      _.findLast(
        playerEvents[player.name],
        (ev) => date >= ev.start && (!ev.end || date <= ev.end),
      ),
      "team",
    );
    if (player.team) {
      if (!(player.team in teamMap)) {
        teamMap[player.team] = [];
      }
      teamMap[player.team].push(player);
    } else {
      lft.push(player);
    }
  });

  // const fullTeams = _.keys(_.pickBy(teamMap, p => p.length >= 3));

  playerLinks.length = 0;
  _.forEach(teamMap, (playerNames) => {
    if (playerNames.length >= 2) {
      const newLinks = combination(playerNames, 2).map((playerCombo) => ({
        source: playerCombo[0],
        target: playerCombo[1],
      }));
      playerLinks.push(...newLinks);
    }
  });

  return {
    playerNodes,
    playerLinks,
  };
};

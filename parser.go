package main

import (
	"regexp"
	"strings"
)

/* Wikitext parsing module */

// ParseTeams parses team info
func ParseTeams(wikitext string) []Team {
	// We are processing all of the lines per tournament
	lines := strings.Split(wikitext, "\n")
	// Each tournament has a set of teams
	teams := []Team{}
	// These are used as we parse one team at a time
	team := Team{}
	foundTeam := false

	// Line format is:
	// |team=iBUYPOWER
	// |p1=Kronovi |p1flag=us
	// |p2=Lachinio |p2flag=ca
	// |p3=Gambit |p3flag=us
	// |p4=0ver Zer0|p4flag=us
	// |qualifier=[[Rocket_League_Championship_Series/Season_1/North_America/Qualifier_1|Qualifier #1]]
	for _, line := range lines {
		// This divides teams, so we save the team we've been collecting so far
		if strings.HasPrefix(line, "|team") {
			// Handle special case for the first team
			if foundTeam && len(team.Players) >= minTeamSize {
				teams = append(teams, team)
				team = Team{}
			}
			team.Name = strings.Replace(line, "|team=", "", 1)
			foundTeam = true
			// Once we've found a team, parse at least 3 players
		} else if foundTeam {
			// Player line has to start as so:
			// TODO: start with `^`? replace [|] with `|?`?
			if res, _ := regexp.Match("[|]p[0-9]=", []byte(line)); res {
				player := strings.TrimSpace(strings.Split(strings.Split(line, "|")[1], "=")[1])
				if len(player) > 0 {
					team.Players = append(team.Players, player)
				}
			}
		}
	}

	// Fencepost for the last team
	if len(team.Players) >= minTeamSize {
		teams = append(teams, team)
	}

	return teams
}

// ParseStart get start of tournament, or returns empty string
func ParseStart(wikitext string) string {
	lines := strings.Split(wikitext, "\n")

	inInfobox := false

	for _, line := range lines {
		if strings.HasPrefix(line, "{{Infobox") {
			inInfobox = true
		} else if inInfobox {
			if strings.HasPrefix(line, "|sdate=") {
				return strings.Replace(line, "|sdate=", "", 1)
			}
		}
	}
	return ""
}

// ParsePlayer parses player from wikitext
func ParsePlayer(wikitext string) Player {
	lines := strings.Split(wikitext, "\n")

	player := Player{Events: []Event{}}

	inInfobox := false
	inHistory := false

	for _, line := range lines {
		if strings.HasPrefix(line, "{{Infobox") {
			inInfobox = true
		} else if inInfobox {
			if strings.HasPrefix(line, "|id=") {
				player.Name = strings.Replace(line, "|id=", "", 1)
			}
		}

		if !inHistory && strings.HasPrefix(line, "|history") {
			inHistory = true
		} else if inHistory {
			if !strings.HasPrefix(line, "{{TH") {
				break
			}

			parts := strings.Split(strings.ReplaceAll(strings.ReplaceAll(line, "{{", ""), "}}", ""), "|")
			dates := strings.Split(parts[1], " ")
			event := Event{Start: dates[0], Team: parts[2]}
			if success, _ := regexp.Match(dateRegex, []byte(dates[len(dates)-1])); success {
				event.End = dates[len(dates)-1]
			}
			player.Events = append(player.Events, event)
		}
	}
	return player
}

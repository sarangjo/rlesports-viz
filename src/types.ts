import { SimulationLinkDatum, SimulationNodeDatum } from "d3-force";

// Events as read in from the JSON
export interface PlayerEvent {
  start: string;
  team: string;
  end?: string;
  role?: string;
}

// Each player has a full list of their events
export interface FullPlayer {
  name: string;
  events: PlayerEvent[];
}

// The translated Player node which stays fixed, with the team changing based on the date chosen
export interface Player extends SimulationNodeDatum {
  name: string;
  team?: string;
}

// We use links to ensure proximity of teammates
export type Teammates = SimulationLinkDatum<Player>;
export interface Team {
  name: string;
  players: string[];
  won?: boolean;
  subs?: string[];
}

export interface TeamNodePart {
  tournamentIndex: number;
}

export interface Tournament {
  name: string;
  start: string;
  end: string;
  teams: Team[];
}

export interface TournamentNode extends d3.SimulationNodeDatum {
  playerIndex: number;
  teamIndex: number;
  tournamentIndex: number;
  id: string; // combination of indices
}

export interface TournamentLink {
  source: TournamentNode;
  target: TournamentNode;
}

// TODO rename
export type SimulationLink = d3.SimulationLinkDatum<TournamentNode>;

export type Chart = d3.Selection<d3.BaseType, unknown, HTMLElement, any>;

export interface RLVisualization {
  main: (chart: Chart) => any;
}

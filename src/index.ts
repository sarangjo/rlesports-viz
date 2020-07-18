import { select } from "d3-selection";
import log from "loglevel";

import { HEIGHT, WIDTH } from "./constants";
import { RLVisualization } from "./types";
// import Simple from "./viz/simple";
// import Timeline from "./viz/timeline";

// import data from "./data/tournaments.json";
// import { SankeyViz } from "./viz/sankey";
import playerTeamsViz from "./viz/playerTeams";
import sankeyViz from "./viz/sankey";
import simpleViz from "./viz/simple";
import forceGraphViz from "./viz/forceGraph";

log.setLevel("debug");

let viz: RLVisualization;
const chart = select("svg").attr("width", WIDTH).attr("height", HEIGHT);

// Removes all elements in the view
function clear() {
  chart.selectAll("*").remove();
  const uiArea = document.getElementById("ui-area");
  while (uiArea && uiArea.firstChild) {
    uiArea.removeChild(uiArea.lastChild!);
  }
}

async function setView(view: string) {
  clear();

  switch (view) {
    case "sankey":
      viz = sankeyViz;
      break;
    case "team-map":
      viz = playerTeamsViz;
      break;
    case "force-graph":
      viz = forceGraphViz;
    default:
      viz = simpleViz;
      break;
  }

  await viz.main(chart);
}

enum Viz {
  SANKEY = "sankey",
  TEAM_MAP = "team-map",
  FORCE_GRAPH = "force-graph",
  SIMPLE = "simple",
}

const VizTitle = {
  [Viz.SANKEY] :"Sankey",
  [Viz.TEAM_MAP] :"Team Map",
  [Viz.FORCE_GRAPH] :"Force Graph",
  [Viz.SIMPLE] :"Simple",
}

const vizSelect = document.getElementById("viz");

if (vizSelect) {
  // Init
        <option value="sankey">Sankey</option>
        <option value="team-map">Player Teams</option>
        <option value="simple">Timeline</option>

  setView((vizSelect as HTMLSelectElement).value);

  // User input
  vizSelect.addEventListener("change", () => {
    setView((vizSelect as HTMLSelectElement).value);
  });
}

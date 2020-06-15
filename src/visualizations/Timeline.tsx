import { drag } from "d3-drag";
import { forceCollide, forceLink, forceSimulation, forceX, forceY } from "d3-force";
import { select } from "d3-selection";
import _ from "lodash";
import log from "loglevel";
import React, { Component } from "react";

import { CIRCLE_RADIUS, HEIGHT, WIDTH } from "../constants";
import { toNodesAndLinks } from "../processor";
import { FullPlayer, Player, Teammates } from "../types";
import { nodeDrag } from "../util";

// The name of the link force
const LINK_FORCE = "link";

// Convenient container to hold onto all of the SVG selections used by D3
/*
interface Selections {
  node?: Selection<SVGGElement, Player, any, any>;
  link?: Selection<SVGLineElement, Teammates, any, any>;
  pathContainer?: Selection<SVGGElement, string, any, any>;
  path?: Selection<SVGPathElement, string, any, any>;
}
*/

interface Props {
  initialData: FullPlayer[];
  date: string;
}

/* Thinking area */
/*
Okay so what do we have going on here?
- The simulation is passed an array of nodes that we want to maintain; we don't want to create new
nodes every time data changes.
- However, whenever the props change, we want to propagate that by updating the team names for all
the nodes and updating links
- So let's try this out.
*/
export default class TimelineViz extends Component<Props> {
  // DOM selections
  private node: SVGSVGElement | null = null;

  public createChart = () => {
    if (!this.node) {
      // can only create chart after mounting
      return;
    }
    const chart = select(this.node);

    chart.selectAll("*").remove();

    const nodesAndLinks = toNodesAndLinks(this.props.initialData, this.props.date);

    // Simulation
    // TODO i removed passing in playerNodes and playerLinks
    const simulation = forceSimulation<Player>(nodesAndLinks.playerNodes)
      .force(
        LINK_FORCE,
        forceLink<Player, Teammates>()
          .id((d) => d.name)
          .links(nodesAndLinks.playerLinks),
      )
      .force("collide", forceCollide(50))
      .force("x", forceX(WIDTH / 2))
      .force("y", forceY(HEIGHT / 2));

    /*
// Team bubbles (TODO)
this.selections.pathContainer = chart
  .append("g")
  .attr("id", "teams")
  .selectAll(".group-path");

this.selections.path = this.selections.pathContainer
  .append("path")
  .attr("stroke", "blue")
  .attr("fill", "lightblue")
  .attr("opacity", 1);
  */

    // TODO need exit

    // Nodes: g + (circle, text)
    const nodeG = chart
      .append("g")
      .attr("id", "nodes")
      .selectAll("circle")
      .data(nodesAndLinks.playerNodes)

      .enter()
      .append("g");
    nodeG
      .append("circle")
      .attr("r", CIRCLE_RADIUS)
      .call(
        // TODO fix type issues
        drag()
          .on("start", nodeDrag.start.bind(null, simulation) as any)
          .on("drag", nodeDrag.in as any)
          .on("end", nodeDrag.end.bind(null, simulation) as any) as any,
      );
    nodeG
      .append("text")
      .attr("x", CIRCLE_RADIUS + 1)
      .attr("y", 3)
      .text((d: Player) => d.name);

    // Links
    const link = chart
      .append("g")
      .attr("id", "links")
      .selectAll("line")
      .data(nodesAndLinks.playerLinks)
      .enter()
      .append("line")
      .attr("stroke", "black");

    // Given a team name, generate the polygon for it
    /*
const polygonGenerator = (teamName: string) => {
const nodeCoords = nodeGSelection
  .filter(d => d.team === teamName)
  .data()
  .map(d => [d.x, d.y]);

return d3.polygonHull(nodeCoords as Array<[number, number]>);
};*/

    const ticked = () => {
      link
        .attr("x1", (d) => _.get(d, "source.x"))
        .attr("y1", (d) => _.get(d, "source.y"))
        .attr("x2", (d) => _.get(d, "target.x"))
        .attr("y2", (d) => _.get(d, "target.y"));

      nodeG.attr("transform", (d) => `translate(${d.x},${d.y})`);

      /*
this.fullTeams.forEach(teamName => {
  let centroid: [number, number] = [0, 0];

  // Set the path
  this.selections
    .path!.filter((d: string) => d === teamName)
    .attr("transform", "scale(1) translate(0,0)")
    .attr("d", (d: string) => {
      const polygon = polygonGenerator(d);
      if (polygon) {
        centroid = polygonCentroid(polygon);

        // to scale the shape properly around its points:
        // move the 'g' element to the centroid point, translate
        // all the path around the center of the 'g' and then
        // we can scale the 'g' element properly
        return valueline(
          polygon.map(point => [point[0] - centroid[0], point[1] - centroid[1]]),
        );
      }
      return null;
    });

  // Set the path container
  this.selections
    .pathContainer!.filter((d: any) => d === teamName)
    .attr("transform", "translate(" + centroid[0] + "," + centroid[1] + ") scale(1.2)");
});
*/
    };
    simulation.on("tick", ticked);
  };

  public componentDidMount() {
    log.debug("mounted");

    this.createChart();
  }

  public componentDidUpdate() {
    log.debug("updated");
    // This is where we handle updates to `date` and `data`
    this.createChart();
  }

  public render() {
    return (
      <svg className="chart" ref={(node) => (this.node = node)} width={WIDTH} height={HEIGHT}></svg>
    );
  }
}

// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@mbostock/u-s-population-by-age/2
// https://observablehq.com/@d3/bar-line-chart
// https://observablehq.com/@d3/bar-chart
// https://observablehq.com/@d3/diverging-bar-chart
// https://observablehq.com/@d3/line-chart
// https://observablehq.com/d/09ce6504a55ab5c6
// https://dev.to/muratkemaldar/using-vue-3-with-d3-composition-api-3h1g
// @ts-nocheck

import * as d3 from "d3"
import type { IKeyable } from "@/interfaces"

export const useBarLineChart = () => {
  function getBarLineChart(
    data: IKeyable[],
    {
      width = 700, // outer width, in pixels
      marginTop = 25, // top margin, in pixels
      marginRight = 40, // right margin, in pixels
      marginBottom = 35, // bottom margin, in pixels
      marginLeft = 40, // left margin, in pixels
    } = {}
  ) {
    data.y1 = "↑ Count"
    data.y2 = "Proportion ↑"
    const margin = ({ top: marginTop, right: marginRight, bottom: marginBottom, left: marginLeft })
    const height = data.length * 30 + margin.top + margin.bottom

    const line = d3.line()
                    .x(d => x(d.period) + x.bandwidth() / 2)
                    .y(d => y2(d.proportion))

    const x = d3.scaleBand()
                  .domain(data.map(d => d.period))
                  .rangeRound([margin.left, width - margin.right])
                  .padding(0.1)

    const y1 = d3.scaleLinear()
                  .domain([0, d3.max(data, d => d.value)])
                  .rangeRound([height - margin.bottom, margin.top])

    const y2 = d3.scaleLinear()
                  // .domain(d3.extent(data, d => d.proportion))
                  .domain([0, 1])
                  .rangeRound([height - margin.bottom, margin.top])
    
    const xAxis = g => g
                  .attr("transform", `translate(0,${height - margin.bottom})`)
                  .call(
                    d3.axisBottom(x)
                      .tickSizeOuter(0)
                  )
                  .selectAll("text")  
                    .style("text-anchor", "end")
                    .attr("dx", "-.8em")
                    .attr("dy", ".15em")
                    .attr("transform", "rotate(-25)");
    
    const y1Axis = g => g
                  .attr("transform", `translate(${margin.left},0)`)
                  .style("color", "#9f491e")
                  .call(d3.axisLeft(y1).ticks(null, "s"))
                  .call(g => g.select(".domain").remove())
                  .call(g => g.append("text")
                      .attr("x", -margin.left)
                      .attr("y", 10)
                      .attr("fill", "currentColor")
                      .attr("text-anchor", "start")
                      .text(data.y1))

    const y2Axis = g => g
                  .attr("transform", `translate(${width - margin.right},0)`)
                  .style("color", "#066486")
                  .call(d3.axisRight(y2))
                  .call(g => g.select(".domain").remove())
                  .call(g => g.append("text")
                      .attr("x", margin.right)
                      .attr("y", 10)
                      .attr("fill", "currentColor")
                      .attr("text-anchor", "end")
                      .text(data.y2))

    const svg = d3.select("#chart")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height]);

    svg.append("g")
        .attr("fill", "#cc7d24")
        .attr("fill-opacity", 0.7)
      .selectAll("rect")
      .data(data)
      .join("rect")
        .attr("x", d => x(d.period))
        .attr("width", x.bandwidth())
        .attr("y", d => y1(d.value))
        .attr("height", d => y1(0) - y1(d.value));

    svg.append("path")
        .attr("fill", "none")
        .attr("stroke", "#066486")
        .attr("stroke-miterlimit", 1)
        .attr("stroke-width", 3)
        .attr("d", line(data));    

    svg.append("g")
        .attr("fill", "none")
        .attr("pointer-events", "all")
      .selectAll("rect")
      .data(data)
      .join("rect")
        .attr("x", d => x(d.period))
        .attr("width", x.bandwidth())
        .attr("y", 0)
        .attr("height", height)
      .append("title")
        .text(d => `${d.period}
${d.value.toLocaleString("en")}
${d.proportion.toLocaleString("en")}`);

    svg.append("g")
        .call(xAxis);

    svg.append("g")
        .call(y1Axis);

    svg.append("g")
        .call(y2Axis);
    
    return svg.node();
  }
  
  return {
    getBarLineChart
  }
}
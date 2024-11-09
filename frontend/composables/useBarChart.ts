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

export const useBarChart = () => {
  function getBarChart(
    data: IKeyable[],
    {
      chartRef = {} as HTMLElement,
      width = 700, // outer width, in pixels
      marginTop = 0, // top margin, in pixels
      marginRight = 20, // right margin, in pixels
      marginBottom = 20, // bottom margin, in pixels
      marginLeft = 20, // left margin, in pixels
      color = ["currentColor", "currentColor", "currentColor"],
    } = {}
  ) {
    const margin = ({ top: marginTop, right: marginRight, bottom: marginBottom, left: marginLeft })
    const height = data.length * 25 + margin.top + margin.bottom

    const x = d3.scaleLinear()
      // .domain([0, d3.max(data, d => d.period)])
      .domain([0, data.length - 1])
      .range([margin.left, width - margin.right])
    const y = d3.scaleBand()
      .domain(data.map(d => d.value))
      .range([height - margin.bottom, margin.top])
      .padding(0.1)
    
    // const svg = (chartRef ? d3.select(chartRef) : d3.create("svg"))
    const svg = d3.select("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", `0 0 ${width} ${height}`);

    svg.append("g")
        .attr("fill", "#d2e1eb")
      .selectAll("rect")
      .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("width", 0);

    svg.append("g")
        .attr("fill", "black")
        .attr("text-anchor", "start")
        .style("font", "12px sans-serif")
      .selectAll("text")
      .data(data)
      .enter().append("text")
        .attr("class", "label")
        .attr("dy", "0.35em")
        .attr("x", margin.left + 20);

      svg.append("g")
          .attr("class", "x-axis");
  
      svg.append("g")
          .attr("class", "y-axis");
  
    svg.selectAll(".bar")
      .data(data, d => d.value)
        .attr("x", x(0))
        .attr("y", d => y(d.value))
        .attr("height", y.bandwidth())
      .transition()
        .delay((d, i) => i * 20)
        .attr("width", d => x(d.period) - x(0));
  
    svg.selectAll(".label")
      .data(data, d => d.value)
        // .attr("text-anchor", "end")
        .attr("x", 0)
        .attr("y", d => y(d.value) + y.bandwidth() / 2)
        .text(d => d.value)
        // .attr("text-anchor", "end")
      .transition()
        .delay((d, i) => i * 20)
        .attr("x", margin.left + 10);
        // .attr("x", d => x(d.period) - 4);
  
    svg.select(".x-axis")
        .attr("transform", `translate(0,${height - margin.bottom})`)
        .call(g => g.transition().call(d3.axisBottom(x).ticks(width / 80, "s")))
        .call(g => g.select(".domain").remove());
    
    // svg.select(".y-axis")
    //     .attr("transform", `translate(${margin.left},0)`)
    //     .call(g => g.transition().call(d3.axisLeft(y).tickSizeOuter(0)));

    return svg.node();
  }
  
  return {
    getBarChart
  }
}
function initializeCharts() {
  if (typeof Plotly === "undefined") return;
  try {
    var trace1 = {
      x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
      y: [850, 820, 780, 750, 700, 680, 710, 760, 810, 840, 880, 890],
      type: "scatter",
      mode: "lines",
      name: "Geração Estimada",
      line: {
        color: "#F59E0B",
        width: 3,
        shape: "spline",
        smoothing: 1.3,
      },
      fill: "tozeroy",
      fillcolor: "rgba(245, 158, 11, 0.1)",
    };

    var trace2 = {
      x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
      y: [750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750, 750],
      type: "scatter",
      mode: "lines",
      name: "Consumo Médio",
      line: {
        color: "#0A2540",
        width: 2,
        dash: "dash",
      },
    };

    var layout = {
      margin: { t: 20, r: 20, b: 40, l: 40 },
      plot_bgcolor: "transparent",
      paper_bgcolor: "transparent",
      showlegend: true,
      legend: {
        orientation: "h",
        y: -0.2,
      },
      xaxis: {
        showgrid: false,
        color: "#6B7280",
      },
      yaxis: {
        showgrid: true,
        gridcolor: "rgba(0,0,0,0.05)",
        color: "#6B7280",
      },
    };

    var config = {
      responsive: true,
      displayModeBar: false,
    };

    Plotly.newPlot("generationChart", [trace1, trace2], layout, config);
  } catch (e) {
    console.warn("Chart init:", e);
  }
}

window.addEventListener("load", initializeCharts);
setTimeout(initializeCharts, 1200);

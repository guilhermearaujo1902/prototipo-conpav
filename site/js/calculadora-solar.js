(function () {
  var PRICE_KWH = 0.95;
  var KWH_PER_KWP_MONTH = 116;
  var PANEL_KW = 0.55;
  var COST_PER_KWP = 4200;
  var SEASON = [0.92, 0.94, 0.98, 1.0, 1.02, 1.04, 1.05, 1.04, 1.01, 0.98, 0.93, 0.91];

  var _bound = false;

  function el(id) {
    return document.getElementById(id);
  }

  function formatBRL(n) {
    return n.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  function shadeMult(idx) {
    if (idx <= 0) return 1;
    if (idx === 1) return 0.93;
    return 0.82;
  }

  function roofMult(idx) {
    if (idx <= 0) return 1;
    if (idx === 1) return 0.98;
    if (idx === 2) return 0.96;
    if (idx === 3) return 0.94;
    return 0.99;
  }

  function baseKwhFromRange(range, toggle) {
    var raw = parseFloat(range.value) || 0;
    if (toggle.checked) return raw;
    return raw / PRICE_KWH;
  }

  function oldBillMonthly(range, toggle) {
    var raw = parseFloat(range.value) || 0;
    if (toggle.checked) return raw * PRICE_KWH;
    return raw;
  }

  function updateChart(monthlyGen, baseKwhDisplay) {
    if (typeof Plotly === "undefined" || !document.getElementById("generationChart")) return;
    var gen = SEASON.map(function (f) {
      return Math.round(monthlyGen * f);
    });
    var cons = SEASON.map(function () {
      return Math.round(baseKwhDisplay);
    });
    var trace1 = {
      x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
      y: gen,
      type: "scatter",
      mode: "lines",
      name: "Geração estimada",
      line: { color: "#F59E0B", width: 3, shape: "spline", smoothing: 1.3 },
      fill: "tozeroy",
      fillcolor: "rgba(245, 158, 11, 0.1)",
    };
    var trace2 = {
      x: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
      y: cons,
      type: "scatter",
      mode: "lines",
      name: "Consumo médio",
      line: { color: "#0A2540", width: 2, dash: "dash" },
    };
    var layout = {
      margin: { t: 20, r: 20, b: 40, l: 40 },
      plot_bgcolor: "transparent",
      paper_bgcolor: "transparent",
      showlegend: true,
      legend: { orientation: "h", y: -0.2 },
      xaxis: { showgrid: false, color: "#6B7280" },
      yaxis: {
        showgrid: true,
        gridcolor: "rgba(0,0,0,0.05)",
        color: "#6B7280",
      },
    };
    var config = { responsive: true, displayModeBar: false };
    try {
      Plotly.react("generationChart", [trace1, trace2], layout, config);
    } catch (e) {
      try {
        Plotly.newPlot("generationChart", [trace1, trace2], layout, config);
      } catch (e2) {}
    }
  }

  function updateSolar() {
    var root = document.getElementById("solar-calculator-app");
    var range = el("cs-main-range");
    var toggle = el("toggle-consumption");
    var label = el("cs-label-main");
    var disp = el("cs-disp-main");
    if (!root || !range || !toggle) return;

    var selects = root.querySelectorAll("select.custom-input");
    var roofIdx = selects[1] ? selects[1].selectedIndex : 0;
    var shadeIdx = selects[2] ? selects[2].selectedIndex : 0;
    var siteEff = shadeMult(shadeIdx) * roofMult(roofIdx);

    var radios = root.querySelectorAll('input[name="property_type"]');
    var commercial = radios[1] && radios[1].checked;
    var propMult = commercial ? 1.12 : 1;

    var baseKwh = baseKwhFromRange(range, toggle);
    var monthlyKwh = baseKwh * propMult;
    var oldBill = oldBillMonthly(range, toggle);

    if (toggle.checked) {
      if (label) label.textContent = "Consumo médio (kWh/mês)";
      if (disp) disp.textContent = Math.round(parseFloat(range.value) || 0) + " kWh/mês";
    } else {
      if (label) label.textContent = "Valor médio da conta de luz (mensal)";
      if (disp) disp.textContent = formatBRL(parseFloat(range.value) || 0);
    }

    var coverage = 0.9;
    var denom = KWH_PER_KWP_MONTH * siteEff;
    var kWpRaw = (monthlyKwh * coverage) / Math.max(30, denom);
    var kWp = Math.min(200, Math.max(1.2, kWpRaw));
    var monthlyGen = kWp * denom;
    var area = kWp * 5.2;
    var modules = Math.max(2, Math.ceil(kWp / PANEL_KW));

    var newBill = Math.max(38, oldBill * (1 - coverage * 0.82));
    var annualSave = (oldBill - newBill) * 12;
    var invest = kWp * COST_PER_KWP;
    var paybackYears = annualSave > 120 ? invest / annualSave : 99;
    var paybackTxt =
      paybackYears < 25
        ? paybackYears.toFixed(1).replace(".", ",") + " anos"
        : "—";
    var barPct = Math.min(100, Math.max(6, Math.round((1 / Math.max(paybackYears, 0.5)) * 35)));

    if (el("cs-out-kwp")) el("cs-out-kwp").textContent = kWp.toFixed(1);
    if (el("cs-out-gen")) el("cs-out-gen").textContent = String(Math.round(monthlyGen));
    if (el("cs-out-area")) el("cs-out-area").textContent = String(Math.round(area));
    if (el("cs-out-mod")) el("cs-out-mod").textContent = String(modules);
    if (el("cs-out-saving")) el("cs-out-saving").textContent = formatBRL(annualSave);
    if (el("cs-out-newbill")) el("cs-out-newbill").textContent = formatBRL(newBill);
    if (el("cs-out-payback")) el("cs-out-payback").textContent = paybackTxt;
    var bar = el("cs-out-payback-bar");
    if (bar) bar.style.width = barPct + "%";
    var trees = Math.round((monthlyGen * 12 * 25) / 6500);
    if (el("cs-out-trees")) el("cs-out-trees").textContent = String(Math.max(1, trees));
    if (el("cs-side-monthly")) el("cs-side-monthly").textContent = String(Math.round(monthlyGen));

    updateChart(monthlyGen, baseKwh);
  }

  function bind() {
    var root = document.getElementById("solar-calculator-app");
    if (!root) return;
    if (_bound) {
      updateSolar();
      return;
    }
    var range = el("cs-main-range");
    var toggle = el("toggle-consumption");
    if (!range || !toggle) return;

    range.addEventListener("input", updateSolar);
    range.addEventListener("change", updateSolar);
    toggle.addEventListener("change", function () {
      var v = parseFloat(range.value) || 0;
      if (toggle.checked) {
        range.min = 100;
        range.max = 3500;
        range.step = 10;
        range.value = String(
          Math.min(3500, Math.max(100, Math.round(v / PRICE_KWH))),
        );
      } else {
        range.min = 100;
        range.max = 5000;
        range.step = 50;
        range.value = String(
          Math.min(5000, Math.max(100, Math.round(v * PRICE_KWH))),
        );
      }
      updateSolar();
    });

    root.querySelectorAll("select.custom-input").forEach(function (s) {
      s.addEventListener("change", updateSolar);
    });
    document.querySelectorAll('input[name="property_type"]').forEach(function (r) {
      r.addEventListener("change", updateSolar);
    });

    _bound = true;
    updateSolar();
  }

  function start() {
    bind();
    if (typeof Plotly !== "undefined") {
      setTimeout(bind, 300);
    } else {
      window.addEventListener("load", function () {
        setTimeout(bind, 200);
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();

(function () {
  function relayoutCharts() {
    if (window.Plotly) {
      document.querySelectorAll(".plot-container.plotly").forEach(function (pc) {
        var gd = pc.parentElement;
        if (!gd) return;
        var rect = gd.getBoundingClientRect();
        if (rect.width <= 0 || rect.height <= 0) return;
        try {
          window.Plotly.relayout(gd, {
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          });
        } catch (e) {}
      });
    }
    if (window.ApexCharts && window.Apex && window.Apex._chartInstances) {
      window.Apex._chartInstances.forEach(function (inst) {
        try {
          (inst.chart || inst).updateOptions({}, false, false);
        } catch (e) {}
      });
    }
    if (window.Chart) {
      try {
        Object.values(window.Chart.instances || {}).forEach(function (c) {
          c.resize();
        });
      } catch (e) {}
    }
  }

  window.addEventListener("load", function () {
    setTimeout(function () {
      relayoutCharts();
      setTimeout(relayoutCharts, 500);
    }, 300);
    try {
      var lastW = 0;
      var lastH = 0;
      var timer = 0;
      new ResizeObserver(function () {
        var w = document.documentElement.clientWidth;
        var h = document.documentElement.clientHeight;
        if (w === lastW && h === lastH) return;
        lastW = w;
        lastH = h;
        clearTimeout(timer);
        timer = setTimeout(relayoutCharts, 150);
      }).observe(document.documentElement);
    } catch (e) {}
  });
})();

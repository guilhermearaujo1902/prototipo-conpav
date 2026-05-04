(function () {
  var APP_NAMES = ["Laje / Piso", "Fundação", "Pilares"];
  var APP_MULT = [1, 1.08, 0.94];
  var TRUCK_M3 = 8;

  function el(id) {
    return document.getElementById(id);
  }

  function num(id, fallback) {
    var v = parseFloat(el(id).value);
    return isFinite(v) && v > 0 ? v : fallback;
  }

  function update() {
    var L = num("cc-in-length", 0);
    var W = num("cc-in-width", 0);
    var tCm = num("cc-in-thick", 0);
    var lossEl = el("cc-in-loss");
    var lossPct = lossEl ? parseInt(lossEl.value, 10) || 0 : 0;
    var radios = document.querySelectorAll('input[name="application_type"]');
    var appIdx = 0;
    for (var i = 0; i < radios.length; i++) {
      if (radios[i].checked) appIdx = i;
    }
    var mult = APP_MULT[appIdx] != null ? APP_MULT[appIdx] : 1;
    var baseM3 =
      L > 0 && W > 0 && tCm > 0 ? L * W * (tCm / 100) * mult : 0;
    var withLoss = baseM3 * (1 + lossPct / 100);
    var trucks = Math.max(1, Math.ceil(withLoss / TRUCK_M3));

    if (el("cc-out-volume")) {
      el("cc-out-volume").textContent =
        withLoss >= 100 ? withLoss.toFixed(1) : withLoss.toFixed(2);
    }
    if (el("cc-out-loss-text")) {
      el("cc-out-loss-text").textContent = "Inclui " + lossPct + "% de perda";
    }
    if (el("cc-in-loss-label")) {
      el("cc-in-loss-label").textContent = lossPct + "%";
    }
    if (el("cc-out-trucks")) {
      el("cc-out-trucks").textContent =
        trucks === 1 ? "1 Caminhão" : trucks + " Caminhões";
    }
    if (el("cc-out-truck-hint")) {
      el("cc-out-truck-hint").textContent =
        trucks === 1
          ? "Betoneira padrão (~" + TRUCK_M3 + " m³)"
          : "Volume total ÷ " + TRUCK_M3 + " m³ por viagem";
    }
    if (el("cc-out-app")) {
      el("cc-out-app").textContent = APP_NAMES[appIdx] || APP_NAMES[0];
    }
    var cap = el("cc-seg-caption");
    if (cap) {
      cap.textContent = APP_NAMES[appIdx] || APP_NAMES[0];
    }
    var fill = el("cc-seg-fill");
    if (fill) {
      fill.style.height = "100%";
    }
    var fck = el("cc-in-fck");
    if (el("cc-out-fck") && fck && fck.selectedOptions[0]) {
      el("cc-out-fck").textContent = fck.selectedOptions[0].textContent.trim();
    }
    var pump = el("cc-in-pump");
    if (el("cc-out-pump")) {
      el("cc-out-pump").textContent = pump && pump.checked ? "Incluso" : "Não incluso";
    }
    var cep = el("cc-in-cep");
    if (el("cc-out-cep")) {
      var c = cep && cep.value ? cep.value.replace(/\D/g, "") : "";
      if (c.length === 8) {
        el("cc-out-cep").textContent =
          c.slice(0, 5) + "-" + c.slice(5);
      } else if (cep && cep.value.trim()) {
        el("cc-out-cep").textContent = cep.value.trim();
      } else {
        el("cc-out-cep").textContent = "Pendente";
      }
    }
  }

  function bind() {
    if (!document.getElementById("calculator-app")) return;
    [
      "cc-in-length",
      "cc-in-width",
      "cc-in-thick",
      "cc-in-loss",
      "cc-in-fck",
      "cc-in-pump",
      "cc-in-cep",
    ].forEach(function (id) {
      var n = el(id);
      if (!n) return;
      n.addEventListener("input", update);
      n.addEventListener("change", update);
    });
    document.querySelectorAll('input[name="application_type"]').forEach(function (r) {
      r.addEventListener("change", update);
    });
    update();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }
})();

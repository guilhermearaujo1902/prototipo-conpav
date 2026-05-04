function switchTab(tabId) {
  var pMix = document.getElementById("panel-conpavmix");
  var pSolar = document.getElementById("panel-unisolar");
  var pCpv = document.getElementById("panel-cpv");
  if (!pMix || !pSolar || !pCpv) return;

  pMix.classList.add("hidden");
  pMix.classList.remove("block", "animate-fade-in");

  pSolar.classList.add("hidden");
  pSolar.classList.remove("block", "animate-fade-in");

  pCpv.classList.add("hidden");
  pCpv.classList.remove("block", "animate-fade-in");

  var selectedPanel = document.getElementById("panel-" + tabId);
  if (!selectedPanel) return;
  selectedPanel.classList.remove("hidden");
  selectedPanel.classList.add("block", "animate-fade-in");

  var badge = document.getElementById("summary-badge");
  var summaryList = document.getElementById("summary-list");
  if (!badge || !summaryList) return;

  if (tabId === "conpavmix") {
    badge.textContent = "CONPAVMIX";
    badge.className = "px-2 py-1 rounded bg-brand-navy/20 text-white";
    summaryList.innerHTML =
      '<li class="flex justify-between items-center text-sm">' +
      '<span class="text-brand-gray-400">Volume Estimado</span>' +
      '<span class="text-white font-semibold">-- m³</span></li>' +
      '<li class="flex justify-between items-center text-sm">' +
      '<span class="text-brand-gray-400">Resistência</span>' +
      '<span class="text-white font-semibold">25 MPa</span></li>';
  } else if (tabId === "unisolar") {
    badge.textContent = "UNISOLAR";
    badge.className = "px-2 py-1 rounded bg-brand-accent/20 text-brand-accent";
    summaryList.innerHTML =
      '<li class="flex justify-between items-center text-sm">' +
      '<span class="text-brand-gray-400">Tipo de Telhado</span>' +
      '<span class="text-white font-semibold">Residencial</span></li>' +
      '<li class="flex justify-between items-center text-sm">' +
      '<span class="text-brand-gray-400">Consumo Informado</span>' +
      '<span class="text-white font-semibold">--</span></li>';
  } else if (tabId === "cpv") {
    badge.textContent = "CPV MINERAÇÃO";
    badge.className = "px-2 py-1 rounded bg-brand-navy/20 text-white";
    summaryList.innerHTML =
      '<li class="flex justify-between items-center text-sm">' +
      '<span class="text-brand-gray-400">Material</span>' +
      '<span class="text-white font-semibold">Brita</span></li>' +
      '<li class="flex justify-between items-center text-sm">' +
      '<span class="text-brand-gray-400">Quantidade</span>' +
      '<span class="text-white font-semibold">-- Ton</span></li>';
  }
}

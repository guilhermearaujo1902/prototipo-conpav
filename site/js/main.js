(function () {
  var header = document.getElementById("header");
  if (header) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 20) {
        header.classList.add("shadow-lg", "bg-white/90");
        header.classList.remove("bg-white/80");
      } else {
        header.classList.remove("shadow-lg", "bg-white/90");
        header.classList.add("bg-white/80");
      }
    });
  }

  var toggle = document.getElementById("nav-toggle");
  var panel = document.getElementById("mobile-nav");
  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      panel.classList.toggle("hidden");
      var open = !panel.classList.contains("hidden");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    panel.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        panel.classList.add("hidden");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  var calcModal = document.getElementById("calc-modal");
  var calcFrame = document.getElementById("calc-modal-frame");
  var calcClose = document.getElementById("calc-modal-close");
  var calcBackdrop = document.getElementById("calc-modal-backdrop");
  var calcTitle = document.getElementById("calc-modal-title");

  function closeCalcModal() {
    if (!calcModal || !calcFrame) return;
    calcModal.classList.add("hidden");
    calcModal.setAttribute("aria-hidden", "true");
    calcFrame.src = "about:blank";
    document.body.classList.remove("calc-modal-open");
  }

  function openCalcModal(href, titleText) {
    if (!calcModal || !calcFrame) return;
    var base = href.split("#")[0];
    var sep = base.indexOf("?") >= 0 ? "&" : "?";
    var url = base + sep + "embed=1";
    if (calcTitle && titleText) calcTitle.textContent = titleText;
    calcFrame.setAttribute("title", titleText || "Calculadora");
    calcFrame.src = url;
    calcModal.classList.remove("hidden");
    calcModal.setAttribute("aria-hidden", "false");
    document.body.classList.add("calc-modal-open");
    var details = document.querySelector("details.nav-orcamento-wrap");
    if (details) details.removeAttribute("open");
    if (toggle && panel && !panel.classList.contains("hidden")) {
      panel.classList.add("hidden");
      toggle.setAttribute("aria-expanded", "false");
    }
    if (calcClose) calcClose.focus();
  }

  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest && e.target.closest("a.js-calc-modal");
    if (!a) return;
    if (e.defaultPrevented) return;
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    openCalcModal(a.getAttribute("href"), a.getAttribute("data-modal-title"));
  });

  if (calcClose) calcClose.addEventListener("click", closeCalcModal);
  if (calcBackdrop) calcBackdrop.addEventListener("click", closeCalcModal);

  document.addEventListener("keydown", function (e) {
    if (!calcModal || calcModal.classList.contains("hidden")) return;
    if (e.key === "Escape") closeCalcModal();
  });

  window.addEventListener("message", function (e) {
    if (!e.data || e.data.type !== "conpav-close-calc-modal") return;
    closeCalcModal();
  });
})();

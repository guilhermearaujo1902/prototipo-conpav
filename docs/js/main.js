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
})();

function switchBlogTab(tabId) {
  var newsGrid = document.getElementById("news-grid");
  var giveawaysList = document.getElementById("giveaways-list");
  var categoryFilters = document.getElementById("category-filters");
  var btns = document.querySelectorAll(".tab-btn");
  var indicator = document.getElementById("tab-indicator");

  if (!newsGrid || !giveawaysList || !categoryFilters || !indicator || btns.length < 2) {
    return;
  }

  btns.forEach(function (btn) {
    btn.classList.remove("active", "text-brand-navy");
    btn.classList.add("text-brand-gray-500");
  });

  if (tabId === "news") {
    newsGrid.classList.remove("hidden");
    giveawaysList.classList.add("hidden");
    categoryFilters.classList.remove("hidden");

    btns[0].classList.add("active");
    btns[0].classList.remove("text-brand-gray-500");

    indicator.style.width = "90px";
    indicator.style.transform = "translateX(0)";
  } else {
    newsGrid.classList.add("hidden");
    giveawaysList.classList.remove("hidden");
    categoryFilters.classList.add("hidden");

    btns[1].classList.add("active");
    btns[1].classList.remove("text-brand-gray-500");

    indicator.style.width = "95px";
    indicator.style.transform = "translateX(122px)";
  }
}

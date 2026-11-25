(() => {
  "use strict";

  const swagger = document.querySelector("#swagger-ui");
  const navigation = document.querySelector("#atlas-nav");
  const status = document.querySelector("#atlas-status");

  function syncCurrentSection() {
    const current = window.location.hash || navigation.firstElementChild?.hash;
    for (const link of navigation.querySelectorAll("a")) {
      if (link.hash === current) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    }
  }

  function buildNavigation() {
    const headings = swagger.querySelectorAll(".opblock-tag[id]");
    if (!headings.length) {
      if (swagger.querySelector(".errors-wrapper")) status.hidden = true;
      return;
    }

    const links = Array.from(headings, (heading) => {
      const link = document.createElement("a");
      const name = heading.querySelector("a")?.textContent.trim() || heading.textContent.trim();
      link.className = "atlas-nav-link";
      link.href = "#" + encodeURIComponent(heading.id);
      link.textContent = name === "default" ? "Общие маршруты" : name;
      return link;
    });
    navigation.replaceChildren(...links);
    syncCurrentSection();
    status.hidden = true;
    observer.disconnect();
  }

  const observer = new MutationObserver(buildNavigation);

  if (typeof SwaggerUIBundle !== "function") {
    status.textContent = "Не удалось загрузить интерфейс документации.";
    return;
  }

  window.addEventListener("hashchange", syncCurrentSection);
  observer.observe(swagger, { childList: true, subtree: true });

  SwaggerUIBundle({
    url: swagger.dataset.spec,
    domNode: swagger,
    oauth2RedirectUrl: new URL(swagger.dataset.redirect, window.location.origin).href,
    presets: [SwaggerUIBundle.presets.apis],
    layout: "BaseLayout",
    deepLinking: true,
    displayRequestDuration: true,
    validatorUrl: null,
  });
})();

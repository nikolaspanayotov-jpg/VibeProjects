(() => {
  const {
    DAYS,
    MEALS,
    parseLocalDate,
    titleCase,
    el,
    showDialog,
    formatShoppingQuantity,
    groupShoppingItems,
    shoppingAisle,
    slotKey,
    mealServings,
  } = globalThis.TopRecipes;

  // Headings use some of the page budget, so an aisle change cannot push rows off screen.
  function paginateShoppingItems(items, budget) {
    const pages = [];
    let current = [];
    let used = 0;
    let lastAisle = null;
    for (const { aisle, items: grouped } of groupShoppingItems(items)) {
      for (const item of grouped) {
        let cost = 1 + (lastAisle === aisle ? 0 : 0.65);
        if (current.length && used + cost > budget) {
          pages.push(current);
          current = [];
          used = 0;
          lastAisle = null;
          cost = 1.65;
        }
        current.push({ ...item, aisle });
        used += cost;
        lastAisle = aisle;
      }
    }
    if (current.length) pages.push(current);
    return pages.length ? pages : [[]];
  }

  function createCapture({
    getWeek,
    getWeekKey,
    getRecipe,
    getShoppingSnapshot,
    getMealSettings = () => ({}),
    getHouseholdSize = () => null,
  }) {
    const dialog = document.querySelector("#capture-dialog");
    const sheet = document.querySelector("#capture-sheet");
    const grid = document.querySelector("#capture-grid");
    const size = document.querySelector("#capture-size");
    let closingFromHistory = false;
    let opener;
    let mode = "plan";
    let page = 0;
    let pageSize = 10;
    let shoppingSnapshot = { items: [], missingCount: 0 };

    function setPageSize() {
      pageSize = Math.max(
        5,
        Math.min(10, Math.floor((window.innerHeight - 280) / 48)),
      );
    }

    function renderShopping(printing = false) {
      const containerEl = document.querySelector("#capture-shopping");
      containerEl.replaceChildren();
      containerEl.setAttribute("role", "list");
      const pages = paginateShoppingItems(shoppingSnapshot.items, pageSize);
      const totalPages = pages.length;
      page = Math.max(0, Math.min(page, totalPages - 1));
      const visible = printing
        ? groupShoppingItems(shoppingSnapshot.items).flatMap(
            (group) => group.items,
          )
        : pages[page];
      let lastAisle;
      visible.forEach((item) => {
        const aisle = item.aisle || shoppingAisle(item.name);
        if (aisle !== lastAisle) {
          const heading = el("div", "shopping-capture-aisle", aisle);
          heading.setAttribute("role", "presentation");
          containerEl.append(heading);
          lastAisle = aisle;
        }
        const rowEl = el("div", "shopping-capture-row");
        rowEl.setAttribute("role", "listitem");
        rowEl.dataset.shoppingKey = item.key;
        const boxEl = el(
          "span",
          "shopping-capture-box",
          item.bought ? "☑" : "□",
        );
        boxEl.setAttribute("aria-hidden", "true");
        rowEl.classList.toggle("bought", !!item.bought);
        if (item.bought)
          rowEl.setAttribute(
            "aria-label",
            `${item.name}, bought, ${formatShoppingQuantity(item)}`,
          );
        rowEl.append(
          boxEl,
          el("span", "shopping-capture-name", item.name),
          el(
            "strong",
            "shopping-capture-quantity",
            formatShoppingQuantity(item),
          ),
        );
        containerEl.append(rowEl);
      });
      if (!visible.length)
        containerEl.append(
          el("p", "empty-message", "No ingredients selected."),
        );
      if (shoppingSnapshot.missingCount)
        containerEl.append(
          el(
            "p",
            "shopping-capture-warning",
            `Ingredients unavailable for ${shoppingSnapshot.missingCount} planned meal${shoppingSnapshot.missingCount === 1 ? "" : "s"}.`,
          ),
        );
      document.querySelector("#capture-pages").hidden = totalPages <= 1;
      document.querySelector("#capture-page-label").textContent =
        `Page ${page + 1} of ${totalPages}`;
      document.querySelector("#capture-previous-page").disabled = page === 0;
      document.querySelector("#capture-next-page").disabled =
        page === totalPages - 1;
      document.querySelector("#capture-footer-label").textContent = printing
        ? `${shoppingSnapshot.items.length} shopping items`
        : `Page ${page + 1} of ${totalPages} · ${shoppingSnapshot.items.length} items`;
    }

    function renderActive({ printing = false } = {}) {
      const shoppingMode = mode === "shopping";
      dialog.classList.toggle("is-shopping", shoppingMode);
      sheet.classList.toggle("shopping-sheet", shoppingMode);
      const headingEl = document.querySelector("#capture-title");
      headingEl.replaceChildren(
        document.createTextNode(shoppingMode ? "My shopping" : "My weekly"),
        el("br"),
        el("em", null, shoppingMode ? "list." : "meal plan."),
      );
      sheet.setAttribute(
        "aria-label",
        `${shoppingMode ? "Shopping list" : "Weekly meal plan"}. Press Enter to toggle screenshot controls.`,
      );
      document.querySelector("#capture-close").textContent = shoppingMode
        ? "← Back to shopping list"
        : "← Back to planning";
      document.querySelector("#capture-shopping").hidden = !shoppingMode;
      grid.hidden = shoppingMode;
      document.querySelector("#capture-instructions").textContent = shoppingMode
        ? "Tap the list to hide controls. Tap again or press Escape to restore them. Use Next page for longer lists."
        : "Tap your plan to hide controls. Tap again, press Escape, or use Back to restore them.";
      renderPlan();
      if (shoppingMode) renderShopping(printing);
      else {
        document.querySelector("#capture-pages").hidden = true;
        document.querySelector("#capture-footer-label").textContent =
          "A week of good meals ✳";
      }
    }

    function measure() {
      const controls = dialog.querySelector(".capture-controls");
      const available = Math.max(
        380,
        window.innerHeight -
          (dialog.classList.contains("controls-hidden")
            ? 0
            : controls.getBoundingClientRect().height + 50),
      );
      sheet.style.setProperty("--capture-height", `${available}px`);
      requestAnimationFrame(() => {
        document.querySelector("#capture-overflow").hidden =
          sheet.scrollHeight <= available + 4 || size.value !== "fit";
      });
    }

    function renderPlan() {
      const week = getWeek();
      const start = parseLocalDate(getWeekKey());
      const end = new Date(start);
      end.setDate(end.getDate() + 6);
      const format = (date) =>
        date.toLocaleDateString(undefined, {
          day: "numeric",
          month: "long",
          year: "numeric",
        });
      document.querySelector("#capture-dates").textContent =
        `${format(start)} — ${format(end)}`;
      grid.replaceChildren();
      const head = el("div", "capture-row");
      head.setAttribute("role", "row");
      for (const label of ["Day", ...MEALS.map(titleCase)]) {
        const cell = el("div", "capture-cell", label);
        cell.setAttribute("role", "columnheader");
        head.append(cell);
      }
      grid.append(head);
      DAYS.forEach((day, index) => {
        const row = el("div", "capture-row");
        row.setAttribute("role", "row");
        const date = new Date(start);
        date.setDate(date.getDate() + index);
        const dayCell = el(
          "div",
          "capture-cell capture-day",
          titleCase(day).slice(0, 3),
        );
        dayCell.setAttribute("role", "rowheader");
        dayCell.append(
          el(
            "small",
            null,
            date.toLocaleDateString(undefined, {
              day: "numeric",
              month: "short",
            }),
          ),
        );
        row.append(dayCell);
        MEALS.forEach((meal) => {
          const id = week[day][meal];
          const cell = el(
            "div",
            "capture-cell",
            id ? getRecipe(id)?.title || "Recipe unavailable" : "—",
          );
          cell.setAttribute("role", "cell");
          const settings = getMealSettings()[slotKey({ day, meal })] || {};
          const recipe = getRecipe(id);
          if (
            recipe &&
            (getHouseholdSize() || settings.servings || settings.leftoverOf)
          ) {
            const servings = mealServings(recipe, settings, getHouseholdSize());
            cell.append(
              el(
                "small",
                "capture-portions",
                `${settings.leftoverOf ? "Leftovers · " : ""}${servings} ${servings === 1 ? "serving" : "servings"}`,
              ),
            );
          }
          row.append(cell);
        });
        grid.append(row);
      });
    }

    function open(trigger, nextMode = "plan") {
      opener = trigger;
      mode = nextMode;
      page = 0;
      setPageSize();
      if (mode === "shopping") shoppingSnapshot = getShoppingSnapshot();
      renderActive();
      dialog.classList.remove("controls-hidden");
      sheet.classList.toggle("fit", size.value === "fit");
      showDialog(dialog, trigger);
      history.pushState({ topRecipesCapture: true, controlsHidden: false }, "");
      measure();
    }

    function toggleControls() {
      const hidden = dialog.classList.toggle("controls-hidden");
      if (hidden)
        history.pushState(
          { topRecipesCapture: true, controlsHidden: true },
          "",
        );
      else if (history.state?.controlsHidden) history.back();
      measure();
    }

    function close() {
      if (history.state?.topRecipesCapture) {
        const hidden = history.state.controlsHidden;
        closingFromHistory = true;
        history.go(hidden ? -2 : -1);
      }
      dialog.close();
    }

    sheet.addEventListener("click", toggleControls);
    document.querySelector("#capture-hide").addEventListener("click", () => {
      toggleControls();
      sheet.focus({ preventScroll: true });
    });
    sheet.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        toggleControls();
      }
      if (
        mode === "shopping" &&
        !event.altKey &&
        !event.metaKey &&
        !event.ctrlKey &&
        ["ArrowLeft", "ArrowRight"].includes(event.key)
      ) {
        event.preventDefault();
        page += event.key === "ArrowRight" ? 1 : -1;
        renderShopping();
        measure();
      }
    });
    document
      .querySelector("#capture-previous-page")
      .addEventListener("click", () => {
        page--;
        renderShopping();
        measure();
      });
    document
      .querySelector("#capture-next-page")
      .addEventListener("click", () => {
        page++;
        renderShopping();
        measure();
      });
    document.querySelector("#capture-close").addEventListener("click", close);
    document
      .querySelector("#capture-print")
      .addEventListener("click", () => window.print());
    size.addEventListener("change", () => {
      sheet.classList.toggle("fit", size.value === "fit");
      measure();
    });
    dialog.addEventListener("cancel", (event) => {
      event.preventDefault();
      if (dialog.classList.contains("controls-hidden")) toggleControls();
      else close();
    });
    window.addEventListener("resize", () => {
      if (dialog.open) {
        if (mode === "shopping") {
          const first = page * pageSize;
          setPageSize();
          page = Math.floor(first / pageSize);
          renderShopping();
        }
        measure();
      }
    });
    window.addEventListener("beforeprint", () => {
      if (!dialog.open) mode = "plan";
      renderActive({ printing: true });
    });
    window.addEventListener("afterprint", () => {
      renderActive();
      if (dialog.open) measure();
    });
    window.addEventListener("popstate", (event) => {
      if (closingFromHistory) {
        closingFromHistory = false;
        return;
      }
      if (!dialog.open) return;
      if (event.state?.topRecipesCapture) {
        dialog.classList.toggle(
          "controls-hidden",
          Boolean(event.state.controlsHidden),
        );
        measure();
      } else {
        dialog.close();
        if (opener?.isConnected) opener.focus({ preventScroll: true });
      }
    });
    return { open, openShopping: (trigger) => open(trigger, "shopping") };
  }

  Object.assign((globalThis.TopRecipes ||= {}), {
    createCapture,
    paginateShoppingItems,
  });
})();

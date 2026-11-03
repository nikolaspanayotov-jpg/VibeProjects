(() => {
  const { DAYS, MEALS, parseLocalDate, titleCase, el, showDialog } =
    globalThis.TopRecipes;

  function createCapture({ getWeek, getWeekKey, getRecipe }) {
    const dialog = document.querySelector("#capture-dialog");
    const sheet = document.querySelector("#capture-sheet");
    const grid = document.querySelector("#capture-grid");
    const size = document.querySelector("#capture-size");
    let closingFromHistory = false;
    let opener;

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
          row.append(cell);
        });
        grid.append(row);
      });
    }

    function open(trigger) {
      opener = trigger;
      renderPlan();
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
      if (dialog.open) measure();
    });
    window.addEventListener("beforeprint", renderPlan);
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
    return { open };
  }

  Object.assign((globalThis.TopRecipes ||= {}), { createCapture });
})();

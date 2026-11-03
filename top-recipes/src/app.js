(() => {
  const {
    DAYS,
    MEALS,
    titleCase,
    emptyWeek,
    mondayKey,
    weekOffset,
    parseLocalDate,
    dateKey,
    assignMeal,
    moveMeal,
    slotLabel,
    createPersistence,
    el,
    button,
    showDialog,
    closeOnBackdrop,
    createRecipeViews,
    recipeImage,
    matchesRecipe,
    validateRecipeData,
    createCapture,
    parseRecipes,
  } = globalThis.TopRecipes;

  const $ = (selector) => document.querySelector(selector);
  let localStorage;
  try {
    localStorage = window.localStorage;
  } catch {
    /* Private browsing may deny access. */
  }
  const persistence = createPersistence(localStorage);
  let selectedWeek = mondayKey();
  let week = persistence.week(selectedWeek);
  let undoState = null;
  let recipes = [];
  let recipeMap = new Map();
  let filter = "all";
  let dragged = null;
  let loadState = "loading";
  let loadError = "";
  const grid = $("#planner-grid");
  const picker = $("#picker-dialog");

  function storageChanged() {
    const issue = persistence.issue;
    $("#storage-banner").hidden = !issue;
    $("#reset-storage").hidden = issue !== "corrupt";
    $("#storage-message").textContent =
      issue === "corrupt"
        ? "Saved data could not be read. The original has been kept. You can plan for this session, or reset saved data to start again."
        : "This plan and your ingredient checks will last until you close the page. Browser storage is unavailable.";
    $("#save-note").textContent = issue
      ? "Changes are kept for this session only."
      : "Your plan saves automatically in this browser.";
  }

  function notify(message) {
    $("#toast").hidden = false;
    $("#status").textContent = message;
    $("#undo").hidden = !undoState;
  }

  function clearDrag() {
    dragged = null;
    document.body.classList.remove("is-dragging");
    grid
      .querySelectorAll(".drag-over")
      .forEach((slot) => slot.classList.remove("drag-over"));
  }

  function makeDraggable(handle, payload) {
    handle.draggable = true;
    handle.addEventListener("dragstart", (event) => {
      if (!event.dataTransfer) return;
      dragged = payload;
      event.dataTransfer.effectAllowed = payload.source ? "move" : "copy";
      event.dataTransfer.setData(
        "application/x-top-recipes",
        JSON.stringify(payload),
      );
      event.dataTransfer.setData(
        "text/plain",
        recipeMap.get(payload.recipeId)?.title || "Meal",
      );
      document.body.classList.add("is-dragging");
      event.stopPropagation();
    });
    handle.addEventListener("dragend", clearDrag);
  }

  const recipeViews = createRecipeViews({
    persistence,
    openPlacement,
    makeDraggable,
    notify,
    storageChanged,
  });
  const capture = createCapture({
    getWeek: () => week,
    getWeekKey: () => selectedWeek,
    getRecipe: (id) => recipeMap.get(id),
  });

  function focusSlot(slot) {
    requestAnimationFrame(() => {
      const cell = grid.querySelector(
        `[data-day="${slot.day}"][data-meal="${slot.meal}"]`,
      );
      cell?.querySelector("button")?.focus({ preventScroll: true });
    });
  }

  function changeWeek(nextWeek, message, target) {
    if (JSON.stringify(nextWeek) === JSON.stringify(week)) return;
    undoState = week;
    week = nextWeek;
    persistence.saveWeek(selectedWeek, week);
    renderPlanner();
    storageChanged();
    notify(message);
    if (target) focusSlot(target);
  }

  function renderPlanner() {
    grid.replaceChildren();
    const start = parseLocalDate(selectedWeek);
    const end = new Date(start);
    end.setDate(end.getDate() + 6);
    const shortDate = (date) =>
      date.toLocaleDateString(undefined, { day: "numeric", month: "short" });
    $("#week-heading").textContent =
      `${shortDate(start)} — ${shortDate(end)}, ${end.getFullYear()}`;
    $("#week-date").value = selectedWeek;
    $("#current-week").disabled = selectedWeek === mondayKey();
    const today = dateKey(new Date());
    DAYS.forEach((day, index) => {
      const date = new Date(start);
      date.setDate(date.getDate() + index);
      const heading = el(
        "div",
        `day-header${dateKey(date) === today ? " today" : ""}`,
      );
      heading.style.setProperty("--day", index);
      heading.append(
        el("strong", null, titleCase(day).slice(0, 3)),
        el("span", null, shortDate(date)),
      );
      grid.append(heading);
    });
    MEALS.forEach((meal, index) => {
      const label = el("div", "meal-label");
      label.dataset.meal = meal;
      label.style.setProperty("--meal", index);
      const symbol = el("span", "meal-symbol", ["☼", "◒", "☾"][index]);
      symbol.setAttribute("aria-hidden", "true");
      label.append(symbol, el("span", null, titleCase(meal)));
      grid.append(label);
    });
    DAYS.forEach((day, dayIndex) =>
      MEALS.forEach((meal, mealIndex) => {
        const target = { day, meal };
        const recipeId = week[day][meal];
        const recipe = recipeMap.get(recipeId);
        const slot = el(
          "div",
          `slot${recipeId ? " filled" : ""}${recipeId && !recipe ? " unavailable" : ""}`,
        );
        slot.dataset.day = day;
        slot.dataset.meal = meal;
        slot.dataset.dropLabel = `Add to ${slotLabel(target)}`;
        slot.style.setProperty("--day", dayIndex);
        slot.style.setProperty("--meal", mealIndex);
        slot.setAttribute("role", "group");
        slot.setAttribute(
          "aria-label",
          `${slotLabel(target)}${recipeId ? `: ${recipe?.title || "Recipe unavailable"}` : ", empty"}`,
        );
        if (recipeId) {
          const title = button(
            recipe?.title ||
              (loadState === "loading"
                ? "Loading recipe…"
                : "Recipe unavailable"),
            "planned-title",
            () => {
              if (recipe) recipeViews.open(recipe, title);
              else openActions(target, title);
            },
            `${slotLabel(target)}: ${recipe?.title || "Recipe unavailable"}. ${recipe ? "View recipe and ingredients" : "Change or remove this meal"}`,
          );
          const tools = el("div", "slot-tools");
          const handle = button(
            "⠿",
            "drag-handle",
            () => openPlacement(recipeId, handle, target),
            `Move ${recipe?.title || "meal"} from ${slotLabel(target)}`,
          );
          makeDraggable(handle, { recipeId, source: target });
          const more = button(
            "···",
            "slot-more",
            () => openActions(target, more),
            `Options for ${slotLabel(target)}`,
          );
          tools.append(handle, more);
          slot.append(title, tools);
        } else {
          const add = button(
            "",
            "slot-empty",
            () => openRecipePicker(target, add),
            `Add a meal to ${slotLabel(target)}`,
          );
          const plus = el("span", "slot-plus", "+");
          plus.setAttribute("aria-hidden", "true");
          add.append(plus, el("span", null, "Add meal"));
          slot.append(add);
        }
        slot.addEventListener("dragover", (event) => {
          if (!dragged) return;
          event.preventDefault();
          event.dataTransfer.dropEffect = dragged.source ? "move" : "copy";
          slot.classList.add("drag-over");
        });
        slot.addEventListener("dragleave", (event) => {
          if (!slot.contains(event.relatedTarget))
            slot.classList.remove("drag-over");
        });
        slot.addEventListener("drop", (event) => {
          if (!dragged) return;
          event.preventDefault();
          const payload = dragged;
          clearDrag();
          if (payload.source)
            changeWeek(
              moveMeal(week, payload.source, target),
              `${recipeMap.get(payload.recipeId)?.title || "Meal"} moved to ${slotLabel(target)}${recipeId ? "; meals swapped" : ""}.`,
              target,
            );
          else if (recipeMap.has(payload.recipeId))
            changeWeek(
              assignMeal(week, target, payload.recipeId),
              `${recipeMap.get(payload.recipeId).title} added to ${slotLabel(target)}.`,
              target,
            );
        });
        grid.append(slot);
      }),
    );
    const filled = DAYS.reduce(
      (count, day) => count + MEALS.filter((meal) => week[day][meal]).length,
      0,
    );
    $("#plan-summary").textContent = filled
      ? `${filled} of 21 meals planned. Something good to look forward to.`
      : "A fresh week, full of possibilities.";
    $("#clear-week").disabled = filled === 0;
    $("#undo-inline").hidden = !undoState;
  }

  function renderLibrary() {
    const list = $("#recipe-list");
    list.replaceChildren();
    if (loadState === "loading") {
      list.append(el("p", "empty-message", "Opening the recipe notebook…"));
      return;
    }
    if (loadState === "error") {
      const error = el(
        "div",
        "empty-message",
        document.location.protocol === "file:"
          ? "Choose your recipes.md file to open the notebook. Your browser keeps local files private until you select one."
          : "The recipe notebook could not be opened. Your saved plan is still here.",
      );
      error.append(button("Try again", "text-button", loadRecipes));
      if (loadError) error.append(el("p", "load-error", loadError));
      const label = el("label", "button button-outline", "Open recipes.md");
      const file = el("input", "sr-only");
      file.type = "file";
      file.accept = ".md,text/markdown,text/plain";
      file.addEventListener("change", async () => {
        if (!file.files[0]) return;
        try {
          acceptRecipes(await file.files[0].text());
        } catch (error) {
          loadState = "error";
          loadError = error.message;
        }
        renderLibrary();
        renderPlanner();
      });
      label.append(file);
      error.append(label);
      list.append(error);
      return;
    }
    const visible = recipes.filter((recipe) =>
      matchesRecipe(recipe, $("#recipe-search").value, filter),
    );
    $("#recipe-count").textContent =
      `${String(visible.length).padStart(2, "0")} RECIPE${visible.length === 1 ? "" : "S"}`;
    if (!visible.length) {
      const empty = el(
        "div",
        "empty-message",
        "No recipes found. A fresh search might do the trick.",
      );
      empty.append(
        button("Clear filters", "text-button", () => {
          $("#recipe-search").value = "";
          setFilter("all");
          $("#recipe-search").focus();
        }),
      );
      list.append(empty);
    } else visible.forEach((recipe) => list.append(recipeViews.card(recipe)));
  }

  function setFilter(value) {
    filter = value;
    $("#meal-filters")
      .querySelectorAll("button")
      .forEach((control) => {
        const active = control.dataset.filter === filter;
        control.classList.toggle("active", active);
        control.setAttribute("aria-pressed", String(active));
      });
    renderLibrary();
  }

  function pickerShell(title, opener) {
    $("#picker-title").textContent = title;
    const content = $("#picker-content");
    content.replaceChildren();
    if (!picker.open) showDialog(picker, opener);
    return content;
  }

  function openRecipePicker(target, opener) {
    const content = pickerShell(`What’s for ${slotLabel(target)}?`, opener);
    const search = el("input");
    search.type = "search";
    search.placeholder = "Search your favourites…";
    search.setAttribute("aria-label", "Search recipes for this meal");
    const field = el("label", "search-field");
    field.append(search);
    const list = el("div", "picker-list");
    list.setAttribute("aria-live", "polite");
    const update = () => {
      list.replaceChildren();
      const visible = recipes.filter((recipe) =>
        matchesRecipe(recipe, search.value),
      );
      if (loadState !== "ready") {
        list.append(
          el(
            "p",
            "picker-context",
            loadState === "loading"
              ? "The recipes are still loading. Close this picker and try again in a moment."
              : "The recipes could not be loaded.",
          ),
        );
        if (loadState === "error")
          list.append(
            button("Try again", "text-button", async () => {
              await loadRecipes();
              update();
            }),
          );
      } else if (!visible.length)
        list.append(
          el(
            "p",
            "picker-context",
            "No recipes found. Try another ingredient or name.",
          ),
        );
      else
        visible.forEach((recipe) => {
          const choice = button(
            "",
            "picker-recipe",
            () => {
              picker.close();
              changeWeek(
                assignMeal(week, target, recipe.id),
                `${recipe.title} added to ${slotLabel(target)}.`,
                target,
              );
            },
            `Choose ${recipe.title} for ${slotLabel(target)}`,
          );
          const image = el("img");
          image.src = recipeImage(recipe);
          image.alt = "";
          const text = el("span");
          text.append(
            el("strong", null, recipe.title),
            el("small", null, recipe.mealTypes.map(titleCase).join(" / ")),
          );
          choice.append(image, text, el("span", null, "+"));
          list.append(choice);
        });
    };
    search.addEventListener("input", update);
    content.append(field, list);
    update();
    search.focus();
  }

  function openPlacement(recipeId, opener, source = null) {
    const recipe = recipeMap.get(recipeId);
    const title = recipe?.title || "Meal";
    const content = pickerShell(
      source ? `Move ${title}` : `Add ${title}`,
      opener,
    );
    content.append(
      el(
        "p",
        "picker-context",
        source
          ? "Choose a new home. If another meal is already there, the two meals will swap places."
          : "Choose a day and a meal. You can enjoy a favourite more than once. An occupied slot will be replaced.",
      ),
    );
    const form = el("form", "picker-form");
    const dayLabel = el("label", null, "Day");
    const daySelect = el("select");
    daySelect.name = "day";
    DAYS.forEach((day) => {
      const option = el("option", null, titleCase(day));
      option.value = day;
      daySelect.append(option);
    });
    const mealLabel = el("label", null, "Meal");
    const mealSelect = el("select");
    mealSelect.name = "meal";
    MEALS.forEach((meal) => {
      const option = el("option", null, titleCase(meal));
      option.value = meal;
      mealSelect.append(option);
    });
    daySelect.value = source?.day || "monday";
    mealSelect.value = source?.meal || recipe?.mealTypes[0] || "dinner";
    dayLabel.append(daySelect);
    mealLabel.append(mealSelect);
    const submit = button(
      source ? "Move meal" : "Add to my week",
      "button button-primary",
    );
    submit.type = "submit";
    form.append(dayLabel, mealLabel, submit);
    content.append(form);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const target = { day: daySelect.value, meal: mealSelect.value };
      const wasOccupied = Boolean(week[target.day][target.meal]);
      picker.close();
      const next = source
        ? moveMeal(week, source, target)
        : assignMeal(week, target, recipeId);
      changeWeek(
        next,
        `${title} ${source ? "moved" : "added"} to ${slotLabel(target)}${source && wasOccupied ? "; meals swapped" : ""}.`,
        target,
      );
    });
  }

  function openActions(target, opener) {
    const recipeId = week[target.day][target.meal];
    const recipe = recipeMap.get(recipeId);
    const content = pickerShell(slotLabel(target), opener);
    const actions = el("div", "meal-actions");
    actions.append(
      el("p", "picker-context", recipe?.title || "Recipe unavailable"),
    );
    if (recipe)
      actions.append(
        button("View recipe & ingredients ↗", "button button-outline", () => {
          picker.close();
          recipeViews.open(recipe, opener);
        }),
      );
    actions.append(
      button("Change meal", "button button-outline", () =>
        openRecipePicker(target, opener),
      ),
      button("Move to another slot", "button button-outline", () =>
        openPlacement(recipeId, opener, target),
      ),
      button("Remove meal", "button button-danger", () => {
        picker.close();
        changeWeek(
          assignMeal(week, target, null),
          `${recipe?.title || "Meal"} removed from ${slotLabel(target)}.`,
          target,
        );
      }),
    );
    content.append(actions);
  }

  function navigateWeek(key) {
    selectedWeek = mondayKey(key);
    week = persistence.week(selectedWeek);
    undoState = null;
    clearDrag();
    renderPlanner();
    $("#toast").hidden = true;
  }

  async function loadRecipes() {
    loadState = "loading";
    renderLibrary();
    try {
      const response = await fetch(new URL("./recipes.md", document.baseURI), {
        cache: "no-cache",
      });
      if (!response.ok) throw new Error("Could not load recipes");
      acceptRecipes(await response.text());
    } catch (error) {
      loadState = "error";
      loadError = error.message;
    }
    renderLibrary();
    renderPlanner();
  }

  function acceptRecipes(markdown) {
    const next = validateRecipeData(parseRecipes(markdown));
    recipes = next;
    recipeMap = new Map(recipes.map((recipe) => [recipe.id, recipe]));
    loadState = "ready";
    loadError = "";
  }

  $("#recipe-search").addEventListener("input", renderLibrary);
  $("#meal-filters")
    .querySelectorAll("button")
    .forEach((control) =>
      control.addEventListener("click", () =>
        setFilter(control.dataset.filter),
      ),
    );
  $("#previous-week").addEventListener("click", () =>
    navigateWeek(weekOffset(selectedWeek, -1)),
  );
  $("#next-week").addEventListener("click", () =>
    navigateWeek(weekOffset(selectedWeek, 1)),
  );
  $("#current-week").addEventListener("click", () => navigateWeek(mondayKey()));
  $("#week-date").addEventListener("change", (event) => {
    if (event.target.value) navigateWeek(event.target.value);
  });
  $("#clear-week").addEventListener("click", () =>
    changeWeek(emptyWeek(), "This week cleared. A fresh start."),
  );
  function undoLastChange() {
    if (!undoState) return;
    week = undoState;
    undoState = null;
    persistence.saveWeek(selectedWeek, week);
    renderPlanner();
    storageChanged();
    notify("Last change undone.");
    focusSlot({ day: "monday", meal: "breakfast" });
  }
  $("#undo").addEventListener("click", undoLastChange);
  $("#undo-inline").addEventListener("click", undoLastChange);
  $("#dismiss-toast").addEventListener("click", () => {
    $("#toast").hidden = true;
  });
  $("#screenshot-open").addEventListener("click", (event) =>
    capture.open(event.currentTarget),
  );
  $("#reset-storage").addEventListener("click", () => {
    persistence.reset();
    week = persistence.week(selectedWeek);
    undoState = null;
    storageChanged();
    renderPlanner();
    recipeViews.refresh();
    notify("Saved data reset. Ready for a fresh week.");
  });
  document
    .querySelectorAll("[data-close]")
    .forEach((control) =>
      control.addEventListener("click", () =>
        document.getElementById(control.dataset.close).close(),
      ),
    );
  document
    .querySelectorAll("dialog:not(#capture-dialog)")
    .forEach(closeOnBackdrop);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") clearDrag();
  });
  storageChanged();
  renderPlanner();
  loadRecipes();
})();

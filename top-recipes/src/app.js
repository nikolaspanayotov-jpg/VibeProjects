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
    recipeIllustration,
    matchesRecipe,
    validateRecipeData,
    createCapture,
    createShoppingList,
    parseRecipes,
    clone,
    slotKey,
    cleanMealSettings,
    moveMealSettings,
    replaceMealSettings,
    mealServings,
    createPlanTools,
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
  let mealSettings = cleanMealSettings(
    week,
    persistence.mealSettings(selectedWeek),
  );
  let preferences = persistence.preferences();
  let undoState = null;
  let recipes = [];
  let recipeMap = new Map();
  let filter = "all";
  let dragged = null;
  let loadState = "loading";
  let loadError = "";
  const grid = $("#planner-grid");
  const picker = $("#picker-dialog");
  const libraryEl = $("#recipes");
  const libraryContentEl = $("#recipes-content");
  const libraryToggleEl = $("#recipes-toggle");
  const stackedLayout = window.matchMedia("(max-width: 960px)");
  let libraryExpanded = false;
  let libraryChosenByUser = false;

  function setLibraryExpanded(
    expanded,
    { user = false, goToPlan = false } = {},
  ) {
    if (user) libraryChosenByUser = true;
    const scrolledPastHeader = libraryEl.getBoundingClientRect().top < 0;
    const focusInContent = libraryContentEl.contains(document.activeElement);
    libraryExpanded = expanded;
    libraryContentEl.hidden = !expanded;
    libraryToggleEl.setAttribute("aria-expanded", String(expanded));
    $("#recipes-toggle-label").textContent = expanded
      ? "Hide recipes"
      : "Show recipes";
    libraryEl.classList.toggle("library-expanded", expanded);
    $(".workspace").classList.toggle("recipes-collapsed", !expanded);
    setMobileTab(expanded ? "recipes" : "plan");
    if (!expanded) {
      clearDrag();
      if (focusInContent && !goToPlan)
        libraryToggleEl.focus({ preventScroll: true });
      if (goToPlan || scrolledPastHeader)
        requestAnimationFrame(() => {
          if (goToPlan) {
            $("#planner-heading").focus({ preventScroll: true });
            $("#weekly-plan").scrollIntoView({
              block: "start",
              behavior: "auto",
            });
          } else libraryEl.scrollIntoView({ block: "start", behavior: "auto" });
        });
    }
  }

  function setMobileTab(tab) {
    document.querySelectorAll(".mobile-nav [data-tab]").forEach((control) => {
      if (control.dataset.tab === tab)
        control.setAttribute("aria-current", "page");
      else control.removeAttribute("aria-current");
    });
  }

  function savePreferences(next) {
    preferences = next;
    persistence.savePreferences(preferences);
    storageChanged();
  }

  function favouriteButton(recipe, onChange) {
    const control = button("", "favourite-button", () => {
      const pinned = preferences.favourites.includes(recipe.id);
      savePreferences({
        ...preferences,
        favourites: pinned
          ? preferences.favourites.filter((id) => id !== recipe.id)
          : [...preferences.favourites, recipe.id],
      });
      syncFavourites();
      if (onChange) onChange();
    });
    control.dataset.favourite = recipe.id;
    updateFavourite(control);
    return control;
  }

  function updateFavourite(control) {
    const id = control.dataset.favourite;
    const pinned = preferences.favourites.includes(id);
    control.textContent = pinned ? "★" : "☆";
    control.setAttribute("aria-pressed", String(pinned));
    control.setAttribute(
      "aria-label",
      `${pinned ? "Unpin" : "Pin"} ${recipeMap.get(id)?.title || "recipe"}`,
    );
    control.title = pinned ? "Unpin favourite" : "Pin favourite";
  }

  function syncFavourites() {
    document.querySelectorAll("[data-favourite]").forEach(updateFavourite);
  }

  function storageChanged() {
    const issue = persistence.issue;
    $("#storage-banner").hidden = !issue;
    $("#reset-storage").hidden = issue !== "corrupt";
    $("#storage-message").textContent =
      issue === "corrupt"
        ? "Saved data could not be read. The original has been kept. You can plan for this session, or reset saved data to start again."
        : "This plan, shopping list and ingredient checks will last until you close the page. Browser storage is unavailable.";
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
    favouriteButton,
  });
  let shopping;
  const capture = createCapture({
    getWeek: () => week,
    getWeekKey: () => selectedWeek,
    getRecipe: (id) => recipeMap.get(id),
    getShoppingSnapshot: () => shopping.snapshot(),
    getMealSettings: () => mealSettings,
    getHouseholdSize: () => preferences.householdSize,
  });
  shopping = createShoppingList({
    getWeek: () => week,
    getWeekKey: () => selectedWeek,
    getRecipe: (id) => recipeMap.get(id),
    persistence,
    storageChanged,
    openCapture: (trigger) => capture.openShopping(trigger),
    getMealSettings: () => mealSettings,
    getHouseholdSize: () => preferences.householdSize,
  });
  const planTools = createPlanTools({
    getWeek: () => week,
    getSettings: () => mealSettings,
    getWeekKey: () => selectedWeek,
    getRecipe: (id) => recipeMap.get(id),
    getPreferences: () => preferences,
    persistence,
    changeWeek,
    pickerShell,
    closePicker: () => picker.close(),
    notify,
    storageChanged,
  });

  function focusSlot(slot) {
    requestAnimationFrame(() => {
      const cell = grid.querySelector(
        `[data-day="${slot.day}"][data-meal="${slot.meal}"]`,
      );
      cell?.querySelector("button")?.focus({ preventScroll: true });
    });
  }

  function changeWeek(
    nextWeek,
    message,
    target,
    nextSettings = replaceMealSettings(week, nextWeek, mealSettings),
  ) {
    if (
      JSON.stringify(nextWeek) === JSON.stringify(week) &&
      JSON.stringify(nextSettings) === JSON.stringify(mealSettings)
    )
      return;
    undoState = { week, mealSettings };
    const unlinked = DAYS.some((day) =>
      MEALS.some(
        (meal) =>
          nextWeek[day][meal] &&
          nextWeek[day][meal] === week[day][meal] &&
          mealSettings[slotKey({ day, meal })]?.leftoverOf &&
          !nextSettings[slotKey({ day, meal })]?.leftoverOf,
      ),
    );
    if (unlinked)
      message +=
        " Affected leftover meals now cook fresh; check their portions.";
    const added = DAYS.flatMap((day) =>
      MEALS.filter(
        (meal) =>
          nextWeek[day][meal] && nextWeek[day][meal] !== week[day][meal],
      ).map((meal) => nextWeek[day][meal]),
    );
    week = nextWeek;
    mealSettings = nextSettings;
    persistence.savePlan(selectedWeek, week, mealSettings);
    if (added.length)
      savePreferences({
        ...preferences,
        recent: [...new Set([...added.reverse(), ...preferences.recent])].slice(
          0,
          12,
        ),
      });
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
    $("#household-size").value = preferences.householdSize || "";
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
          const settings = mealSettings[slotKey(target)] || {};
          if (
            recipe &&
            (preferences.householdSize ||
              settings.servings ||
              settings.leftoverOf)
          ) {
            const servings = mealServings(
              recipe,
              settings,
              preferences.householdSize,
            );
            slot.insertBefore(
              el(
                "span",
                "slot-portions",
                `${settings.leftoverOf ? "Leftovers · " : ""}${servings} ${servings === 1 ? "serving" : "servings"}`,
              ),
              tools,
            );
          }
          slot.classList.toggle("is-leftover", !!settings.leftoverOf);
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
              moveMealSettings(
                moveMeal(week, payload.source, target),
                mealSettings,
                payload.source,
                target,
              ),
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
    $("#shopping-open").disabled = loadState !== "ready";
    $("#mobile-shopping").disabled = loadState !== "ready";
    $("#templates-open").disabled = loadState !== "ready";
    shopping?.refresh();
  }

  function renderLibrary() {
    const list = $("#recipe-list");
    list.replaceChildren();
    $("#recipe-count").textContent =
      loadState === "ready"
        ? `${recipes.length} recipe${recipes.length === 1 ? "" : "s"}`
        : loadState === "error"
          ? "Recipes unavailable"
          : "Opening the collection…";
    $("#recipe-results").textContent = "";
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
    $("#recipe-results").textContent =
      visible.length === recipes.length
        ? "All your favourites"
        : `${visible.length} of ${recipes.length} recipes`;
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
    search.placeholder = "Search by dish or ingredient…";
    search.setAttribute("aria-label", "Search recipes for this meal");
    const field = el("label", "search-field");
    field.append(search);
    const filters = el("div", "picker-filters");
    filters.setAttribute("role", "group");
    filters.setAttribute("aria-label", "Recipe shortcuts");
    let shortcut = "suggested";
    const count = el("p", "picker-count");
    count.setAttribute("role", "status");
    const list = el("div", "picker-list");
    const modes = [
      ["suggested", `For ${target.meal}`],
      ["all", "All recipes"],
      ["favourites", "★ Pinned"],
      ["recent", "Recent"],
    ];
    for (const [value, label] of modes) {
      const control = button(label, "picker-filter", () => {
        shortcut = value;
        update();
      });
      control.dataset.shortcut = value;
      filters.append(control);
    }
    function update() {
      filters
        .querySelectorAll("button")
        .forEach((control) =>
          control.setAttribute(
            "aria-pressed",
            String(control.dataset.shortcut === shortcut),
          ),
        );
      list.replaceChildren();
      // Searching always looks across the collection; meal suitability still ranks first.
      let visible = recipes.filter(
        (recipe) =>
          matchesRecipe(recipe, search.value) &&
          (shortcut !== "favourites" ||
            preferences.favourites.includes(recipe.id)) &&
          (shortcut !== "recent" || preferences.recent.includes(recipe.id)) &&
          (shortcut !== "suggested" ||
            !!search.value.trim() ||
            recipe.mealTypes.includes(target.meal)),
      );
      visible.sort((a, b) => {
        if (shortcut === "recent")
          return (
            preferences.recent.indexOf(a.id) - preferences.recent.indexOf(b.id)
          );
        return (
          Number(b.mealTypes.includes(target.meal)) -
            Number(a.mealTypes.includes(target.meal)) ||
          Number(preferences.favourites.includes(b.id)) -
            Number(preferences.favourites.includes(a.id)) ||
          a.title.localeCompare(b.title)
        );
      });
      count.textContent = `${visible.length} recipe${visible.length === 1 ? "" : "s"}${search.value.trim() ? " matching your search" : ""}`;
      if (loadState !== "ready") {
        list.append(
          el(
            "p",
            "picker-context",
            loadState === "loading"
              ? "The recipes are still loading. Try again in a moment."
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
      } else if (!visible.length) {
        list.append(
          el(
            "p",
            "picker-context",
            shortcut === "favourites"
              ? "Tap ☆ beside a recipe to pin it here."
              : shortcut === "recent"
                ? "Meals you add to your plan will appear here."
                : "No recipes found. Try another name, ingredient or All recipes.",
          ),
        );
      } else
        visible.forEach((recipe) => {
          const row = el("div", "picker-recipe-row");
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
          const text = el("span");
          text.append(
            el("strong", null, recipe.title),
            el(
              "small",
              null,
              `${recipe.mealTypes.map(titleCase).join(" / ")} · ${recipe.servings} recipe servings`,
            ),
          );
          choice.append(
            recipeIllustration(recipe, undefined, "lazy"),
            text,
            el("span", null, "+"),
          );
          row.append(
            choice,
            favouriteButton(recipe, () => {
              if (shortcut === "favourites") {
                update();
                filters.querySelector('[data-shortcut="favourites"]').focus();
              }
            }),
          );
          list.append(row);
        });
    }
    search.addEventListener("input", update);
    content.append(field, filters, count, list);
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
        source
          ? moveMealSettings(next, mealSettings, source, target)
          : replaceMealSettings(week, next, mealSettings),
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
        button("Portions & leftovers", "button button-outline", () =>
          planTools.openPortions(target, opener),
        ),
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
    mealSettings = cleanMealSettings(
      week,
      persistence.mealSettings(selectedWeek),
    );
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

  libraryToggleEl.addEventListener("click", () =>
    setLibraryExpanded(!libraryExpanded, { user: true }),
  );
  $("#recipes-close").addEventListener("click", () =>
    setLibraryExpanded(false, { user: true, goToPlan: true }),
  );
  $("#recipes-nav-link").addEventListener("click", () =>
    setLibraryExpanded(true, { user: true }),
  );
  $("#planner-nav-link").addEventListener("click", () => {
    if (stackedLayout.matches) setLibraryExpanded(false, { user: true });
  });
  window.addEventListener("hashchange", () => {
    if (window.location.hash === "#recipes")
      setLibraryExpanded(true, { user: true });
  });
  stackedLayout.addEventListener("change", (event) => {
    if (!libraryChosenByUser) setLibraryExpanded(!event.matches);
  });
  setLibraryExpanded(
    window.location.hash === "#recipes" || !stackedLayout.matches,
    { user: window.location.hash === "#recipes" },
  );

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
    week = undoState.week;
    mealSettings = undoState.mealSettings;
    undoState = null;
    persistence.savePlan(selectedWeek, week, mealSettings);
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
  $("#shopping-open").addEventListener("click", (event) =>
    shopping.open(event.currentTarget),
  );
  $("#copy-last-week").addEventListener("click", planTools.copyLastWeek);
  $("#templates-open").addEventListener("click", (event) =>
    planTools.openTemplates(event.currentTarget),
  );
  $("#household-size").addEventListener("change", (event) => {
    savePreferences({
      ...preferences,
      householdSize: event.target.value ? Number(event.target.value) : null,
    });
    renderPlanner();
    notify(
      "Household portions updated. Shopping amounts have been recalculated; individual meal overrides stay as you set them.",
    );
  });
  $("#mobile-plan").addEventListener("click", () => {
    setLibraryExpanded(false, { user: true, goToPlan: true });
  });
  $("#mobile-recipes").addEventListener("click", () => {
    setLibraryExpanded(true, { user: true });
    libraryToggleEl.focus({ preventScroll: true });
    libraryEl.scrollIntoView({ block: "start", behavior: "auto" });
  });
  $("#mobile-shopping").addEventListener("click", (event) => {
    shopping.open(event.currentTarget);
    setMobileTab("shopping");
  });
  $("#shopping-dialog").addEventListener("close", () =>
    setMobileTab(libraryExpanded ? "recipes" : "plan"),
  );
  $("#reset-storage").addEventListener("click", () => {
    persistence.reset();
    week = persistence.week(selectedWeek);
    mealSettings = {};
    preferences = persistence.preferences();
    undoState = null;
    storageChanged();
    renderPlanner();
    recipeViews.refresh();
    syncFavourites();
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

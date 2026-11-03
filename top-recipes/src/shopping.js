(() => {
  const { DAYS, MEALS, el, button, showDialog, parseLocalDate } =
    globalThis.TopRecipes;
  const round = (value) => Math.round(value * 1000) / 1000;
  const MAX_QUANTITY = 1e9;

  function parseShoppingQuantity(raw) {
    let text = String(raw)
      .trim()
      .toLowerCase()
      .replace(/½/g, " 1/2")
      .replace(/¼/g, " 1/4")
      .replace(/¾/g, " 3/4")
      .trim();
    if (/^to taste$/.test(text))
      return { quantity: 1, unit: "pack", step: 1, pantry: true };
    text = text.replace(/^half(?:\s+an?)?\b/, "0.5");
    const match = text.match(
      /^(\d+\s+\d+\/\d+|\d+\/\d+|\d+(?:\.\d+)?)\s*(.*)$/,
    );
    if (!match) return { quantity: 1, unit: "pack", step: 1, pantry: true };
    const number = match[1].split(/\s+/).reduce((sum, part) => {
      if (!part.includes("/")) return sum + Number(part);
      const [numerator, denominator] = part.split("/").map(Number);
      return sum + numerator / denominator;
    }, 0);
    if (!Number.isFinite(number) || number <= 0)
      return { quantity: 1, unit: "pack", step: 1, pantry: true };
    const remainder = match[2];
    const units = [
      [/^kg\b|^kilograms?\b/, "g", 1000, 25],
      [/^g\b|^grams?\b/, "g", 1, 25],
      [/^ml\b|^millilitres?\b|^milliliters?\b/, "ml", 1, 50],
      [/^l\b|^litres?\b|^liters?\b/, "ml", 1000, 50],
      [/^tsp\b|^teaspoons?\b/, "tsp", 1, 0.5],
      [/^tbsp\b|^tablespoons?\b/, "tbsp", 1, 0.5],
      [/^cloves?\b/, "clove", 1, 1],
      [/^sticks?\b/, "stick", 1, 1],
      [/^(?:small\s+)?handfuls?\b/, "handful", 1, 0.5],
      [/^(?:ready-rolled\s+)?sheets?\b/, "sheet", 1, 1],
      [/^pinch(?:es)?\b/, "pack", 1, 1],
    ];
    for (const [pattern, unit, factor, step] of units) {
      if (pattern.test(remainder))
        return {
          quantity: unit === "pack" ? 1 : round(number * factor),
          unit,
          step,
          pantry: unit === "pack",
        };
    }
    // A leading count remains a count: "4, about 140 g each" is four fillets.
    return { quantity: round(number), unit: "item", step: 1, pantry: false };
  }

  function shoppingName(ingredient) {
    const name = ingredient.name.replace(/\s*\(optional\)/gi, "").trim();
    const aliases = {
      egg: "Eggs",
      eggs: "Eggs",
      onion: "Onions",
      onions: "Onions",
      carrot: "Carrots",
      carrots: "Carrots",
      lemon: "Lemons",
      lemons: "Lemons",
      milk: "Milk",
      "milk or unsweetened plant milk": "Milk",
      "fresh berries": "Berries",
      "fresh or frozen berries": "Berries",
      "bay leaf": "Bay leaves",
      "bay leaves": "Bay leaves",
    };
    const base = name
      .replace(/^hot\s+/i, "")
      .replace(/^boneless,?\s*skinless\s+/i, "")
      .replace(
        /,\s*(?:finely|roughly|chopped|diced|sliced|grated|trimmed|peeled|washed|cut|crumbled|melted|divided|rinsed|juiced|half|thawed|beaten|plus)\b.*$/i,
        "",
      )
      .trim();
    return Object.hasOwn(aliases, base.toLowerCase())
      ? aliases[base.toLowerCase()]
      : base.charAt(0).toUpperCase() + base.slice(1);
  }

  function buildShoppingList(week, getRecipe) {
    const combined = new Map();
    const recipeIds = new Set();
    let mealCount = 0;
    let missingCount = 0;
    for (const day of DAYS)
      for (const meal of MEALS) {
        const id = week[day]?.[meal];
        if (!id) continue;
        mealCount++;
        const recipe = getRecipe(id);
        if (!recipe) {
          missingCount++;
          continue;
        }
        recipeIds.add(id);
        for (const ingredient of recipe.ingredients) {
          const amount = parseShoppingQuantity(ingredient.quantity);
          const name = shoppingName(ingredient);
          const key = `${encodeURIComponent(name.normalize("NFKC").toLowerCase())}|${amount.unit}`;
          const optional = /\(optional\)/i.test(ingredient.name);
          let item = combined.get(key);
          if (!item) {
            item = {
              key,
              name,
              quantity: 0,
              unit: amount.unit,
              step: amount.step,
              pantry: amount.pantry,
              optional: true,
              sources: new Set(),
              notes: new Set(),
            };
            combined.set(key, item);
          }
          item.quantity = amount.pantry
            ? 1
            : round(item.quantity + amount.quantity);
          item.optional = item.optional && optional;
          item.sources.add(recipe.title);
          item.notes.add(
            `${ingredient.quantity} ${ingredient.name.replace(/\s*\(optional\)/gi, "")}`,
          );
        }
      }
    const items = [...combined.values()]
      .map((item) => ({
        ...item,
        quantity:
          item.unit === "item" ? Math.ceil(item.quantity) : item.quantity,
        sources: [...item.sources],
        notes: [...item.notes],
      }))
      .sort(
        (a, b) => a.name.localeCompare(b.name) || a.unit.localeCompare(b.unit),
      );
    return { items, mealCount, recipeCount: recipeIds.size, missingCount };
  }

  function applyShoppingEdits(items, edits) {
    return items.map((item) => {
      const edit = Object.hasOwn(edits, item.key) ? edits[item.key] : null;
      return {
        ...item,
        baseline: item.quantity,
        quantity:
          edit?.baseline === item.quantity ? edit.quantity : item.quantity,
        selected: edit ? edit.selected : true,
      };
    });
  }

  function formatShoppingQuantity(item) {
    const number = new Intl.NumberFormat(undefined, {
      maximumFractionDigits: 3,
    }).format(item.quantity);
    const plurals = {
      item: "items",
      clove: "cloves",
      stick: "sticks",
      handful: "handfuls",
      sheet: "sheets",
      pack: "packs",
    };
    const unit =
      item.quantity === 1 ? item.unit : plurals[item.unit] || item.unit;
    return `${number} ${unit}`;
  }

  function createShoppingList({
    getWeek,
    getWeekKey,
    getRecipe,
    persistence,
    storageChanged,
    openCapture,
  }) {
    const dialogEl = document.querySelector("#shopping-dialog");
    const listEl = document.querySelector("#shopping-items");
    const summaryEl = document.querySelector("#shopping-summary");
    const captureEl = document.querySelector("#shopping-screenshot");
    const statusEl = document.querySelector("#shopping-status");
    let items = [];
    let edits = {};
    let details = { mealCount: 0, recipeCount: 0, missingCount: 0 };

    function remember(item) {
      edits[item.key] = {
        baseline: item.baseline,
        quantity: item.quantity,
        selected: item.selected,
      };
    }

    function persist() {
      persistence.saveShoppingWeek(getWeekKey(), edits);
      storageChanged();
    }

    function save(item) {
      remember(item);
      persist();
    }

    function summary() {
      const selected = items.filter(
        (item) => item.selected && item.quantity > 0,
      ).length;
      summaryEl.textContent = `${selected} of ${items.length} items selected · ${details.mealCount} planned meal${details.mealCount === 1 ? "" : "s"}`;
      captureEl.disabled = selected === 0;
    }

    function renderRow(item) {
      const rowEl = el("div", "shopping-item");
      rowEl.dataset.shoppingKey = item.key;
      const labelEl = el("label", "shopping-check");
      const checkEl = el("input");
      checkEl.type = "checkbox";
      checkEl.checked = item.selected;
      checkEl.setAttribute(
        "aria-label",
        `Include ${item.name} in shopping screenshot`,
      );
      const copyEl = el("span", "shopping-copy");
      copyEl.append(el("strong", null, item.name));
      if (item.optional)
        copyEl.append(el("small", "shopping-optional", "Optional"));
      copyEl.append(el("small", "shopping-source", item.sources.join(" · ")));
      const notesEl = el("details", "shopping-notes");
      notesEl.append(el("summary", null, "Recipe amounts"));
      item.notes.forEach((note) => notesEl.append(el("p", null, note)));
      labelEl.append(checkEl, copyEl);
      const controlsEl = el("div", "quantity-controls");
      const inputEl = el("input", "quantity-input");
      inputEl.type = "number";
      inputEl.min = "0";
      inputEl.max = String(MAX_QUANTITY);
      inputEl.step = "any";
      inputEl.inputMode = "decimal";
      inputEl.value = item.quantity;
      inputEl.setAttribute(
        "aria-label",
        `${item.name} quantity in ${item.unit === "item" ? "items" : item.unit}`,
      );
      const update = () => {
        inputEl.value = item.quantity;
        minusEl.disabled = item.quantity <= 0;
        plusEl.disabled = item.quantity >= MAX_QUANTITY;
        rowEl.classList.toggle(
          "excluded",
          !item.selected || item.quantity === 0,
        );
        save(item);
        summary();
      };
      const change = (value) => {
        item.quantity = round(Math.min(MAX_QUANTITY, Math.max(0, value)));
        update();
        statusEl.textContent = `${item.name}: ${formatShoppingQuantity(item)}.`;
      };
      const minusEl = button(
        "−",
        "quantity-button",
        () => change(item.quantity - item.step),
        `Decrease ${item.name} quantity`,
      );
      const plusEl = button(
        "+",
        "quantity-button",
        () => change(item.quantity + item.step),
        `Increase ${item.name} quantity`,
      );
      const unitEl = el(
        "span",
        "quantity-unit",
        item.unit === "item" ? "items" : item.unit,
      );
      controlsEl.append(minusEl, inputEl, plusEl, unitEl);
      inputEl.addEventListener("change", () => {
        const value = Number(inputEl.value);
        if (
          inputEl.value.trim() &&
          Number.isFinite(value) &&
          value >= 0 &&
          value <= MAX_QUANTITY
        )
          change(value);
        else {
          inputEl.value = item.quantity;
          statusEl.textContent = "Enter a quantity from 0 to 1,000,000,000.";
        }
      });
      checkEl.addEventListener("change", () => {
        item.selected = checkEl.checked;
        update();
      });
      minusEl.disabled = item.quantity <= 0;
      plusEl.disabled = item.quantity >= MAX_QUANTITY;
      rowEl.classList.toggle("excluded", !item.selected || item.quantity === 0);
      rowEl.append(labelEl, controlsEl, notesEl);
      return rowEl;
    }

    function refresh() {
      if (!dialogEl.open) return;
      details = buildShoppingList(getWeek(), getRecipe);
      edits = persistence.shoppingWeek(getWeekKey());
      items = applyShoppingEdits(details.items, edits);
      const date = parseLocalDate(getWeekKey());
      document.querySelector("#shopping-week").textContent =
        `Week of ${date.toLocaleDateString(undefined, { day: "numeric", month: "long", year: "numeric" })}`;
      const warningEl = document.querySelector("#shopping-warning");
      warningEl.hidden = details.missingCount === 0;
      warningEl.textContent = `Ingredients are unavailable for ${details.missingCount} planned meal${details.missingCount === 1 ? "" : "s"}. Change those recipes in your plan to complete the list.`;
      listEl.replaceChildren(...items.map(renderRow));
      if (!items.length)
        listEl.append(
          el(
            "p",
            "empty-message",
            details.mealCount
              ? "No ingredients are available for these meals yet."
              : "Plan a few meals first. Their ingredients will appear here automatically.",
          ),
        );
      document.querySelector("#shopping-bulk-actions").hidden =
        items.length === 0;
      statusEl.textContent = "";
      summary();
    }

    document
      .querySelector("#shopping-select-all")
      .addEventListener("click", () => {
        items.forEach((item) => {
          item.selected = true;
          if (!item.quantity) item.quantity = item.baseline;
          remember(item);
        });
        persist();
        refresh();
      });
    document
      .querySelector("#shopping-clear-selection")
      .addEventListener("click", () => {
        items.forEach((item) => {
          item.selected = false;
          remember(item);
        });
        persist();
        refresh();
      });
    document.querySelector("#shopping-reset").addEventListener("click", () => {
      persistence.saveShoppingWeek(getWeekKey(), {});
      storageChanged();
      refresh();
      statusEl.textContent = "Shopping list reset to the recipe amounts.";
    });
    captureEl.addEventListener("click", () => openCapture(captureEl));
    return {
      open(trigger) {
        showDialog(dialogEl, trigger);
        refresh();
        dialogEl.scrollTop = 0;
      },
      refresh,
      snapshot() {
        return {
          items: items
            .filter((item) => item.selected && item.quantity > 0)
            .map((item) => ({ ...item })),
          missingCount: details.missingCount,
        };
      },
    };
  }

  Object.assign((globalThis.TopRecipes ||= {}), {
    MAX_QUANTITY,
    parseShoppingQuantity,
    shoppingName,
    buildShoppingList,
    applyShoppingEdits,
    formatShoppingQuantity,
    createShoppingList,
  });
})();

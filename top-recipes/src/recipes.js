(() => {
  const {
    el,
    button,
    formatMinutes,
    showDialog,
    titleCase,
    validRecipeImagePath,
  } = globalThis.TopRecipes;

  const placeholderImage = () =>
    new URL("./assets/recipe-placeholder.svg", document.baseURI).href;
  const recipeImage = (recipe) =>
    validRecipeImagePath(recipe.image)
      ? new URL(`./${recipe.image}`, document.baseURI).href
      : placeholderImage();

  function recipeIllustration(recipe, className, loading = "eager") {
    const image = el("img", className);
    image.alt = "";
    image.loading = loading;
    image.decoding = "async";
    image.addEventListener(
      "error",
      () => {
        image.src = placeholderImage();
      },
      { once: true },
    );
    image.src = recipeImage(recipe);
    return image;
  }

  function matchesRecipe(recipe, query, meal = "all") {
    const text = [
      recipe.title,
      recipe.description,
      ...recipe.tags,
      ...recipe.ingredients.map((ingredient) => ingredient.name),
    ]
      .join(" ")
      .toLocaleLowerCase();
    return (
      (meal === "all" || recipe.mealTypes.includes(meal)) &&
      query
        .toLocaleLowerCase()
        .trim()
        .split(/\s+/)
        .every((word) => text.includes(word))
    );
  }

  function validateRecipeData(data) {
    if (!Array.isArray(data) || !data.length)
      throw new Error("The recipe collection is empty.");
    const ids = new Set();
    for (const recipe of data) {
      if (
        !recipe ||
        typeof recipe.id !== "string" ||
        ids.has(recipe.id) ||
        typeof recipe.title !== "string" ||
        typeof recipe.description !== "string" ||
        (recipe.image !== undefined && !validRecipeImagePath(recipe.image)) ||
        !Array.isArray(recipe.mealTypes) ||
        !recipe.mealTypes.length ||
        recipe.mealTypes.some(
          (meal) => !["breakfast", "lunch", "dinner"].includes(meal),
        ) ||
        !Array.isArray(recipe.tags) ||
        recipe.tags.some((tag) => typeof tag !== "string") ||
        !Array.isArray(recipe.ingredients) ||
        !recipe.ingredients.length ||
        recipe.ingredients.some(
          (ingredient) =>
            !ingredient ||
            ["id", "quantity", "name", "group"].some(
              (field) => typeof ingredient[field] !== "string",
            ),
        ) ||
        !Array.isArray(recipe.method) ||
        !recipe.method.length ||
        recipe.method.some((step) => typeof step !== "string") ||
        !Array.isArray(recipe.notes) ||
        recipe.notes.some((note) => typeof note !== "string") ||
        !Number.isSafeInteger(recipe.servings) ||
        recipe.servings < 1 ||
        ["prepMinutes", "cookMinutes", "waitMinutes"].some(
          (field) => !Number.isSafeInteger(recipe[field]) || recipe[field] < 0,
        )
      ) {
        throw new Error("The recipe collection could not be read.");
      }
      ids.add(recipe.id);
    }
    return data;
  }

  function createRecipeViews({
    persistence,
    openPlacement,
    makeDraggable,
    notify,
    storageChanged,
    favouriteButton,
    cooking,
  }) {
    const dialog = document.querySelector("#recipe-dialog");
    const container = document.querySelector("#recipe-detail");
    let activeRecipe = null;
    let activeOpener = null;

    function card(recipe) {
      const article = el("article", "recipe-card");
      const main = el("div", "recipe-card-main");
      const image = recipeIllustration(recipe, "recipe-illustration", "lazy");
      image.width = 86;
      image.height = 92;
      const copy = el("div", "recipe-card-copy");
      const title = button(recipe.title, "recipe-title", () =>
        open(recipe, title),
      );
      const meta = el(
        "p",
        "recipe-meta",
        `${recipe.servings} serving${recipe.servings === 1 ? "" : "s"} · ${formatMinutes(recipe.prepMinutes + recipe.cookMinutes)} active`,
      );
      if (recipe.waitMinutes)
        meta.append(
          el(
            "span",
            "wait-note",
            `${formatMinutes(recipe.waitMinutes)} ${recipe.tags.includes("no-cook") ? "overnight chill" : "rest / wait"}`,
          ),
        );
      copy.append(
        el("span", "meal-badge", recipe.mealTypes.map(titleCase).join(" / ")),
        title,
        meta,
      );
      main.append(image, copy);
      const bottom = el("div", "recipe-card-bottom");
      const view = button(
        "Recipe & ingredients ↗",
        "view-recipe",
        () => open(recipe, view),
        `View ${recipe.title} recipe and ingredients`,
      );
      const handle = button(
        "⠿",
        "drag-handle",
        () => openPlacement(recipe.id, handle),
        `Drag ${recipe.title}, or activate to choose a meal slot`,
      );
      makeDraggable(handle, { recipeId: recipe.id });
      const add = button(
        "+ Add",
        "add-recipe",
        () => openPlacement(recipe.id, add),
        `Add ${recipe.title} to your week`,
      );
      bottom.append(view, handle, add);
      if (favouriteButton) bottom.insertBefore(favouriteButton(recipe), handle);
      article.append(
        main,
        el("p", "recipe-card-description", recipe.description),
        bottom,
      );
      return article;
    }

    function open(recipe, opener) {
      activeRecipe = recipe;
      activeOpener = opener;
      renderDetails();
      showDialog(dialog, opener);
      dialog.scrollTop = 0;
    }

    function renderDetails() {
      const recipe = activeRecipe;
      container.replaceChildren();
      const header = el("div", "detail-header");
      const image = recipeIllustration(recipe);
      const intro = el("div");
      const title = el("h2", null, recipe.title);
      title.id = "detail-title";
      intro.append(
        el("span", "meal-badge", recipe.mealTypes.map(titleCase).join(" / ")),
        title,
      );
      header.append(image, intro);
      const timings = el("div", "detail-timings");
      timings.append(
        el(
          "span",
          null,
          `${recipe.servings} serving${recipe.servings === 1 ? "" : "s"}`,
        ),
        el("span", null, `Prep ${formatMinutes(recipe.prepMinutes)}`),
        el("span", null, `Cook ${formatMinutes(recipe.cookMinutes)}`),
      );
      if (recipe.waitMinutes)
        timings.append(
          el("span", null, `Wait ${formatMinutes(recipe.waitMinutes)}`),
        );
      timings.append(
        el(
          "span",
          null,
          `Total ${formatMinutes(recipe.prepMinutes + recipe.cookMinutes + recipe.waitMinutes)}`,
        ),
      );
      const actions = el("div", "detail-actions");
      const add = button("+ Add to week", "button button-primary", () => {
        dialog.close();
        openPlacement(recipe.id, activeOpener);
      });
      const copy = button(
        "Copy ingredients",
        "button button-outline",
        async () => {
          const checklist = [
            `${recipe.title} — ${recipe.servings} serving${recipe.servings === 1 ? "" : "s"}`,
            "",
            ...recipe.ingredients.map(
              (ingredient) =>
                `- [${persistence.isChecked(recipe.id, ingredient.id) ? "x" : " "}] ${ingredient.quantity} ${ingredient.name}`,
            ),
          ].join("\n");
          try {
            if (!navigator.clipboard?.writeText)
              throw new Error("Clipboard unavailable");
            await navigator.clipboard.writeText(checklist);
            notify("Ingredient checklist copied.");
          } catch {
            fallback.hidden = false;
            textarea.value = checklist;
            textarea.focus();
            textarea.select();
          }
        },
      );
      actions.append(add, copy);
      if (cooking) {
        const start = button("Start cooking →", "button button-outline", () =>
          cooking.open(recipe, start),
        );
        start.id = "recipe-start-cooking";
        actions.prepend(start);
      }
      const fallback = el("div", "copy-fallback");
      fallback.hidden = true;
      const label = el(
        "label",
        null,
        "Select and copy your ingredient checklist:",
      );
      const textarea = el("textarea");
      textarea.readOnly = true;
      label.append(textarea);
      fallback.append(label);
      container.append(
        header,
        timings,
        el("p", "detail-description", recipe.description),
        actions,
        fallback,
        el("h3", "detail-section-title", "Ingredients — what to buy"),
        el(
          "p",
          "detail-help",
          `Quantities make ${recipe.servings} serving${recipe.servings === 1 ? "" : "s"}. Tick anything you already have or have bought. Checks are saved for this recipe.`,
        ),
      );
      const groups = new Map();
      for (const ingredient of recipe.ingredients) {
        if (!groups.has(ingredient.group)) {
          const fieldset = el("fieldset", "ingredient-group");
          fieldset.append(el("legend", null, ingredient.group));
          groups.set(ingredient.group, fieldset);
          container.append(fieldset);
        }
        const row = el("label", "ingredient-row");
        const check = el("input");
        check.type = "checkbox";
        check.checked = persistence.isChecked(recipe.id, ingredient.id);
        check.dataset.ingredient = ingredient.id;
        check.addEventListener("change", () => {
          persistence.check(recipe.id, ingredient.id, check.checked);
          storageChanged();
        });
        const text = el("span");
        text.append(
          el("span", "ingredient-quantity", ingredient.quantity),
          el("span", "ingredient-name", ingredient.name),
        );
        row.append(check, text);
        groups.get(ingredient.group).append(row);
      }
      container.append(
        button("Reset ingredient checks", "text-button", () => {
          persistence.resetChecks(recipe.id);
          container
            .querySelectorAll('input[type="checkbox"]')
            .forEach((input) => {
              input.checked = false;
            });
          storageChanged();
          notify("Ingredient checks reset.");
        }),
        el("h3", "detail-section-title", "Make it"),
      );
      const method = el("ol", "method-list");
      recipe.method.forEach((step) => method.append(el("li", null, step)));
      container.append(method);
      if (recipe.notes.length) {
        container.append(el("h3", "detail-section-title", "Kitchen notes"));
        const notes = el("ul", "recipe-notes");
        recipe.notes.forEach((note) => notes.append(el("li", null, note)));
        container.append(notes);
      }
    }
    return {
      card,
      open,
      refresh: () => {
        if (dialog.open && activeRecipe) renderDetails();
      },
    };
  }

  Object.assign((globalThis.TopRecipes ||= {}), {
    recipeImage,
    recipeIllustration,
    matchesRecipe,
    validateRecipeData,
    createRecipeViews,
  });
})();

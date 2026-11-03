(() => {
  const {
    el,
    button,
    clone,
    weekOffset,
    slotKey,
    slotFromKey,
    slotLabel,
    slotIndex,
    planSlots,
    cleanMealSettings,
    mealServings,
    cookingBatches,
  } = globalThis.TopRecipes;

  function createPlanTools({
    getWeek,
    getSettings,
    getWeekKey,
    getRecipe,
    getPreferences,
    persistence,
    changeWeek,
    pickerShell,
    closePicker,
    notify,
    storageChanged,
  }) {
    function copyLastWeek() {
      const key = weekOffset(getWeekKey(), -1);
      const previous = persistence.week(key);
      if (!planSlots().some(({ day, meal }) => previous[day][meal])) {
        notify("Last week is empty. Choose another week or make a new plan.");
        return;
      }
      changeWeek(
        previous,
        "Last week copied. You can undo this change.",
        null,
        cleanMealSettings(previous, persistence.mealSettings(key)),
      );
    }

    function openTemplates(opener) {
      const content = pickerShell("A good week, worth repeating.", opener);
      content.append(
        el(
          "p",
          "picker-context",
          "Save meals, portions and leftover links as a reusable week. Applying a template replaces this week’s meals; Undo brings them back. Shopping edits stay with their original week.",
        ),
      );
      const form = el("form", "template-form");
      const label = el("label", null, "Name this week");
      const input = el("input");
      input.name = "template-name";
      input.placeholder = "e.g. Easy family favourites";
      input.maxLength = 80;
      input.required = true;
      label.append(input);
      const save = button("Save this week", "button button-primary");
      save.type = "submit";
      save.disabled = !planSlots().some(
        ({ day, meal }) => getWeek()[day][meal],
      );
      form.append(label, save);
      const status = el("p", "template-status");
      status.setAttribute("role", "status");
      const list = el("div", "template-list");
      function render() {
        list.replaceChildren(el("h3", null, "Your saved weeks"));
        const templates = persistence.templates();
        save.disabled =
          !planSlots().some(({ day, meal }) => getWeek()[day][meal]) ||
          templates.length >= 50;
        if (templates.length >= 50)
          status.textContent =
            "You have 50 saved weeks. Delete one to save another.";
        if (!templates.length)
          list.append(
            el(
              "p",
              "picker-context",
              "Your saved weeks will be kept here, in this browser.",
            ),
          );
        for (const template of templates) {
          const row = el("div", "template-row");
          const copy = el("div");
          const count = planSlots().filter(
            ({ day, meal }) => template.week[day][meal],
          ).length;
          copy.append(
            el("strong", null, template.title),
            el("small", null, `${count} planned meals`),
          );
          const apply = button(
            "Use week",
            "button button-outline",
            () => {
              closePicker();
              changeWeek(
                clone(template.week),
                `“${template.title}” applied. You can undo this change.`,
                null,
                cleanMealSettings(template.week, template.settings),
              );
            },
            `Use saved week ${template.title}`,
          );
          const remove = button(
            "Delete",
            "text-button",
            () => {
              persistence.saveTemplates(
                persistence
                  .templates()
                  .filter((entry) => entry.id !== template.id),
              );
              storageChanged();
              save.disabled = !planSlots().some(
                ({ day, meal }) => getWeek()[day][meal],
              );
              render();
              status.textContent = `“${template.title}” deleted.`;
              input.focus();
            },
            `Delete saved week ${template.title}`,
          );
          row.append(copy, apply, remove);
          list.append(row);
        }
      }
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        const title = input.value.trim();
        const templates = persistence.templates();
        if (!title || templates.length >= 50 || save.disabled) return;
        templates.push({
          id: `template-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
          title,
          week: clone(getWeek()),
          settings: clone(getSettings()),
        });
        persistence.saveTemplates(templates);
        storageChanged();
        input.value = "";
        render();
        status.textContent = `“${title}” saved.`;
      });
      content.append(form, status, list);
      render();
    }

    function openPortions(target, opener) {
      const recipe = getRecipe(getWeek()[target.day][target.meal]);
      if (!recipe) return;
      const key = slotKey(target);
      const current = getSettings()[key] || {};
      const household = getPreferences().householdSize;
      const content = pickerShell(`Portions for ${slotLabel(target)}`, opener);
      content.append(el("p", "picker-context", recipe.title));
      const form = el("form", "portion-form");
      const defaultLabel = el("label", "default-portions");
      const useDefault = el("input");
      useDefault.type = "checkbox";
      useDefault.name = "use-default";
      useDefault.checked = !current.servings;
      defaultLabel.append(
        useDefault,
        el(
          "span",
          null,
          household
            ? `Use household size (${household} ${household === 1 ? "person" : "people"})`
            : `Use recipe servings (${recipe.servings})`,
        ),
      );
      const servingLabel = el("label", null, "Servings for this meal");
      const servings = el("input");
      servings.type = "number";
      servings.name = "servings";
      servings.min = "1";
      servings.max = "100";
      servings.step = "1";
      servings.value = mealServings(recipe, current, household);
      servings.disabled = useDefault.checked;
      servingLabel.append(servings);
      const sourceLabel = el("label", null, "Cook fresh or use leftovers");
      const source = el("select");
      source.name = "leftover-source";
      const fresh = el("option", null, "Cook fresh");
      fresh.value = "";
      source.append(fresh);
      for (const slot of planSlots()) {
        const candidate = slotKey(slot);
        if (
          slotIndex(candidate) >= slotIndex(key) ||
          getWeek()[slot.day][slot.meal] !== recipe.id ||
          getSettings()[candidate]?.leftoverOf
        )
          continue;
        const option = el("option", null, `Leftovers from ${slotLabel(slot)}`);
        option.value = candidate;
        source.append(option);
      }
      source.value = current.leftoverOf || "";
      sourceLabel.append(source);
      const help = el("p", "portion-help");
      const warning = el(
        "p",
        "picker-context",
        "Leftovers can link to an earlier fresh cooking of this recipe. Shopping adds all linked servings to that cooking batch. Store and reheat food safely for your recipe.",
      );
      const nextSettings = () => {
        const settings = clone(getSettings());
        settings[key] = {};
        if (!useDefault.checked)
          settings[key].servings = Number(servings.value);
        if (source.value) settings[key].leftoverOf = source.value;
        // A source cannot itself become leftovers while other meals depend on it.
        if (source.value)
          for (const value of Object.values(settings))
            if (value.leftoverOf === key) value.leftoverOf = source.value;
        return cleanMealSettings(getWeek(), settings);
      };
      function preview() {
        servings.disabled = useDefault.checked;
        if (useDefault.checked) servings.value = household || recipe.servings;
        const batchKey = source.value || key;
        const batch = cookingBatches(
          getWeek(),
          getRecipe,
          nextSettings(),
          household,
        ).find((entry) => entry.key === batchKey);
        help.textContent = batch
          ? `Shopping will include ${batch.servings} servings cooked for ${slotLabel(slotFromKey(batchKey))}${batch.meals > 1 ? `, covering ${batch.meals} meals including leftovers` : ""}.`
          : "";
      }
      [useDefault, servings, source].forEach((control) =>
        control.addEventListener("change", preview),
      );
      servings.addEventListener("input", preview);
      const submit = button("Save meal settings", "button button-primary");
      submit.type = "submit";
      form.append(
        defaultLabel,
        servingLabel,
        sourceLabel,
        help,
        warning,
        submit,
      );
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (
          !useDefault.checked &&
          (!Number.isInteger(Number(servings.value)) ||
            Number(servings.value) < 1 ||
            Number(servings.value) > 100)
        )
          return;
        const settings = nextSettings();
        closePicker();
        changeWeek(
          clone(getWeek()),
          `Meal settings saved for ${slotLabel(target)}.`,
          target,
          settings,
        );
      });
      content.append(form);
      preview();
    }
    return { copyLastWeek, openTemplates, openPortions };
  }

  Object.assign((globalThis.TopRecipes ||= {}), { createPlanTools });
})();

(() => {
  const DAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
  ];
  const MEALS = ["breakfast", "lunch", "dinner"];
  const titleCase = (value) => value.charAt(0).toUpperCase() + value.slice(1);
  const emptyWeek = () =>
    Object.fromEntries(
      DAYS.map((day) => [
        day,
        Object.fromEntries(MEALS.map((meal) => [meal, null])),
      ]),
    );
  const clone = (value) => JSON.parse(JSON.stringify(value));

  function parseLocalDate(key) {
    if (typeof key !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(key))
      throw new Error("Invalid date");
    const [year, month, day] = key.split("-").map(Number);
    const date = new Date(0);
    date.setFullYear(year, month - 1, day);
    date.setHours(12, 0, 0, 0);
    if (
      date.getFullYear() !== year ||
      date.getMonth() !== month - 1 ||
      date.getDate() !== day
    )
      throw new Error("Invalid date");
    return date;
  }

  function dateKey(date) {
    return `${String(date.getFullYear()).padStart(4, "0")}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
  }

  function mondayKey(input = new Date()) {
    const date =
      typeof input === "string" ? parseLocalDate(input) : new Date(input);
    date.setHours(12, 0, 0, 0);
    date.setDate(date.getDate() - ((date.getDay() + 6) % 7));
    return dateKey(date);
  }

  function weekOffset(key, offset) {
    const date = parseLocalDate(key);
    date.setDate(date.getDate() + offset * 7);
    return dateKey(date);
  }

  function checkSlot(slot) {
    if (!slot || !DAYS.includes(slot.day) || !MEALS.includes(slot.meal))
      throw new Error("Invalid meal slot");
  }

  function assignMeal(week, target, recipeId) {
    checkSlot(target);
    if (
      recipeId !== null &&
      (typeof recipeId !== "string" ||
        !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(recipeId))
    )
      throw new Error("Invalid recipe ID");
    const next = clone(week);
    next[target.day][target.meal] = recipeId;
    return next;
  }

  function moveMeal(week, source, target) {
    checkSlot(source);
    checkSlot(target);
    const next = clone(week);
    if (source.day === target.day && source.meal === target.meal) return next;
    [next[source.day][source.meal], next[target.day][target.meal]] = [
      next[target.day][target.meal],
      next[source.day][source.meal],
    ];
    return next;
  }

  const slotLabel = (slot) => `${titleCase(slot.day)} ${slot.meal}`;

  const slotKey = (slot) => `${slot.day}-${slot.meal}`;
  const planSlots = () =>
    DAYS.flatMap((day) => MEALS.map((meal) => ({ day, meal })));
  const slotFromKey = (key) =>
    planSlots().find((slot) => slotKey(slot) === key);
  const slotIndex = (key) =>
    planSlots().findIndex((slot) => slotKey(slot) === key);

  // Slot IDs stay strings in saved weeks. Portions and leftover links live alongside them.
  function cleanMealSettings(week, settings = {}) {
    const next = {};
    for (const slot of planSlots()) {
      const key = slotKey(slot);
      const value = settings[key];
      if (!week[slot.day][slot.meal] || !value) continue;
      const entry = {};
      if (
        Number.isInteger(value.servings) &&
        value.servings >= 1 &&
        value.servings <= 100
      )
        entry.servings = value.servings;
      const source = slotFromKey(value.leftoverOf);
      if (
        source &&
        slotIndex(value.leftoverOf) < slotIndex(key) &&
        week[source.day][source.meal] === week[slot.day][slot.meal] &&
        !settings[value.leftoverOf]?.leftoverOf
      )
        entry.leftoverOf = value.leftoverOf;
      if (Object.keys(entry).length) next[key] = entry;
    }
    return next;
  }

  function moveMealSettings(week, settings, source, target) {
    const from = slotKey(source);
    const to = slotKey(target);
    if (from === to) return clone(settings);
    const remap = (key) => (key === from ? to : key === to ? from : key);
    const next = {};
    for (const [key, value] of Object.entries(settings)) {
      next[remap(key)] = { ...value };
      if (value.leftoverOf)
        next[remap(key)].leftoverOf = remap(value.leftoverOf);
    }
    return cleanMealSettings(week, next);
  }

  function replaceMealSettings(previousWeek, nextWeek, settings) {
    const next = clone(settings);
    for (const slot of planSlots())
      if (previousWeek[slot.day][slot.meal] !== nextWeek[slot.day][slot.meal])
        delete next[slotKey(slot)];
    return cleanMealSettings(nextWeek, next);
  }

  function mealServings(recipe, settings = {}, householdSize = null) {
    return settings.servings || householdSize || recipe?.servings || 1;
  }

  function cookingBatches(
    week,
    getRecipe,
    settings = {},
    householdSize = null,
  ) {
    const clean = cleanMealSettings(week, settings);
    const batches = new Map();
    for (const slot of planSlots()) {
      const id = week[slot.day][slot.meal];
      if (!id) continue;
      const recipe = getRecipe(id);
      if (!recipe) continue;
      const key = slotKey(slot);
      const source = clean[key]?.leftoverOf || key;
      if (!batches.has(source))
        batches.set(source, { key: source, recipe, servings: 0, meals: 0 });
      const batch = batches.get(source);
      batch.servings += mealServings(recipe, clean[key], householdSize);
      batch.meals++;
    }
    return [...batches.values()].map((batch) => ({
      ...batch,
      factor: batch.servings / (batch.recipe.servings || 1),
    }));
  }

  Object.assign((globalThis.TopRecipes ||= {}), {
    DAYS,
    MEALS,
    titleCase,
    emptyWeek,
    clone,
    parseLocalDate,
    dateKey,
    mondayKey,
    weekOffset,
    assignMeal,
    moveMeal,
    slotLabel,
    slotKey,
    slotFromKey,
    slotIndex,
    planSlots,
    cleanMealSettings,
    moveMealSettings,
    replaceMealSettings,
    mealServings,
    cookingBatches,
  });
})();

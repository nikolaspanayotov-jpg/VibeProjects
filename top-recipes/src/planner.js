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
  });
})();

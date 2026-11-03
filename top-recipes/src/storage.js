(() => {
  const { DAYS, MEALS, emptyWeek, mondayKey, clone, slotFromKey } =
    globalThis.TopRecipes;

  const PLAN_KEY = "top-recipes:planner:v1";
  const CHECKS_KEY = "top-recipes:ingredients:v1";
  const object = (value) =>
    value !== null && typeof value === "object" && !Array.isArray(value);
  const slug = (value) =>
    typeof value === "string" && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value);

  const validWeek = (week) =>
    object(week) &&
    Object.keys(week).length === DAYS.length &&
    DAYS.every(
      (day) =>
        object(week[day]) &&
        Object.keys(week[day]).length === MEALS.length &&
        MEALS.every(
          (meal) => week[day][meal] === null || slug(week[day][meal]),
        ),
    );
  const validSettings = (settings) =>
    object(settings) &&
    Object.entries(settings).every(
      ([key, value]) =>
        slotFromKey(key) &&
        object(value) &&
        (value.servings === undefined ||
          (Number.isInteger(value.servings) &&
            value.servings >= 1 &&
            value.servings <= 100)) &&
        (value.leftoverOf === undefined || !!slotFromKey(value.leftoverOf)),
    );
  const defaultPreferences = () => ({
    householdSize: null,
    favourites: [],
    recent: [],
  });
  const validPreferences = (value) =>
    object(value) &&
    (value.householdSize === null ||
      (Number.isInteger(value.householdSize) &&
        value.householdSize >= 1 &&
        value.householdSize <= 24)) &&
    [value.favourites, value.recent].every(
      (ids) =>
        Array.isArray(ids) &&
        ids.length <= 1000 &&
        ids.every(slug) &&
        new Set(ids).size === ids.length,
    );
  const validTemplates = (value) =>
    Array.isArray(value) &&
    value.length <= 50 &&
    new Set(value.map((template) => template?.id)).size === value.length &&
    value.every(
      (template) =>
        object(template) &&
        slug(template.id) &&
        typeof template.title === "string" &&
        template.title.trim().length > 0 &&
        template.title.length <= 80 &&
        validWeek(template.week) &&
        validSettings(template.settings),
    );
  function validWeeksOf(value, validate) {
    return (
      object(value) &&
      Object.entries(value).every(([key, entry]) => {
        try {
          return mondayKey(key) === key && validate(entry);
        } catch {
          return false;
        }
      })
    );
  }

  function validPlanner(value) {
    if (!object(value) || value.schemaVersion !== 1 || !object(value.weeks))
      return false;
    if (value.preferences !== undefined && !validPreferences(value.preferences))
      return false;
    if (
      value.mealSettings !== undefined &&
      !validWeeksOf(value.mealSettings, validSettings)
    )
      return false;
    if (value.templates !== undefined && !validTemplates(value.templates))
      return false;
    if (
      value.shoppingWeeks !== undefined &&
      (!object(value.shoppingWeeks) ||
        !Object.entries(value.shoppingWeeks).every(([key, edits]) => {
          try {
            if (mondayKey(key) !== key) return false;
          } catch {
            return false;
          }
          return validShoppingEdits(edits);
        }))
    )
      return false;
    return validWeeksOf(value.weeks, validWeek);
  }

  function validShoppingEdits(edits) {
    return (
      object(edits) &&
      Object.entries(edits).every(
        ([key, edit]) =>
          key.length > 0 &&
          key.length <= 1000 &&
          key.includes("|") &&
          object(edit) &&
          typeof edit.selected === "boolean" &&
          (edit.bought === undefined || typeof edit.bought === "boolean") &&
          Number.isFinite(edit.quantity) &&
          edit.quantity >= 0 &&
          edit.quantity <= 1e9 &&
          Number.isFinite(edit.baseline) &&
          edit.baseline > 0 &&
          edit.baseline <= 1e9,
      )
    );
  }

  function validChecks(value) {
    return (
      object(value) &&
      value.schemaVersion === 1 &&
      object(value.recipes) &&
      Object.entries(value.recipes).every(
        ([id, checks]) =>
          slug(id) &&
          object(checks) &&
          Object.entries(checks).every(
            ([ingredient, checked]) =>
              slug(ingredient) && typeof checked === "boolean",
          ),
      )
    );
  }

  function createPersistence(storage) {
    let planner = { schemaVersion: 1, weeks: {} };
    let checks = { schemaVersion: 1, recipes: {} };
    let issue = storage ? null : "unavailable";
    try {
      if (storage) {
        const planRaw = storage.getItem(PLAN_KEY);
        const checksRaw = storage.getItem(CHECKS_KEY);
        const planValue = planRaw === null ? planner : JSON.parse(planRaw);
        const checksValue = checksRaw === null ? checks : JSON.parse(checksRaw);
        if (!validPlanner(planValue) || !validChecks(checksValue))
          issue = "corrupt";
        else {
          planner = planValue;
          checks = checksValue;
        }
      }
    } catch (error) {
      issue = error instanceof SyntaxError ? "corrupt" : "unavailable";
    }

    const write = (key, value) => {
      if (issue === "corrupt") return;
      try {
        if (!storage) throw new Error("Storage unavailable");
        storage.setItem(key, JSON.stringify(value));
      } catch {
        issue = "unavailable";
      }
    };
    return {
      get issue() {
        return issue;
      },
      week(key) {
        return clone(planner.weeks[key] || emptyWeek());
      },
      saveWeek(key, week) {
        planner.weeks[key] = clone(week);
        write(PLAN_KEY, planner);
      },
      mealSettings(key) {
        return clone(planner.mealSettings?.[key] || {});
      },
      savePlan(key, week, settings) {
        if (!validWeek(week) || !validSettings(settings))
          throw new Error("Invalid plan");
        planner.weeks[key] = clone(week);
        (planner.mealSettings ||= {})[key] = clone(settings);
        write(PLAN_KEY, planner);
      },
      preferences() {
        return clone(planner.preferences || defaultPreferences());
      },
      savePreferences(preferences) {
        if (!validPreferences(preferences))
          throw new Error("Invalid preferences");
        planner.preferences = clone(preferences);
        write(PLAN_KEY, planner);
      },
      templates() {
        return clone(planner.templates || []);
      },
      saveTemplates(templates) {
        if (!validTemplates(templates)) throw new Error("Invalid templates");
        planner.templates = clone(templates);
        write(PLAN_KEY, planner);
      },
      shoppingWeek(key) {
        return clone(planner.shoppingWeeks?.[key] || {});
      },
      saveShoppingWeek(key, edits) {
        if (!validShoppingEdits(edits))
          throw new Error("Invalid shopping list edits");
        if (!planner.shoppingWeeks) planner.shoppingWeeks = {};
        planner.shoppingWeeks[key] = clone(edits);
        write(PLAN_KEY, planner);
      },
      isChecked(recipeId, ingredientId) {
        return (
          Object.hasOwn(checks.recipes, recipeId) &&
          Object.hasOwn(checks.recipes[recipeId], ingredientId) &&
          checks.recipes[recipeId][ingredientId] === true
        );
      },
      check(recipeId, ingredientId, checked) {
        if (!Object.hasOwn(checks.recipes, recipeId))
          checks.recipes[recipeId] = {};
        checks.recipes[recipeId][ingredientId] = checked;
        write(CHECKS_KEY, checks);
      },
      resetChecks(recipeId) {
        delete checks.recipes[recipeId];
        write(CHECKS_KEY, checks);
      },
      reset() {
        planner = { schemaVersion: 1, weeks: {} };
        checks = { schemaVersion: 1, recipes: {} };
        issue = storage ? null : "unavailable";
        write(PLAN_KEY, planner);
        write(CHECKS_KEY, checks);
      },
    };
  }

  Object.assign((globalThis.TopRecipes ||= {}), {
    PLAN_KEY,
    CHECKS_KEY,
    validPlanner,
    validChecks,
    validShoppingEdits,
    validSettings,
    createPersistence,
  });
})();

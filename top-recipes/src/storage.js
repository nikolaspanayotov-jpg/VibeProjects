(() => {
  const { DAYS, MEALS, emptyWeek, mondayKey, clone } = globalThis.TopRecipes;

  const PLAN_KEY = "top-recipes:planner:v1";
  const CHECKS_KEY = "top-recipes:ingredients:v1";
  const object = (value) =>
    value !== null && typeof value === "object" && !Array.isArray(value);
  const slug = (value) =>
    typeof value === "string" && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value);

  function validPlanner(value) {
    if (!object(value) || value.schemaVersion !== 1 || !object(value.weeks))
      return false;
    return Object.entries(value.weeks).every(([key, week]) => {
      try {
        if (mondayKey(key) !== key) return false;
      } catch {
        return false;
      }
      return (
        object(week) &&
        Object.keys(week).length === DAYS.length &&
        DAYS.every(
          (day) =>
            object(week[day]) &&
            Object.keys(week[day]).length === MEALS.length &&
            MEALS.every(
              (meal) => week[day][meal] === null || slug(week[day][meal]),
            ),
        )
      );
    });
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
    createPersistence,
  });
})();

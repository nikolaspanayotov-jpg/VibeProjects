import { api, runScript } from "./setup.js";
import test from "node:test";
import assert from "node:assert/strict";
const {
  DAYS,
  MEALS,
  emptyWeek,
  mondayKey,
  weekOffset,
  parseLocalDate,
  assignMeal,
  moveMeal,
} = api;
const { createPersistence, PLAN_KEY, CHECKS_KEY, validPlanner } = api;

function memoryStorage(initial = {}) {
  const data = new Map(Object.entries(initial));
  return {
    data,
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, value),
  };
}

test("a new week has all 21 empty meal slots", () => {
  const week = emptyWeek();
  assert.equal(
    DAYS.flatMap((day) => MEALS.map((meal) => week[day][meal])).length,
    21,
  );
  assert.ok(
    DAYS.every((day) => MEALS.every((meal) => week[day][meal] === null)),
  );
});

test("local week calculations handle Sundays, year boundaries and daylight-saving weeks", () => {
  assert.equal(mondayKey("2026-11-03"), "2026-11-02");
  assert.equal(mondayKey("2026-11-08"), "2026-11-02");
  assert.equal(mondayKey("2027-01-01"), "2026-12-28");
  assert.equal(weekOffset("2026-12-28", 1), "2027-01-04");
  assert.equal(weekOffset("2026-03-23", 1), "2026-03-30");
  assert.equal(weekOffset("2026-10-19", 1), "2026-10-26");
  assert.throws(() => parseLocalDate("2026-02-30"));
  assert.throws(() => parseLocalDate("not-a-date"));
});

test("placement copies, replacement replaces, and movement swaps without mutating history", () => {
  const breakfast = { day: "monday", meal: "breakfast" };
  const lunch = { day: "monday", meal: "lunch" };
  const original = emptyWeek();
  const one = assignMeal(original, breakfast, "overnight-oats");
  const two = assignMeal(one, lunch, "chicken-and-leek-pie");
  const swapped = moveMeal(two, breakfast, lunch);
  assert.equal(original.monday.breakfast, null);
  assert.equal(one.monday.lunch, null);
  assert.equal(two.monday.breakfast, "overnight-oats");
  assert.equal(swapped.monday.lunch, "overnight-oats");
  assert.equal(swapped.monday.breakfast, "chicken-and-leek-pie");
  const moved = moveMeal(swapped, lunch, { day: "sunday", meal: "dinner" });
  assert.equal(moved.monday.lunch, null);
  assert.equal(moved.sunday.dinner, "overnight-oats");
  assert.deepEqual(moveMeal(moved, breakfast, breakfast), moved);
  assert.equal(
    assignMeal(moved, breakfast, "moussaka").monday.breakfast,
    "moussaka",
  );
  assert.throws(() =>
    assignMeal(original, { day: "bad", meal: "dinner" }, "moussaka"),
  );
});

test("plans and ingredient checks survive a reload and weeks stay independent", () => {
  const storage = memoryStorage();
  const first = createPersistence(storage);
  first.saveWeek(
    "2026-11-02",
    assignMeal(
      emptyWeek(),
      { day: "monday", meal: "breakfast" },
      "overnight-oats",
    ),
  );
  first.saveWeek(
    "2026-11-09",
    assignMeal(emptyWeek(), { day: "friday", meal: "dinner" }, "moussaka"),
  );
  first.check("overnight-oats", "rolled-oats", true);
  const reloaded = createPersistence(storage);
  assert.equal(reloaded.issue, null);
  assert.equal(reloaded.week("2026-11-02").monday.breakfast, "overnight-oats");
  assert.equal(reloaded.week("2026-11-09").monday.breakfast, null);
  assert.equal(reloaded.week("2026-11-09").friday.dinner, "moussaka");
  assert.equal(reloaded.isChecked("overnight-oats", "rolled-oats"), true);
  const detached = reloaded.week("2026-11-02");
  detached.monday.breakfast = null;
  assert.equal(reloaded.week("2026-11-02").monday.breakfast, "overnight-oats");
  reloaded.resetChecks("overnight-oats");
  assert.equal(
    createPersistence(storage).isChecked("overnight-oats", "rolled-oats"),
    false,
  );
});

test("corrupt saved data is preserved until an explicit reset", () => {
  const original = "{this is broken";
  const storage = memoryStorage({ [PLAN_KEY]: original });
  const saved = createPersistence(storage);
  assert.equal(saved.issue, "corrupt");
  saved.saveWeek("2026-11-02", emptyWeek());
  saved.check("overnight-oats", "milk", true);
  assert.equal(storage.getItem(PLAN_KEY), original);
  assert.equal(storage.getItem(CHECKS_KEY), null);
  saved.reset();
  assert.equal(saved.issue, null);
  assert.ok(validPlanner(JSON.parse(storage.getItem(PLAN_KEY))));
});

test("unavailable storage and write failures retain an in-memory plan", () => {
  for (const storage of [
    null,
    {
      getItem: () => null,
      setItem: () => {
        throw new Error("Quota exceeded");
      },
    },
  ]) {
    const saved = createPersistence(storage);
    saved.saveWeek(
      "2026-11-02",
      assignMeal(
        emptyWeek(),
        { day: "sunday", meal: "dinner" },
        "removed-recipe",
      ),
    );
    assert.equal(saved.issue, "unavailable");
    assert.equal(saved.week("2026-11-02").sunday.dinner, "removed-recipe");
  }
});

test("stored data validation rejects malformed dates and slot types while retaining unknown recipe IDs", () => {
  assert.equal(
    validPlanner({ schemaVersion: 1, weeks: { "2026-11-02": emptyWeek() } }),
    true,
  );
  assert.equal(
    validPlanner({ schemaVersion: 1, weeks: { "2026-11-03": emptyWeek() } }),
    false,
  );
  assert.equal(validPlanner({ schemaVersion: 2, weeks: {} }), false);
  const week = emptyWeek();
  week.monday.breakfast = { bad: true };
  assert.equal(
    validPlanner({ schemaVersion: 1, weeks: { "2026-11-02": week } }),
    false,
  );
});

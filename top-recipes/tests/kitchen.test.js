import test from "node:test";
import assert from "node:assert/strict";
import { api } from "./setup.js";

test("kitchen timers use elapsed time, pause and resume without drift, and finish once", () => {
  const timer = api.kitchenTimer(1.5, "Rice", 1000);
  assert.equal(api.formatKitchenTime(timer.remaining), "1:30");
  const paused = api.pauseKitchenTimer(timer, 61000);
  assert.equal(paused.state, "paused");
  assert.equal(paused.remaining, 30000);
  assert.deepEqual(api.tickKitchenTimer(paused, 600000), paused);
  const resumed = api.resumeKitchenTimer(paused, 600000);
  assert.equal(resumed.deadline, 630000);
  assert.equal(api.tickKitchenTimer(resumed, 629001).remaining, 999);
  const done = api.tickKitchenTimer(resumed, 700000);
  assert.equal(done.state, "done");
  assert.equal(done.remaining, 0);
  assert.deepEqual(api.tickKitchenTimer(done, 900000), done);
  assert.deepEqual(api.resumeKitchenTimer(done, 900000), done);
  assert.equal(api.formatKitchenTime(3600000), "1:00:00");
  assert.equal(api.formatKitchenTime(999), "0:01");
  assert.equal(timer.remaining, 90000);
});

test("custom shopping items save by week without changing plans, recipe edits or checks", () => {
  const key = "2026-11-02";
  const week = api.emptyWeek();
  week.monday.breakfast = "pancakes";
  const initial = {
    schemaVersion: 1,
    weeks: { [key]: week },
    preferences: {
      householdSize: 2,
      favourites: ["pancakes"],
      recent: ["pancakes"],
    },
  };
  const data = new Map([[api.PLAN_KEY, JSON.stringify(initial)]]);
  const storage = {
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, value),
  };
  const state = api.createPersistence(storage);
  assert.deepEqual(state.customShoppingWeek(key), []);
  assert.equal(data.get(api.PLAN_KEY), JSON.stringify(initial));
  const item = {
    id: "extra-coffee",
    name: "Coffee",
    quantity: 2,
    unit: "pack",
    aisle: "Cupboard & other",
    selected: true,
    bought: true,
  };
  const edits = {
    "milk|ml": { baseline: 250, quantity: 350, selected: false },
  };
  state.check("pancakes", "egg", true);
  state.saveShoppingState(key, edits, [item]);
  const loaded = api.createPersistence(storage);
  assert.equal(loaded.issue, null);
  assert.deepEqual(loaded.customShoppingWeek(key), [item]);
  assert.deepEqual(loaded.customShoppingWeek("2026-11-09"), []);
  assert.deepEqual(loaded.shoppingWeek(key), edits);
  assert.deepEqual(loaded.week(key), week);
  assert.equal(loaded.isChecked("pancakes", "egg"), true);
  loaded.customShoppingWeek(key)[0].quantity = 99;
  assert.equal(loaded.customShoppingWeek(key)[0].quantity, 2);
  assert.equal(
    api.formatShoppingQuantity({ quantity: 2, unit: "bottle" }),
    "2 bottles",
  );
});

test("invalid custom items preserve corrupt saved data until reset and unavailable storage works in memory", () => {
  const valid = {
    id: "extra-coffee",
    name: "Coffee",
    quantity: 1,
    unit: "pack",
    aisle: "Cupboard & other",
    selected: true,
    bought: false,
  };
  for (const patch of [
    { name: " " },
    { quantity: -1 },
    { quantity: Infinity },
    { unit: "invalid" },
    { aisle: "invalid" },
    { bought: "yes" },
  ])
    assert.equal(api.validCustomShopping([{ ...valid, ...patch }]), false);
  assert.equal(api.validCustomShopping([valid, valid]), false);
  const raw = JSON.stringify({
    schemaVersion: 1,
    weeks: {},
    customShoppingWeeks: { "2026-11-02": [{ ...valid, unit: "invalid" }] },
  });
  const data = new Map([[api.PLAN_KEY, raw]]);
  const storage = {
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, value),
  };
  const broken = api.createPersistence(storage);
  assert.equal(broken.issue, "corrupt");
  broken.saveShoppingState("2026-11-02", {}, [valid]);
  assert.equal(data.get(api.PLAN_KEY), raw);
  broken.reset();
  assert.deepEqual(broken.customShoppingWeek("2026-11-02"), []);
  const memory = api.createPersistence(null);
  memory.saveShoppingState("2026-11-02", {}, [valid]);
  assert.deepEqual(memory.customShoppingWeek("2026-11-02"), [valid]);
});

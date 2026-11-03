import test from "node:test";
import assert from "node:assert/strict";
import { loadImage } from "@napi-rs/canvas";
import { api } from "./setup.js";
import { imageCanvas } from "./image-canvas.js";

const measureCanvas = imageCanvas();
const context = measureCanvas.getContext("2d");
const measure = (value, font) => {
  context.font = font;
  return context.measureText(value).width;
};
const planModel = () => ({
  mode: "plan",
  weekKey: "2026-11-02",
  dateLabel: "2 November 2026 — 8 November 2026",
  days: api.DAYS.map((day, index) => ({
    label: api.titleCase(day).slice(0, 3),
    date: `${index + 2} Nov`,
    meals: api.MEALS.map((meal) => ({
      meal,
      name:
        meal === "breakfast"
          ? "Overnight oats"
          : meal === "lunch"
            ? "Chicken and leek pie"
            : "Roast turkey with potatoes",
      note:
        day === "wednesday" && meal === "lunch"
          ? "Leftovers · 2 servings"
          : "2 servings",
    })),
  })),
});
const shoppingModel = () => ({
  mode: "shopping",
  weekKey: "2026-11-02",
  dateLabel: "2 November 2026 — 8 November 2026",
  page: 1,
  totalPages: 3,
  itemCount: 20,
  missingCount: 1,
  items: [
    {
      key: "milk|ml",
      name: "Milk",
      amount: "450 ml",
      aisle: "Dairy & eggs",
      bought: false,
    },
    {
      key: "extra:coffee|pack",
      name: "Extra-special coffee for the weekend",
      amount: "2 packs",
      aisle: "Cupboard & other",
      bought: true,
    },
    {
      key: "extra:soap|bottle",
      name: "Washing-up liquid",
      amount: "1 bottle",
      aisle: "Cupboard & other",
      bought: false,
    },
  ],
});

test("image text wraps long names and unbroken words without truncation", () => {
  const source = "Averylongrecipenamethatmustwrapwithoutclipping 🥞 pancakes";
  const lines = api.wrapImageText(source, 180, "36px Georgia", measure);
  assert.ok(lines.length > 2);
  assert.equal(lines.join("").replace(/\s/g, ""), source.replace(/\s/g, ""));
  assert.ok(lines.every((line) => measure(line, "36px Georgia") <= 180));
});

test("portrait plan image lays out all days, meals and leftover labels within the canvas", async () => {
  const model = planModel();
  const layout = api.layoutCaptureImage(model, measure);
  assert.equal(layout.width, 1080);
  assert.ok(layout.height > layout.width);
  const text = layout.commands.filter((command) => command.kind === "text");
  for (const day of model.days)
    assert.ok(text.some((command) => command.value === day.label));
  assert.equal(
    layout.commands.filter((command) => command.kind === "rect").length,
    21,
  );
  assert.match(text.map((command) => command.value).join(" "), /Leftovers/);
  for (const command of text) {
    const width = measure(command.value, command.font);
    const left =
      command.align === "center"
        ? command.x - width / 2
        : command.align === "right"
          ? command.x - width
          : command.x;
    assert.ok(left >= 0 && left + width <= layout.width + 1, command.value);
    assert.ok(command.y >= 0 && command.y < layout.height - 20, command.value);
  }
  const blob = await api.captureImageBlob(model, imageCanvas);
  const bytes = Buffer.from(await blob.arrayBuffer());
  assert.equal(blob.type, "image/png");
  assert.deepEqual(
    [...bytes.subarray(0, 8)],
    [137, 80, 78, 71, 13, 10, 26, 10],
  );
  const image = await loadImage(bytes);
  assert.equal(image.width, 1080);
  assert.equal(image.height, layout.height);
});

test("shopping images include only their page with aisles, custom groceries, quantities, bought marks and missing warnings", async () => {
  const model = shoppingModel();
  const layout = api.layoutCaptureImage(model, measure);
  const text = layout.commands
    .filter((command) => command.kind === "text")
    .map((command) => command.value)
    .join(" ");
  assert.match(text, /Page 2 of 3/);
  assert.match(text, /CUPBOARD & OTHER/);
  assert.match(text, /Washing-up liquid/);
  assert.match(text, /450 ml/);
  assert.match(text, /Ingredients unavailable for 1 planned meal/);
  // One checked item contributes exactly two tick strokes.
  assert.equal(
    layout.commands.filter(
      (command) => command.kind === "line" && command.width === 5,
    ).length,
    2,
  );
  const blob = await api.captureImageBlob(model, imageCanvas);
  const image = await loadImage(Buffer.from(await blob.arrayBuffer()));
  assert.equal(image.width, 1080);
  assert.ok(image.height > image.width);
});

test("an unavailable canvas gives a recoverable export failure", async () => {
  await assert.rejects(
    api.captureImageBlob(planModel(), () => ({ getContext: () => null })),
    /Canvas/,
  );
  await assert.rejects(
    api.captureImageBlob(planModel(), () => {
      const canvas = imageCanvas();
      canvas.toBlob = (callback) => callback(null);
      return canvas;
    }),
    /Could not create image/,
  );
});

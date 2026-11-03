(() => {
  const { el } = globalThis.TopRecipes;
  const IMAGE_WIDTH = 1080;
  const IMAGE_COLOURS = {
    cream: "#faf7f0",
    ink: "#252a24",
    olive: "#36513e",
    muted: "#656c60",
    line: "#dedfd4",
    breakfast: "#f4ecd9",
    lunch: "#e8efdf",
    dinner: "#f3e4db",
    warning: "#8f422d",
  };
  const sans = (size, weight = "normal") =>
    `${weight} ${size}px Arial, sans-serif`;
  const serif = (size, italic = false) =>
    `${italic ? "italic " : ""}${size}px Georgia, serif`;

  function wrapImageText(value, width, font, measure) {
    const lines = [];
    for (const paragraph of String(value).split(/\n/)) {
      let line = "";
      for (const word of paragraph.trim().split(/\s+/).filter(Boolean)) {
        if (line && measure(`${line} ${word}`, font) <= width) {
          line += ` ${word}`;
          continue;
        }
        if (line) {
          lines.push(line);
          line = "";
        }
        if (measure(word, font) <= width) {
          line = word;
          continue;
        }
        for (const character of Array.from(word)) {
          if (line && measure(line + character, font) > width) {
            lines.push(line);
            line = "";
          }
          line += character;
        }
      }
      lines.push(line);
    }
    return lines;
  }

  // A measured canvas layout avoids screenshot libraries, external fonts and clipped HTML.
  function layoutCaptureImage(model, measure) {
    const c = IMAGE_COLOURS;
    const commands = [];
    const text = (value, x, y, font, colour = c.ink, align = "left") =>
      commands.push({ kind: "text", value, x, y, font, colour, align });
    const rect = (x, y, width, height, colour, radius = 0) =>
      commands.push({ kind: "rect", x, y, width, height, colour, radius });
    const line = (x1, y1, x2, y2, colour = c.line, width = 2) =>
      commands.push({ kind: "line", x1, y1, x2, y2, colour, width });
    const paragraph = (
      value,
      x,
      y,
      width,
      font,
      lineHeight,
      colour = c.ink,
      align = "left",
    ) => {
      const lines = wrapImageText(value, width, font, measure);
      lines.forEach((value, index) =>
        text(value, x, y + index * lineHeight, font, colour, align),
      );
      return lines.length * lineHeight;
    };
    text(
      "GOOD FOOD. A LITTLE FORETHOUGHT.",
      540,
      60,
      sans(22),
      c.olive,
      "center",
    );
    text(
      model.mode === "shopping" ? "My shopping" : "My weekly",
      540,
      114,
      serif(88),
      c.ink,
      "center",
    );
    text(
      model.mode === "shopping" ? "list." : "meal plan.",
      540,
      208,
      serif(88, true),
      c.olive,
      "center",
    );
    const dateHeight = paragraph(
      model.dateLabel,
      540,
      322,
      952,
      sans(27),
      36,
      c.muted,
      "center",
    );
    let y = 322 + dateHeight + 30;
    line(64, y, 1016, y);
    y += 30;
    if (model.mode === "plan") {
      const dayWidth = 116;
      const cellWidth = (952 - dayWidth) / 3;
      ["Breakfast", "Lunch", "Dinner"].forEach((meal, index) =>
        text(
          meal.toUpperCase(),
          64 + dayWidth + cellWidth * (index + 0.5),
          y,
          sans(21, "bold"),
          c.olive,
          "center",
        ),
      );
      y += 52;
      for (const day of model.days) {
        const cells = day.meals.map((meal) => {
          const titles = wrapImageText(
            meal.name,
            cellWidth - 42,
            serif(36),
            measure,
          );
          const notes = meal.note
            ? wrapImageText(meal.note, cellWidth - 42, sans(23), measure)
            : [];
          return {
            ...meal,
            titles,
            notes,
            height:
              titles.length * 44 + (notes.length ? 12 + notes.length * 30 : 0),
          };
        });
        const rowHeight = Math.max(
          158,
          ...cells.map((cell) => cell.height + 48),
        );
        text(day.label, 64, y + rowHeight / 2 - 32, sans(28, "bold"), c.olive);
        text(day.date, 64, y + rowHeight / 2 + 10, sans(22), c.muted);
        cells.forEach((cell, index) => {
          const x = 64 + dayWidth + index * cellWidth;
          rect(x + 5, y + 6, cellWidth - 10, rowHeight - 12, c[cell.meal], 12);
          let top = y + (rowHeight - cell.height) / 2;
          cell.titles.forEach((value) => {
            text(value, x + cellWidth / 2, top, serif(36), c.ink, "center");
            top += 44;
          });
          if (cell.notes.length) top += 12;
          cell.notes.forEach((value) => {
            text(value, x + cellWidth / 2, top, sans(23), c.olive, "center");
            top += 30;
          });
        });
        y += rowHeight;
      }
    } else {
      text(
        `Page ${model.page + 1} of ${model.totalPages} · ${model.itemCount} items in your list`,
        64,
        y,
        sans(24),
        c.muted,
      );
      y += 52;
      let previousAisle;
      for (const item of model.items) {
        if (item.aisle !== previousAisle) {
          text(item.aisle.toUpperCase(), 64, y + 16, sans(24, "bold"), c.olive);
          y += 62;
          previousAisle = item.aisle;
        }
        const names = wrapImageText(item.name, 650, sans(36), measure);
        const quantities = wrapImageText(
          item.amount,
          212,
          sans(30, "bold"),
          measure,
        );
        const height = Math.max(
          84,
          Math.max(names.length * 46, quantities.length * 40) + 28,
        );
        const middle = y + height / 2;
        line(66, middle - 17, 100, middle - 17, c.olive, 3);
        line(100, middle - 17, 100, middle + 17, c.olive, 3);
        line(100, middle + 17, 66, middle + 17, c.olive, 3);
        line(66, middle + 17, 66, middle - 17, c.olive, 3);
        if (item.bought) {
          line(72, middle, 81, middle + 9, c.olive, 5);
          line(81, middle + 9, 96, middle - 10, c.olive, 5);
        }
        names.forEach((value, index) =>
          text(
            value,
            126,
            middle - names.length * 23 + index * 46,
            sans(36),
            item.bought ? c.muted : c.ink,
          ),
        );
        quantities.forEach((value, index) =>
          text(
            value,
            1016,
            middle - quantities.length * 20 + index * 40,
            sans(30, "bold"),
            c.olive,
            "right",
          ),
        );
        line(64, y + height, 1016, y + height);
        y += height;
      }
      if (!model.items.length)
        y += paragraph("No items selected.", 64, y, 952, sans(32), 42, c.muted);
      if (model.missingCount)
        y +=
          24 +
          paragraph(
            `Ingredients unavailable for ${model.missingCount} planned meal${model.missingCount === 1 ? "" : "s"}.`,
            64,
            y + 24,
            952,
            sans(24),
            34,
            c.warning,
          );
    }
    const height = Math.max(model.mode === "plan" ? 1660 : 1440, y + 150);
    if (height > 8192)
      throw new Error(
        "This image is too tall. Use Print or the screenshot view instead.",
      );
    line(64, height - 114, 1016, height - 114);
    text("top recipes.", 64, height - 80, serif(34), c.olive);
    text(
      model.mode === "shopping"
        ? `Page ${model.page + 1} of ${model.totalPages}`
        : "A week of good meals",
      1016,
      height - 74,
      sans(24),
      c.muted,
      "right",
    );
    return { width: IMAGE_WIDTH, height, background: c.cream, commands };
  }

  function paintCaptureImage(context, layout) {
    context.fillStyle = layout.background;
    context.fillRect(0, 0, layout.width, layout.height);
    context.textBaseline = "top";
    for (const command of layout.commands) {
      if (command.kind === "text") {
        context.font = command.font;
        context.fillStyle = command.colour;
        context.textAlign = command.align;
        context.fillText(command.value, command.x, command.y);
      } else if (command.kind === "rect") {
        context.fillStyle = command.colour;
        if (command.radius && context.roundRect) {
          context.beginPath();
          context.roundRect(
            command.x,
            command.y,
            command.width,
            command.height,
            command.radius,
          );
          context.fill();
        } else
          context.fillRect(command.x, command.y, command.width, command.height);
      } else {
        context.strokeStyle = command.colour;
        context.lineWidth = command.width;
        context.lineCap = "round";
        context.beginPath();
        context.moveTo(command.x1, command.y1);
        context.lineTo(command.x2, command.y2);
        context.stroke();
      }
    }
  }

  async function captureImageBlob(
    model,
    canvasFactory = () => document.createElement("canvas"),
  ) {
    const canvas = canvasFactory();
    const context = canvas.getContext("2d");
    if (!context) throw new Error("Canvas is unavailable");
    const layout = layoutCaptureImage(model, (value, font) => {
      context.font = font;
      return context.measureText(value).width;
    });
    canvas.width = layout.width;
    canvas.height = layout.height;
    paintCaptureImage(context, layout);
    return new Promise((resolve, reject) =>
      canvas.toBlob(
        (blob) =>
          blob ? resolve(blob) : reject(new Error("Could not create image")),
        "image/png",
      ),
    );
  }

  function createCaptureExporter({ getModel }) {
    const saveEl = document.querySelector("#capture-save");
    const shareEl = document.querySelector("#capture-share");
    const statusEl = document.querySelector("#capture-export-status");
    let generation = 0;
    let file = null;
    async function prepare() {
      const current = ++generation;
      file = null;
      saveEl.disabled = true;
      shareEl.disabled = true;
      shareEl.hidden = true;
      statusEl.textContent = "Preparing your image…";
      const model = getModel();
      saveEl.textContent =
        model.mode === "shopping" && model.totalPages > 1
          ? "Save this page"
          : "Save image";
      try {
        const blob = await captureImageBlob(model);
        if (current !== generation) return;
        const suffix =
          model.mode === "shopping" ? `-page-${model.page + 1}` : "";
        file = new File(
          [blob],
          `top-recipes-${model.mode}-${model.weekKey}${suffix}.png`,
          { type: "image/png" },
        );
        saveEl.disabled = false;
        let canShare = false;
        try {
          canShare =
            !!navigator.share && !!navigator.canShare?.({ files: [file] });
        } catch {
          /* File sharing is optional. */
        }
        shareEl.hidden = !canShare;
        shareEl.disabled = !canShare;
        statusEl.textContent =
          model.mode === "shopping" && model.totalPages > 1
            ? "This image contains the page shown. Use Next page to save the rest."
            : "Your portrait PNG is ready to save.";
      } catch {
        if (current === generation)
          statusEl.textContent =
            "Image export is unavailable here. You can still take a screenshot or use Print.";
      }
    }
    saveEl.addEventListener("click", () => {
      if (!file) return;
      let url;
      try {
        url = URL.createObjectURL(file);
        const link = el("a");
        link.href = url;
        link.download = file.name;
        saveEl.closest("dialog").append(link);
        link.click();
        link.remove();
        window.setTimeout(() => URL.revokeObjectURL(url), 30000);
        statusEl.textContent = shareEl.hidden
          ? "Image download started. Find the PNG in Downloads."
          : "Image download started. Find it in Downloads, or use Share image for your phone’s saving options.";
      } catch {
        if (url) URL.revokeObjectURL(url);
        statusEl.textContent =
          "The download could not start. Try Share image, or take a screenshot.";
      }
    });
    shareEl.addEventListener("click", async () => {
      if (!file || !navigator.share) return;
      const current = generation;
      shareEl.disabled = true;
      // The file is prepared before the tap so native sharing keeps its user gesture.
      try {
        await navigator.share({
          files: [file],
          title:
            getModel().mode === "shopping"
              ? "My shopping list"
              : "My weekly meal plan",
        });
        if (current === generation) statusEl.textContent = "Image shared.";
      } catch (error) {
        if (current === generation)
          statusEl.textContent =
            error.name === "AbortError"
              ? "Sharing cancelled. Your image is still ready to save."
              : "Sharing is unavailable. Use Save image to download the PNG.";
      } finally {
        if (current === generation) shareEl.disabled = false;
      }
    });
    return {
      prepare,
      invalidate() {
        generation++;
        file = null;
        saveEl.disabled = true;
        shareEl.disabled = true;
      },
    };
  }
  Object.assign((globalThis.TopRecipes ||= {}), {
    wrapImageText,
    layoutCaptureImage,
    paintCaptureImage,
    captureImageBlob,
    createCaptureExporter,
  });
})();

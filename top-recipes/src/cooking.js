(() => {
  const { el, button, showDialog } = globalThis.TopRecipes;

  function kitchenTimer(minutes, label, now = Date.now()) {
    const duration = Math.round(minutes * 60000);
    return {
      id: `timer-${now.toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
      label,
      duration,
      remaining: duration,
      deadline: now + duration,
      state: "running",
    };
  }
  function tickKitchenTimer(timer, now = Date.now()) {
    if (timer.state !== "running") return { ...timer };
    const remaining = Math.max(0, timer.deadline - now);
    return { ...timer, remaining, state: remaining ? "running" : "done" };
  }
  function pauseKitchenTimer(timer, now = Date.now()) {
    const next = tickKitchenTimer(timer, now);
    return { ...next, state: next.state === "running" ? "paused" : next.state };
  }
  function resumeKitchenTimer(timer, now = Date.now()) {
    return timer.state === "paused"
      ? { ...timer, deadline: now + timer.remaining, state: "running" }
      : { ...timer };
  }
  function formatKitchenTime(milliseconds) {
    const seconds = Math.max(0, Math.ceil(milliseconds / 1000));
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return hours
      ? `${hours}:${String(minutes).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`
      : `${minutes}:${String(seconds % 60).padStart(2, "0")}`;
  }

  function createCookingMode() {
    const $ = (selector) => document.querySelector(selector);
    const dialogEl = $("#cook-dialog");
    const sessions = new Map();
    let recipe = null;
    let session = null;
    let clock = null;
    let wakeLock = null;
    let wakeRequest = 0;

    function renderStep(focus = false) {
      const step = session.step;
      $("#cook-step-count").textContent =
        `Step ${step + 1} of ${recipe.method.length}`;
      $("#cook-step-select").value = String(step);
      $("#cook-step-heading").textContent = `Step ${step + 1}`;
      $("#cook-step-text").textContent = recipe.method[step];
      $("#cook-step-done").checked = session.completed.has(step);
      $("#cook-step-done").setAttribute(
        "aria-label",
        `Step ${step + 1} completed`,
      );
      $("#cook-progress").max = recipe.method.length;
      $("#cook-progress").value = session.completed.size;
      $("#cook-completed-count").textContent =
        `${session.completed.size} of ${recipe.method.length} done`;
      $("#cook-previous").disabled = step === 0;
      $("#cook-next").disabled = step === recipe.method.length - 1;
      $("#cook-complete").hidden =
        session.completed.size !== recipe.method.length;
      if (focus) {
        $("#cook-step-heading").focus({ preventScroll: true });
        $(".cook-method").scrollIntoView({ block: "start", behavior: "auto" });
      }
    }

    function renderIngredients() {
      const listEl = $("#cook-ingredient-list");
      listEl.replaceChildren();
      const groups = new Map();
      for (const ingredient of recipe.ingredients) {
        if (!groups.has(ingredient.group)) {
          const group = el("fieldset", "ingredient-group");
          group.append(el("legend", null, ingredient.group));
          groups.set(ingredient.group, group);
          listEl.append(group);
        }
        const label = el("label", "ingredient-row");
        const check = el("input");
        check.type = "checkbox";
        check.checked = session.ingredients.has(ingredient.id);
        check.dataset.cookIngredient = ingredient.id;
        check.addEventListener("change", () => {
          if (check.checked) session.ingredients.add(ingredient.id);
          else session.ingredients.delete(ingredient.id);
        });
        label.append(
          check,
          el("span", null, `${ingredient.quantity} ${ingredient.name}`),
        );
        groups.get(ingredient.group).append(label);
      }
    }

    function updateTimerRows() {
      for (const timer of session.timers) {
        const row = $("#cook-timer-list").querySelector(
          `[data-timer="${timer.id}"]`,
        );
        if (!row) continue;
        row.querySelector(".cook-timer-time").textContent = formatKitchenTime(
          timer.remaining,
        );
        row.classList.toggle("finished", timer.state === "done");
        row.querySelector(".cook-timer-finished").hidden =
          timer.state !== "done";
        const toggle = row.querySelector('[data-action="toggle"]');
        toggle.disabled = timer.state === "done";
        toggle.textContent = timer.state === "paused" ? "Resume" : "Pause";
        toggle.setAttribute(
          "aria-label",
          `${timer.state === "paused" ? "Resume" : "Pause"} ${timer.label} timer`,
        );
      }
      $("#cook-timer-add").disabled = session.timers.length >= 8;
    }

    function renderTimers() {
      const listEl = $("#cook-timer-list");
      listEl.replaceChildren();
      for (const timer of session.timers) {
        const row = el("div", "cook-timer");
        row.dataset.timer = timer.id;
        const label = el("strong", "cook-timer-label", timer.label);
        const time = el("span", "cook-timer-time");
        time.setAttribute("aria-live", "off");
        const finished = el(
          "p",
          "cook-timer-finished",
          "Time’s up — check your food.",
        );
        const actions = el("div", "cook-timer-actions");
        const toggle = button("Pause", "text-button", () => {
          session.timers = session.timers.map((entry) =>
            entry.id === timer.id
              ? entry.state === "paused"
                ? resumeKitchenTimer(entry)
                : pauseKitchenTimer(entry)
              : entry,
          );
          updateTimerRows();
        });
        toggle.dataset.action = "toggle";
        const reset = button(
          "Reset",
          "text-button",
          () => {
            session.timers = session.timers.map((entry) =>
              entry.id === timer.id
                ? { ...entry, remaining: entry.duration, state: "paused" }
                : entry,
            );
            updateTimerRows();
          },
          `Reset ${timer.label} timer`,
        );
        const remove = button(
          "Remove",
          "text-button",
          () => {
            session.timers = session.timers.filter(
              (entry) => entry.id !== timer.id,
            );
            renderTimers();
            $("#cook-timer-add").focus();
          },
          `Remove ${timer.label} timer`,
        );
        actions.append(toggle, reset, remove);
        row.append(label, time, finished, actions);
        listEl.append(row);
      }
      updateTimerRows();
    }

    function tick() {
      if (!session || !dialogEl.open) return;
      const finished = [];
      session.timers = session.timers.map((timer) => {
        const next = tickKitchenTimer(timer);
        if (timer.state === "running" && next.state === "done")
          finished.push(timer.label);
        return next;
      });
      updateTimerRows();
      if (finished.length)
        $("#cook-status").textContent =
          `${finished.join(" and ")}: time’s up. Check your food.`;
    }

    async function releaseWakeLock() {
      wakeRequest++;
      const previous = wakeLock;
      wakeLock = null;
      try {
        await previous?.release();
      } catch {
        /* The browser may already have released it. */
      }
    }
    async function requestWakeLock() {
      if (
        !$("#cook-awake").checked ||
        !dialogEl.open ||
        document.visibilityState === "hidden" ||
        wakeLock
      )
        return;
      const request = ++wakeRequest;
      try {
        const next = await navigator.wakeLock.request("screen");
        if (
          request !== wakeRequest ||
          !dialogEl.open ||
          !$("#cook-awake").checked
        ) {
          await next.release();
          return;
        }
        wakeLock = next;
        next.addEventListener("release", () => {
          if (wakeLock === next) {
            wakeLock = null;
            $("#cook-awake-status").textContent =
              "Screen awake paused. It will resume when you return to this page.";
          }
        });
        $("#cook-awake-status").textContent =
          "Your screen will stay awake while cooking mode is visible.";
      } catch {
        if (request !== wakeRequest || !dialogEl.open) return;
        $("#cook-awake").checked = false;
        $("#cook-awake-status").textContent =
          "Screen awake is unavailable. You can still follow the steps and use timers.";
      }
    }

    $("#cook-next").addEventListener("click", () => {
      if (session.step < recipe.method.length - 1) {
        session.step++;
        renderStep(true);
      }
    });
    $("#cook-previous").addEventListener("click", () => {
      if (session.step > 0) {
        session.step--;
        renderStep(true);
      }
    });
    $("#cook-step-select").addEventListener("change", (event) => {
      const step = Number(event.target.value);
      if (Number.isInteger(step) && step >= 0 && step < recipe.method.length) {
        session.step = step;
        renderStep(true);
      }
    });
    $("#cook-step-done").addEventListener("change", (event) => {
      if (event.target.checked) session.completed.add(session.step);
      else session.completed.delete(session.step);
      renderStep();
      if (session.completed.size === recipe.method.length)
        $("#cook-status").textContent = "All steps complete. Enjoy your meal!";
    });
    $("#cook-timer-form").addEventListener("submit", (event) => {
      event.preventDefault();
      const minutes = Number($("#cook-timer-minutes").value);
      if (
        !session ||
        !Number.isFinite(minutes) ||
        minutes < 0.5 ||
        minutes > 1440 ||
        session.timers.length >= 8
      )
        return;
      const label =
        $("#cook-timer-name").value.trim().slice(0, 50) ||
        `Step ${session.step + 1}`;
      session.timers.push(kitchenTimer(minutes, label));
      $("#cook-timer-name").value = "";
      renderTimers();
      $("#cook-status").textContent =
        `${label} timer started for ${minutes} minutes.`;
    });
    $("#cook-awake").addEventListener("change", () => {
      if ($("#cook-awake").checked) requestWakeLock();
      else {
        releaseWakeLock();
        $("#cook-awake-status").textContent = "";
      }
    });
    document.addEventListener("visibilitychange", () => {
      if (dialogEl.open) {
        tick();
        requestWakeLock();
      }
    });
    $("#cook-close").addEventListener("click", () => dialogEl.close());
    dialogEl.addEventListener("close", () => {
      clearInterval(clock);
      clock = null;
      if (session)
        session.timers = session.timers.map((timer) =>
          pauseKitchenTimer(timer),
        );
      $("#cook-awake").checked = false;
      releaseWakeLock();
    });
    return {
      open(nextRecipe, opener) {
        recipe = nextRecipe;
        if (!sessions.has(recipe.id))
          sessions.set(recipe.id, {
            step: 0,
            completed: new Set(),
            ingredients: new Set(),
            timers: [],
          });
        session = sessions.get(recipe.id);
        $("#cook-title").textContent = recipe.title;
        $("#cook-yield").textContent =
          `Recipe makes ${recipe.servings} serving${recipe.servings === 1 ? "" : "s"}`;
        $("#cook-ingredients-help").textContent =
          `Amounts make ${recipe.servings} servings. Tick ingredients as you use them; shopping checks stay separate.`;
        $("#cook-step-select").replaceChildren(
          ...recipe.method.map((_, index) => {
            const option = el("option", null, `Step ${index + 1}`);
            option.value = index;
            return option;
          }),
        );
        $("#cook-ingredients").open = window.innerWidth > 760;
        $("#cook-awake-label").hidden = !navigator.wakeLock?.request;
        $("#cook-awake-status").textContent = "";
        $("#cook-status").textContent = "";
        renderStep();
        renderIngredients();
        renderTimers();
        showDialog(dialogEl, opener);
        dialogEl.scrollTop = 0;
        clearInterval(clock);
        clock = setInterval(tick, 1000);
      },
    };
  }
  Object.assign((globalThis.TopRecipes ||= {}), {
    kitchenTimer,
    tickKitchenTimer,
    pauseKitchenTimer,
    resumeKitchenTimer,
    formatKitchenTime,
    createCookingMode,
  });
})();

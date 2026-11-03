(() => {
  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function button(text, className, action, label) {
    const node = el("button", className, text);
    node.type = "button";
    if (label) node.setAttribute("aria-label", label);
    if (action) node.addEventListener("click", action);
    return node;
  }

  function formatMinutes(minutes) {
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    return `${hours} hr${minutes % 60 ? ` ${minutes % 60} min` : ""}`;
  }

  function showDialog(dialog, opener = document.activeElement) {
    dialog.showModal();
    const close = () => {
      if (opener?.isConnected) opener.focus({ preventScroll: true });
      dialog.removeEventListener("close", close);
    };
    dialog.addEventListener("close", close);
  }

  function closeOnBackdrop(dialog) {
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  }

  Object.assign((globalThis.TopRecipes ||= {}), {
    el,
    button,
    formatMinutes,
    showDialog,
    closeOnBackdrop,
  });
})();

(() => {
  const slug = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  const mealTypes = new Set(["breakfast", "lunch", "dinner"]);
  const plain = (node) =>
    Array.isArray(node)
      ? node.map(plain).join("")
      : node.tokens
        ? plain(node.tokens)
        : node.text || "";

  function parseRecipes(markdown) {
    const sections = [];
    for (const node of globalThis.marked.lexer(markdown, { gfm: true })) {
      if (node.type === "space") continue;
      if (node.type === "heading" && node.depth === 2) sections.push([node]);
      else if (sections.length) sections.at(-1).push(node);
    }
    if (!sections.length)
      throw new Error(
        "recipes.md: no recipes found (expected a level-two heading).",
      );
    const ids = new Set();
    return sections.map(([heading, ...nodes]) => {
      const title = plain(heading).trim();
      const fail = (field, message) => {
        throw new Error(
          `recipes.md → ${title || "Untitled recipe"} → ${field}: ${message}`,
        );
      };
      if (!title) fail("title", "must not be empty");
      const metadataNode = nodes[0];
      if (metadataNode?.type !== "code" || metadataNode.lang !== "yaml")
        fail(
          "metadata",
          "place a fenced YAML block immediately after the recipe heading",
        );
      let metadata;
      try {
        metadata = globalThis.jsyaml.load(metadataNode.text, {
          schema: globalThis.jsyaml.JSON_SCHEMA,
        });
      } catch (error) {
        fail("metadata", error.message);
      }
      if (!metadata || typeof metadata !== "object" || Array.isArray(metadata))
        fail("metadata", "must be a mapping");
      if (typeof metadata.id !== "string" || !slug.test(metadata.id))
        fail("id", "must be a lowercase slug");
      if (ids.has(metadata.id))
        fail("id", `duplicate recipe ID "${metadata.id}"`);
      ids.add(metadata.id);
      if (
        !Array.isArray(metadata.meal_types) ||
        !metadata.meal_types.length ||
        metadata.meal_types.some((meal) => !mealTypes.has(meal))
      )
        fail("meal_types", "use breakfast, lunch and/or dinner");
      for (const field of [
        "servings",
        "prep_minutes",
        "cook_minutes",
        "wait_minutes",
      ]) {
        if (
          !Number.isSafeInteger(metadata[field]) ||
          metadata[field] < (field === "servings" ? 1 : 0)
        )
          fail(field, "must be a whole number within the allowed range");
      }
      if (
        !Array.isArray(metadata.tags) ||
        metadata.tags.some((tag) => typeof tag !== "string" || !tag.trim())
      )
        fail("tags", "must be a list of nonempty strings, or []");
      const body = { description: [], ingredients: [], method: [], notes: [] };
      let section = "description";
      for (const node of nodes.slice(1)) {
        if (node.type === "heading" && node.depth === 3) {
          section = plain(node).trim().toLowerCase();
          if (!["ingredients", "method", "notes"].includes(section))
            fail("section", `unknown heading "${plain(node)}"`);
          continue;
        }
        if (section === "description" && node.type === "paragraph")
          body.description.push(plain(node));
        else if (section === "ingredients" && node.type === "table") {
          if (
            node.header.map(plain).join("|") !== "ID|Quantity|Ingredient|Group"
          )
            fail(
              "ingredients",
              "expected columns ID, Quantity, Ingredient, Group",
            );
          const ingredientIds = new Set(
            body.ingredients.map((ingredient) => ingredient.id),
          );
          for (const cells of node.rows) {
            const row = cells.map((cell) => plain(cell).trim());
            if (row.length !== 4 || row.some((value) => !value))
              fail(
                "ingredients",
                "each row needs an ID, quantity, ingredient and group",
              );
            const [id, quantity, name, group] = row;
            if (!slug.test(id) || ingredientIds.has(id))
              fail("ingredients", `invalid or duplicate ingredient ID "${id}"`);
            ingredientIds.add(id);
            body.ingredients.push({ id, quantity, name, group });
          }
        } else if (
          section === "method" &&
          node.type === "list" &&
          node.ordered
        ) {
          body.method.push(...node.items.map((item) => plain(item).trim()));
        } else if (section === "notes") {
          if (node.type === "list")
            body.notes.push(...node.items.map((item) => plain(item).trim()));
          else if (node.type === "paragraph") body.notes.push(plain(node));
          else fail("notes", `unexpected ${node.type}`);
        } else
          fail(
            section,
            `unexpected ${node.type}; follow the recipe template in design.md`,
          );
      }
      for (const field of ["description", "ingredients", "method"]) {
        if (
          !body[field].length ||
          body[field].some((item) => typeof item === "string" && !item.trim())
        )
          fail(field, "must not be empty");
      }
      return {
        id: metadata.id,
        title,
        mealTypes: [...new Set(metadata.meal_types)],
        servings: metadata.servings,
        prepMinutes: metadata.prep_minutes,
        cookMinutes: metadata.cook_minutes,
        waitMinutes: metadata.wait_minutes,
        tags: metadata.tags,
        ...body,
        description: body.description.join("\n\n"),
      };
    });
  }
  Object.assign((globalThis.TopRecipes ||= {}), { parseRecipes });
})();

const SHOWCASE_PAGE_SIZE = 4;

const state = {
  data: null,
  view: "source-event-swaps",
  offset: 0,
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function metric(label, value) {
  return `
    <div class="metric">
      <strong>${escapeHtml(value)}</strong>
      <span>${escapeHtml(label)}</span>
    </div>
  `;
}

function renderHeroMetrics(project) {
  const target = document.getElementById("hero-metrics");
  target.innerHTML = [
    metric("released audio records", formatNumber(project.totals.records)),
    metric(
      "caption-level pairs",
      formatNumber(project.totals.paired_caption_instances)
    ),
    metric("reported top-1 retrieval gain", project.retrieval_gain),
  ].join("");
}

function renderDatasetCards(datasets) {
  const target = document.getElementById("dataset-cards");

  target.innerHTML = datasets
    .map((dataset) => {
      const chips = [
        `${formatNumber(dataset.paired_caption_instances)} paired caption instances`,
        `${dataset.captions_per_clip} captions per clip`,
        `avg duration ${dataset.duration_mean}s`,
        `path: ${dataset.path_pattern}`,
      ];

      if (dataset.identical_pairs > 0) {
        chips.push(
          `${formatNumber(dataset.identical_pairs)} identical factual/counterfactual pairs`
        );
      }

      return `
        <article class="card dataset-card">
          <p class="card-label">${escapeHtml(dataset.name)} / ${escapeHtml(
            dataset.split_label
          )}</p>
          <h3>${formatNumber(dataset.records)} records</h3>
          <p>${escapeHtml(dataset.notes)}</p>
          <div class="dataset-meta">
            ${chips
              .map((chip) => `<span class="meta-chip">${escapeHtml(chip)}</span>`)
              .join("")}
          </div>
          <div class="dataset-links">
            <a href="${escapeHtml(dataset.source_url)}">Source dataset</a>
            <span> · </span>
            <a href="${escapeHtml(dataset.download_url)}">Download entry point</a>
            <span> · </span>
            <a href="${escapeHtml(dataset.release_url)}">Release JSON</a>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderPromptCards(prompts) {
  const target = document.getElementById("prompt-cards");
  target.innerHTML = prompts
    .map(
      (prompt, index) => `
        <article class="card prompt-card">
          <span>Prompt ${index + 1}</span>
          <p>${escapeHtml(prompt)}</p>
        </article>
      `
    )
    .join("");
}

function buildShowcaseButtons(showcases) {
  const target = document.getElementById("showcase-filters");

  target.innerHTML = showcases
    .map(
      (view) => `
        <button
          class="filter-button ${view.id === state.view ? "active" : ""}"
          type="button"
          data-view="${escapeHtml(view.id)}"
        >
          ${escapeHtml(view.label)}
        </button>
      `
    )
    .join("");

  target.querySelectorAll("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.dataset.view;
      state.offset = 0;
      buildShowcaseButtons(state.data.showcases);
      renderShowcase();
    });
  });
}

function rotate(items, offset) {
  if (items.length === 0) {
    return items;
  }

  const normalizedOffset = ((offset % items.length) + items.length) % items.length;
  return items.slice(normalizedOffset).concat(items.slice(0, normalizedOffset));
}

function currentShowcase() {
  return state.data.showcases.find((view) => view.id === state.view);
}

function renderShowcase() {
  const view = currentShowcase();
  const gridTarget = document.getElementById("sample-grid");
  const labelTarget = document.getElementById("showcase-label");
  const titleTarget = document.getElementById("showcase-title");
  const descriptionTarget = document.getElementById("showcase-description");
  const noteTarget = document.getElementById("showcase-note");
  const reshuffleButton = document.getElementById("reshuffle");

  if (!view) {
    gridTarget.innerHTML = "";
    labelTarget.textContent = "";
    titleTarget.textContent = "Curated examples";
    descriptionTarget.textContent = "";
    noteTarget.textContent = "";
    reshuffleButton.disabled = true;
    return;
  }

  labelTarget.textContent = view.label;
  titleTarget.textContent = view.title;
  descriptionTarget.textContent = view.description;
  noteTarget.textContent = view.note;

  const examples = rotate(view.examples, state.offset).slice(0, SHOWCASE_PAGE_SIZE);

  gridTarget.innerHTML = examples
    .map(
      (example) => `
        <article class="card sample-card">
          <header>
            <div class="sample-header">
              <div class="sample-header-top">
                <span class="tag-chip">${escapeHtml(example.dataset)}</span>
                <span class="tag-chip tag-chip-accent">${escapeHtml(example.tag)}</span>
              </div>
              <h3 class="sample-focus">${escapeHtml(example.focus)}</h3>
              <p class="sample-path">${escapeHtml(example.path)}</p>
            </div>
          </header>
          <div class="sample-pair">
            <div class="sample-block factual">
              <strong>Factual</strong>
              <p>${escapeHtml(example.factual)}</p>
            </div>
            <div class="sample-block counterfactual">
              <strong>Counterfactual</strong>
              <p>${escapeHtml(example.counterfactual)}</p>
            </div>
          </div>
        </article>
      `
    )
    .join("");

  reshuffleButton.disabled = view.examples.length <= SHOWCASE_PAGE_SIZE;
}

function renderValidationNote(datasets) {
  const validation = datasets.find((dataset) => dataset.id === "clotho-val");
  const target = document.getElementById("validation-note");

  if (!validation) {
    target.textContent = "";
    return;
  }

  target.textContent =
    "Release note: the current Clotho validation JSON mirrors the factual captions in its counterfactual field, so the curated examples focus on the non-identical releases.";
}

async function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.append(textarea);
  textarea.select();

  const successful = document.execCommand("copy");
  textarea.remove();

  if (!successful) {
    throw new Error("Copy command failed");
  }
}

function setupCopyButtons() {
  document.querySelectorAll("[data-copy-target]").forEach((button) => {
    const initialLabel = button.textContent;

    button.addEventListener("click", async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      if (!target) {
        return;
      }

      try {
        await copyText(target.textContent.trim());
        button.textContent = "Copied";
      } catch (error) {
        button.textContent = "Copy failed";
      }

      window.setTimeout(() => {
        button.textContent = initialLabel;
      }, 1400);
    });
  });
}

async function initialize() {
  const response = await fetch("data/site-data.json");
  if (!response.ok) {
    throw new Error(`Failed to load site data: ${response.status}`);
  }

  state.data = await response.json();
  state.view = state.data.showcases[0]?.id || state.view;

  renderHeroMetrics(state.data.project);
  renderDatasetCards(state.data.datasets);
  renderPromptCards(state.data.prompts);
  buildShowcaseButtons(state.data.showcases);
  renderValidationNote(state.data.datasets);
  renderShowcase();

  const reshuffleButton = document.getElementById("reshuffle");
  reshuffleButton.addEventListener("click", () => {
    state.offset += SHOWCASE_PAGE_SIZE;
    renderShowcase();
  });
}

setupCopyButtons();

initialize().catch((error) => {
  const target = document.getElementById("sample-grid");
  target.innerHTML = `<article class="card sample-card"><p>${escapeHtml(
    error.message
  )}</p></article>`;
});

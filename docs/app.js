const state = {
  data: null,
  filter: "all",
  offset: 0,
};

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value);
}

function metric(label, value) {
  return `
    <div class="metric">
      <strong>${value}</strong>
      <span>${label}</span>
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
    metric("reported retrieval gain", project.retrieval_gain),
  ].join("");
}

function renderDatasetCards(datasets) {
  const target = document.getElementById("dataset-cards");
  target.innerHTML = datasets
    .map(
      (dataset) => `
        <article class="card dataset-card">
          <p class="card-label">${dataset.name} / ${dataset.split_label}</p>
          <h3>${formatNumber(dataset.records)} records</h3>
          <p>${dataset.notes}</p>
          <div class="dataset-meta">
            <span class="meta-chip">${formatNumber(
              dataset.paired_caption_instances
            )} paired caption instances</span>
            <span class="meta-chip">${dataset.captions_per_clip} captions per clip</span>
            <span class="meta-chip">avg duration ${dataset.duration_mean}s</span>
            <span class="meta-chip">path: ${dataset.path_pattern}</span>
          </div>
          <div class="dataset-links">
            <a href="${dataset.source_url}">Source dataset</a>
            <span> · </span>
            <a href="${dataset.download_url}">Download entry point</a>
            <span> · </span>
            <a href="${dataset.release_url}">Release JSON</a>
          </div>
        </article>
      `
    )
    .join("");
}

function renderPromptCards(prompts) {
  const target = document.getElementById("prompt-cards");
  target.innerHTML = prompts
    .map(
      (prompt, index) => `
        <article class="card prompt-card">
          <span>Prompt ${index + 1}</span>
          <p>${prompt}</p>
        </article>
      `
    )
    .join("");
}

function buildFilterButtons(datasets) {
  const filterTarget = document.getElementById("dataset-filters");
  const available = datasets.filter((dataset) => dataset.examples.length > 0);
  const filters = [
    { id: "all", label: "All" },
    ...available.map((dataset) => ({ id: dataset.id, label: dataset.name })),
  ];

  filterTarget.innerHTML = filters
    .map(
      (filter) => `
        <button
          class="filter-button ${filter.id === state.filter ? "active" : ""}"
          type="button"
          data-filter="${filter.id}"
        >
          ${filter.label}
        </button>
      `
    )
    .join("");

  filterTarget.querySelectorAll("[data-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      state.filter = button.dataset.filter;
      state.offset = 0;
      buildFilterButtons(state.data.datasets);
      renderSamples();
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

function collectExamples() {
  if (state.filter === "all") {
    return state.data.datasets.flatMap((dataset) =>
      dataset.examples.map((example) => ({ ...example, dataset: dataset.name }))
    );
  }

  const dataset = state.data.datasets.find((entry) => entry.id === state.filter);
  if (!dataset) {
    return [];
  }

  return dataset.examples.map((example) => ({ ...example, dataset: dataset.name }));
}

function renderSamples() {
  const target = document.getElementById("sample-grid");
  const examples = rotate(collectExamples(), state.offset);
  const maxItems = state.filter === "all" ? 6 : 4;

  target.innerHTML = examples
    .slice(0, maxItems)
    .map(
      (example) => `
        <article class="card sample-card">
          <header>
            <div>
              <p class="card-label">${example.dataset}</p>
              <h3>${example.path}</h3>
            </div>
          </header>
          <div class="sample-pair">
            <div class="sample-block factual">
              <strong>Factual</strong>
              <p>${example.factual}</p>
            </div>
            <div class="sample-block counterfactual">
              <strong>Counterfactual</strong>
              <p>${example.counterfactual}</p>
            </div>
          </div>
        </article>
      `
    )
    .join("");
}

function renderValidationNote(datasets) {
  const validation = datasets.find((dataset) => dataset.id === "clotho-val");
  const target = document.getElementById("validation-note");

  if (!validation) {
    target.textContent = "";
    return;
  }

  target.textContent =
    "Release note: the current Clotho validation JSON mirrors the factual captions in its counterfactual field, so the interactive sample view focuses on the non-identical releases.";
}

async function initialize() {
  const response = await fetch("data/site-data.json");
  if (!response.ok) {
    throw new Error(`Failed to load site data: ${response.status}`);
  }

  state.data = await response.json();
  renderHeroMetrics(state.data.project);
  renderDatasetCards(state.data.datasets);
  renderPromptCards(state.data.prompts);
  buildFilterButtons(state.data.datasets);
  renderValidationNote(state.data.datasets);
  renderSamples();

  const reshuffle = document.getElementById("reshuffle");
  reshuffle.addEventListener("click", () => {
    state.offset += 1;
    renderSamples();
  });
}

initialize().catch((error) => {
  const target = document.getElementById("sample-grid");
  target.innerHTML = `<article class="card sample-card"><p>${error.message}</p></article>`;
});

<p align="center">
  <img src="assets/hero.svg" alt="BREW/LAB — The Anatomy of a Coffee Empire" width="100%" />
</p>

<p align="center">
  <a href="https://shab-analytics.github.io/coffee-strategy-dashboard/"><img src="assets/launch.svg" alt="Open live simulation analysis" width="430" /></a>
</p>

<p align="center">
  <strong>Interactive strategy intelligence built directly from the Coffee Shop Strategy Review workbook.</strong><br/>
  A portfolio project connecting strategic choices, operating economics and profitable growth.
</p>

---

## Executive snapshot

| **15** simulation runs | **3** growth stages | **14** strategic experiments | **93%** target achievement |
|:---:|:---:|:---:|:---:|
| Portfolio evidence | L1 → L2 → L3 | Controlled / observational tests | 14 of 15 runs met target |

> ### The strategic question
> **What actually creates profitable scale?**  
> BREW/LAB treats the simulation as a sequence of managerial decisions rather than a scoreboard. It asks where value was created, which choices changed economics, and whether a successful capability remained valuable as the business moved into a different market context.

## The growth journey

<p align="center">
  <img src="assets/journey.svg" alt="Local shop to brand to international scale" width="95%" />
</p>

The analysis follows the business through three increasingly complex stages. **Level 1** tests location, price and people decisions at store level. **Level 2** introduces capability choices such as roasting and organic sourcing. **Level 3** asks whether those capabilities still make economic sense when the business scales across Mature and Emerging markets.

## What the evidence revealed

| Signal | Workbook evidence | Executive interpretation |
|---|---:|---|
| **Location sets the ceiling** | City vs Suburb: **+$77.6K**; Campus parity strategy vs City premium: **−$246.1K** | Cheap rent cannot compensate for a small, price-sensitive market. Market potential comes before cost optimization. |
| **Roasting is a capability—not a universal answer** | Own roasting in L2: **+$134.0K**; Mature market: **+$584.0K**; Emerging market: **−$157.8K** | The same capability creates value only when demand is large enough to absorb its fixed economics. |
| **Organic can support premium differentiation** | Organic beans: **+$49.9K** | Quality investment paid back while supporting stronger customer experience at a premium price. |
| **Expansion has a J-curve** | Faster Emerging-market expansion: **+$952.8K** | Growth initially pressures profit, then overtakes as the larger store base begins to compound. |
| **More labour is not automatically more value** | One extra job: **−$122.8K** | Better service capacity must translate into sustained demand; otherwise the people investment becomes structural cost. |

<sub>Profit effects above are taken from the workbook's experiment table. They are experiment-specific comparisons, not universal causal estimates.</sub>

---

## From bean to business model

<p align="center">
  <img src="assets/coffee-lifecycle.png" alt="Coffee lifecycle from blossom and cherry through green and roasted bean to cup" width="620" />
</p>

<p align="center"><em>From blossom to cup — the product is the visible end of an interconnected value system.</em></p>

Coffee creates value long before the final transaction. Origin, processing, roasting, preparation and service shape the experience the customer eventually buys. BREW/LAB applies the same logic to strategy:

**SOURCE → ROAST → BRAND → PRICE → SERVE → SCALE**

The simulation shows why these decisions cannot be optimized independently. Roasting can improve differentiation but fail when volume cannot cover fixed economics. Organic sourcing can strengthen willingness to pay. Expansion can create operating leverage, but only after the economics of the underlying model are strong enough to scale.

---

## Inside the live analysis

### 01 · Executive Pulse
See portfolio performance without letting Level 3's absolute scale hide Levels 1 and 2. The dashboard uses **Target Multiple = Game Total ÷ Target** as a calculated comparison metric while preserving reported dollar outcomes.

### 02 · Performance
Move from portfolio-level results into individual runs and annual operating trajectories. Filters and selections expose the operating choices behind the outcome rather than treating every run as an isolated score.

### 03 · Decision Lab
The workbook's 14 experiments become an interactive profit-impact view. Select an experiment to inspect the **question, change tested, runs compared, measured effect, evidence quality and strategic implication**.

### 04 · Strategy Playbook
Translate individual tests into reusable managerial rules—while keeping the boundary between **workbook evidence** and **interpretation** visible.

<p align="center">
  <a href="https://shab-analytics.github.io/coffee-strategy-dashboard/"><img src="assets/launch.svg" alt="Launch BREW/LAB live analysis" width="430" /></a>
</p>

---

## Analytical discipline

**Reported values remain reported values.** Calculated metrics are labelled as calculated. The dashboard does not silently manufacture missing fields or substitute assumptions for workbook data.

- **Target Multiple** = `Game total ÷ Target`.
- **Target Achievement** = count of runs where `Game total ≥ Target`.
- Level 3's displayed annual operating trajectory uses **Mature + Emerging operating profit by year**.
- That annual trajectory is **not** used to reconstruct the workbook-reported Level 3 game total, because the workbook contains broader all-market/franchise information.
- Experiment effects are presented in the context of the runs compared; they should not be interpreted as universal causal effects beyond the simulation.

## Why this project exists

This is not intended to be a decorative coffee dashboard. It is an exercise in **strategic reasoning through data**: turning a multi-stage business simulation into an interface that helps a reader move from outcome → evidence → interpretation → decision.

The project demonstrates:

`Strategy analysis` · `Experiment interpretation` · `Data storytelling` · `Interactive visualization` · `Executive communication` · `Static web deployment`

---

<details>
<summary><strong>Technical architecture & GitHub Pages deployment</strong></summary>

<br/>

The published experience is a static site designed for GitHub Pages. No server is required.

```text
coffee-strategy-dashboard/
├── index.html
├── styles.css
├── app.js
├── data.json
├── README.md
├── .nojekyll
└── assets/
    ├── hero.svg
    ├── launch.svg
    ├── journey.svg
    └── coffee-lifecycle.png
```

To deploy, place the files at the repository root and set **Settings → Pages → Deploy from a branch → `main` → `/ (root)`**.

The live experience is available at:

**https://shab-analytics.github.io/coffee-strategy-dashboard/**

</details>

---

<p align="center">
  <strong>BREW/LAB</strong><br/>
  <sub>Strategy performance, explained through evidence.</sub>
</p>

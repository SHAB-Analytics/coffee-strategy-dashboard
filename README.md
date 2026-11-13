<div align="center">

# ☕ BREW/LAB — Strategy to Scale

### Coffee Shop Strategy Simulation · Executive Analytics

**15 simulation runs · 3 stages of growth · 14 strategic experiments**  
*What creates profitable growth in a coffee business?*

### [▶ OPEN THE LIVE SIMULATION ANALYSIS](https://shab-analytics.github.io/coffee-strategy-dashboard/)

![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-LIVE-2f6b55?style=for-the-badge&logo=github)
![Data Source](https://img.shields.io/badge/Data-Excel%20Workbook-b46a3c?style=for-the-badge&logo=microsoftexcel)
![Runs](https://img.shields.io/badge/Simulation%20Runs-15-231711?style=for-the-badge)
![Experiments](https://img.shields.io/badge/Strategic%20Experiments-14-cb8a5a?style=for-the-badge)

</div>

---

## Executive brief

BREW/LAB turns the supplied **Coffee Shop Strategy Review** workbook into an interactive strategy-intelligence experience. The objective is not simply to rank simulation scores. It is to understand **which operating choices created value, which destroyed it, and which capabilities remained economically attractive as the simulated business moved from a local shop to international scale**.

| Strategic stage | Management focus | Analytical question |
|---|---|---|
| **☕ L1 · Local Shop** | Location, price, people | Can the store establish attractive unit economics? |
| **☕☕ L2 · Build the Brand** | Roasting, sourcing, operating model | Which capabilities strengthen differentiation and profit? |
| **☕☕☕ L3 · Go International** | Market mix, store expansion, scale | Do successful capabilities still create value across different markets? |

> **Portfolio signal:** 14 of 15 simulation runs met their workbook-reported target. The more important finding, however, is that **scale alone did not explain performance**—market context, capability economics and expansion timing materially changed outcomes.

### [Explore the interactive evidence →](https://shab-analytics.github.io/coffee-strategy-dashboard/)

---

## What the evidence revealed

| Decision signal | Workbook evidence | Executive interpretation |
|---|---:|---|
| **Location sets the economic ceiling** | City vs Suburb **+$77.6K**; low-price Campus strategy **−$246.1K** | Lower rent cannot automatically compensate for a smaller or more price-sensitive market. Market attractiveness precedes cost optimization. |
| **Roasting is a capability, not a universal answer** | L2 own roasting **+$134.0K**; Mature market **+$584.0K**; Emerging market **−$157.8K** | The same capability can create or destroy value depending on throughput and market economics. |
| **Organic sourcing can support premium differentiation** | Organic beans **+$49.9K** | Product-quality investment can pay back when it supports willingness to pay and customer experience. |
| **Expansion can produce a J-curve** | Faster Emerging-market expansion **+$952.8K** | Growth can depress profit before a larger store base creates operating leverage. Timing matters. |
| **More labour is not automatically more value** | One extra job **−$122.8K** | Service capacity becomes structural cost when incremental demand does not justify it. |

<sub>Experiment effects above are taken from the workbook's experiment table. They are comparisons within the simulation—not universal causal estimates.</sub>

---

## From bean to business model

<div align="center">
  <img src="coffee-lifecycle.png" alt="Coffee lifecycle from blossom and cherry through green and roasted bean to cup" width="560">
  <br>
  <em>From blossom to cup: the final product is the visible end of an interconnected value system.</em>
</div>

Coffee creates value long before the final transaction. Origin, processing, roasting, preparation and service shape the experience a customer eventually buys. BREW/LAB applies the same logic to strategy:

<div align="center">

### 🌱 SOURCE → 🔥 ROAST → ✦ BRAND → 🏷️ PRICE → ☕ SERVE → 🌍 SCALE

</div>

The simulation shows why these decisions cannot be optimized independently. **Roasting** can improve differentiation but fail when volume cannot cover its economics. **Organic sourcing** can strengthen willingness to pay. **Expansion** can create operating leverage—but only after the underlying operating model is strong enough to scale.

---

## Inside the analysis

### 01 · Executive Pulse
A fast view of portfolio performance, target achievement and the central strategic signal. Calculated KPIs are explicitly identified rather than mixed with workbook-reported values.

### 02 · Performance
Explore individual simulation runs, target multiples and annual operating trajectories. **Target Multiple = Game Total ÷ Target** provides a normalized comparison so Level 3's much larger absolute scale does not visually erase Levels 1 and 2.

### 03 · Decision Lab
The workbook's 14 experiments become an interactive profit-impact view. Selecting an experiment reveals the **question tested, change made, runs compared, measured effect and strategic implication**.

### 04 · Strategy Playbook
Individual experiments are translated into reusable managerial rules while preserving the boundary between **workbook evidence** and **interpretation**.

<div align="center">

## [▶ LAUNCH BREW/LAB — STRATEGY TO SCALE](https://shab-analytics.github.io/coffee-strategy-dashboard/)

</div>

---

## Analytical discipline

- **Reported simulation values remain reported values.**
- Calculated metrics are labelled as calculated.
- **Target Multiple** = `Game total ÷ Target`.
- **Target Achievement** = count of runs where `Game total ≥ Target`.
- Level 3 annual trajectory uses **Mature + Emerging operating profit by year**.
- That annual trajectory is **not** used to reconstruct the workbook-reported L3 game total because the workbook contains broader all-market/franchise information.
- Experiment effects remain tied to the runs compared and are not presented as universal causal estimates.

<details>
<summary><strong>Technical architecture & GitHub Pages deployment</strong></summary>

<br>

The experience is a static GitHub Pages site—no application server is required.

```text
coffee-strategy-dashboard/
├── index.html
├── styles.css
├── app.js
├── data.json
├── coffee-lifecycle.png
├── README.md
└── .nojekyll
```

Deploy from **Settings → Pages → main → / (root)**.

Live site: **https://shab-analytics.github.io/coffee-strategy-dashboard/**

</details>

---

<div align="center">

**BREW/LAB · STRATEGY TO SCALE**  
*Strategy performance, explained through evidence.*

</div>

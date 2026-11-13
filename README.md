# BREW/LAB — Coffee Shop Strategy Dashboard

A static, interactive GitHub Pages dashboard generated from **Coffee_Shop_Strategy_Review (1)(1).xlsx**.

## What is in the workbook

The source workbook contains 15 sheets. The dashboard uses:
- `Run Summary`: 15 simulation runs, five runs each for L1/L2/L3.
- `Data L1-L2`: 50 run-year records with location, roasting, coffee, pricing, stars, demand, revenue, costs and operating profit.
- `Data L3`: 50 market-year records split between Mature and Emerging markets.
- `Experiments & Playbook`: 14 strategic comparisons and 7 evidence-supported decision rules.

## Calculated metrics

- **Target achievement** = count of filtered runs where `Game total ($) >= Target ($)`.
- **Average game total** = arithmetic mean of `Game total ($)` for filtered runs.
- **Average target multiple** = mean of `Game total ($) / Target ($)`.
- **Level average** = arithmetic mean of the five `Game total ($)` values within each level.
- **L3 annual market operating profit** = Mature operating profit + Emerging operating profit for the selected year. This deliberately excludes franchise/all-markets results and is labelled as such in the dashboard.

## Run locally

The site has no build step and no external JavaScript dependencies. Open `index.html` directly in a modern browser. For a local web server, run:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy to GitHub Pages

1. Create a GitHub repository, for example `coffee-strategy-dashboard`.
2. Upload **all files in this folder** to the repository root.
3. Commit to the `main` branch.
4. Open **Settings → Pages**.
5. Under **Build and deployment**, choose **Deploy from a branch**.
6. Select **main** and **/(root)**, then save.
7. GitHub will show the published Pages URL after deployment.

## Updating the Excel data

The browser does not read `.xlsx` files directly. `data.js` and `data.json` are generated snapshots of the workbook.

When the workbook changes, regenerate those files from the updated workbook, keeping the same field names used by `app.js`. The safest workflow is to rerun the workbook-to-dashboard generator used to create this package. If columns/sheets are renamed, update the extraction mapping before publishing.

## Reliability and privacy

- No analytics, trackers, account credentials, or external APIs are included.
- No workbook formulas are executed in the browser.
- Missing chart data is handled by the dashboard's selection logic; unsupported fields are not fabricated.
- The site respects `prefers-reduced-motion` for accessibility.
- `data.json` is included for transparency and auditing; `data.js` is the browser-ready equivalent.

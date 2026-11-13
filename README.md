# BREW/LAB — Executive Coffee Strategy Dashboard

A static, responsive GitHub Pages dashboard generated from `Coffee_Shop_Strategy_Review (1)(1).xlsx`.

## Publish on GitHub Pages
1. Upload **all files in this folder** to the root of your `coffee-strategy-dashboard` repository.
2. In GitHub: **Settings → Pages → Deploy from a branch → main → /(root) → Save**.
3. Wait for the Pages deployment to complete, then hard-refresh the live URL.

## Files
- `index.html` — dashboard structure
- `styles.css` — executive visual system and responsive layout
- `app.js` — filters, charts, interactions, CSV export
- `data.json` — workbook-derived dashboard snapshot
- `.nojekyll` — prevents Jekyll processing

## Updating the data
This version is a static snapshot. When the Excel workbook changes, regenerate `data.json` from these workbook sheets: `Run Summary`, `Data L1-L2`, `Data L3`, and `Experiments & Playbook`. Do not hand-edit simulation results in the UI.

## Metric definitions
- **Average game total** = arithmetic mean of `Game total ($)` for runs currently shown.
- **Target achievement** = runs where `Game total ($) >= Target ($)` / runs shown.
- **Average target multiple** = mean of `Game total ($) / Target ($)`.
- For Level 3, the overall game total comes from `Run Summary`. The Mature + Emerging operating-profit series is used only as a trajectory view and is not presented as a reconstruction of the total.

## Design direction
The interface is original, but informed by contemporary executive analytics patterns: restrained typography, high information density, strong hierarchy, limited accent color, progressive disclosure, and low cognitive load.

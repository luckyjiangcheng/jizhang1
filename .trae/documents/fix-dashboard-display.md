# Plan: Fix Dashboard Display and Date Logic Issues

## Summary
The user reported that the dashboard is not displaying correctly. Based on the analysis of `src/dashboard.txt`, there are several potential issues:
1.  **Date Logic Bug**: The use of `toISOString()` causes transaction dates to shift to the previous day in UTC-based keys (e.g., in China UTC+8).
2.  **Interaction Crash**: The `switchSection` function uses the global `event` object which might be undefined in some WebViews, causing a crash when clicking navigation items.
3.  **UI/Logic Inconsistency**: The dashboard does not yet display the `Account` and `Notes` fields added in the recent update to `confirm.txt`.
4.  **Robustness**: Lack of explicit checks for the `echarts` library before usage.

## Current State Analysis
-   `src/dashboard.txt` and `public/dashboard.txt` are identical and synchronized.
-   The HTML/CSS structure is sound.
-   The core parsing logic is functional but sensitive to timezone offsets due to `toISOString()`.
-   Navigation items call a function (`switchSection`) that is incomplete and potentially buggy.

## Proposed Changes

### 1. Fix Date Handling (`src/dashboard.txt`)
-   **Why**: `toISOString()` returns UTC time, which causes dates to be off by one day for users in most timezones when used as keys or labels.
-   **How**: 
    -   Create a helper function `toLocalDateString(date)` that returns `YYYY-MM-DD` in local time.
    -   Use this helper for trend chart keys and date range labels.

### 2. Fix Navigation Interaction (`src/dashboard.txt`)
-   **Why**: Accessing `event.currentTarget` without passing `event` explicitly can throw a `ReferenceError`.
-   **How**: 
    -   Update HTML `onclick` attributes to pass `event`: `switchSection('trends', event)`.
    -   Update `switchSection` signature: `function switchSection(section, event)`.
    -   Add a safeguard: `const target = event ? event.currentTarget : null;`.

### 3. Update UI to Show New Fields (`src/dashboard.txt`)
-   **Why**: Users want to see the `Account` and `Notes` they recorded.
-   **How**: 
    -   Update `renderList` to include `item.Account` and `item.Notes` in the metadata line of each transaction.

### 4. Improve Chart Robustness (`src/dashboard.txt`)
-   **Why**: Ensure the dashboard doesn't crash if ECharts fails to load or if data is missing.
-   **How**: 
    -   Check `window.echarts` before calling `initChart`.
    -   Refine the `expenseData` filter to be more intuitive (handle negative amounts more consistently if possible).

### 5. Sync Assets
-   Run `python3 scripts/build.py` to ensure `public/dashboard.txt` is updated.

## Assumptions & Decisions
-   We assume the user is using the latest Shortcuts flow that renames the `.txt` to `.html`.
-   We decide to keep the `CSV_DATA_PLACEHOLDER` replacement as is but ensure the parsing around it is solid.
-   We assume "收入" is the only category name for income, or amounts are negative.

## Verification Steps
1.  **Syntax Check**: Ensure no JavaScript syntax errors are introduced.
2.  **Logic Verification**: Verify that the local date helper correctly handles the timezone offset.
3.  **Build Verification**: Run `build.py` and check the exit code.
4.  **Visual Check (Manual)**: The user will need to re-install or update the template to verify on their device.

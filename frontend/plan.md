# Frontend Bug Fix Plan

This document outlines the steps to fix 5 specific bugs in `frontend/index.html`.

## 1. Fix "Add Transaction" Failure
*   **Problem**: The `addTransaction` function fails silently or with vague errors.
*   **Fix**:
    *   Add comprehensive `try-catch` block.
    *   Validate `amount` (> 0) and `date` before sending.
    *   Display detailed error messages using `showToast`.
    *   Ensure the request body matches the backend schema exactly.

## 2. Fix "Stats Analysis" Month/Year Tab Switching
*   **Problem**: The `switchStatsPeriod` function is missing, causing buttons to be unresponsive.
*   **Fix**:
    *   Implement `switchStatsPeriod(period, btn)`.
    *   Update the `STATS_PERIOD` global variable.
    *   Calculate `start_date` and `end_date` for the selected period ("week", "month", "year").
    *   Call `loadStatsData(startDate, endDate)` and `loadCharts(period)` with the correct parameters.
    *   Update button active states (`.segment-btn.active`).

## 3. Fix "Set Budget" Button Response
*   **Problem**: The `showBudgetModal` function is missing.
*   **Fix**:
    *   Implement `showBudgetModal()`.
    *   Clear the budget form inputs.
    *   Call `openModal('budget-modal')`.

## 4. Fix "Create Family" Input Response
*   **Problem**: The `confirmCreateFamily` function lacks error handling and feedback.
*   **Fix**:
    *   Add `showLoading(true)` at the start.
    *   Add `try-catch` block for the API call.
    *   On success: `showToast('创建成功')`, close modal, reload family data.
    *   On failure: `showToast(error.message, 'error')`.
    *   Add `finally { showLoading(false) }`.

## 5. Remove Settings Tab
*   **Problem**: User requested removal of the "Settings" tab.
*   **Fix**:
    *   Remove "Settings" link from Sidebar (`<button ... data-tab="settings">`).
    *   Remove "Settings/Mine" link from Bottom Nav.
    *   Remove `<div id="settings-view">` block.
    *   **Preserve Critical Settings**:
        *   Move "API Server URL" input to the **Login View** (collapsible or footer).
        *   Add a **Logout** button to the top-right of the **Family View** (or Home View) for mobile users who lose the "Mine" tab.

## Implementation Details
*   Modify `frontend/index.html` exclusively.
*   Test each fix by verifying the code logic (since execution is not possible in this environment).

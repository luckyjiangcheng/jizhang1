# Tasks

- [x] Task 1: Define Unified Design Variables
  - [x] SubTask 1.1: Create a shared set of CSS variables (primary, bg, card-bg, text, border, radius, shadow) for both files.
  - [x] SubTask 1.2: Standardize primary color to `#007aff` (Apple-style blue).
  - [x] SubTask 1.3: Define consistent light and dark mode mappings for all variables.

- [x] Task 2: Redesign Confirmation Page (`src/confirm.txt`)
  - [x] SubTask 2.1: Update `:root` and `@media (prefers-color-scheme: dark)` with the unified variables.
  - [x] SubTask 2.2: Refine the `.card` styling (shadow, padding, border-radius).
  - [x] SubTask 2.3: Improve the `.chip` selection UI (active state, tap feedback, spacing).
  - [x] SubTask 2.4: Clean up input fields (typography, focus states, validation error presentation).
  - [x] SubTask 2.5: Standardize button styles (padding, radius, colors).

- [x] Task 3: Redesign Dashboard Page (`src/dashboard.txt`)
  - [x] SubTask 3.1: Update `:root` and `@media (prefers-color-scheme: dark)` with the same unified variables.
  - [x] SubTask 3.2: Redesign `.metric-card` to match the Confirmation card style.
  - [x] SubTask 3.3: Refine the `.tab-btn` styling for a more integrated tab-bar feel.
  - [x] SubTask 3.4: Polished ECharts styling (color palette, rounded line segments, minimal grid lines, consistent tooltip design).
  - [x] SubTask 3.5: Clean up the transaction list (typography, spacing, subtle separators).
  - [x] SubTask 3.6: Improve the empty state visual for no transactions.

- [x] Task 4: Final Polishing and Verification
  - [x] SubTask 4.1: Ensure smooth and consistent transitions between light and dark modes in both files.
  - [x] SubTask 4.2: Verify mobile responsiveness (iOS/Android) for all components.
  - [x] SubTask 4.3: Perform a visual "smoke test" to confirm the unified style is consistently applied.
  - [x] SubTask 4.4: Execute `python3 scripts/build.py` to update the `public` folder.

# Task Dependencies
- Task 2 and Task 3 both depend on Task 1.
- Task 4 depends on the completion of Task 2 and Task 3.

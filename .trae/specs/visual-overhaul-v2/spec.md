# Apple-Style UI Overhaul (V2) Spec

## Why
The user wants a more sophisticated and modern Apple-inspired UI for the "Confirmation" and "Dashboard" pages, specifically matching a reference image that features cleaner layouts, better information hierarchy, and intuitive icons.

## What Changes
- **Confirmation Page (`confirm.txt`)**:
  - **Prominent Amount Display**: Large, bold amount field with currency symbol.
  - **Category Icons**: Categories now include emojis (e.g., 🍔 Dining, 🚗 Transport).
  - **Enhanced Fields**: Added simulated "Account" selection and "Notes" textarea.
  - **Button Update**: Primary button labeled "Save Transaction".
  - **Layout**: Centered card with soft shadows and generous padding.
- **Dashboard Page (`dashboard.txt`)**:
  - **Tabbed Navigation**: "Overview", "Trends", "Categories", "Settings" tabs.
  - **Summary Metrics**: Three-column display for Income, Expenses, and Balance.
  - **Chart Layout**: Grid-based display for Spending Trends (Line) and Categories (Bar/Pie).
  - **Transaction List**: Redesigned list with category icons and formatted amounts.
  - **Floating Action Button (FAB)**: Added a fixed "+" button at the bottom right.
- **Unified Theme**: Shared CSS variables for colors, typography, and spacing to ensure a consistent experience across both files.

## Impact
- Affected files: `src/confirm.txt`, `src/dashboard.txt`.
- Data flow remains unchanged (JSON placeholder replacement and CSV generation).

## ADDED Requirements
### Requirement: Visual Fidelity to Reference
The system SHALL implement the visual layout and styling as depicted in the provided reference image.

#### Scenario: Responsive Behavior
- **WHEN** viewed on a mobile device
- **THEN** the Dashboard charts should stack vertically, and the Confirmation card should fill the screen width with appropriate margins.

### Requirement: Category Icons
The category selection SHALL include relevant emojis for each category to improve scannability.

## MODIFIED Requirements
### Requirement: Confirmation Page Buttons
The primary action button on the Confirmation page SHALL be labeled "Save Transaction" to match the reference UI.

### Requirement: Dashboard Summary
The Dashboard summary section SHALL display Income, Expenses, and Balance in a horizontal row on desktop and a flexible grid on mobile.

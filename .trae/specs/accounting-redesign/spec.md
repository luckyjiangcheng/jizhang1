# Redesign: Concise and Unified Style for Confirmation and Dashboard

## Why
The current "Confirmation" and "Dashboard" pages, while functional and modern, lack a unified design language. There are subtle differences in color palettes, spacing, and component styles that detract from a seamless user experience. This redesign aims to create a consistent, minimalist, and premium "Apple-style" feel across both pages to improve visual clarity and user satisfaction.

## What Changes
- **Unified Design System**: Establish a shared set of CSS variables for colors, typography, spacing, border-radius, and shadows.
- **Consistent Color Palette**: Standardize on a refined blue primary color (`#007aff`) and a consistent set of neutral grays for light and dark modes.
- **Confirmation Page (`confirm.txt`)**:
  - Compact form layout with improved visual hierarchy.
  - Refined "Chip" components for category selection with better active states.
  - Consistent card styling (shadows, padding, radius).
  - Subtle micro-interactions for input focus and button states.
- **Dashboard Page (`dashboard.txt`)**:
  - Metric cards redesign to match the "Confirmation" card style.
  - Polished ECharts styling (softer colors, rounded line segments, minimal grid lines).
  - Cleaner transaction list with improved typography and spacing.
  - Consistent tab bar styling.
- **Robust Dark Mode**: Ensure seamless and consistent dark mode transitions for all UI elements and charts.

## Impact
- Affected files: `src/confirm.txt`, `src/dashboard.txt`.
- No breaking changes to data flow or logic; this is purely a UI/UX overhaul.

## ADDED Requirements
### Requirement: Unified Visual Identity
The system SHALL use a shared design language defined by a common set of CSS variables in both `confirm.txt` and `dashboard.txt`.

#### Scenario: Switching between pages
- **WHEN** a user moves from the Confirmation page to the Dashboard
- **THEN** the primary color, font weights, card radius, and overall "feel" should remain identical.

### Requirement: Minimalist Chart Aesthetics
The Dashboard charts SHALL prioritize clarity and minimalism, using a soft, coordinated color palette and removing non-essential visual clutter (e.g., heavy grid lines, borders).

#### Scenario: Viewing the Trend Chart
- **WHEN** the trend chart is rendered
- **THEN** it should use smooth line interpolation and a subtle area fill, with colors consistent with the unified design system.

## MODIFIED Requirements
### Requirement: Category Selection (Confirm Page)
The category selection Chips SHALL have a more distinct "active" state that uses the primary color with high contrast text, and a "hover/tap" state that provides clear visual feedback.

### Requirement: Metric Cards (Dashboard)
The metric cards in the Dashboard SHALL be visually consistent with the main card in the Confirmation page, using the same border-radius and shadow values.

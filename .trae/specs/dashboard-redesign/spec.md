# Dashboard Redesign Spec

## Why
The user wants to transition from a budget-focused tool to a comprehensive expense analysis dashboard. The goal is to improve aesthetics and provide deeper insights through various visualizations (trend, scatter, detailed tables) and flexible time aggregation (Day, Week, Month, Year) with comparison capabilities.

## What Changes
- **Remove** all budget-related logic (hardcoded limit, progress bars, warning colors).
- **Refactor** `src/dashboard.txt` to use a tabbed interface for different views (Overview, Trends, Details).
- **Add** time range filtering (Start Date, End Date) affecting all charts.
- **Add** data aggregation logic for different granularities: Day, Week, Month, Year.
- **Add** new visualizations using ECharts:
    - **Trend Chart**: Bar/Line chart showing spending over time with YoY/MoM comparison.
    - **Scatter Plot**: Date vs Amount (colored by Category) to spot outliers.
    - **Detailed Table**: A sortable/filterable HTML table of transactions.
- **Improve** UI styling for a modern, clean look (using custom CSS).

## Impact
- **Affected specs**: Replaces the logic defined in the original `zenledger` dashboard task.
- **Affected code**: `src/dashboard.txt` (complete rewrite of the internal HTML/JS).
- **No new files**: All logic must be contained within `src/dashboard.txt`.

## ADDED Requirements
### Requirement: Time Filtering & Aggregation
The system SHALL allow users to select a date range.
The system SHALL support grouping data by Day, Week, Month, and Year.

### Requirement: Advanced Visualizations
The system SHALL display:
- **Trend Chart**: Spending amount over the selected granularity.
- **Scatter Plot**: Individual transactions plotted by Time (X) and Amount (Y).
- **Category Breakdown**: Pie/Donut chart.
- **Comparison**: Visual indicator or secondary line showing previous period's data (e.g., same month last year).

### Requirement: Tabbed UI
The system SHALL organize content into tabs:
- **Dashboard**: Summary cards, Trend Chart, Pie Chart.
- **Analysis**: Scatter Plot, YoY Comparison.
- **Details**: Data Table.

## MODIFIED Requirements
### Requirement: Dashboard Logic
**Modified**: The dashboard no longer calculates budget adherence. Instead, it focuses on historical analysis and trends.

## REMOVED Requirements
### Requirement: Budget
**Reason**: User explicitly requested to remove budget features.

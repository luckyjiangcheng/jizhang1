# Tasks

- [x] Task 1: Create Dashboard Redesign Structure
  - [x] SubTask 1.1: Refactor `src/dashboard.txt` with a responsive HTML5 layout using CSS Grid/Flexbox for a modern look.
  - [x] SubTask 1.2: Implement tab navigation logic (Dashboard, Analysis, Details) in vanilla JS.
  - [x] SubTask 1.3: Add date range picker inputs and granularity selector (Day, Week, Month, Year).

- [x] Task 2: Implement Data Processing Logic
  - [x] SubTask 2.1: Implement CSV parsing to JSON objects (Date, Amount, Category, etc.).
  - [x] SubTask 2.2: Implement filtering logic based on selected date range.
  - [x] SubTask 2.3: Implement aggregation logic (group by Day/Week/Month/Year) for charts.
  - [x] SubTask 2.4: Implement comparison logic (e.g., calculate YoY or MoM percentage change).

- [x] Task 3: Implement Visualizations
  - [x] SubTask 3.1: **Trend Chart**: Line/Bar chart showing spending over time with granularity support.
  - [x] SubTask 3.2: **Category Pie Chart**: Interactive pie chart with drill-down capabilities (if possible, otherwise simple breakdown).
  - [x] SubTask 3.3: **Scatter Plot**: Date vs Amount scatter plot colored by Category to identify outliers.
  - [x] SubTask 3.4: **Summary Cards**: Total Spend, Avg Spend, Max Spend, Comparison % (YoY/MoM).

- [x] Task 4: Implement Detail View
  - [x] SubTask 4.1: Render a sortable HTML table with transaction details.
  - [x] SubTask 4.2: Add simple pagination or infinite scroll if data is large (optional, start with simple list).

- [x] Task 5: Final Polish & Verification
  - [x] SubTask 5.1: Ensure all charts resize correctly on window resize.
  - [x] SubTask 5.2: Verify data correctness with sample data.
  - [x] SubTask 5.3: Check mobile responsiveness (since it runs on iPhone).

# Task Dependencies
- Task 3 depends on Task 2 (Data Processing).
- Task 4 depends on Task 2.

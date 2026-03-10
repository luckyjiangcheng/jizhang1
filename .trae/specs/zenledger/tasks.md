# Tasks

- [x] Task 1: Project Initialization & Prompt Engineering
  - [x] SubTask 1.1: Create project structure (folders for src, docs).
  - [x] SubTask 1.2: Design and write the System Prompt for Gemini 1.5 Pro to parse screenshots and voice text into CSV format. Save as `src/prompt.txt`.
  - [x] SubTask 1.3: Create a sample CSV file `src/sample_data.csv` for testing the dashboard.

- [x] Task 2: Analysis Dashboard Implementation
  - [x] SubTask 2.1: Create `src/dashboard.html` with basic layout.
  - [x] SubTask 2.2: Integrate ECharts library (via CDN or local) into `dashboard.html`.
  - [x] SubTask 2.3: Implement CSV parsing logic in JavaScript to read data injected by Shortcuts.
  - [x] SubTask 2.4: Implement "Consumption Pie Chart" (消费饼图) logic.
  - [x] SubTask 2.5: Implement "Monthly Budget Curve" (月度预算曲线) logic.
  - [x] SubTask 2.6: Implement "Budget Warning" (预算预警) logic (background color change).

- [x] Task 3: Shortcut Logic Documentation/Scripting
  - [x] SubTask 3.1: Document the specific steps required to build the iOS Shortcut (since we cannot generate `.shortcut` files directly). Create `docs/shortcut_guide.md`.
  - [x] SubTask 3.2: Include the logic for API Key configuration and iCloud Drive file paths in the documentation.
  - [x] SubTask 3.3: Create a helper script (optional, e.g., Python) to test the Gemini API with the prompt and sample images/text to verify the "Brain" logic locally.

- [x] Task 4: Final Verification & Cleanup
  - [x] SubTask 4.1: Verify the dashboard using the sample CSV.
  - [x] SubTask 4.2: Verify the prompt efficacy using the helper script.
  - [x] SubTask 4.3: Finalize `README.md` with "Easy Setup" instructions.

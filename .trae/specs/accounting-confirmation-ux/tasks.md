# Tasks

- [ ] Task 1: 优化 Prompt 输出格式 (JSON)
  - [ ] SubTask 1.1: 修改 `src/prompt.txt`，要求输出格式为标准 JSON 对象。
  - [ ] SubTask 1.2: 验证 Prompt 在多场景下（语音、图片）输出 JSON 的稳定性。

- [ ] Task 2: 设计并开发确认页模板 (`src/confirm.txt`)
  - [ ] SubTask 2.1: 使用 HTML5 + CSS3 创建一个移动端风格的精美表单（参考截图风格：圆角、阴影、大标题）。
  - [ ] SubTask 2.2: 实现 JavaScript 逻辑：
    - [ ] 接收 AI 识别的 JSON 数据并填充表单。
    - [ ] 实现日期/时间选择器。
    - [ ] 实现类目选择器（下拉或 Chip 标签）。
    - [ ] 点击“确认”时，生成最终的 CSV 字符串。
    - [ ] 调用 `completion()` 或复制到剪贴板，以便快捷指令获取。

- [ ] Task 3: 更新开发者指南 (`docs/developer_distribution_guide.md`)
  - [ ] SubTask 3.1: 更新“安装器”流程：
    - [ ] 增加下载 `confirm.txt` 的步骤。
    - [ ] 路径：`ZenLedger/confirm.txt`。
  - [ ] SubTask 3.2: 更新“主程序”流程：
    - [ ] 逻辑变更为：API 调用 -> 获取 JSON -> 读取 `confirm.txt` -> 替换 JSON 占位符 -> 显示网页视图 -> 获取网页输出 -> 写入 CSV。
    - [ ] 增加“显示通知”步骤。

- [ ] Task 4: 更新构建脚本 (`scripts/build.py`)
  - [ ] SubTask 4.1: 将 `src/confirm.txt` 加入打包流程。
  - [ ] SubTask 4.2: 确保 `public/confirm.txt` 生成正确。

- [ ] Task 5: 验证与测试
  - [ ] SubTask 5.1: 验证 Prompt 输出的 JSON 能被 HTML 正确解析。
  - [ ] SubTask 5.2: 验证 HTML 表单修改后的数据能正确传回快捷指令。
  - [ ] SubTask 5.3: 验证最终 CSV 写入格式无误。

# Task Dependencies
- Task 2 依赖 Task 1 (Prompt 确定后，HTML 才能解析数据)。
- Task 4 依赖 Task 2。

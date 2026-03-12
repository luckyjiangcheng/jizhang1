# ZenLedger 开发者分发指南

本指南教您如何作为开发者，构建并发布 ZenLedger 快捷指令，以便普通用户可以通过 iCloud 链接一键安装。

## 架构说明

*   **Installer (安装器)**: 这是一个一次性的快捷指令。用户运行它，输入 API Key，它会自动从网络下载配置文件和模板，并在用户的 iCloud Drive 中创建必要的文件夹结构。
*   **Main App (主程序)**: 这是一个通用的快捷指令。它只读取本地配置文件，不包含任何敏感信息。
*   **Static Resources (静态资源)**: 托管在 GitHub Pages 上的 `config_template.json` 和 `dashboard.html`，供安装器下载。

---

## 第一步：准备静态资源服务器

1.  将本项目推送到 GitHub。
2.  在 GitHub 仓库设置中，开启 **GitHub Pages**，源选择 `public` 文件夹（如果无法选择子文件夹，可能需要通过 GitHub Actions 或将 public 内容推送到独立分支，最简单的方式是将 public 内容直接放在根目录或 `docs` 目录）。
    *   *建议*：为了简单起见，您可以直接将 `public` 文件夹内的文件上传到一个支持直链的图床或对象存储（如 OSS/S3），或者直接使用 GitHub Raw 链接（注意缓存问题）。
    *   假设您的资源 URL 为：
        *   `https://luckyjiangcheng.github.io/jizhang1/public/config.json`
        *   `https://luckyjiangcheng.github.io/jizhang1/public/dashboard.txt`

---

## 第二步：制作 "ZenLedger Installer" (安装器)

在您的 iPhone 上创建一个新的快捷指令，命名为 **`ZenLedger Installer`**。

1.  **获取 URL 内容**:
    *   URL: `https://luckyjiangcheng.github.io/jizhang1/public/config.json` (包含您预设 API Key 的静态资源地址)
2.  **获取字典**: 从 URL 内容获取字典。
3.  **保存文件**:
    *   文件: 上一步的字典
    *   路径: `Shortcuts/ZenLedger/config.json` (开启覆盖)
4.  **获取 URL 内容**:
    *   URL: `https://luckyjiangcheng.github.io/jizhang1/public/dashboard.txt`
5.  **保存文件**:
    *   路径: `Shortcuts/ZenLedger/dashboard.txt` (开启覆盖)
6.  **获取 URL 内容**:
    *   URL: `https://luckyjiangcheng.github.io/jizhang1/public/confirm.txt`
7.  **保存文件**:
    *   路径: `Shortcuts/ZenLedger/confirm.txt` (开启覆盖)
8.  **创建文件夹**: (如果需要) 确保 `ZenLedger` 存在。
9.  **文本**: 输入 `Date,Time,Amount,Category,Item,Merchant`
10. **将文本保存到文件**:
    *   文件: 上一步的文本
    *   路径: `Shortcuts/ZenLedger/ZenLedger.csv`
    *   **重要设置**: 点击“展开”，取消勾选“覆盖（如果文件存在）”。
    *   *说明*：这样如果 CSV 文件已经存在（里面有用户的旧账本），就不会被覆盖；如果不存在，则会创建一个新的并写入表头。
9.  **显示提醒**: "环境配置完成！即将安装主程序。"
10. **打开 URL**: (填入第三步生成的主程序分享链接)

> **完成后**：点击分享按钮 -> 拷贝 iCloud 链接。这就是发给用户的 **链接 A**。

---

## 第三步：制作 "ZenLedger" (主程序)

这是一个**三合一**的快捷指令。请在 iPhone 上创建一个新的快捷指令，命名为 **`ZenLedger`**。

### 1. 读取全局配置
1.  **获取文件**:
    *   路径: `Shortcuts/ZenLedger/config.json`
    *   (如果不存，提示用户先运行安装器)
2.  **获取字典**: 从上一步的文件获取字典。
3.  **获取字典值**: 分别获取以下值并存为变量：
    *   `api_key`
    *   `api_base`
    *   `text_model`
    *   `vision_model`
    *   `system_prompt`

### 2. 创建主菜单
4.  **从菜单中选择**:
    *   提示: "请选择操作"
    *   选项 1: 🎙️ 语音记账
    *   选项 2: 📷 截图记账
    *   选项 3: 📊 查看账单

### 3. 分支逻辑 A：语音记账
5.  **在“🎙️ 语音记账”下**:
    *   **听写文本**: 语言选中文。
    *   **获取当前日期**: 格式选择 `自定义: yyyy-MM-dd` (结果存为变量 `CurrentDate`)。
    *   **获取 URL 内容** (调用 API):
        *   ... (API调用部分保持不变)
        *   (这一步获取到的结果是 AI 生成的 JSON，例如 `{"amount": 12.00, ...}`)
        *   (我们将这个结果存为变量 **AIResult**)
    *   **获取文件**:
        *   路径: `Shortcuts/ZenLedger/confirm.txt`
        *   (存为变量 **ConfirmTemplate**)
    *   **替换文本**:
        *   查找: `JSON_DATA_PLACEHOLDER`
        *   替换为: 变量 **AIResult**
        *   在: 变量 **ConfirmTemplate**
        *   (存为变量 **ConfirmHTML**)
    *   **设置名称** (Set Name):
        *   输入: 变量 **ConfirmHTML**
        *   名称: `confirm.html`
    *   **显示网页视图**:
        *   输入: 上一步的结果
        *   (用户在网页中点击确认后，网页会显示最终的 CSV 字符串)
        *   (Shortcuts 会自动获取网页显示的文本)
        *   (存为变量 **FinalCSV**)
    *   **如果** (If): 变量 **FinalCSV** 有值
        *   **追加到文件**:
            *   文件: 变量 **FinalCSV**
            *   路径: `Shortcuts/ZenLedger/ZenLedger.csv`
        *   **显示通知**: "✨ 记账成功！"
    *   **否则**:
        *   **显示通知**: "已取消记账"
    *   **结束如果**

### 4. 分支逻辑 B：截图记账
6.  **在“📷 截图记账”下**:
    *   **截取屏幕**。
    *   **Base64 编码**: 换行选“无”。
    *   **获取当前日期**: 格式选择 `自定义: yyyy-MM-dd` (结果存为变量 `CurrentDate`)。
    *   **获取 URL 内容** (调用 API):
        *   ... (API调用部分保持不变)
        *   (这一步获取到的结果存为变量 **AIResult**)
    *   **获取文件**:
        *   路径: `Shortcuts/ZenLedger/confirm.txt`
        *   (存为变量 **ConfirmTemplate**)
    *   **替换文本**:
        *   查找: `JSON_DATA_PLACEHOLDER`
        *   替换为: 变量 **AIResult**
        *   在: 变量 **ConfirmTemplate**
        *   (存为变量 **ConfirmHTML**)
    *   **设置名称** (Set Name):
        *   输入: 变量 **ConfirmHTML**
        *   名称: `confirm.html`
    *   **显示网页视图**:
        *   输入: 上一步的结果
        *   (用户在网页中点击确认后，网页会显示最终的 CSV 字符串)
        *   (Shortcuts 会自动获取网页显示的文本)
        *   (存为变量 **FinalCSV**)
    *   **获取 URL 的内容** (Get Contents of URL):
        *   URL: `data:text/html,` + 变量 **FinalCSV**
        *   (这是一个Hack技巧：网页视图返回的结果虽然看起来是文本，但有时会被包装成 WebArchive。通过这个动作可以强制把它转为纯文本。)
        *   (或者更简单：直接使用 **从输入中获取文本** (Get Text from Input) 动作，输入选 **FinalCSV**)
        *   *修正步骤*：添加动作 **从输入中获取文本**，输入选择 **FinalCSV**。结果存为 **TrueCSVString**。
    *   **如果** (If): 变量 **TrueCSVString** 有值
        *   **追加到文件**:
            *   文件: 变量 **TrueCSVString**
            *   路径: `Shortcuts/ZenLedger/ZenLedger.csv`
        *   **删除照片**: 输入为“屏幕快照”。
        *   **显示通知**: "✨ 记账成功！"
    *   **否则**:
        *   **显示通知**: "已取消记账"
    *   **结束如果**

### 5. 分支逻辑 C：查看账单
7.  **在“📊 查看账单”下**:
    *   **获取文件**:
        *   路径: `Shortcuts/ZenLedger/ZenLedger.csv`
        *   *注意：一定要带上 .csv 后缀*。
        *   (这一步获取到的结果，我们称之为变量 **CSVData**)
    *   **获取文件**:
        *   路径: `Shortcuts/ZenLedger/dashboard.txt`
        *   (因为是 .txt，iOS 会直接把它当作文本读取，不会去渲染它)
        *   (这一步获取到的结果，我们称之为变量 **HTMLTemplate**)
    *   **替换文本**:
        *   查找: `CSV_DATA_PLACEHOLDER`
        *   替换为: 选择变量 **CSVData**
        *   在: 选择变量 **HTMLTemplate**
        *   (这一步生成的结果是“更新后的文本”)
    *   **设置名称** (Set Name):
        *   输入: 选择上一步的 **“更新后的文本”**
        *   名称: `dashboard.html`
        *   (这一步是为了让 iOS 知道这是一段 HTML 代码，以便后续渲染)
    *   **显示网页视图**:
        *   输入: 选择上一步 **“设置名称后的项目”**

> **完成后**：点击分享按钮 -> 拷贝 iCloud 链接。这就是 **链接 B**（填入安装器的最后一步）。

---

## 第四步：发布给用户

您只需要把 **链接 A (安装器)** 发给用户即可。

**用户操作流程：**
1.  用户点击链接 A，安装 `ZenLedger Installer`。
2.  用户运行 `Installer`，粘贴 API Key。
3.  Installer 自动配置环境，并自动弹出链接 B。
4.  用户点击链接 B，安装 `ZenLedger` 主程序。
5.  **完成！** 用户只需运行主程序即可使用。

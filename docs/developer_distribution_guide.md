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
        *   `https://your-username.github.io/zenledger/config_template.json`
        *   `https://your-username.github.io/zenledger/dashboard.html`

---

## 第二步：制作 "ZenLedger Installer" (安装器)

在您的 iPhone 上创建一个新的快捷指令，命名为 **`ZenLedger Installer`**。

1.  **获取 URL 内容**:
    *   URL: `https://your-username.github.io/zenledger/config.json` (包含您预设 API Key 的静态资源地址)
2.  **获取字典**: 从 URL 内容获取字典。
3.  **保存文件**:
    *   文件: 上一步的字典
    *   路径: `Shortcuts/ZenLedger/config.json` (开启覆盖)
4.  **获取 URL 内容**:
    *   URL: `https://your-username.github.io/zenledger/dashboard.html`
5.  **保存文件**:
    *   路径: `Shortcuts/ZenLedger/dashboard.html` (开启覆盖)
6.  **创建文件夹**: (如果需要) 确保 `Shortcuts/ZenLedger` 存在。
7.  **文本**: 输入 `Date,Time,Amount,Category,Item,Merchant`
8.  **保存文件**:
    *   文件: 上一步的文本
    *   路径: `Shortcuts/ZenLedger/ZenLedger.csv` (关闭覆盖，仅当文件不存在时创建，或者检查文件是否存在) -> *为了简化，可以直接覆盖或者用“追加到文件”如果不存的话*。
    *   *建议逻辑*：获取文件 `ZenLedger.csv` -> 如果报错 -> 保存文本到 `ZenLedger.csv`。
9.  **显示提醒**: "环境配置完成！即将安装主程序。"
10. **打开 URL**: (填入第三步生成的主程序分享链接)

> **完成后**：点击分享按钮 -> 拷贝 iCloud 链接。这就是发给用户的 **链接 A**。

---

## 第三步：制作 "ZenLedger" (主程序)

创建一个新的快捷指令，命名为 **`ZenLedger`**。

1.  **获取文件**: `Shortcuts/ZenLedger/config.json` -> 获取字典 -> 存为变量 `Config`。
2.  **从菜单中选择**:
    *   选项 1: 🎙️ 语音记账
    *   选项 2: 📷 截图记账
    *   选项 3: 📊 查看账单
3.  **如果选择 语音记账**:
    *   听写文本 -> 调用 API (使用 `Config` 中的 `api_key` 等参数) -> 追加到 CSV。
4.  **如果选择 截图记账**:
    *   截屏 -> Base64 -> 调用 API (使用 `Config` 中的 `vision_model` 等参数) -> 追加到 CSV。
5.  **如果选择 查看账单**:
    *   获取 CSV -> 获取 HTML -> 替换文本 -> 显示网页。

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

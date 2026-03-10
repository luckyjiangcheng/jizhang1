# iOS 快捷指令手把手配置指南

本指南将一步步教您在 iPhone 上创建快捷指令。
**前提条件**：您已经将电脑上的 `ZenLedger` 文件夹放入了 iCloud Drive 的 `Shortcuts` 文件夹中。

---

## 准备工作：检查 iCloud 文件

1.  在 iPhone 上打开 **“文件” (Files)** App。
2.  点击底部的 **“浏览”** -> **“iCloud 云盘”** -> **“Shortcuts”**。
3.  确保里面有一个 **`ZenLedger`** 文件夹，点进去应该能看到 `config.json` 等文件。

---

## 🎯 任务一：创建“语音记账”

这个指令最简单，适合练手。

1.  **新建指令**
    *   打开 **“快捷指令” (Shortcuts)** App。
    *   点击右上角的 **`+`** 号。
    *   点击顶部的 **“新建快捷指令”**，重命名为 **“语音记账”**。

2.  **步骤 1：读取配置**
    *   点击底部的 **“搜索 App 和操作”**，搜索 **“获取文件”** (Get File) 并添加。
    *   点击动作里的 `文件`，手动输入路径：`ZenLedger/config.json`。
    *   确保关闭了“显示文档选择器”。
    *   **搜索并添加**：**“获取字典”** (Get Dictionary from Input)。
    *   系统会自动将上一步的文件作为输入。

3.  **步骤 2：听写内容**
    *   **搜索并添加**：**“听写文本”** (Dictate Text)。
    *   点击展开箭头 `>`，语言选择 **“中文”**。

4.  **步骤 3：准备 API 参数**
    *   我们需要从配置字典里提取 4 个值：`api_base`, `api_key`, `text_model`, `system_prompt`。
    *   **搜索并添加**：**“获取字典值”** (Get Dictionary Value)。
        *   键 (Key) 填：`api_base`
        *   字典选择：步骤 1 的 **“字典”**。
    *   **重复添加 3 次“获取字典值”**：
        *   键：`api_key` (字典选步骤 1 的“字典”)
        *   键：`text_model` (字典选步骤 1 的“字典”)
        *   键：`system_prompt` (字典选步骤 1 的“字典”)

5.  **步骤 4：调用 AI (核心)**
    *   **搜索并添加**：**“获取 URL 内容”** (Get Contents of URL)。
    *   **URL**: 点击参数框，选择键盘上方的 **“变量”** (魔术棒图标) -> 选择步骤 4 获取的 `api_base` 值。
        *   然后在后面手动输入：`/chat/completions`
    *   **方法**: 选择 **`POST`**。
    *   **头部 (Headers)**:
        *   点击 `+` 添加新头部。
        *   键: `Authorization`
        *   值: 输入 `Bearer ` (注意有个空格)，然后选择变量 `api_key`。
        *   点击 `+` 再添加一个。
        *   键: `Content-Type`
        *   值: `application/json`
    *   **请求体 (Request Body)**: 选择 **`JSON`**。
        *   点击 **“添加新字段”** -> **文本**。
            *   键: `model`
            *   值: 选择变量 `text_model`。
        *   点击 **“添加新字段”** -> **数组**。
            *   键: `messages`
            *   点击 `messages` 下面的 **“添加新项”** -> **字典**。
                *   点击 `项 1` 下面的 **“添加新字段”** -> **文本** -> 键 `role` 值 `system`。
                *   点击 `项 1` 下面的 **“添加新字段”** -> **文本** -> 键 `content` 值 变量 `system_prompt`。
            *   点击 `messages` 下面的 **“添加新项”** -> **字典**。
                *   点击 `项 2` 下面的 **“添加新字段”** -> **文本** -> 键 `role` 值 `user`。
                *   点击 `项 2` 下面的 **“添加新字段”** -> **文本** -> 键 `content` 值：
                    *   先选择变量 **“听写文本”**。
                    *   然后手动输入：` (Today is `
                    *   点击键盘上方的 **“当前日期”**
                    *   手动输入：`)`
        *   点击 **“添加新字段”** -> **数字**。
            *   键: `temperature`
            *   值: `0.1`

6.  **步骤 5：处理结果**
    *   **搜索并添加**：**“获取字典值”**。
        *   键: `choices.1.message.content`
        *   字典: 选择上一步的 **“URL 的内容”**。
    *   **搜索并添加**：**“追加到文件”** (Append to File)。
        *   文本: 选择上一步的 **“字典值”**。
        *   文件路径: `ZenLedger/ZenLedger.csv`。
        *   **重要**: 点击展开箭头 `>`，确保 **“追加新行”** 是开启的。
    *   **搜索并添加**：**“朗读文本”**。
        *   文本输入：“记好了”。

---

## 🎯 任务二：创建“一键截图记账”

这个稍微复杂一点，因为要处理图片。

1.  **新建指令**，重命名为 **“一键截图记账”**。

2.  **步骤 1：读取配置** (同上)
    *   获取文件 `ZenLedger/config.json` -> 获取字典。
    *   提取变量：`api_base`, `api_key`, `vision_model`, `system_prompt`。

3.  **步骤 2：获取并处理截图**
    *   **搜索并添加**：**“截取屏幕”** (Take Screenshot)。
    *   **搜索并添加**：**“Base64 编码”**。
        *   输入: **“屏幕快照”**。
        *   **重要**: 点击展开箭头 `>`，**“换行”** 选择 **“无”** (None)。

4.  **步骤 3：调用 AI**
    *   **搜索并添加**：**“获取 URL 内容”**。
    *   URL: 变量 `api_base` + `/chat/completions`。
    *   方法: `POST`。
    *   头部: 同上 (`Authorization`, `Content-Type`)。
    *   请求体 (JSON):
        *   `model`: 变量 `vision_model`。
        *   `messages` (数组):
            *   Item 1 (字典): `role`=`system`, `content`=变量 `system_prompt`。
            *   Item 2 (字典): `role`=`user`。
                *   在此字典下添加 `content` (数组)。
                    *   Item 1 (字典): `type`=`text`, `text`=`Extract details`。
                    *   Item 2 (字典): `type`=`image_url`。
                        *   在此字典下添加 `image_url` (字典)。
                            *   在此字典下添加 `url` (文本): 输入 `data:image/jpeg;base64,` 然后拼接变量 **“Base64 编码”**。
        *   `temperature`: `0.1`。

5.  **步骤 4：保存结果** (同上)
    *   获取 `choices.1.message.content` -> 追加到 `ZenLedger/ZenLedger.csv`。
    *   **搜索并添加**：**“删除照片”** (Delete Photos)。
        *   输入: **“屏幕快照”** (这一步是为了不让截图占满相册)。

---

## 🎯 任务三：创建“查看账单”

1.  **新建指令**，重命名为 **“查看账单”**。
2.  **搜索并添加**：**“获取文件”**。
    *   路径: `ZenLedger/ZenLedger.csv`。
    *   重命名此变量为 **“CSV数据”**。
3.  **搜索并添加**：**“获取文件”**。
    *   路径: `ZenLedger/dashboard.html`。
    *   重命名此变量为 **“HTML模板”**。
4.  **搜索并添加**：**“替换文本”** (Replace Text)。
    *   查找: `/* CSV_DATA_PLACEHOLDER */` (注意空格要完全一致)。
    *   替换为: 变量 **“CSV数据”**。
    *   在: 变量 **“HTML模板”**。
5.  **搜索并添加**：**“显示网页视图”** (Show Web View)。
    *   输入: 上一步的 **“更新后的文本”**。

---
🎉 **大功告成！**
现在您可以对着 Siri 说“语音记账”，或者在手机背面轻点两下触发“一键截图记账”了！

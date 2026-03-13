import os
import json
import shutil
from pathlib import Path

def build_public():
    # 1. Define paths
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / "src"
    public_dir = root_dir / "public"
    
    # Clean and create public dir
    if public_dir.exists():
        shutil.rmtree(public_dir)
    public_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Building public resources in: {public_dir}")

    # 2. Read Config (for API Key and Models)
    config_path = src_dir / "config.json"
    api_key = "sk-ohgicalwixwraxcmzckymthpjnktwzokmuzrakwtbkibxabf"
    text_model = "Qwen/Qwen2.5-7B-Instruct"
    vision_model = "Qwen/Qwen2-VL-72B-Instruct"

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            api_key = config.get("api_key", api_key)
            text_model = config.get("text_model", text_model)
            vision_model = config.get("vision_model", vision_model)
    except Exception as e:
        print(f"Warning: Could not read config.json: {e}")

    # 3. Read Prompt
    prompt_path = src_dir / "prompt.txt"
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_content = f.read()
    except Exception as e:
        print(f"Error: Could not read prompt.txt: {e}")
        return

    # 4. Create CSV Prompt
    csv_prompt = '''你是一个专业的交易数据提取助手，只从用户提供的小票、文字、语音内容里把消费信息提取成一行 CSV 格式，只输出 CSV，不输出任何多余内容。
 输出格式为 Date,Time,Amount,Category,Item,Merchant。
 日期格式 YYYY-MM-DD，不能为空，优先用内容明确日期，无则按今天 / 昨天 / 前天结合当前日期计算，仍无则用当前日期。
 时间格式 HH:MM，未知填空（直接留空，不要加引号）。
 金额为纯数字，无货币符号，未知填 0。
 分类必须从餐饮美食、交通出行、购物消费、居家生活、休闲娱乐、人情往来、医疗健康、教育培训、金融保险、孝敬父母、其他中选一个，未知填空（直接留空，不要加引号）。
 项目为简短中文描述，未知填空（直接留空，不要加引号）。
 商家为名称，未知填空（直接留空，不要加引号）。
 空字段直接留空，不要用任何引号包围，只输出一行 CSV，不要表头、解释、JSON、符号、换行。'''

    # 5. Create Public Config (WITH API Key)
    config_public = {
        "api_key": api_key,
        "api_base": "https://api.siliconflow.cn/v1",
        "text_model": text_model,
        "vision_model": vision_model,
        "system_prompt": prompt_content,
        "jj_prompt": csv_prompt
    }
    
    with open(public_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_public, f, indent=4, ensure_ascii=False)
    print("✓ Created config.json (with API Key)")

    # 4. Copy Dashboard & Confirm Templates
    try:
        shutil.copy2(src_dir / "dashboard.txt", public_dir / "dashboard.txt")
        print("✓ Copied dashboard.txt")
        shutil.copy2(src_dir / "confirm.txt", public_dir / "confirm.txt")
        print("✓ Copied confirm.txt")
    except Exception as e:
        print(f"Error copying templates: {e}")

    # 5. Create index.html (Simple landing page)
    index_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ZenLedger Resources</title>
</head>
<body>
    <h1>ZenLedger Resources</h1>
    <p>This page hosts static resources for ZenLedger Shortcuts.</p>
    <ul>
        <li><a href="config.json">Config Template</a></li>
        <li><a href="dashboard.txt">Dashboard Template (TXT)</a></li>
        <li><a href="confirm.txt">Confirmation Page Template (TXT)</a></li>
    </ul>
</body>
</html>
    """
    with open(public_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✓ Created index.html")

    print("\nPublic Build Complete!")
    print(f"ACTION REQUIRED: Push the 'public' folder to GitHub Pages or any static host.")

if __name__ == "__main__":
    build_public()

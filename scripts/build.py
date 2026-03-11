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

    # 2. Read Config (for API Key)
    config_path = src_dir / "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            api_key = config.get("api_key", "sk-ohgicalwixwraxcmzckymthpjnktwzokmuzrakwtbkibxabf")
    except Exception as e:
        print(f"Warning: Could not read config.json: {e}")
        api_key = "sk-ohgicalwixwraxcmzckymthpjnktwzokmuzrakwtbkibxabf"

    # 3. Read Prompt
    prompt_path = src_dir / "prompt.txt"
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_content = f.read()
    except Exception as e:
        print(f"Error: Could not read prompt.txt: {e}")
        return

    # 4. Create Public Config (WITH API Key)
    config_public = {
        "api_key": api_key,
        "api_base": "https://api.siliconflow.cn/v1",
        "text_model": "deepseek-ai/DeepSeek-V3",
        "vision_model": "Qwen/Qwen2-VL-72B-Instruct",
        "system_prompt": prompt_content
    }
    
    with open(public_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_public, f, indent=4, ensure_ascii=False)
    print("✓ Created config.json (with API Key)")

    # 4. Copy Dashboard Template
    try:
        shutil.copy2(src_dir / "dashboard.txt", public_dir / "dashboard.txt")
        print("✓ Copied dashboard.txt")
    except Exception as e:
        print(f"Error copying dashboard: {e}")

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

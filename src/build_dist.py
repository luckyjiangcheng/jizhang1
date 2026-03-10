import os
import json
import shutil
from pathlib import Path

def build_distribution():
    # 1. Define paths
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / "src"
    dist_dir = root_dir / "dist" / "ZenLedger"
    
    # Clean and create dist dir
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Building distribution in: {dist_dir}")

    # 2. Read Config and Prompt
    config_path = src_dir / "config.json"
    prompt_path = src_dir / "prompt.txt"
    
    config = {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Warning: Could not read config.json: {e}")
        config = {
            "api_key": "YOUR_API_KEY_HERE",
            "api_base": "https://api.siliconflow.cn/v1",
            "text_model": "deepseek-ai/DeepSeek-V3",
            "vision_model": "Qwen/Qwen2-VL-72B-Instruct"
        }

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_content = f.read()
    except Exception as e:
        print(f"Error: Could not read prompt.txt: {e}")
        return

    # 3. Create Unified Config (embed prompt to save Shortcut actions)
    # We add the prompt to the config so the Shortcut only needs to read one file.
    config["system_prompt"] = prompt_content
    
    with open(dist_dir / "config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    print("✓ Created config.json (with embedded prompt)")

    # 4. Copy Dashboard Template
    try:
        shutil.copy2(src_dir / "dashboard_template.html", dist_dir / "dashboard.html")
        print("✓ Copied dashboard.html")
    except Exception as e:
        print(f"Error copying dashboard: {e}")

    # 5. Create Empty CSV if not exists
    csv_header = "Date,Time,Amount,Category,Item,Merchant\n"
    with open(dist_dir / "ZenLedger.csv", "w", encoding="utf-8") as f:
        f.write(csv_header)
    print("✓ Created ZenLedger.csv with header")

    print("\nBuild Complete!")
    print(f"ACTION REQUIRED: Copy the folder '{dist_dir}' to your iCloud Drive under 'Shortcuts/'")
    print(f"Final Path on iPhone should be: Files -> iCloud Drive -> Shortcuts -> ZenLedger")

if __name__ == "__main__":
    build_distribution()

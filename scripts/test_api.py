import os
import argparse
import base64
import json
from pathlib import Path
from datetime import datetime
from openai import OpenAI

# Ensure you have the library installed:
# pip install openai

def load_config():
    """Reads configuration from config.json."""
    config_path = Path(__file__).parent.parent / "src" / "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: config.json not found at {config_path}")
        print("Please create it from config.json.example")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse config.json")
        return None

def load_prompt():
    """Reads the prompt from prompt.txt."""
    prompt_path = Path(__file__).parent.parent / "src" / "prompt.txt"
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: prompt.txt not found at {prompt_path}")
        return None

def encode_image(image_path):
    """Encodes an image to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def send_to_siliconflow(content, is_image=False):
    """
    Sends content (text or image path) to SiliconFlow API.
    
    Args:
        content (str): Text string or path to image file.
        is_image (bool): True if content is an image path.
    """
    config = load_config()
    if not config:
        return

    api_key = config.get("api_key")
    if not api_key:
        print("Error: api_key not found in config.json.")
        return

    api_base = config.get("api_base", "https://api.siliconflow.cn/v1")
    text_model = config.get("text_model", "deepseek-ai/DeepSeek-V3")
    vision_model = config.get("vision_model", "Qwen/Qwen2-VL-72B-Instruct")

    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )
    
    system_prompt = load_prompt()
    if not system_prompt:
        return

    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    model = text_model

    if is_image:
        image_path = Path(content)
        if not image_path.exists():
            print(f"Error: Image file not found at {image_path}")
            return
        
        print(f"Sending image: {image_path}...")
        base64_image = encode_image(image_path)
        
        # Use a Vision-capable model
        model = vision_model
        
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract transaction details from this receipt image."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        })
    else:
        # It's text input (e.g. voice transcription)
        print(f"Sending text: \"{content}\"...")
        messages.append({
            "role": "user",
            "content": content + f" (Assuming today is {datetime.now().strftime('%Y-%m-%d')})"
        })

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1 # Low temperature for consistent formatting
        )
        print("\n--- SiliconFlow Response ---")
        print(response.choices[0].message.content)
        print("----------------------------")
    except Exception as e:
        print(f"Error communicating with SiliconFlow: {e}")

def main():
    parser = argparse.ArgumentParser(description="Test SiliconFlow API for ZenLedger")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", help="Text input (e.g. voice transcription)")
    group.add_argument("-i", "--image", help="Path to image file (e.g. receipt)")
    
    args = parser.parse_args()

    if args.text:
        send_to_siliconflow(args.text, is_image=False)
    elif args.image:
        send_to_siliconflow(args.image, is_image=True)

if __name__ == "__main__":
    main()

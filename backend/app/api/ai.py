import httpx
import base64
from fastapi import APIRouter, Depends, HTTPException, status
from app.config import settings
from app.core.security import get_current_user
from app.core.access import get_bound_license_code
from app.schemas import AIExtractRequest, AIExtractResponse

router = APIRouter(dependencies=[Depends(get_bound_license_code)])


async def call_ai_service(text: str = None, image: str = None) -> dict:
    """
    调用AI服务提取交易信息
    """
    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.AI_TEXT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "你是一个专业的交易数据提取助手，只从用户提供的小票、文字、语音内容里把消费信息提取成JSON格式，只输出JSON，不输出任何多余内容。输出格式为{\"date\":\"YYYY-MM-DD\",\"time\":\"HH:MM\",\"amount\":数字,\"category\":\"分类\",\"item\":\"项目\",\"merchant\":\"商家\"}。分类必须从以下12个中文分类中选择一个：餐饮美食、交通出行、购物消费、居家生活、休闲娱乐、人情往来、医疗健康、教育培训、金融贷款、孝敬父母、工作商务、其他支出。日期格式YYYY-MM-DD，时间格式HH:MM，金额为纯数字，未知字段填null。"
            },
            {
                "role": "user",
                "content": text or "请识别图片中的交易信息"
            }
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    # 如果有图片，使用视觉模型
    if image:
        payload["model"] = settings.AI_VISION_MODEL
        payload["messages"][1]["content"] = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}"
                }
            }
        ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{settings.AI_API_BASE}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI服务调用失败: {str(e)}"
            )


@router.post("/extract", response_model=AIExtractResponse)
async def extract_transaction(
    request: AIExtractRequest,
    current_user = Depends(get_current_user)
):
    """
    提取交易信息（语音或图片）
    """
    if not request.text and not request.image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供文本或图片"
        )
    
    # 调用AI服务
    ai_response = await call_ai_service(
        text=request.text,
        image=request.image
    )
    
    def normalize_category(value: str | None) -> str:
        if not value:
            return "其他"
        v = str(value).strip()
        v = v.replace("其他支出", "其他").replace("金融贷款", "金融保险")
        v = v.replace("餐饮", "餐饮美食").replace("交通", "交通出行").replace("购物", "购物消费").replace("居家", "居家生活")
        v = v.replace("娱乐", "休闲娱乐").replace("人情", "人情往来").replace("医疗", "医疗健康").replace("教育", "教育培训")
        v = v.replace("工作商务", "其他")
        v = v.replace("　", " ").strip()
        if " " in v:
            parts = [p for p in v.split(" ") if p]
            if parts:
                v = parts[-1]
        if "、" in v:
            v = v.split("、")[0].strip()
        allowed = {
            "餐饮美食",
            "交通出行",
            "购物消费",
            "居家生活",
            "休闲娱乐",
            "人情往来",
            "医疗健康",
            "教育培训",
            "金融保险",
            "孝敬父母",
            "其他"
        }
        return v if v in allowed else "其他"

    def parse_ai_json(text: str) -> dict:
        import json
        import re

        s = (text or "").strip()
        m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", s, re.IGNORECASE)
        if m:
            s = m.group(1).strip()
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            start = s.find("{")
            end = s.rfind("}")
            if start != -1 and end != -1 and end > start:
                return json.loads(s[start:end + 1])
            raise

    # 解析AI响应
    try:
        content = ai_response["choices"][0]["message"]["content"]
        result = parse_ai_json(content)
        amount_raw = result.get("amount", 0)
        amount = 0.0 if amount_raw is None or amount_raw == "" else float(amount_raw)
        
        return AIExtractResponse(
            date=result.get("date") or "",
            time=result.get("time"),
            amount=amount,
            category=normalize_category(result.get("category")),
            item=result.get("item"),
            merchant=result.get("merchant")
        )
    except (KeyError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI响应解析失败: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI响应解析失败: {str(e)}"
        )

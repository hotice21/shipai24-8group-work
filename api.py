import os
import json
import re
import uuid
from typing import Dict, List, Tuple, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI

# 初始化异步 OpenAI 客户端
client = AsyncOpenAI(
    api_key="sk-121d468f5cb343cc8c48b042a3d2df02",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# FastAPI 应用
app = FastAPI()

# 全局变量
classifier_sessions: Dict[str, Dict] = {}

# 请求模型
class ClassifyRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    max_new_tokens: int = 1024

# 简历分类器
class OllamaResumeClassifier:
    def __init__(self):
        self.modules = {
            "个人信息": "小", "求职目标": "小", "技能关键词": "小",
            "工作经历": "小", "教育背景": "小", "实习经历": "小",
            "证书 & 培训": "小", "校内/社会活动": "小",
            "兴趣爱好": "小", "隐私声明 & 推荐人": "小"
        }
        self.module_content = {m: [] for m in self.modules}

    async def classify_and_evaluate(self, user_input: str, max_tokens: int = 1024) -> List[Tuple[str, str, str, str]]:
        modules_list = ", ".join(self.modules.keys())
        prompt = f"""
你是一位专业简历优化师。请按以下步骤处理用户输入：

步骤1. 把输入拆成多个"信息点"，每点只匹配一个简历模块（{modules_list}）。
步骤2. 对每点：
  ① 归类到最匹配的简历模块：{modules_list}
  ② 评估价值：大/中/小（"大"=有效突出用户优点；"中"=模糊；"小"=不利于展示用户优点）
  ③ 用专业简历语言改写，要求：
    - 以动词开头，量化成果，保留关键词
    - 去掉口语/情感词
    - 不超过25个中文字
  ④ 输出JSON对象，字段：
    {{
      "module": "模块名",
      "value": "大/中/小",
      "reason": "一句话理由",
      "polished": "优化后的简历句"
    }}

步骤3. 把所有对象放进一个JSON数组。

用户输入：{user_input}
"""

        response = await client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt + "\n\n返回格式：仅返回 JSON 数组，不要任何解释。"}],
            temperature=0.3,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        return self.parse_response(content, user_input)

    def parse_response(self, response: str, user_input: str) -> List[Tuple[str, str, str, str]]:
        json_str = self.extract_json_from_response(response)
        if not json_str:
            return [("个人信息", "中", "解析失败", user_input)]

        try:
            data = json.loads(json_str)
            if not isinstance(data, list):
                data = [data]

            cleaned = []
            for d in data:
                if all(k in d for k in ["module", "value", "reason", "polished"]):
                    cleaned.append((d["module"], d["value"], d["reason"], d["polished"]))
            return cleaned
        except Exception as e:
            print("JSON解析失败:", e)
            return [("个人信息", "中", "解析失败", user_input)]

    def extract_json_from_response(self, response: str) -> Optional[str]:
        code_blocks = re.findall(r'```(?:json)?\s*(\[.*?\])\s*```', response, re.S)
        if code_blocks:
            return code_blocks[0]
        json_match = re.search(r'(\[\s*\{.*?\}\s*\])', response, re.S)
        return json_match.group(1) if json_match else None

    def update_module_value(self, module: str, new_value: str):
        value_order = {"小": 0, "中": 1, "大": 2}
        if module in self.modules and value_order[new_value] > value_order[self.modules[module]]:
            self.modules[module] = new_value

    async def get_input_suggestion(self, user_input: str, current_module: str) -> str:
        low_value_modules = [m for m, v in self.modules.items() if v == "小"]
        prompt = f"""
用户刚输入了关于"{current_module}"的信息: "{user_input}"

当前简历模块的价值状态:
{json.dumps(self.modules, ensure_ascii=False, indent=2)}

请提供一句简短的建议，指导用户下一步可以输入什么内容来完善简历。
特别关注那些当前价值为"小"的模块: {', '.join(low_value_modules)}

只返回建议本身，不要有其他解释。
"""
        response = await client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt + "\n\n返回格式：仅返回 JSON 数组，不要任何解释。"}],
            temperature=0.3,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content.strip()

    async def process_input(self, user_input: str) -> Dict:
        items = await self.classify_and_evaluate(user_input)
        for mod, val, _, polished in items:
            self.update_module_value(mod, val)
            self.module_content[mod].append(polished)

        suggestion = await self.get_input_suggestion(user_input, items[-1][0] if items else "个人信息")
        return {
            "items": items,
            "suggestion": suggestion,
            "current_modules": self.modules.copy(),
            "current_content": self.module_content.copy()
        }

# API 端点
@app.post("/classify")
async def classify_text_stream(request: ClassifyRequest):
    session_id = request.session_id or str(uuid.uuid4())
    classifier = OllamaResumeClassifier()

    if session_id in classifier_sessions:
        classifier.modules = classifier_sessions[session_id]["modules"]
        classifier.module_content = classifier_sessions[session_id]["module_content"]

    result = await classifier.process_input(request.text)

    classifier_sessions[session_id] = {
        "modules": classifier.modules,
        "module_content": classifier.module_content
    }

    return {
        "session_id": session_id,
        **result
    }

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    if session_id in classifier_sessions:
        del classifier_sessions[session_id]
    return {"message": "Session deleted"}

# 启动命令
# uvicorn api:app --reload
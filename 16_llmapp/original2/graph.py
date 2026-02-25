import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

# 環境変数を読み込む
def _load_env() -> None:
    """.env を読み込み、必要なら OPENAI_API_KEY を設定する。"""
    load_dotenv(".env")
    if not os.getenv("OPENAI_API_KEY") and os.getenv("API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.environ["API_KEY"]

_load_env()

# 使用するモデル名
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
THREAD_ID = "1"

@dataclass
class SimpleMessage:
    role: str
    content: str


class SimpleMemory:
    """LangGraphの MemorySaver の代わりに使う、最小限のメモリ実装。"""

    def __init__(self) -> None:
        self.storage: dict[str, list[SimpleMessage]] = {}

    def clear(self) -> None:
        self.storage.clear()

    def append(self, thread_id: str, message: SimpleMessage) -> None:
        self.storage.setdefault(thread_id, []).append(message)

    def get(self, config: dict[str, Any]):
        thread_id = config.get("configurable", {}).get("thread_id")
        if not thread_id or thread_id not in self.storage:
            return None
        return {"channel_values": {"messages": list(self.storage[thread_id])}}


memory = SimpleMemory()


def _system_prompt_message() -> SimpleMessage | None:
    system_prompt = (os.getenv("SYSTEM_PROMPT") or "").strip()
    if not system_prompt:
        return None
    return SimpleMessage(role="system", content=system_prompt)


def _ensure_system_prompt(memory_obj: SimpleMemory, thread_id: str) -> None:
    existing = memory_obj.storage.get(thread_id, [])
    if any(m.role == "system" for m in existing):
        return
    system_msg = _system_prompt_message()
    if system_msg:
        memory_obj.append(thread_id, system_msg)


def _call_openai(messages: list[SimpleMessage], model_name: str) -> str:
    if OpenAI is None:
        raise RuntimeError("openai パッケージが見つかりません。requirements を確認してください。")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY (または .env の API_KEY) が未設定です。")

    client = OpenAI()
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": m.role, "content": m.content} for m in messages if m.role in {"system", "user", "assistant"}],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""


def get_bot_response(user_message: str, memory_obj: SimpleMemory, thread_id: str = THREAD_ID) -> str:
    """ユーザー入力に応答し、会話履歴を memory に保存して返す（常にLLMへ問い合わせ）。"""

    _ensure_system_prompt(memory_obj, thread_id)

    # 会話履歴にユーザー発話を保存
    memory_obj.append(thread_id, SimpleMessage(role="user", content=user_message))

    # そのまま会話履歴をLLMに渡す
    messages_for_llm = list(memory_obj.storage.get(thread_id, []))
    reply = _call_openai(messages_for_llm, MODEL_NAME)
    memory_obj.append(thread_id, SimpleMessage(role="assistant", content=reply))
    return reply


def get_messages_list(memory_obj: SimpleMemory):
    messages: list[dict[str, str]] = []
    data = memory_obj.get({"configurable": {"thread_id": THREAD_ID}})
    if not data:
        return messages

    for message in data["channel_values"]["messages"]:
        if message.role == "user":
            messages.append({"class": "user-message", "text": message.content})
        elif message.role == "assistant" and message.content != "":
            messages.append({"class": "bot-message", "text": message.content})
    return messages
"""Read and write the message format used by the legacy chatbot."""

import json

from langchain_core.messages import messages_to_dict


def extract_messages_from_buffer_mem(conversation):
    """Serialize messages from a legacy LangChain conversation buffer."""
    return json.dumps(messages_to_dict(conversation.memory.chat_memory.messages))


def legacy_chat_messages(transcript):
    """Convert serialized human and AI messages into SQLite role/content pairs."""
    if not transcript or not transcript.strip():
        return []

    messages = json.loads(transcript)
    if not isinstance(messages, list):
        raise ValueError("Expected a list of LangChain messages")

    roles = {"human": "user", "ai": "assistant"}
    converted = []
    for message in messages:
        role = message.get("type") if isinstance(message, dict) else None
        if not isinstance(role, str) or role not in roles:
            raise ValueError("Expected a human or AI message")
        data = message.get("data")
        if not isinstance(data, dict) or not isinstance(data.get("content"), str):
            raise ValueError("Expected text in the message content")
        converted.append((roles[role], data["content"]))
    return converted

"""
Thin wrapper around the Anthropic Claude API.
All prompt logic lives in pipeline.py — this file only handles API calls.
"""

import json

import anthropic

from app.core.config import settings

_client: anthropic.AsyncAnthropic | None = None


def get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set in .env")
        _client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


async def chat_completion(
    messages: list[dict],
    system: str,
    max_tokens: int = 1024,
) -> str:
    """Send messages to Claude and return the text response."""
    client = get_client()
    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text
    except anthropic.BadRequestError as e:
        msg = str(e)
        if "credit balance" in msg.lower():
            raise RuntimeError(
                "Your Anthropic API credit balance is too low. "
                "Please add credits at console.anthropic.com/settings/billing"
            )
        raise RuntimeError(f"Anthropic API error: {msg}")
    except anthropic.AuthenticationError:
        raise RuntimeError("Invalid Anthropic API key. Please check your .env file.")
    except anthropic.APIError as e:
        raise RuntimeError(f"Anthropic API error: {e}")


async def structured_completion(
    messages: list[dict],
    system: str,
    max_tokens: int = 512,
) -> dict:
    """
    Same as chat_completion but expects Claude to return valid JSON.
    Returns a parsed dict.
    """
    system_with_json = system + "\n\nYou MUST respond with valid JSON only. No markdown, no explanation."
    raw = await chat_completion(messages, system_with_json, max_tokens)

    # Strip markdown code fences if Claude adds them anyway
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(cleaned)

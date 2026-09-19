"""Text Polisher Agent - converts any input into clean, correct English."""
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


POLISH_PROMPT = """You are a world-class English editor.

You receive input that may be:
- Broken English, typos, or SMS-speak ("u r gr8, cn u cm tmrw?")
- Hinglish / Roman Urdu / mixed languages ("yaar meeting kl 3 baje rakho")
- Slang, emojis, abbreviations, or fragments
- Very casual or grammatically messy writing

Your job: REWRITE it as clean, natural, grammatically correct English.

RULES:
1. Preserve the ORIGINAL meaning - never invent facts.
2. Preserve the ORIGINAL intent: question stays a question, request stays a request.
3. Match the requested TONE (formal / neutral / casual / friendly / professional).
4. Remove slang, filler, and emojis (unless tone is "casual").
5. Fix grammar, punctuation, spelling, capitalization.
6. Expand abbreviations ("tmrw" -> "tomorrow", "u" -> "you").
7. If the input is already correct, make only minimal changes.

Return ONLY valid JSON with these exact keys:
{
  "polished": "<the rewritten English text>",
  "detected_language": "<English / Hinglish / Roman Urdu / Spanish / Mixed / etc.>",
  "tone_applied": "<formal / neutral / casual / friendly / professional>",
  "changes_summary": ["<short bullet of what you fixed>"],
  "confidence": <0.0-1.0>
}

Return raw JSON only. No markdown fences, no extra text.
"""


class TextPolisher:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is missing. Add it to your .env file.")

        self.model = model or os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")

        self.llm = ChatGoogleGenerativeAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0,
            max_retries=2,
        )

    def polish(self, text: str, tone: str | None = None,
               variety: str | None = None) -> dict:
        """Rewrite arbitrary text into proper English. Returns structured dict."""
        tone = tone or os.getenv("DEFAULT_TONE", "professional")
        variety = variety or os.getenv("DEFAULT_VARIETY", "Standard English")

        user_msg = (
            f"TONE: {tone}\n"
            f"ENGLISH VARIETY: {variety}\n"
            f"INPUT:\n{text}"
        )

        try:
            response = self.llm.invoke([
                SystemMessage(content=POLISH_PROMPT),
                HumanMessage(content=user_msg),
            ])
            raw = response.content.strip()

            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.lower().startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            data = json.loads(raw)
            data.setdefault("polished", "")
            data.setdefault("detected_language", "Unknown")
            data.setdefault("tone_applied", tone)
            data.setdefault("changes_summary", [])
            data.setdefault("confidence", 0.0)
            return data

        except Exception as e:
            return {
                "polished": "",
                "detected_language": "Unknown",
                "tone_applied": tone,
                "changes_summary": [],
                "confidence": 0.0,
                "error": str(e),
            }
# ✍️ Text Polisher Agent

An AI-powered agent that converts **any** messy text — broken English, Hinglish, Roman Urdu, SMS-speak, slang, emojis, or mixed languages — into **clean, grammatically correct English**, while preserving the original meaning and intent.

Built with **Streamlit**, **LangChain**, and **Google Gemini**.

---

## 🎯 What It Does

Paste any informal, broken, or mixed-language text and get back polished English in one click.

| Input | Output |
|-------|--------|
| `yaar tmrw meeting 3pm ok?` | Could we schedule tomorrow's meeting at 3 PM? |
| `u r gr8, cn u cm tmrw?` | You are great. Can you come tomorrow? |
| `i am not understanding what u saying plz explain again` | I do not understand what you are saying. Please explain again. |
| `habibi plz send me the file asap, shukran` | Please send me the file as soon as possible. Thank you. |

The agent also tells you:
- **Detected language** (Hinglish, Roman Urdu, English, Mixed, etc.)
- **Tone applied** (professional, formal, neutral, friendly, casual)
- **What changed** (expanded abbreviations, fixed grammar, etc.)
- **Confidence score** (0–100%)

---

## ✨ Features

- 🔤 **Any input format** — SMS-speak, Hinglish, Roman Urdu, emoji-heavy, fragmented
- 🎭 **5 tone presets** — professional, formal, neutral, friendly, casual
- 🌍 **4 English varieties** — Standard, American, British, Simple/Plain
- 🔍 **Transparency** — shows detected language + specific changes made
- ⚡ **Fast** — powered by Gemini 2.5 Flash
- 🎨 **Clean Streamlit UI** — no setup beyond API key
- 🔐 **Secure** — API keys stored in `.env`, never committed

🖥️ How to Use
Paste any messy text into the input box

Example: yaar kal meeting 3 baje rakh lo, main thora late ho jaunga

Choose your tone and English variety from the sidebar

Click ✨ Polish

Get clean English + detected language + confidence score + change summary


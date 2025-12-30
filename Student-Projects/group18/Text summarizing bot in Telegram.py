"""
Advanced Telegram Summarization Bot
----------------------------------
Features:
- 3 summarization modes (short / medium / detailed)
- OpenAI-powered summarization
- SQLite caching to reduce API calls
- Async & clean architecture
"""

import os
import asyncio
import logging
import hashlib

import aiosqlite
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from openai import AsyncOpenAI

# =========================== Logging ===========================

logging.basicConfig(level=logging.INFO)

# =========================== Paths & Database ===========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "summary_cache.sqlite")
os.makedirs(BASE_DIR, exist_ok=True)

# =========================== Config (ENV VARS) ===========================
TELEGRAM_TOKEN="TELEGRAM_TOKEN"
OPENAI_API_KEY= "OPENAI_API_KEY"

SUMMARY_PROMPTS = {
    "short": "Summarize the following text in exactly 3 concise bullet points.",
    "medium": "Provide a clear and concise one-paragraph summary.",
    "detailed": "Provide a detailed, structured, and easy-to-understand summary.",
}

# =========================== OpenAI Client ===========================

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# =========================== Database ===========================

async def ensure_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS summaries (
                text_hash TEXT,
                mode TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (text_hash, mode)
            )
            """
        )
        await db.commit()

async def get_cached_summary(text_hash: str, mode: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT summary FROM summaries WHERE text_hash = ? AND mode = ?",
            (text_hash, mode),
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def save_summary(text_hash: str, summary: str, mode: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT OR REPLACE INTO summaries (text_hash, mode, summary)
            VALUES (?, ?, ?)
            """,
            (text_hash, mode, summary),
        )
        await db.commit()

# =========================== Utilities ===========================

def hash_text(text: str) -> str:
    """Generate a stable hash for caching."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

async def summarize_text(text: str, mode: str) -> str:
    """Summarize text using OpenAI."""
    prompt = SUMMARY_PROMPTS.get(mode, SUMMARY_PROMPTS["medium"])

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional text summarizer."},
            {"role": "user", "content": f"{prompt}\n\n{text}"},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()

# =========================== Telegram Handlers ===========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n\n"
        "من متن شما را با هوش مصنوعی خلاصه می‌کنم.\n\n"
        "📌 حالت‌های خلاصه‌سازی:\n"
        "🔹 /short  → خلاصه خیلی کوتاه (۳ بولت پوینت)\n"
        "🔹 /medium → خلاصه متعادل در یک پاراگراف (پیش‌فرض)\n"
        "🔹 /detailed → خلاصه کامل و دقیق\n\n"
        "بعد از انتخاب حالت، متن خود را ارسال کنید.\n"
        "ℹ️ /help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 راهنما:\n\n"
        "1️⃣ یکی از حالت‌ها را انتخاب کنید:\n"
        "/short\n"
        "/medium\n"
        "/detailed\n\n"
        "2️⃣ متن خود را ارسال کنید\n\n"
        "🔁 اگر حالت انتخاب نکنید، حالت پیش‌فرض medium است."
    )

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = update.message.text.replace("/", "")
    if mode in SUMMARY_PROMPTS:
        context.user_data["mode"] = mode
        await update.message.reply_text(
            f"✅ حالت خلاصه‌سازی تنظیم شد: {mode.upper()}"
        )
    else:
        await update.message.reply_text("❌ حالت نامعتبر است.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "medium")

    text_hash = hash_text(text)

    cached = await get_cached_summary(text_hash, mode)
    if cached:
        await update.message.reply_text("📌 خلاصه (از کش):\n\n" + cached)
        return

    summary = await summarize_text(text, mode)
    await save_summary(text_hash, summary, mode)

    await update.message.reply_text(summary)

# =========================== Main ===========================

def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("❌ TELEGRAM_TOKEN is not set")

    if not OPENAI_API_KEY:
        raise RuntimeError("❌ OPENAI_API_KEY is not set")

    asyncio.run(ensure_db())

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("short", set_mode))
    app.add_handler(CommandHandler("medium", set_mode))
    app.add_handler(CommandHandler("detailed", set_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

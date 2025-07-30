from collections import defaultdict
import time
import subprocess
import sys
import platform
import asyncio

try:
    from telegram import Update
    from telegram.constants import ParseMode
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
    from telegram.ext import (
        ApplicationBuilder,
        CommandHandler,
        MessageHandler,
        ContextTypes,
        filters,
        ConversationHandler,
        CallbackQueryHandler
    )
except ImportError:
    print("Telegram API is not installed but needed.")
    answer = input("Install it now? (Y/n): ").strip().lower()
    if answer in ["", "y", "yes"]:
        print("Installing python-telegram-bot...")
        try:
            if platform.system() == "Linux":
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "python-telegram-bot", "--break-system-packages"
                ])
            else:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "python-telegram-bot"
                ])
            print("Installed successfully. Please rerun your script.")
            sys.exit(0)
        except Exception as e:
            print(f"Installation failed: {e}")
            sys.exit(1)
    else:
        print("Telegram support not installed. Exiting.")
        sys.exit(1)

from .core import search

USERNAME = 1
_app = None  
TOKEN = None
REQUIRE_JOIN = False
CHANNEL_ID = None
RATE_LIMIT = None
RATE_LIMIT_LENGTH = None
user_command_history = defaultdict(list)

def selfhost(bot_token: str = None, requireJOIN=False, channelID=None, rateLimit=None, rateLimitLengh=None):
    global _app, TOKEN, REQUIRE_JOIN, CHANNEL_ID, RATE_LIMIT, RATE_LIMIT_LENGTH

    if bot_token and bot_token != "run":
        TOKEN = bot_token
        REQUIRE_JOIN = requireJOIN
        CHANNEL_ID = channelID
        RATE_LIMIT = rateLimit
        RATE_LIMIT_LENGTH = rateLimitLengh
        _app = ApplicationBuilder().token(TOKEN).build()
        print("DEBUG : Bot running")

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username)]
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )

        _app.add_handler(conv_handler)
        _app.add_handler(CallbackQueryHandler(check_join_callback, pattern="check_join"))

    elif bot_token == "run" and _app:
        _app.run_polling()
    else:
        raise ValueError("selfhost must be called with a bot_token first, then with 'run'")


async def is_member(user_id: int, bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def is_rate_limited(user_id: int) -> tuple[bool, int]:
    if RATE_LIMIT is None or RATE_LIMIT_LENGTH is None:
        return False, 0

    now = time.time()
    history = user_command_history[user_id]

    user_command_history[user_id] = [t for t in history if now - t <= RATE_LIMIT_LENGTH]

    if len(user_command_history[user_id]) >= RATE_LIMIT:
        next_allowed = user_command_history[user_id][0] + RATE_LIMIT_LENGTH
        wait_time = int(next_allowed - now)
        return True, wait_time
    else:
        user_command_history[user_id].append(now)
        return False, 0

async def prompt_to_join(update: Update):
    print("DEBUG : Prompt to join executed")
    keyboard = [
        [InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    text = (
        "🚫 To use this bot, you must join our channel!\n\n"
        "👉 Join using the button below, then click '✅ I've Joined' to verify."
    )

    if update.message:
        await update.message.reply_text(text, reply_markup=markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=markup)

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("DEBUG : Check Join")
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if await is_member(user_id, context.bot):
        try:
            await query.message.delete()
        except BadRequest:
            pass

        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Verification successful! You can now use the bot.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await query.answer("❌ You're still not in the channel! Join and try again.", show_alert=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("DEBUG : /start executed")

    user_id = update.effective_user.id

    if REQUIRE_JOIN and not await is_member(user_id, context.bot):
        await prompt_to_join(update)
        return ConversationHandler.END

    is_limited, wait_time = is_rate_limited(user_id)
    if is_limited:
        print("DEBUG : Rate-Limit ")
        minutes, seconds = divmod(wait_time, 60)
        await update.message.reply_text(
            f"🚫 Rate limit exceeded. Please wait {minutes}m {seconds}s before using /start again."
        )
        return ConversationHandler.END

    await update.message.reply_text(
        r"👋 Hi Send me a TikTok username to get account details, "
        r"You can send /cancel at any time to stop",
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return USERNAME


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('❌ Operation cancelled')
    return ConversationHandler.END

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    username = update.message.text.strip().lstrip("@")
    print("DEBUG : Searching User")

    if REQUIRE_JOIN and not await is_member(user.id, context.bot):
        await prompt_to_join(update)
        return ConversationHandler.END

    try:
        data = search(username)

        profile_pic_url = data.get("Profile Picture")
        if profile_pic_url:
            await update.message.reply_photo(photo=profile_pic_url)

        data.pop("Profile Picture", None)
        data.pop("Profile Link", None)

        ordered_keys = [
            "ID", "Username", "Display Name", "Bio", "Bio Links", "Country",
            "Account Language", "Verified", "Private", "Secret", "Suggest Acc Bind",
            "Organisation", "AD Account", "Seller", "Account Created", "Name Updated",
            "Username Updated", "Family Pairing", "Live Status", "Following Visibility",
            "New Account", "Following", "Followers", "Videos", "Likes", "Friends",
            "Profile Link"
        ]

        message_lines = []
        for key in ordered_keys:
            if key in data:
                message_lines.append(f"*{key}*: {data[key]}")

        for key in data:
            if key not in ordered_keys:
                message_lines.append(f"*{key}*: {data[key]}")

        full_message = "\n".join(message_lines)
        await update.message.reply_text(full_message, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

    return ConversationHandler.END

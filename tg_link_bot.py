# tg_link_bot.py
#
# FastAPI-friendly PTB polling service + Telethon user client title lookup
#
# Env vars required:
#   TELETHON_STRING_SESSION=...   (generated once via Telethon StringSession)
#
# Args or env vars required:
#   BOT_TOKEN=...
#   API_ID=...
#   API_HASH=...
#
# Reply format:
#   • Title
#      URL

import os
import asyncio
import re
import unicodedata
from typing import List, Tuple, Optional

from telegram import Update
from telegram.constants import MessageEntityType
from telegram.ext import Application as TgApplication, MessageHandler, ContextTypes, filters

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    UsernameInvalidError,
    UsernameNotOccupiedError,
    InviteHashInvalidError,
    InviteHashExpiredError,
    FloodWaitError,
    RPCError,
)
from telethon.tl.functions.messages import CheckChatInviteRequest
from telethon.tl.functions.chatlists import CheckChatlistInviteRequest


# ----------------------------
# Link classifier/extractor
# ----------------------------
INVITE_RE = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/\+([A-Za-z0-9_=-]+)")
JOINCHAT_RE = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/joinchat/([A-Za-z0-9_=-]+)")
ADDLIST_RE = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/addlist/([A-Za-z0-9_=-]+)")
USERNAME_RE = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/([A-Za-z0-9_]{5,32})\b")

# fallback for plain URLs in text (when Telegram didn't create entities)
URL_FALLBACK_RE = re.compile(r"(?i)\bhttps?://(?:t\.me|telegram\.me)/[^\s<>\]]+")

RESERVED = {"share", "addstickers", "addemoji", "addtheme", "c", "joinchat", "addlist"}


# ----------------------------
# Normalization helpers
# ----------------------------
_ZERO_WIDTH = dict.fromkeys(map(ord, [
    "\u200b", "\u200c", "\u200d", "\u2060", "\ufeff",  # ZWSP/ZWNJ/ZWJ/WJ/BOM
    "\u200e", "\u200f",                                # LRM/RLM
    "\u202a", "\u202b", "\u202c", "\u202d", "\u202e",   # bidi controls
]))

def _sanitize_text(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    return s.translate(_ZERO_WIDTH)

def _clean_url(u: str) -> str:
    u = _sanitize_text(u or "")
    return u.strip().rstrip(").,!?]}>\"'")

def _dedup_preserve_order(items: List[str]) -> List[str]:
    seen, out = set(), []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _classify(url: str) -> Tuple[str, str]:
    url = _clean_url(url)

    m = ADDLIST_RE.search(url)
    if m:
        return "addlist", m.group(1)

    m = INVITE_RE.search(url)
    if m:
        return "invite", m.group(1)

    m = JOINCHAT_RE.search(url)
    if m:
        return "invite", m.group(1)

    m = USERNAME_RE.search(url)
    if m:
        username = m.group(1)
        if username.lower() in RESERVED:
            return "unknown", ""
        return "username", username

    return "unknown", ""


def _extract_links(msg) -> List[str]:
    """
    Native-first:
      1) msg.parse_entities / msg.parse_caption_entities for URL + TEXT_LINK
      2) sanitize/clean + dedup
      3) fallback regex over sanitized combined text/caption
    """
    out: List[str] = []

    # 1) entities (most reliable)
    if msg.text:
        ent_map = msg.parse_entities([MessageEntityType.URL, MessageEntityType.TEXT_LINK])
        for ent, extracted in ent_map.items():
            if ent.type == MessageEntityType.TEXT_LINK and ent.url:
                out.append(ent.url)
            else:
                out.append(extracted)

    if msg.caption:
        ent_map = msg.parse_caption_entities([MessageEntityType.URL, MessageEntityType.TEXT_LINK])
        for ent, extracted in ent_map.items():
            if ent.type == MessageEntityType.TEXT_LINK and ent.url:
                out.append(ent.url)
            else:
                out.append(extracted)

    out = _dedup_preserve_order([_clean_url(x) for x in out if x])

    # 2) fallback
    combined = _sanitize_text((msg.text or "") + "\n" + (msg.caption or ""))
    fallback = [_clean_url(x) for x in URL_FALLBACK_RE.findall(combined)]
    if fallback:
        out = _dedup_preserve_order(out + fallback)

    return out


# ----------------------------
# Bot service
# ----------------------------
class TelegramLinkBotService:
    """
    PTB polling loop + Telethon (user) client to fetch titles for Telegram links.
    Safe to integrate with FastAPI startup/shutdown.
    """

    def __init__(
        self,
        bot_token: Optional[str] = None,
        api_id: Optional[int] = None,
        api_hash: Optional[str] = None,
        telethon_string_session: Optional[str] = None,
        debug: bool = False,
    ):
        self.bot_token = bot_token or os.getenv("BOT_TOKEN", "")
        self.api_id = api_id if api_id is not None else int(os.getenv("API_ID", "0"))
        self.api_hash = api_hash or os.getenv("API_HASH", "")
        self.string_session = telethon_string_session or os.getenv("TELETHON_STRING_SESSION", "")
        self.debug = debug

        self._bot_app: Optional[TgApplication] = None
        self._bot_task: Optional[asyncio.Task] = None
        self._stop_event: Optional[asyncio.Event] = None

        self._tg_client: Optional[TelegramClient] = None
        self._tg_lock = asyncio.Lock()

        self._validate_config()

    def _validate_config(self) -> None:
        missing = []
        if not self.bot_token:
            missing.append("BOT_TOKEN")
        if not self.api_id:
            missing.append("API_ID")
        if not self.api_hash:
            missing.append("API_HASH")
        if not self.string_session:
            missing.append("TELETHON_STRING_SESSION")
        if missing:
            raise RuntimeError(f"Missing required env/args: {', '.join(missing)}")

    async def start(self):
        """
        Start polling in a background task. Safe for FastAPI startup.
        """
        if self._bot_task and not self._bot_task.done():
            return
        self._stop_event = asyncio.Event()
        self._bot_task = asyncio.create_task(self._run_polling())

    async def stop(self):
        """
        Stop polling + disconnect Telethon. Safe for FastAPI shutdown.
        """
        if self._stop_event:
            self._stop_event.set()

        if self._bot_app:
            try:
                await self._bot_app.updater.stop()
            except Exception:
                pass
            try:
                await self._bot_app.stop()
            except Exception:
                pass
            try:
                await self._bot_app.shutdown()
            except Exception:
                pass
            self._bot_app = None

        if self._bot_task and not self._bot_task.done():
            self._bot_task.cancel()
        self._bot_task = None

        if self._tg_client:
            try:
                await self._tg_client.disconnect()
            except Exception:
                pass
            self._tg_client = None

    async def _run_polling(self):
        """
        Keep this coroutine alive; if it returns, your bot stops receiving updates.
        """
        self._bot_app = TgApplication.builder().token(self.bot_token).build()
        self._bot_app.add_handler(MessageHandler(filters.ALL, self._handle_any_message))

        await self._bot_app.initialize()
        await self._bot_app.start()
        await self._bot_app.updater.start_polling(drop_pending_updates=True)

        if self.debug:
            print("PTB polling started.")

        assert self._stop_event is not None
        try:
            await self._stop_event.wait()
        finally:
            if self.debug:
                print("PTB polling stopping...")

    async def _ensure_user_client(self) -> TelegramClient:
        """
        Create/connect Telethon user client once; reconnect if dropped.
        """
        if self._tg_client is None:
            self._tg_client = TelegramClient(
                StringSession(self.string_session),
                self.api_id,
                self.api_hash,
            )

        if not self._tg_client.is_connected():
            await self._tg_client.connect()

        if not await self._tg_client.is_user_authorized():
            raise RuntimeError("Telethon StringSession is not authorized/valid.")

        return self._tg_client

    async def _get_title(self, client: TelegramClient, url: str) -> Optional[str]:
        kind, token = _classify(url)
        if kind == "unknown":
            return None

        try:
            if kind == "username":
                ent = await client.get_entity(token)
                title = getattr(ent, "title", None)
                if title:
                    return title
                name = f"{getattr(ent,'first_name','') or ''} {getattr(ent,'last_name','') or ''}".strip()
                return name or token

            if kind == "invite":
                res = await client(CheckChatInviteRequest(token))
                return (
                    getattr(res, "title", None)
                    or getattr(getattr(res, "chat", None), "title", None)
                    or "Untitled chat"
                )

            if kind == "addlist":
                res = await client(CheckChatlistInviteRequest(slug=token))
                return res.title.text if res.title else "Untitled folder"

            return None

        except (ValueError, UsernameInvalidError, UsernameNotOccupiedError,
                InviteHashInvalidError, InviteHashExpiredError):
            return None
        except FloodWaitError:
            return None
        except RPCError:
            return None
        except Exception:
            return None

    async def _handle_any_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Never let exceptions break future updates.
        """
        try:
            msg = update.effective_message
            if not msg:
                return

            links = _extract_links(msg)
            if self.debug:
                print("Extracted links:", links)

            if not links:
                return

            try:
                client = await self._ensure_user_client()
            except Exception as e:
                if self.debug:
                    print("Telethon client error:", repr(e))
                return

            blocks = []
            async with self._tg_lock:
                for link in links:
                    title = await self._get_title(client, link)
                    if title:
                        blocks.append(f"• {title}\n   {link}")

            if not blocks:
                return

            await msg.reply_text(
                "📌 Telegram Links\n\n" + "\n\n".join(blocks),
                disable_web_page_preview=True
            )

        except Exception as e:
            if self.debug:
                print("Handler error:", repr(e))
            # swallow errors
            return

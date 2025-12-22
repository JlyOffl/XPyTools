# tg_link_bot.py
import asyncio
import re
from typing import List, Tuple, Optional

from telegram import Update, MessageEntity
from telegram.ext import Application as TgApplication, MessageHandler, ContextTypes, filters

from telethon import TelegramClient
from telethon.errors import (
    UsernameInvalidError, UsernameNotOccupiedError,
    InviteHashInvalidError, InviteHashExpiredError,
    FloodWaitError, RPCError
)
from telethon.tl.functions.messages import CheckChatInviteRequest
from telethon.tl.functions.chatlists import CheckChatlistInviteRequest


# ----------------------------
# Link classifier/extractor
# ----------------------------
INVITE_RE   = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/\+([A-Za-z0-9_=-]+)")
JOINCHAT_RE = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/joinchat/([A-Za-z0-9_=-]+)")
ADDLIST_RE  = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/addlist/([A-Za-z0-9_=-]+)")
USERNAME_RE = re.compile(r"(?i)(?:https?://)?(?:t\.me|telegram\.me)/([A-Za-z0-9_]{5,32})\b")
URL_FALLBACK_RE = re.compile(r"(?i)\bhttps?://(?:t\.me|telegram\.me)/[^\s<>\]]+")

RESERVED = {"share", "addstickers", "addemoji", "addtheme", "c", "joinchat", "addlist"}


def _clean_url(u: str) -> str:
    return (u or "").strip().rstrip(").,!?]}>\"'")


def _dedup_preserve_order(items: List[str]) -> List[str]:
    seen, out = set(), []
    for x in items:
        if x not in seen:
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
    out = []

    # Entities in text
    if msg.text and msg.entities:
        for e in msg.entities:
            if e.type == MessageEntity.URL:
                out.append(msg.text[e.offset: e.offset + e.length])
            elif e.type == MessageEntity.TEXT_LINK and e.url:
                out.append(e.url)

    # Entities in caption
    if msg.caption and msg.caption_entities:
        for e in msg.caption_entities:
            if e.type == MessageEntity.URL:
                out.append(msg.caption[e.offset: e.offset + e.length])
            elif e.type == MessageEntity.TEXT_LINK and e.url:
                out.append(e.url)

    # Fallback regex
    combined = (msg.text or "") + "\n" + (msg.caption or "")
    out.extend(URL_FALLBACK_RE.findall(combined))

    out = [_clean_url(x) for x in out if x]
    return _dedup_preserve_order(out)


# ----------------------------
# Bot service (start/stop)
# ----------------------------
class TelegramLinkBotService:
    """
    Starts a python-telegram-bot polling loop in the background and uses a shared
    Telethon USER client to fetch titles for Telegram links.

    Reply format:
      • Title
         URL
    """

    def __init__(
        self,
        bot_token: str,
        api_id: int,
        api_hash: str,
        telethon_session: str,
        debug: bool = False,
    ):
        self.bot_token = bot_token
        self.api_id = api_id
        self.api_hash = api_hash
        self.telethon_session = telethon_session
        self.debug = debug

        self._bot_app: Optional[TgApplication] = None
        self._bot_task: Optional[asyncio.Task] = None

        self._tg_client: Optional[TelegramClient] = None
        self._tg_lock = asyncio.Lock()

    async def start(self):
        """
        Start polling in a background task. Safe to call from FastAPI startup.
        """
        if self._bot_task and not self._bot_task.done():
            return
        self._bot_task = asyncio.create_task(self._run_polling())

    async def stop(self):
        """
        Stop polling + disconnect telethon.
        Safe to call from FastAPI shutdown.
        """
        # Stop PTB
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

        # Cancel background task
        if self._bot_task and not self._bot_task.done():
            self._bot_task.cancel()
        self._bot_task = None

        # Disconnect Telethon
        if self._tg_client:
            try:
                await self._tg_client.disconnect()
            except Exception:
                pass
            self._tg_client = None

    async def _run_polling(self):
        self._bot_app = TgApplication.builder().token(self.bot_token).build()
        self._bot_app.add_handler(MessageHandler(filters.ALL, self._handle_any_message))

        await self._bot_app.initialize()
        await self._bot_app.start()
        await self._bot_app.updater.start_polling(drop_pending_updates=True)

    async def _ensure_user_client(self) -> TelegramClient:
        if self._tg_client is None:
            self._tg_client = TelegramClient(self.telethon_session, self.api_id, self.api_hash)
            await self._tg_client.connect()
            if not await self._tg_client.is_user_authorized():
                raise RuntimeError(
                    f"Telethon session '{self.telethon_session}' is not authorized. "
                    f"Authorize once with phone login and deploy the .session file "
                    f"(Render persistent disk) or use StringSession."
                )
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
        msg = update.effective_message
        links = _extract_links(msg)
        if not links:
            return

        client = await self._ensure_user_client()

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

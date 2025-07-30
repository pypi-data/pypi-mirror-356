from typing import Optional
import logging
from telegram.constants import ParseMode
from telegram import Message
from telegram_bot.config.telegram_send_config import TelegramSendConfig
from telegram_bot.core.interfaces.base_sender import BaseSender

class DocumentSender(BaseSender):
    """
    Telegram 문서(document) 파일 전송용 Sender 클래스.

    Telegram API의 send_document 메서드를 래핑하며,
    파일 경로나 파일 객체를 문서로 전송할 수 있습니다.

    Example:
        ```python
        config = TelegramSendConfig(
            chat_id="-1001234567890",
            parse_mode=ParseMode.HTML,
            message_thread_id=20,
            reply_to_message_id=None
        )
        sender = TelegramDocumentSender(token="YOUR_BOT_TOKEN")

        # 파일 경로로 문서 전송
        await sender.send(config, document="/path/to/file.pdf", caption="📎 문서 첨부")

        # 동기 호출 예 (비동기 환경이 아닐 때)
        sender.send_sync(config, document="/path/to/file.pdf", caption="📎 문서 첨부")
        ```
    """

    def __init__(self, token: str, verbose: bool = True):
        """
        Args:
            token (str): Telegram 봇 토큰
        """
        super().__init__(token=token, verbose=verbose)
        self.logger = logging.getLogger(type(self).__name__)

    async def send(self, config: TelegramSendConfig, *, document: str, caption: Optional[str] = None, **kwargs) -> Message:
        """
        문서 파일을 Telegram 채팅방에 전송합니다.

        Args:
            config (TelegramSendConfig): Telegram 메시지 전송 설정 객체
            document (str): 전송할 문서의 파일 경로 또는 파일 객체
            caption (Optional[str], optional): 문서에 첨부할 설명(캡션), 기본값 None
            **kwargs: send_document 호출 시 추가 파라미터 (disable_notification 등)

        Returns:
            telegram.Message: Telegram API가 반환하는 메시지 객체
        """
        self.logger.info(f"Sending document to chat_id={config.chat_id} with caption={caption}")
        return await self._send_document_async(config, document=document, caption=caption or "", **kwargs)

    async def _send_document_async(self, config: TelegramSendConfig, *, document: str, caption: str = "", **kwargs) -> Message:
        """
        실제 비동기 문서 전송을 수행하는 내부 메서드.

        Args:
            config (TelegramSendConfig): 메시지 전송 설정 객체
            document (str): 전송할 문서 경로 또는 파일 객체
            caption (str): 문서 캡션
            **kwargs: Telegram API에 추가 전달할 파라미터

        Returns:
            telegram.Message: Telegram 메시지 객체
        """
        return await self.bot.send_document(
            chat_id=config.chat_id,
            document=document,
            caption=caption,
            parse_mode=config.parse_mode,
            message_thread_id=config.message_thread_id,
            reply_to_message_id=config.reply_to_message_id,
            read_timeout=config.read_timeout,
            write_timeout=config.write_timeout,
            connect_timeout=config.connect_timeout,
            pool_timeout=config.pool_timeout,
            **kwargs
        )

if __name__ == "__main__":

    from telegram_bot.config.telegram_send_config import TelegramSendConfig
    from telegram.constants import ParseMode
    from dotenv import load_dotenv
    import os

    load_dotenv(verbose=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    config = TelegramSendConfig(
        chat_id="-1001999281217",
        parse_mode=ParseMode.HTML,
        message_thread_id=33708
    )

    sender = DocumentSender(token=token)

    p = "/Users/mjun/dev/02_packages/telegram_bot/assets/img.jpeg"
    sender.send_sync(config, document=p, caption="테스트 문서 전송")
    sender.send_sync(config, document=p, caption="테스트 문서 전송 1")
    sender.send_sync(config, document=p, caption="테스트 문서 전송 2")
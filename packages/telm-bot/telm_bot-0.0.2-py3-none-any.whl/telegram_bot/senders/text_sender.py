# src/telegram_bot/senders/text.py
import os

from telegram_bot.core.interfaces.base_sender import BaseSender
from telegram_bot.config.telegram_send_config import TelegramSendConfig
from typing import List


class TextSender(BaseSender):
    """
    Telegram 메시지를 전송하는 Sender 클래스.

    메시지 텍스트가 Telegram 메시지 최대 길이 제한보다 길 경우,
    자동으로 텍스트를 여러 개의 청크로 분할하여 여러 메시지로 나누어 전송합니다.

    Example:
        config = TelegramSendConfig(
            chat_id="-1001999281217",
            parse_mode=ParseMode.HTML,
            message_thread_id=33708
        )

        sender = TextSender(token=token)
        text = "Hello, this is a test message!"# * 1000

        # Send the message synchronously
        sender.send_sync(config, text=text)

    Attributes:
        max_message_length (int): Telegram 메시지 최대 길이 제한 (기본 4096자).
        logger (logging.Logger): 클래스 전용 로거 인스턴스.
    """

    def __init__(self, token: str, max_message_length: int = 4096, verbose: bool = True):
        """
        Args:
            token (str): Telegram 봇 토큰
            max_message_length (int, optional): 메시지 최대 길이 제한 (기본값: 4096)
        """
        super().__init__(token=token, verbose=verbose)
        self.max_message_length = max_message_length

    async def send(self, config: TelegramSendConfig, text: str, **kwargs):
        """
        텍스트 메시지를 전송합니다.

        메시지 길이가 max_message_length를 초과할 경우, 텍스트를 여러 청크로 분할해 순차적으로 전송합니다.

        Args:
            config (TelegramSendConfig): Telegram 메시지 전송 설정 객체
            text (str): 전송할 메시지 텍스트
            **kwargs: Telegram send_message 메서드에 전달할 추가 인자들

        Example:
            config = TelegramSendConfig(
                chat_id="-1001999281217",
                parse_mode=ParseMode.HTML,
                message_thread_id=33708
            )

            sender = TextSender(token=token)
            text = "Hello, this is a test message!"# * 1000

            # Send the message synchronously
            sender.send_sync(config, text=text) or sender.send(config, text=text)

        Returns:
            list | telegram.Message: 여러 메시지를 전송한 경우 리스트 반환,
                                    단일 메시지인 경우 메시지 객체 단독 반환
        """

        if isinstance(text, str) and len(text) > self.max_message_length:
            chunks = self._split_text(text)
            results = []
            total = len(chunks)

            for i, chunk in enumerate(chunks, 1):
                self.logger.info(f"[{i}/{total}] 분할 메시지 전송 중...")
                # 중복 text 키 제거 (없으면 에러 가능)
                kwargs.pop("text", None)
                res = await self._send_single(config, chunk, **kwargs)
                results.append(res)
            return results
        else:
            return await self._send_single(config, text, **kwargs)

    async def _send_single(self, config: TelegramSendConfig, text: str, **kwargs):
        """
        단일 메시지를 Telegram에 비동기 전송합니다.

        Args:
            config (TelegramSendConfig): 메시지 전송 설정
            text (str): 메시지 텍스트
            **kwargs: 추가 Telegram send_message 파라미터

        Returns:
            telegram.Message: Telegram API가 반환하는 메시지 객체
        """
        return await self.bot.send_message(
            chat_id=config.chat_id,
            text=text,
            parse_mode=config.parse_mode,
            message_thread_id=config.message_thread_id,
            **kwargs
        )

    def _split_text(self, text: str) -> List[str]:
        """
        텍스트를 max_message_length 크기 기준으로 분할합니다.

        현재는 단순 문자 기준 분할로, 중간 단어가 끊길 수 있습니다.
        필요시 단어 단위 분할 또는 문장 단위 분할로 개선 가능.

        Args:
            text (str): 분할할 전체 텍스트

        Returns:
            List[str]: 분할된 텍스트 청크 리스트
        """
        chunks = []
        current = 0
        length = len(text)

        while current < length:
            end = current + self.max_message_length
            chunk = text[current:end]
            chunks.append(chunk)
            current = end

        return chunks


if __name__ == "__main__":
    # Example usage
    from telegram_bot.config.telegram_send_config import TelegramSendConfig
    from telegram.constants import ParseMode
    from dotenv import load_dotenv

    load_dotenv(verbose=True)
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    config = TelegramSendConfig(
        chat_id="-1002431753833",
        parse_mode=ParseMode.HTML,
        message_thread_id=23 # 일부러 오류 발생
        # message_thread_id = 33708  # 일부러 오류 발생
    )

    sender = TextSender(token=token)
    text = "Hello, this is a test message!"  # * 1000

    # Send the message synchronously
    try:
        sender.send_sync(config, text=text)
        # ...
    except Exception as e:
        print(f"Get Error,, {e}")
    # sender.send_sync(config, text=text + "1" )
    # time.sleep(2)
    # sender.send_sync(config, text=text + "2")

    # logging.info(f"Message sent successfully using PTB version {ptb_version}")

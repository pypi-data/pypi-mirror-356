# src/telegram_bot/senders/media_group_sender.py
from typing import List, Union, BinaryIO
from pathlib import Path

from telegram import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio
from telegram.constants import ParseMode

from telegram_bot.core.interfaces.base_sender import BaseSender
from telegram_bot.config.telegram_send_config import TelegramSendConfig

class MediaGroupSender(BaseSender):
    """
    Telegram 미디어 그룹(앨범) 전송용 Sender 클래스.

    InputMediaPhoto 또는 InputMediaVideo 객체 리스트를 받아,
    `send_media_group` API로 한 번에 전송합니다.

    ⚠️ 주의: 텔레그램은 같은 타입의 미디어만 한 번에 보낼 수 있습니다.

    Attributes:
        logger (logging.Logger): 클래스 전용 로거

    Example:
        ```python
        from telegram import InputMediaPhoto
        config = TelegramSendConfig(
            chat_id="-1001234567890",
            parse_mode=ParseMode.HTML,
            message_thread_id=123
        )
        sender = TelegramMediaGroupSender(token="YOUR_BOT_TOKEN")

        media = [
            InputMediaPhoto(media=sender.resolve_media_input("photo1.jpg"), caption="첫번째 사진"),
            InputMediaPhoto(media=sender.resolve_media_input("photo2.jpg"))
        ]

        # 비동기 전송 (async context 내에서)
        await sender.send(config, media=media)

        # 동기 전송 (비동기 환경이 아닐 때)
        sender.send_sync(config, media=media)
        ```
    """

    def __init__(self, token: str, verbose: bool = True):
        """
        TelegramMediaGroupSender 초기화

        Args:
            token (str): Telegram Bot Token
        """
        super().__init__(token, verbose=verbose)
        self.logger.info("TelegramMediaGroupSender 초기화 완료")

    async def send(
        self,
        config: TelegramSendConfig,
        *args,
        media: List[Union[InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio]],
        **kwargs
    ) -> List[Message]:
        """
        미디어 그룹을 비동기로 전송합니다.

        Args:
            config (TelegramSendConfig): 메시지 전송 설정
            media (List[InputMediaPhoto | InputMediaVideo]): 전송할 미디어 리스트 (동일 타입이어야 함)
            **kwargs: send_media_group API 호출 시 추가 인자

        Returns:
            List[telegram.Message]: 전송된 메시지 리스트

        Raises:
            ValueError: media 리스트가 비어있거나 타입이 섞인 경우
            RuntimeError: Telegram API 호출 실패 시
        """
        self.logger.info("🟡 [START] 미디어 그룹 전송 시도 중...")

        if not media:
            raise ValueError("📛 media 리스트에 최소 한 개 이상의 미디어가 필요합니다.")

        first_type = type(media[0])
        if not all(isinstance(item, first_type) for item in media):
            raise ValueError(
                "📛 'send_media_group'에는 동일 타입의 미디어만 포함되어야 합니다. "
                "예: 모두 InputMediaPhoto 또는 모두 InputMediaVideo"
            )

        self.logger.debug(f"🔍 전송 대상 미디어 수: {len(media)}, 타입: {first_type.__name__}")
        self.logger.debug(f"📨 채팅 ID: {config.chat_id}")

        try:
            messages = await self._send_message_async(config, media=media, *args, **kwargs)
            self.logger.info(f"✅ [SUCCESS] 미디어 그룹 전송 완료 ({len(messages)}개 메시지)")
            return messages
        except Exception as e:
            self.logger.exception("❌ Telegram API 호출 중 오류 발생")
            raise RuntimeError(f"Telegram API 오류 발생: {e}")

    async def _send_message_async(
        self,
        config: TelegramSendConfig,
        *args,
        media: List[Union[InputMediaPhoto, InputMediaVideo]],
        **kwargs
    ) -> List[Message]:
        """
        Telegram API send_media_group 호출 내부 비동기 함수

        Args:
            config (TelegramSendConfig): 메시지 전송 설정
            media (List[InputMediaPhoto | InputMediaVideo]): 미디어 리스트
            **kwargs: 추가 API 파라미터

        Returns:
            List[telegram.Message]: 전송된 메시지 리스트
        """
        return await self.bot.send_media_group(
            chat_id=config.chat_id,
            media=media,
            message_thread_id=config.message_thread_id,
            reply_to_message_id=config.reply_to_message_id,
            read_timeout=config.read_timeout,
            write_timeout=config.write_timeout,
            connect_timeout=config.connect_timeout,
            pool_timeout=config.pool_timeout,
            *args,
            **kwargs
        )

    def resolve_media_input(self, media: Union[str, Path, BinaryIO]) -> BinaryIO:
        """
        경로나 파일 객체를 바이너리 파일 객체로 안전하게 변환

        Args:
            media (Union[str, Path, BinaryIO]): 경로 또는 이미 열린 파일 객체

        Returns:
            BinaryIO: 바이너리 모드로 열린 파일 객체

        Raises:
            ValueError: 적합하지 않은 타입 전달 시
        """
        if isinstance(media, (str, Path)):
            self.logger.debug(f"📂 파일 경로 '{media}' 바이너리 모드로 열기")
            return open(media, "rb")
        elif hasattr(media, "read"):
            self.logger.debug("📄 이미 열린 파일 객체 사용")
            return media
        else:
            raise ValueError("📛 media는 경로(str/Path) 또는 바이너리 파일 객체여야 합니다.")


if __name__ == "__main__":
    # async def main():
    #     config = TelegramSendConfig(
    #         chat_id="-1002431753833",  # 실제 채팅방 ID로 교체하세요
    #         parse_mode=ParseMode.HTML,
    #         message_thread_id=19
    #     )
    #     sender = MediaGroupSender(token="YOUR_BOT_TOKEN")
    #
    #     img_path = '/Users/mjun/dev/02_packages/telegram_bot/assets/img.jpeg'
    #
    #     media = [
    #         InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 1"),
    #         InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 2"),
    #         InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 3"),
    #         InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 4"),
    #     ]
    #
    #     await sender.send(config, media=media)
    #
    # asyncio.run(main())

    from dotenv import load_dotenv
    import os
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    config = TelegramSendConfig(
        chat_id="-1001999281217",  # 실제 채팅방 ID로 교체하세요
        parse_mode=ParseMode.HTML,
        message_thread_id=33708
    )
    sender = MediaGroupSender(token=token)

    img_path = "/Users/mjun/dev/02_packages/telegram_bot/assets/cluster_img.png"
    html_path = "/Users/mjun/dev/02_packages/telegram_bot/assets/cluster_html.html"

    media = [
        InputMediaDocument(media=sender.resolve_media_input(img_path), caption="사진 1"),
        InputMediaDocument(media=sender.resolve_media_input(html_path), caption="html"),
        # InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 2"),
        # InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 3"),
        # InputMediaPhoto(media=sender.resolve_media_input(img_path), caption="사진 4"),
    ]

    print(media)

    sender.send_sync(config, media=media)
    # sender.send_sync(config, media=media)
    # sender.send_sync(config, media=media)

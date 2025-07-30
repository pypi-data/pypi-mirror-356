import os
from telegram_bot.config.telegram_send_config import TelegramSendConfig
from telegram_bot.senders.media_group_sender import MediaGroupSender
from telegram_bot.services.base.base_telegram_sender import BaseTelegramSender
from telegram import InputMediaPhoto


class TelegramMediaGroupSender(BaseTelegramSender):
    """
    텔레그램 미디어 그룹 전송기

    여러 개의 이미지, 비디오, 오디오, 문서 등을 하나의 메시지 그룹으로 전송합니다.
    각 미디어는 InputMedia 형식으로 전달되어야 하며, 예외 발생 시 로깅합니다.

    Example:
        >>> sender = TelegramMediaGroupSender()
        >>> media = [
        ...     InputMediaPhoto(media=sender.resolve_media_input("img1.jpg")),
        ...     InputMediaPhoto(media=sender.resolve_media_input("img2.jpg"))
        ... ]
        >>> sender.send(media_list=media, chat_id="-1001234567890", thread_id=123)
    """

    def __init__(self, token: str | None = None, verbose: bool = True):
        """
        전송기 초기화

        Args:
            token (str | None): 텔레그램 봇 토큰. 생략 시 환경 변수에서 불러옴.
        """
        super().__init__(token, verbose=verbose)
        self.sender = MediaGroupSender(token=self.token, verbose=verbose)

    def send(
        self,
        media_list: list,
        chat_id: str,
        thread_id: int = 0
    ) -> None:
        """
        미디어 그룹 전송 함수

        Args:
            media_list (list): 전송할 InputMedia 객체 리스트 (e.g., InputMediaPhoto 등)
            chat_id (str): 대상 채팅 ID
            thread_id (int): 메시지 스레드 ID (기본값 0)

        Example:
            >>> sender = TelegramMediaGroupSender()
            >>> media = [
            ...     InputMediaPhoto(media=sender.resolve_media_input("img1.jpg")),
            ...     InputMediaPhoto(media=sender.resolve_media_input("img2.jpg"))
            ... ]
            >>> sender.send(media_list=media, chat_id="-1001234567890", thread_id=123)
        """
        try:
            config = self._build_config(chat_id=chat_id, thread_id=thread_id)
            self._send_media_group(config=config, media_list=media_list)
        except Exception as e:
            self.logger.error("미디어 그룹 전송 실패: %s", e, exc_info=True)

    def resolve_media_input(self, media: str | os.PathLike) -> any:
        """
        파일 경로 또는 미디어 입력을 텔레그램 전송 형식으로 변환

        Args:
            media (str | PathLike): 로컬 파일 경로 또는 URL

        Returns:
            Telegram InputMedia-compatible object (파일 핸들 등)

        Example:
            >>> sender = TelegramMediaGroupSender()
            >>> sender.resolve_media_input("image.png")
        """
        return self.sender.resolve_media_input(media)

    def _build_config(self, chat_id: str, thread_id: int) -> TelegramSendConfig:
        """
        전송용 설정 객체 생성

        Args:
            chat_id (str): 전송할 채팅 ID
            thread_id (int): 메시지 스레드 ID

        Returns:
            TelegramSendConfig: 전송 설정 객체
        """
        return TelegramSendConfig(chat_id=chat_id, message_thread_id=thread_id)

    def _send_media_group(self, config: TelegramSendConfig, media_list: list) -> None:
        """
        실제 미디어 그룹 전송 수행

        Args:
            config (TelegramSendConfig): 텔레그램 전송 설정
            media_list (list): InputMedia 리스트
        """
        self.sender.send_sync(config=config, media=media_list)
        self.logger.info("미디어 그룹 전송 성공 - 항목 수: %s", len(media_list))


# ✅ 실행 예시
if __name__ == "__main__":
    from mjkit.utiles.get_folder_path import get_assets_folder_path

    media_sender = TelegramMediaGroupSender()
    media_items = [
        InputMediaPhoto(
            media_sender.resolve_media_input(
                os.path.join(get_assets_folder_path(), "test.jpeg")
            )
        ),
        InputMediaPhoto(
            media_sender.resolve_media_input(
                os.path.join(get_assets_folder_path(), "test.jpeg")
            )
        )
    ]
    media_sender.send(
        media_list=media_items,
        chat_id="-1002431753833",
        thread_id=23,
    )
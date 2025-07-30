from telegram_bot.config.telegram_send_config import TelegramSendConfig, ParseMode
from telegram_bot.senders.document_sender import DocumentSender
from telegram_bot.services.base.base_telegram_sender import BaseTelegramSender


class TelegramDocumentSender(BaseTelegramSender):
    """
    텔레그램 문서 전송기

    문서 파일을 전송하며, 문서와 함께 캡션(텍스트)을 보낼 수 있습니다.
    예외 처리를 포함하여 안정적인 전송을 보장합니다.

    Example:
        >>> sender = TelegramDocumentSender()
        >>> sender.send(document_path="report.pdf", caption="📄 보고서입니다.")
    """

    def __init__(self, token: str | None = None, verbose: bool = True):
        """
        문서 전송기 초기화

        Args:
            token (str | None): 텔레그램 봇 토큰. 지정하지 않으면 환경변수에서 불러옴.
        """
        super().__init__(token, verbose=verbose)
        self.sender = DocumentSender(token=self.token, verbose=verbose)

    def send(
        self,
        document_path: str,
        caption: str,
        chat_id: str = "-1002431753833",
        thread_id: int = 23,
        parse_mode: ParseMode = ParseMode.HTML
    ) -> None:
        """
        문서를 캡션과 함께 전송합니다. 예외가 발생하면 로깅합니다.

        Example:
            doc_sender = TelegramDocumentSender()
            doc_sender.send(
                document_path=os.path.join(get_assets_folder_path(), 'test.jpeg'),
                caption="<b>📊 일일 보고서 첨부</b>",
                chat_id="-1002694727655",
                thread_id=20,
                parse_mode=ParseMode.HTML,
            )

        Args:
            document_path (str): 전송할 문서 경로
            caption (str): 문서에 첨부될 캡션 (예: 설명, 제목)
            chat_id (str): 텔레그램 채팅 ID
            thread_id (int): 텔레그램 포럼 스레드 ID
            parse_mode (ParseMode): 텍스트 파싱 방식 (HTML or Markdown)
        """
        try:
            self._send_document_with_caption(
                document_path=document_path,
                caption=caption,
                chat_id=chat_id,
                thread_id=thread_id,
                parse_mode=parse_mode
            )
        except Exception as e:
            self.logger.exception("문서 전송 실패: %s", e, exc_info=True)

    def _send_document_with_caption(
        self,
        document_path: str,
        caption: str,
        chat_id: str,
        thread_id: int,
        parse_mode: ParseMode
    ) -> None:
        """
        설정 생성 및 전송 로직을 분리하여 문서를 전송합니다.

        Args:
            document_path (str): 전송할 문서 경로
            caption (str): 전송할 캡션
        """
        config = self._build_config(chat_id, thread_id, parse_mode)
        self._send_document(config, document_path, caption)
        self.logger.info("문서 전송 성공: %s", document_path)

    def _build_config(
        self,
        chat_id: str,
        thread_id: int,
        parse_mode: ParseMode
    ) -> TelegramSendConfig:
        """
        전송 설정(config) 생성 함수

        Args:
            chat_id (str): 텔레그램 채팅 ID
            thread_id (int): 메시지 스레드 ID
            parse_mode (ParseMode): 메시지 파싱 방식

        Returns:
            TelegramSendConfig: 설정 객체
        """
        return TelegramSendConfig(
            chat_id=chat_id,
            message_thread_id=thread_id,
            parse_mode=parse_mode,
        )

    def _send_document(
        self,
        config: TelegramSendConfig,
        document_path: str,
        caption: str
    ) -> None:
        """
        실질적인 문서 전송 로직

        Args:
            config (TelegramSendConfig): 전송 설정
            document_path (str): 문서 경로
            caption (str): 첨부할 캡션
        """
        self.sender.send_sync(config=config, document=document_path, caption=caption)


if __name__ == "__main__":
    # from mjkit.utiles.get_folder_path import get_assets_folder_path
    #
    # doc_sender = TelegramDocumentSender()
    # doc_sender.send(
    #     document_path=os.path.join(get_assets_folder_path(), "test.jpeg"),
    #     caption="<b>📊 일일 보고서 첨부</b>",
    #     chat_id="-1002431753833",
    #     thread_id=23,
    #     parse_mode=ParseMode.HTML,
    # )
    ...

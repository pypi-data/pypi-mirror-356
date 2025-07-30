from telegram_bot.services.telegram_text_sender import TelegramTextSender
from telegram_bot.services.telegram_document_sender import TelegramDocumentSender
from telegram_bot.services.telegram_media_group_sender import TelegramMediaGroupSender

class TelegramSenderMixin:
    """
    텔레그램 전송 기능을 제공하는 믹스인 클래스입니다.

    이 믹스인을 상속하면 텍스트, 문서, 미디어 그룹을 텔레그램 채널/스레드로 전송하는 기능을 사용할 수 있습니다.
    공통된 전송 설정을 위한 `TelegramSenderConfig`를 통해 메시지 일관성을 유지합니다.

    사용 예:
        class MyWorker(TelegramSenderMixin):
            def __init__(self):
                super().__init__()
                self.sender.send_message("Hello, Telegram!", self.default_telegram_sender_config)

    Attributes:
        sender (TelegramTextSender): 텍스트 메시지 전송기
        document_sender (TelegramDocumentSender): 문서 전송기
        group_sender (TelegramMediaGroupSender): 이미지/미디어 그룹 전송기
        default_telegram_sender_config (TelegramSenderConfig): 메시지 전송 시 사용할 기본 설정
    """

    def __init__(self, *args, **kwargs):
        """
        텔레그램 전송기를 초기화하고 기본 설정을 저장합니다.

        Args:
            telegram_sender_config (TelegramSenderConfig, optional):
                전송기별 공통적으로 사용할 기본 설정. 미지정 시 기본 설정이 사용됩니다.
        """
        print("Initializing TelegramSenderMixin")
        super().__init__(*args, **kwargs)
        self.sender = TelegramTextSender()
        self.document_sender = TelegramDocumentSender()
        self.group_sender = TelegramMediaGroupSender()
class TelegramSendError(Exception):
    """
    Telegram 메시지 전송 실패 시 발생하는 예외

    Args:
        message (str): 예외 메시지
        chat_id (str, optional): 대상 채팅 ID
        thread_id (int, optional): 대상 스레드 ID
    """
    def __init__(self, message: str, chat_id: str = None, thread_id: int = None):
        super().__init__(message)
        self.message = message
        self.chat_id = chat_id
        self.thread_id = thread_id

    def __str__(self):
        info = [self.message]
        if self.chat_id:
            info.append(f"[chat_id={self.chat_id}]")
        if self.thread_id is not None:
            info.append(f"[thread_id={self.thread_id}]")
        return " ".join(info)
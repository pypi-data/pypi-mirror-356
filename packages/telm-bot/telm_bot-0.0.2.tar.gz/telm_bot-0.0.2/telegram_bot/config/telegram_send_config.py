from pydantic import BaseModel, field_validator
from typing import Optional, Union
from telegram.constants import ParseMode

class TelegramSendConfig(BaseModel):
    """
    텔레그램 메시지 전송 시 필요한 설정 정보를 담는 Pydantic 모델 클래스.

    Attributes:
        chat_id (str): 전송 대상 채팅 ID (예: "-1001234567890")
        parse_mode (Union[str, ParseMode], default=ParseMode.HTML):
            메시지 파싱 형식 (HTML, Markdown 등). ParseMode enum 또는 문자열 가능.
        message_thread_id (Optional[int]):
            메시지를 보낼 포럼 채널의 스레드 ID (없을 경우 None).
        reply_to_message_id (Optional[int]):
            회신하려는 메시지의 ID (선택값, 기본 None).
        read_timeout (int): 읽기 타임아웃 (초 단위, 기본값: 20)
        write_timeout (int): 쓰기 타임아웃 (초 단위, 기본값: 20)
        connect_timeout (int): 연결 타임아웃 (초 단위, 기본값: 20)
        pool_timeout (int): 커넥션 풀 타임아웃 (초 단위, 기본값: 20)
    """
    chat_id: str
    parse_mode: Union[str, ParseMode] = ParseMode.HTML
    message_thread_id: Optional[int] = None
    reply_to_message_id: Optional[int] = None

    read_timeout: int = 30
    write_timeout: int = 30
    connect_timeout: int = 30
    pool_timeout: int = 30

    @field_validator("parse_mode", mode="before")
    @classmethod
    def validate_parse_mode(cls, v):
        """
        parse_mode 필드의 값을 사전 검증하여 문자열로 변환함.

        - Enum(ParseMode) 타입일 경우 `.value` 속성을 추출 (예: ParseMode.HTML → "HTML")
        - 이미 문자열이면 그대로 반환
        - 그 외 타입은 오류 발생

        Raises:
            ValueError: parse_mode가 str 또는 ParseMode가 아닌 경우 예외 발생
        """
        if isinstance(v, ParseMode):
            return v.value
        elif isinstance(v, str):
            return v
        raise ValueError("parse_mode 반드시 str or telegram.constants.ParseMode")



# ✅ 사용 예시
if __name__ == "__main__":
    from telegram.constants import ParseMode

    # ✔️ 정상 케이스: Enum ParseMode 사용
    config = TelegramSendConfig(
        chat_id="-1002431753833",  # 전송 대상 채널 ID (실제 값으로 교체 필요)
        parse_mode=ParseMode.HTML,  # Enum → 문자열로 자동 변환됨
        message_thread_id=10,
        reply_to_message_id=1234567890
    )
    print("✅ 유효한 설정:", config)

    # ❌ 오류 케이스: 잘못된 타입의 parse_mode
    try:
        invalid_cfg = TelegramSendConfig(chat_id="-10012345", parse_mode=123)  # int는 허용되지 않음
    except ValueError as e:
        print("❌ 예외 발생 (잘못된 parse_mode):", e)
